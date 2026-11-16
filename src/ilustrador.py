"""Ilustrador: gera uma ilustração para cada plano do roteiro com a API de imagens do Gemini.

Para manter tudo coerente entre os planos, cada pedido leva imagens de referência:
  - o estilo do canal (assets/estilo/*.jpg);
  - a folha do protagonista (assets/personagem/v3/<homem|mulher>.png), se existir; senão, a primeira
    ilustração do vídeo em que ele aparece passa a ser a referência dele;
  - a folha da ameaça (assets/personagem/v3/ameacas/<tipo>.png), se existir;
  - a primeira ilustração do mesmo lugar (para o cômodo não mudar de um plano para o outro).

A API de imagens é PAGA (cerca de US$ 0,04 a 0,05 por imagem). O limite por vídeo fica em config/serie.json
("imagens" -> "max_por_video"). Se a geração falhar, o plano usa um cenário pronto de assets/cenarios.
"""
import base64
import hashlib
import io
import json
import os
import time
from pathlib import Path

import requests
from PIL import Image

from .util import RAIZ, log

URL = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
PASTA_ESTILO = RAIZ / "assets" / "estilo"
PASTA_PERS = RAIZ / "assets" / "personagem" / "v3"
PASTA_CEN = RAIZ / "assets" / "cenarios"
LARGURA_REF = 768            # as referências vão reduzidas: mais rápido e mais barato

ESTILO_PADRAO = (
    "2D digital cartoon illustration for a horror animation channel, flat colors with soft cel shading, "
    "clean thin dark outlines, simple and readable shapes, cozy detailed everyday Brazilian home, "
    "dark night atmosphere with deep navy blue shadows and small warm light sources, cinematic framing"
)
AMEACAS_TEXTO = {
    "vulto": "a tall completely black human silhouette with two small glowing white eyes and no other features",
    "abismo": "a thin humanoid figure entirely pitch black, with a pale grey bald face, huge round staring eyes and an enormously wide smile",
    "invasor": "a person in a dirty yellow raincoat with the hood up, the face completely hidden in darkness",
}


def _chave() -> str:
    chave = os.environ.get("GEMINI_IMAGE_API_KEY", "").strip() or os.environ.get("GEMINI_API_KEY", "").strip()
    if not chave:
        raise RuntimeError("Falta a chave GEMINI_API_KEY (ou GEMINI_IMAGE_API_KEY) para gerar as ilustrações.")
    return chave


def _parte_imagem(caminho: Path) -> dict:
    img = Image.open(caminho).convert("RGB")
    if img.width > LARGURA_REF:
        img = img.resize((LARGURA_REF, int(img.height * LARGURA_REF / img.width)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=88)
    return {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(buf.getvalue()).decode()}}


def _pedir(prompt: str, refs: list, cfg_img: dict) -> bytes:
    """Chama a API e devolve os bytes da imagem. Tenta os modelos da lista em ordem."""
    partes = [_parte_imagem(r) for r in refs] + [{"text": prompt}]
    corpo = {
        "contents": [{"role": "user", "parts": partes}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": "9:16", "imageSize": cfg_img.get("tamanho", "1K")},
        },
    }
    ultimo = ""
    for modelo in cfg_img.get("modelos", ["gemini-3.1-flash-image"]):
        for tentativa in range(3):
            try:
                r = requests.post(URL.format(modelo=modelo), json=corpo, timeout=180,
                                  headers={"x-goog-api-key": _chave()})
            except requests.RequestException as e:
                ultimo = f"sem resposta ({type(e).__name__})"
                time.sleep(10 * (tentativa + 1))
                continue
            if r.status_code == 200:
                for cand in r.json().get("candidates", []):
                    for p in cand.get("content", {}).get("parts", []):
                        dado = p.get("inlineData") or p.get("inline_data")
                        if dado and not p.get("thought"):
                            return base64.b64decode(dado["data"])
                ultimo = "a resposta veio sem imagem (talvez bloqueada pelo filtro de conteúdo)"
                break
            if r.status_code == 404 or (r.status_code == 400 and "not found" in r.text.lower()):
                ultimo = f"modelo {modelo} não encontrado"
                break
            if r.status_code == 429 and ("limit: 0" in r.text or "free_tier" in r.text.lower()):
                raise RuntimeError("A API de imagens recusou por falta de cobrança ativa (plano gratuito não gera imagens). "
                                   "Ative o faturamento no Google AI Studio para a chave usada.")
            if r.status_code in (429, 500, 503):
                ultimo = f"{r.status_code}: {r.text[:200]}"
                time.sleep(15 * (tentativa + 1))
                continue
            ultimo = f"{r.status_code}: {r.text[:300]}"
            break
    raise RuntimeError(f"Não consegui gerar a ilustração: {ultimo}")


