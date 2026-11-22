"""Buraco negro com cara de buraco negro (no estilo das simulações da NASA e de Interstellar): sombra preta,
anel de fótons fino e brilhante, o disco de gás visto quase de lado cruzando a frente da sombra, e a parte de trás
do disco aparecendo "dobrada" pela gravidade por cima e por baixo da sombra. O lado que vem na nossa direção
brilha mais (efeito Doppler). Tudo em numpy; devolve a imagem com o buraco negro somado por cima."""
import math
from functools import lru_cache

import numpy as np
from PIL import Image, ImageFilter


@lru_cache(maxsize=4)
def _geo(R: int):
    w, h = int(R * 7), int(R * 4.6)
    X = (np.arange(w, dtype=np.float32)[None, :] - w / 2) / R
    Y = (np.arange(h, dtype=np.float32)[:, None] - h / 2) / R
    X, Y = np.broadcast_arrays(X, Y)
    d = np.sqrt(X ** 2 + Y ** 2) + 1e-6
    ang = np.arctan2(Y, X)
    Yd = Y / 0.15                                                   # disco achatado: visto quase de lado
    rho = np.sqrt(X ** 2 + Yd ** 2) + 1e-6
    angd = np.arctan2(Yd, X)
    sombra = np.clip((d - 0.985) * R * 0.5, 0, 1)                   # 0 dentro da sombra, borda suave
    cima = Y < 0
    larg = np.where(cima, 0.2, 0.11)                                # parte de trás dobrada: grossa em cima, fina embaixo
    forca = np.where(cima, 1.0, 0.55)
    halo = np.exp(-((d - 1.3) / larg) ** 2) * forca * (d > 1.0)
    disco = np.clip((rho - 1.55) * 6, 0, 1) * np.clip((3.3 - rho) * 2.5, 0, 1) * (1.55 / rho) ** 2
    disco = disco * np.where(d < 1.0, (Y > 0).astype(np.float32), 1.0)   # atrás da sombra não aparece
    anel = np.exp(-((d - 1.04) / 0.022) ** 2)
    dop_h = 1 + 0.55 * (-X / d)
    dop_d = 1 + 0.65 * (-X / rho)
    return w, h, d, ang, rho, angd, sombra, halo * dop_h, disco * dop_d, anel


def desenhar(img: Image.Image, cx: float, cy: float, R: float, t: float, brilho: float = 1.0) -> None:
    R = int(R)
    w, h, d, ang, rho, angd, sombra, halo, disco, anel = _geo(R)
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    box = (max(0, x0), max(0, y0), min(img.width, x0 + w), min(img.height, y0 + h))
    sx, sy = box[0] - x0, box[1] - y0
    ex, ey = sx + box[2] - box[0], sy + box[3] - box[1]
    sl = (slice(sy, ey), slice(sx, ex))
    gira_h = 0.85 + 0.15 * np.sin(ang[sl] * 7 - t * 2.4 + d[sl] * 9)            # filamentos girando
    gira_d = 0.7 + 0.3 * np.sin(angd[sl] * 9 - t * 4.0 * (1.55 / rho[sl]) ** 1.5 + rho[sl] * 3)
    I = (halo[sl] * gira_h * 0.75 + disco[sl] * gira_d * 0.95 + anel[sl] * 1.4) * brilho
    quente = np.clip(I, 0, 2.2)[..., None]
    laranja = np.array([255, 110, 25], np.float32)
    amarelo = np.array([255, 205, 110], np.float32)
    branco = np.array([255, 250, 238], np.float32)
    a = np.clip(quente, 0, 1)
    b = np.clip(quente - 1, 0, 1)
    cor = (laranja * (1 - a) + amarelo * a) * (1 - b) + branco * b
    emis = cor * np.clip(quente * 1.15, 0, 1)
    base = np.asarray(img.crop(box), np.float32)
    base = base * sombra[sl][..., None]                                         # a sombra apaga o fundo
    brilho_img = Image.fromarray(emis.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(R * 0.09))
    glow = np.asarray(brilho_img, np.float32)
    saida = base + emis + glow * 0.8 * (0.25 + 0.75 * sombra[sl][..., None])   # dentro da sombra quase não brilha
    img.paste(Image.fromarray(saida.clip(0, 255).astype(np.uint8)), box[:2])
