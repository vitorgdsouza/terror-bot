"""Gera ilustrações (cenários e cenas especiais) com o Gemini, no estilo da série.

    python -m src.imagem_ia <nome> "<descrição em inglês>"
Salva em assets/cenarios/<nome>.png (1188x2112) e uma prévia em data/previas/img_<nome>.jpg.
"""
import base64
import io
import os
import sys

import requests
from PIL import Image

from .util import RAIZ, log

ESTILO = ("2D cartoon illustration, clean dark outlines, detailed hand-drawn horror comic style, flat colors with soft "
          "shading, night time, dark navy and blue palette with one warm light source, eerie and quiet mood, vertical "
          "9:16 composition, no text, no letters, no watermark")
MODELOS = ["gemini-2.5-flash-image", "gemini-2.5-flash-image-preview", "gemini-2.0-flash-preview-image-generation"]


def gerar(descricao: str, destino, estilo: str = ESTILO) -> str:
    chave = os.environ.get("GEMINI_API_KEY", "").strip()
    if not chave:
        raise RuntimeError("Falta o segredo GEMINI_API_KEY.")
    texto = f"{descricao}. {estilo}."
    erros = []
    for modelo in MODELOS:
        corpo = {"contents": [{"parts": [{"text": texto}]}],
                 "generationConfig": {"responseModalities": ["TEXT", "IMAGE"], "imageConfig": {"aspectRatio": "9:16"}}}
        r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent",
                          params={"key": chave}, json=corpo, timeout=180)
        if r.status_code == 400 and "imageConfig" in r.text:          # modelo antigo sem proporção: pede no texto
            corpo["generationConfig"].pop("imageConfig")
            r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent",
                              params={"key": chave}, json=corpo, timeout=180)
        if r.status_code >= 400:
            erros.append(f"{modelo}: {r.status_code} {r.text[:160]}")
            continue
        for parte in r.json().get("candidates", [{}])[0].get("content", {}).get("parts", []):
            dado = (parte.get("inlineData") or parte.get("inline_data") or {}).get("data")
            if dado:
                img = Image.open(io.BytesIO(base64.b64decode(dado))).convert("RGB")
                _salvar(img, destino)
                log(f"Ilustração gerada com {modelo}: {img.size}")
                return modelo
        erros.append(f"{modelo}: sem imagem na resposta")
    raise RuntimeError("Não consegui gerar a imagem: " + " | ".join(erros))


def _salvar(img: Image.Image, destino) -> None:
    alvo_w, alvo_h = 1188, 2112
    k = max(alvo_w / img.width, alvo_h / img.height)                   # cobre 9:16 e corta o excesso
    img = img.resize((int(img.width * k + 0.5), int(img.height * k + 0.5)), Image.LANCZOS)
    x0, y0 = (img.width - alvo_w) // 2, (img.height - alvo_h) // 2
    img.crop((x0, y0, x0 + alvo_w, y0 + alvo_h)).save(destino)


if __name__ == "__main__":
    nome, descricao = sys.argv[1], sys.argv[2]
    destino = RAIZ / "assets" / "cenarios" / f"{nome}.png"
    gerar(descricao, destino)
    prev = RAIZ / "data" / "previas"
    prev.mkdir(parents=True, exist_ok=True)
    Image.open(destino).resize((594, 1056)).save(prev / f"img_{nome}.jpg", quality=85)