def _montar_prompt(plano: dict, roteiro: dict, cfg: dict, tem_ref_personagem: bool, tem_ref_lugar: bool) -> str:
    cfg_img = cfg.get("imagens", {})
    prot = roteiro.get("protagonista", "homem")
    desc_prot = cfg.get("protagonistas", {}).get(prot, {}).get("visual", "")
    linhas = [
        f"Art style: {cfg_img.get('estilo', ESTILO_PADRAO)}. Match the art style of the style reference images exactly.",
        f"Story setting (keep it consistent in every image): {roteiro.get('casa', 'a small two-story suburban house at night')}.",
        f"Location of this shot: {plano.get('lugar', '')}.",
        "",
        f"SHOT: {plano['imagem']}",
        "",
    ]
    if plano.get("personagem"):
        linhas.append(f"The protagonist appears in this shot: {desc_prot}. "
                      + ("Keep EXACTLY the same character design as in the character reference image (same head, hair, "
                         "face, outfit and colors). " if tem_ref_personagem else "")
                      + "Only one protagonist; no other people unless the shot says so.")
    else:
        linhas.append("The protagonist does NOT appear in this shot (unless only their hands are described).")
    amea = plano.get("ameaca")
    if amea:
        linhas.append(f"The threat in this shot: {AMEACAS_TEXTO.get(amea, amea)}. It must look subtle and eerie, partly hidden in the dark.")
    if tem_ref_lugar:
        linhas.append("This shot happens in the same room as the location reference image: keep the same furniture, "
                      "walls, colors and layout (the camera angle can change).")
    linhas += [
        "Vertical 9:16 frame. Keep the lower third of the image calm and simple, because subtitles will be placed there.",
        "No text, no letters, no numbers, no captions, no speech bubbles, no watermark, no logos, no borders.",
        "No blood, no gore.",
    ]
    return "\n".join(linhas)


def _ref_lugar_fixa(lugar: str):
    """Cenário pronto com o mesmo nome do lugar (assets/cenarios), usado como referência de continuidade e reserva."""
    for nome in (lugar, lugar.split("_")[0]):
        arq = PASTA_CEN / f"{nome}.png"
        if nome and arq.exists():
            return arq
    return None


def gerar_ilustracoes(roteiro: dict, cfg: dict, pasta: Path, refazer: list | None = None) -> list:
    """Gera (ou reaproveita) a ilustração de cada plano. Devolve a lista de caminhos, na ordem dos planos."""
    cfg_img = cfg.get("imagens", {})
    pasta.mkdir(parents=True, exist_ok=True)
    contagem_arq = pasta / "contagem.json"
    contagem = json.loads(contagem_arq.read_text()) if contagem_arq.exists() else {"geradas": 0}
    limite = int(cfg_img.get("max_por_video", 48))
    estilo = sorted(PASTA_ESTILO.glob("*.jpg"))[:2] + sorted(PASTA_ESTILO.glob("*.png"))[:1]
    prot = roteiro.get("protagonista", "homem")
    folha = next((p for p in (PASTA_PERS / f"{prot}.png", PASTA_PERS / f"{prot}.jpg") if p.exists()), None)
    ref_prot = folha
    ref_lugar: dict = {}
    caminhos, falhas, aviso_cobranca = [], 0, ""
    refazer = set(refazer or [])

    for i, plano in enumerate(roteiro["cenas"]):
        lugar = (plano.get("lugar") or "casa").strip().lower()
        refs = list(estilo)
        if lugar not in ref_lugar and _ref_lugar_fixa(lugar):
            ref_lugar[lugar] = _ref_lugar_fixa(lugar)   # cômodo já existente na biblioteca: mantém a mesma casa
        if lugar in ref_lugar:
            refs.append(ref_lugar[lugar])
        if plano.get("personagem") and ref_prot:
            refs.append(ref_prot)
        amea = plano.get("ameaca")
        if amea:
            folha_am = PASTA_PERS / "ameacas" / f"{amea}.png"
            if folha_am.exists():
                refs.append(folha_am)
        prompt = _montar_prompt(plano, roteiro, cfg, bool(plano.get("personagem") and ref_prot), lugar in ref_lugar)
        assinatura = hashlib.sha1((prompt + "|".join(map(str, refs))).encode()).hexdigest()[:10]
        destino = pasta / f"plano_{i:02d}_{assinatura}.png"
        if destino.exists() and i not in refazer:
            log(f"Ilustração {i + 1}/{len(roteiro['cenas'])}: reaproveitada")
        elif aviso_cobranca or contagem["geradas"] >= limite:
            destino = None
        else:
            try:
                log(f"Ilustração {i + 1}/{len(roteiro['cenas'])} ({lugar})")
                dados = _pedir(prompt, refs, cfg_img)
                contagem["geradas"] += 1
                contagem_arq.write_text(json.dumps(contagem))
                Image.open(io.BytesIO(dados)).convert("RGB").save(destino)
            except RuntimeError as e:
                falhas += 1
                log(f"  falhou: {e}")
                if "cobrança" in str(e):
                    aviso_cobranca = str(e)
                destino = None
        if destino is None:                      # reserva: cenário pronto do lugar ou a ilustração anterior
            destino = _ref_lugar_fixa(lugar) or (caminhos[-1] if caminhos else PASTA_CEN / "sala.png")
            plano["_reserva"] = True
        else:
            ref_lugar.setdefault(lugar, destino)
            if plano.get("personagem") and ref_prot is None:
                ref_prot = destino             # sem folha do personagem: o primeiro plano com ele vira a referência
        plano["_img"] = str(destino)
        caminhos.append(destino)

    custo = contagem["geradas"] * float(cfg_img.get("custo_por_imagem_usd", 0.045))
    log(f"Ilustrações: {contagem['geradas']} geradas neste vídeo (~US$ {custo:.2f}), {falhas} falhas")
    if aviso_cobranca:
        log("AVISO: " + aviso_cobranca)
    roteiro["_ilustracoes"] = {"geradas": contagem["geradas"], "falhas": falhas, "custo_usd": round(custo, 2),
                               "aviso": aviso_cobranca}
    return caminhos
