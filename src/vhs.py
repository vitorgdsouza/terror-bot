"""Estilo "fita VHS de câmera caseira" pixelado (terror analógico): baixa resolução de propósito.

Pixeliza o quadro (paleta curta), puxa a cor para o verde-amarelado de fita velha, separa as cores (RGB tremido),
adiciona linhas de TV, chiado, faixa de tracking que sobe pela tela, tremidinha de câmera na mão e o texto
"REC ●" com data e hora correndo. A legenda vai dentro do quadro, em letra de vídeo antigo.
"""
import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .util import RAIZ

FONTE = next((p for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
                          "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
                          str(RAIZ / "assets" / "fontes" / "Poppins-Bold.ttf")) if Path(p).exists()))
_fontes: dict = {}


def _f(px):
    if px not in _fontes:
        _fontes[px] = ImageFont.truetype(FONTE, px)
    return _fontes[px]


def _texto_fita(d, xy, txt, px, cor=(236, 236, 228)):
    x, y = xy
    d.text((x + 3, y + 3), txt, font=_f(px), fill=(0, 0, 0))
    d.text((x, y), txt, font=_f(px), fill=cor)


def aplicar(img: Image.Image, cena: dict, t: float, dur: float, n: int) -> Image.Image:
    W, H = img.size
    rnd = random.Random(n)
    # câmera na mão
    dx, dy = int(6 * math.sin(t * 2.1) + 3 * math.sin(t * 5.3)), int(5 * math.sin(t * 1.7 + 1))
    img = img.transform(img.size, Image.AFFINE, (1, 0, dx, 0, 1, dy), resample=Image.BILINEAR)
    # pixelização + paleta curta
    p = int(cena.get("_pixel", 6))
    peq = img.resize((W // p, H // p), Image.BOX).convert("P", palette=Image.ADAPTIVE, colors=40).convert("RGB")
    a = np.asarray(peq.resize((W, H), Image.NEAREST)).astype(np.float32)
    # cor de fita velha (menos saturação, verde-amarelado, pretos lavados)
    cinza = a.mean(axis=2, keepdims=True)
    a = a * 0.62 + cinza * 0.38
    a = a * np.array([1.0, 1.04, 0.86]) + np.array([10, 12, 6])
    # RGB tremido
    sh = 5 + (8 if rnd.random() < 0.06 else 0)
    a[..., 0] = np.roll(a[..., 0], sh, axis=1)
    a[..., 2] = np.roll(a[..., 2], -sh, axis=1)
    # linhas e chiado
    a[::3] *= 0.78
    a += np.random.default_rng(n).normal(0, 9, (H, W, 1))
    # faixa de tracking subindo
    yb = int((H - (t * 260 + n % 7) % (H + 200)))
    for y0 in range(max(0, yb), min(H, yb + 70), 2):
        a[y0] = np.roll(a[y0], rnd.randint(-40, 40), axis=0) * 1.15 + 18
    # vinheta
    if (W, H) not in _fontes:
        yy, xx = np.mgrid[0:H, 0:W]
        _fontes[(W, H)] = np.clip(1.1 - 0.55 * (((xx - W / 2) / W) ** 2 * 2.2 + ((yy - H / 2) / H) ** 2 * 1.6),
                                  0.25, 1)[..., None].astype(np.float32)
    a *= _fontes[(W, H)]
    img = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    # REC e data/hora (a hora corre ao longo do vídeo)
    if int(t * 2) % 2 == 0:
        d.ellipse((60, 92, 96, 128), fill=(230, 30, 30))
    _texto_fita(d, (110, 84), "REC", 46)
    _texto_fita(d, (W - 300, 84), "SP ▸" if FONTE.endswith("Bold.ttf") else "SP", 40)
    seg = int(cena.get("_t0", 0) + t)
    h0, m0, s0 = cena.get("_hora", (3, 12, 40))
    tot = s0 + m0 * 60 + h0 * 3600 + seg
    _texto_fita(d, (60, H - 230), f"{cena.get('_data', 'NOV 16 1997')}", 40)
    _texto_fita(d, (60, H - 180), f"{tot // 3600 % 12 or 12:02d}:{tot // 60 % 60:02d}:{tot % 60:02d} AM", 40)
    # legenda dentro do quadro, palavra por palavra
    palavras = cena.get("_palavras") or []
    ditas = [w["texto"] for w in palavras if w["inicio"] <= t]
    if ditas:
        linhas, linha = [], ""
        for w in ditas:
            if _f(46).getlength((linha + " " + w).strip()) > W * 0.84:
                linhas.append(linha)
                linha = w
            else:
                linha = (linha + " " + w).strip()
        linhas.append(linha)
        y = int(H * 0.70)
        for ln in linhas[-2:]:
            _texto_fita(d, ((W - _f(46).getlength(ln)) / 2, y), ln, 46, (240, 236, 210))
            y += 62
    borda = min(t, dur - t)
    if borda < 0.12:                                   # corte de fita: chiado branco rápido
        ruido = np.random.default_rng(n + 1).integers(0, 255, (H // 8, W // 8, 1), dtype=np.uint8).repeat(3, 2)
        img = Image.blend(img, Image.fromarray(ruido).resize((W, H), Image.NEAREST), 0.6 * (1 - borda / 0.12))
    return img
