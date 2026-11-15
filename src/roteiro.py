"""Agente roteirista: gera a história original em JSON usando a API gratuita do Gemini."""
import json
import os
import re
import time

import requests

from .util import carregar_historico, env, log

URL = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"

# Tenta o modelo definido em GEMINI_MODEL e, se não existir, os seguintes (todos do plano gratuito).
MODELOS_PADRAO = ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-flash-latest", "gemini-2.5-flash"]

MOVIMENTOS = ["zoom_in", "zoom_out", "pan_cima", "pan_baixo", "tremor"]


def _chamar_gemini(prompt: str, temperatura: float = 1.0) -> str:
    chave = env("GEMINI_API_KEY")
    modelos = [m for m in [os.environ.get("GEMINI_MODEL", "").strip()] if m] + MODELOS_PADRAO
    corpo = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": temperatura, "responseMimeType": "application/json"},
    }
    ultimo_erro = ""
    for modelo in modelos:
        for tentativa in range(4):
            r = requests.post(URL.format(modelo=modelo), json=corpo, timeout=120,
                              headers={"x-goog-api-key": chave})
            if r.status_code == 200:
                dados = r.json()
                try:
                    return dados["candidates"][0]["content"]["parts"][0]["text"]
                except (KeyError, IndexError):
                    ultimo_erro = f"resposta vazia: {str(dados)[:300]}"
                    break
            if r.status_code in (404, 400) and "not found" in r.text.lower():
                ultimo_erro = f"modelo {modelo} não encontrado"
                break  # tenta o próximo modelo
            if r.status_code in (429, 500, 503):
                espera = 20 * (tentativa + 1)
                log(f"Gemini ocupado ({r.status_code}), tentando de novo em {espera}s...")
                time.sleep(espera)
                ultimo_erro = r.text[:300]
                continue
            ultimo_erro = f"{r.status_code}: {r.text[:300]}"
            break
        log(f"Falhou com {modelo}: {ultimo_erro}")
    raise RuntimeError(f"Não foi possível usar o Gemini. Último erro: {ultimo_erro}")


def _extrair_json(texto: str) -> dict:
    texto = texto.strip()
    texto = re.sub(r"^```(json)?|```$", "", texto, flags=re.M).strip()
    inicio, fim = texto.find("{"), texto.rfind("}")
    return json.loads(texto[inicio:fim + 1])


def _protagonista(cfg: dict) -> dict:
    return cfg.get("protagonista") or cfg.get("narrador") or {"nome": "Você", "visual": "simple cartoon person"}


def gerar_roteiro(cfg: dict, tema: str | None = None) -> dict:
    tema = tema or cfg["tema_padrao"]
    ja_feitos = [h["titulo"] for h in carregar_historico()][-40:]
    n = cfg["numero_de_cenas"]
    prot = _protagonista(cfg)
    palavras = int(cfg["duracao_alvo_segundos"] * 2.3)

    prompt = f"""Você é roteirista do canal brasileiro de animações de terror "{cfg['nome_serie']}".
O formato do canal: o espectador É o protagonista. A narração fala com ele em SEGUNDA PESSOA ("você"),
descrevendo uma situação de terror que acontece com ele, e termina com um DILEMA em que ele precisa escolher.

Tema deste vídeo: {tema}

Regras da história:
- História ORIGINAL, em português do Brasil, linguagem simples e natural, frases curtas.
- Cerca de {palavras} palavras no total (uns {cfg['duracao_alvo_segundos']} segundos narrados), em exatamente {n} cenas.
- Cena 1: GANCHO imediato que coloca o espectador na situação ("Sua família viajou e você ficou sozinho em casa...").
- Use detalhes concretos e horários ("às duas e seis da manhã"), pequenas pistas estranhas e tensão crescente.
- Perto do fim, o perigo fica cara a cara com você.
- Última cena: apresente DUAS escolhas, "opção A: ..." e "opção B: ...", e termine EXATAMENTE com "Comente A ou B."
- Suspense e atmosfera: nada de violência explícita, sangue ou gore.
- Não repita estas histórias: {json.dumps(ja_feitos, ensure_ascii=False)}

Regras das imagens:
- O protagonista se chama "{prot['nome']}" e aparece na maioria das cenas: coloque "{prot['nome']}" em "personagens_na_cena" sempre que ele estiver visível.
- Varie os enquadramentos como num desenho animado: plano aberto da casa por fora, plano médio do personagem,
  close nas mãos segurando o celular, tela do celular mostrando a câmera de segurança, close na porta, a ameaça na sombra.
- A ameaça (intruso, criatura, vulto) deve ser uma silhueta escura com olhos brancos brilhando, sem rosto detalhado.
- Para cada cena, escreva o prompt da imagem em INGLÊS: lugar, luz, ação e enquadramento. Não descreva textos ou letras.

Responda SOMENTE com JSON válido neste formato:
{{
  "titulo": "título curto e chamativo",
  "personagens": [
    {{"nome": "Nome de outro personagem (se houver)", "visual": "aparência em inglês, sempre igual"}}
  ],
  "cenas": [
    {{
      "narracao": "texto narrado desta cena",
      "imagem": "English image prompt for this scene",
      "personagens_na_cena": ["{prot['nome']}"],
      "movimento": "um de: {', '.join(MOVIMENTOS)}"
    }}
  ],
  "legenda_post": "legenda curta para o post, terminando com: E você, A ou B?",
  "hashtags": ["#exemplo"]
}}"""

    log(f"Gerando roteiro sobre: {tema}")
    for tentativa in range(3):
        try:
            roteiro = _extrair_json(_chamar_gemini(prompt))
            _validar(roteiro, cfg)
            log(f"Roteiro pronto: {roteiro['titulo']} ({len(roteiro['cenas'])} cenas)")
            roteiro["tema"] = tema
            return roteiro
        except (ValueError, KeyError) as e:
            log(f"Roteiro veio inválido ({e}), pedindo de novo...")
    raise RuntimeError("O Gemini não devolveu um roteiro válido após 3 tentativas.")


def _validar(roteiro: dict, cfg: dict) -> None:
    if not roteiro.get("titulo") or not roteiro.get("cenas"):
        raise ValueError("faltou título ou cenas")
    # o visual do protagonista vem sempre da configuração, para ficar igual em todos os vídeos
    prot = _protagonista(cfg)
    roteiro["personagens"] = [p for p in roteiro.get("personagens", [])
                              if p.get("nome") and p.get("nome") != prot["nome"]]
    roteiro["personagens"].append({"nome": prot["nome"], "visual": prot["visual"]})
    for c in roteiro["cenas"]:
        if not c.get("narracao") or not c.get("imagem"):
            raise ValueError("cena sem narração ou imagem")
        if c.get("movimento") not in MOVIMENTOS:
            c["movimento"] = "zoom_in"
        c.setdefault("personagens_na_cena", [])


def gerar_ideias(cfg: dict, quantidade: int = 5) -> list:
    ja_feitos = [h["titulo"] for h in carregar_historico()][-40:]
    prompt = f"""Sugira {quantidade} ideias ORIGINAIS de histórias curtas de terror para o canal "{cfg['nome_serie']}",
dentro do tema: {cfg['tema_padrao']}. Evite repetir: {json.dumps(ja_feitos, ensure_ascii=False)}.
Responda SOMENTE com JSON: {{"ideias": ["ideia em uma frase", "..."]}}"""
    return _extrair_json(_chamar_gemini(prompt))["ideias"]
