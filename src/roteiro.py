"""Agente roteirista: gera a história original em JSON usando a API gratuita do Gemini."""
import json
import os
import re
import time

import requests

from .animacao import GUIA_CENAS, normalizar
from .personagem import escolher_protagonista
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
            try:
                r = requests.post(URL.format(modelo=modelo), json=corpo, timeout=240,
                                  headers={"x-goog-api-key": chave})
            except requests.RequestException as e:  # demora ou queda de conexão: tenta de novo
                espera = 15 * (tentativa + 1)
                log(f"Gemini não respondeu a tempo ({type(e).__name__}), tentando de novo em {espera}s...")
                ultimo_erro = f"sem resposta ({type(e).__name__})"
                time.sleep(espera)
                continue
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
    return {"nome": "Você", "visual": ""}


def gerar_roteiro(cfg: dict, tema: str | None = None) -> dict:
    tema = tema or cfg["tema_padrao"]
    ja_feitos = [h["titulo"] for h in carregar_historico()][-40:]
    n = cfg["numero_de_cenas"]
    prot = _protagonista(cfg)
    palavras = int(cfg["duracao_alvo_segundos"] * 2.3)
    quem = escolher_protagonista(cfg, carregar_historico())
    info = cfg.get("protagonistas", {}).get(quem, {"genero": "masculino", "descricao": ""})

    prompt = f"""Você é roteirista do canal brasileiro de animações de terror "{cfg['nome_serie']}".
O formato do canal: o espectador É o protagonista. A narração fala com ele em SEGUNDA PESSOA ("você"),
descrevendo uma situação de terror que acontece com ele, e termina com um DILEMA em que ele precisa escolher.

Tema deste vídeo: {tema}
Protagonista deste vídeo: {info['descricao']}. Gênero {info['genero'].upper()}: escreva adjetivos e particípios
referentes a "você" no {info['genero']} (ex.: "{'sozinha, assustada' if info['genero'] == 'feminino' else 'sozinho, assustado'}").

Regras da história:
- História ORIGINAL, em português do Brasil, linguagem simples e natural, frases curtas.
- Cerca de {palavras} palavras no total (uns {cfg['duracao_alvo_segundos']} segundos narrados), em exatamente {n} cenas.
- Cena 1: GANCHO imediato que coloca o espectador na situação ("Sua família viajou e você ficou sozinho em casa...").
- Use detalhes concretos e horários ("às duas e seis da manhã"), pequenas pistas estranhas e tensão crescente.
- Perto do fim, o perigo fica cara a cara com você.
- Última cena: apresente DUAS escolhas, "opção A: ..." e "opção B: ...", e termine EXATAMENTE com "Comente A ou B."
- Suspense e atmosfera: nada de violência explícita, sangue ou gore.
- Não repita estas histórias: {json.dumps(ja_feitos, ensure_ascii=False)}

Como cada cena vira animação:
{GUIA_CENAS}

Responda SOMENTE com JSON válido neste formato:
{{
  "titulo": "título curto e chamativo",
  "cenas": [
    {{
      "narracao": "texto narrado desta cena",
      "cenario": "sala",
      "personagem": {{"pose": "frente", "acao": "parado", "posicao": "centro", "tamanho": "medio"}},
      "ameaca": null,
      "efeito": "nenhum",
      "camera": "zoom_in"
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
            roteiro["protagonista"] = quem
            return roteiro
        except (ValueError, KeyError) as e:
            log(f"Roteiro veio inválido ({e}), pedindo de novo...")
    raise RuntimeError("O Gemini não devolveu um roteiro válido após 3 tentativas.")


def _validar(roteiro: dict, cfg: dict) -> None:
    if not roteiro.get("titulo") or not roteiro.get("cenas"):
        raise ValueError("faltou título ou cenas")
    roteiro.setdefault("personagens", [])
    for c in roteiro["cenas"]:
        if not c.get("narracao"):
            raise ValueError("cena sem narração")
        normalizar(c)


def gerar_ideias(cfg: dict, quantidade: int = 5) -> list:
    ja_feitos = [h["titulo"] for h in carregar_historico()][-40:]
    prompt = f"""Sugira {quantidade} ideias ORIGINAIS de histórias curtas de terror para o canal "{cfg['nome_serie']}",
dentro do tema: {cfg['tema_padrao']}. Evite repetir: {json.dumps(ja_feitos, ensure_ascii=False)}.
Responda SOMENTE com JSON: {{"ideias": ["ideia em uma frase", "..."]}}"""
    return _extrair_json(_chamar_gemini(prompt))["ideias"]
