"""Terra realista para o E Se Fosse Real?: continentes de verdade (máscara do Natural Earth em
assets/esfr/terra_mapa.png), oceano com profundidade, gelo nos polos, nuvens andando, luz de lado,
luzes de cidade no lado da noite e atmosfera azul. Usada nos vídeos (voce.py) e nas thumbs (thumb_esfr.py).

terra(R, lon=..., nuvens=..., inclina=...) devolve um RGBA de lado 2.6R com a Terra no centro."""
import math
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from .util import RAIZ

MAPA = RAIZ / "assets" / "esfr" / "terra_mapa.png"


def tem_mapa() -> bool:
    return MAPA.exists()


@lru_cache(maxsize=1)
def _mapa() -> np.ndarray:
    m = Image.open(MAPA).convert("L").resize((2048, 1024), Image.BILINEAR)
    return np.asarray(m, np.float32) / 255.0


def _ruido(w, h, cel, seed):
    r = np.random.RandomState(seed)
    out, amp, tot = np.zeros((h, w), np.float32), 1.0, 0.0
    for _ in range(5):
        g = r.rand(int(h / cel) + 3, int(w / cel) + 3).astype(np.float32)
        img = Image.fromarray((g * 255).astype(np.uint8)).resize((w + int(cel * 2), h + int(cel * 2)), Image.BICUBIC)
        out += np.asarray(img, np.float32)[:h, :w] / 255 * amp
        tot += amp
        amp *= 0.5
        cel = max(cel / 2, 2)
    return out / tot


@lru_cache(maxsize=1)
def _texturas():
    """Variação do verde (mata x campo), nuvens e cidades, em equirretangular 1024x512."""
    return _ruido(1024, 512, 40, 8), _ruido(1024, 512, 22, 30), np.random.RandomState(4).rand(512, 1024)


@lru_cache(maxsize=8)
def _geo(R: int, inclina: float):
    S = int(R * 2.6)
    c = S / 2
    X = (np.arange(S, dtype=np.float32)[None, :] - c) / R
    Y = (np.arange(S, dtype=np.float32)[:, None] - c) / R
    X, Y = np.broadcast_arrays(X, Y)
    r2 = X ** 2 + Y ** 2
    dentro = r2 < 1.0
    Z = np.sqrt(np.clip(1 - r2, 0, 1))
    yw = -Y * math.cos(inclina) + Z * math.sin(inclina)          # inclina o polo norte para quem olha
    zw = Y * math.sin(inclina) + Z * math.cos(inclina)
    lat = np.arcsin(np.clip(yw, -1, 1))
    lon = np.arctan2(X, zw)
    L = np.array([-0.62, -0.42, 0.66], np.float32)
    L /= np.linalg.norm(L)
    luz = np.clip(X * L[0] + Y * L[1] + Z * L[2], 0, 1)
    alfa = (np.clip((1 - np.sqrt(r2)) * R * 1.5, 0, 1) * 255).astype(np.uint8)
    borda = (1 - Z) ** 3                                          # brilho azul na borda (atmosfera por dentro)
    halo = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse((c - R * 1.1, c - R * 1.1, c + R * 1.1, c + R * 1.1), fill=(80, 170, 255, 140))
    halo = halo.filter(ImageFilter.GaussianBlur(R * 0.1))
    return S, dentro, lat[dentro], lon[dentro], luz[dentro], borda[dentro], Z[dentro], alfa, halo


def terra(R: int, lon: float = 0.0, nuvens: float = 0.0, inclina: float = 0.35, cidades: bool = True) -> Image.Image:
    """lon: quanto a Terra já girou (radianos, aumenta para leste). nuvens: deslocamento extra das nuvens."""
    R = int(R)
    S, dentro, lat, lon0, luz, borda, Z, alfa, halo = _geo(R, round(inclina, 3))
    m = _mapa()
    var, nuv, cid = _texturas()
    lo = (lon0 + lon + math.pi) % (2 * math.pi)
    u = (lo / (2 * math.pi) * 2047).astype(np.int32)
    v = ((math.pi / 2 - lat) / math.pi * 1023).astype(np.int32).clip(0, 1023)
    terra_ = m[v, u]
    u2, v2 = u >> 1, v >> 1
    alat = np.abs(lat)
    mist = np.clip((var[v2, u2] - 0.42) * 2.5, 0, 1)
    seco = np.clip((0.55 - np.abs(alat - 0.42) * 3.0), 0, 1) * mist  # faixas secas perto dos trópicos, só onde o ruído deixa
    solo = (np.array([58, 150, 72], np.float32) * (1 - mist[:, None] * 0.5)
            + np.array([96, 170, 84], np.float32) * mist[:, None] * 0.5)
    solo = solo * (1 - seco[:, None] * 0.6) + np.array([196, 170, 112], np.float32) * seco[:, None] * 0.6
    fundo = np.clip(Z, 0, 1)[:, None]
    mar = np.array([14, 70, 170], np.float32) * (1 - fundo * 0.4) + np.array([30, 120, 215], np.float32) * fundo * 0.4
    cor = solo * terra_[:, None] + mar * (1 - terra_[:, None])
    gelo = np.clip((alat - (1.27 + (var[v2, u2] - 0.5) * 0.1)) * 25, 0, 1)               # calotas polares
    gelo = np.maximum(gelo, terra_ * np.clip((alat - 1.15) * 20, 0, 1))                     # Groenlândia e Antártida
    cor = cor * (1 - gelo[:, None]) + np.array([236, 243, 250], np.float32) * gelo[:, None]
    un = ((lo + nuvens * 0.35) / (2 * math.pi) * 1023).astype(np.int32) % 1024
    n_ = np.clip((nuv[v2, un] - 0.55) * 2.6, 0, 0.75)
    cor = cor * (1 - n_[:, None]) + 255 * n_[:, None]
    cor = cor * (0.1 + 1.05 * luz ** 1.1)[:, None]
    cor += np.array([90, 170, 255], np.float32) * (borda * (0.25 + 0.6 * luz))[:, None]
    if cidades:
        noite = np.clip(0.16 - luz, 0, 0.16) / 0.16
        acesa = (cid[v2, u2] > 0.975) & (terra_ > 0.5) & (gelo < 0.5)
        cor[acesa] += np.array([255, 200, 110], np.float32) * (noite[acesa] * 0.9)[:, None]
    cor += 255 * (luz ** 40 * (terra_ < 0.5))[:, None] * 0.45                               # reflexo do Sol no mar
    rgb = np.zeros((S, S, 3), np.uint8)
    rgb[dentro] = cor.clip(0, 255).astype(np.uint8)
    pl = Image.fromarray(np.dstack([rgb, alfa]), "RGBA")
    out = halo.copy()
    out.alpha_composite(pl)
    return out
