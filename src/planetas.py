"""Planetas do Sistema Solar no mesmo padrão da Terra nova (src/globo.py): esfera sombreada com textura
própria (gerada em código), luz de lado, atmosfera quando o planeta tem uma e anéis em Saturno e Urano.

planeta(nome, R, t) devolve um RGBA com o planeta no centro. Nomes: mercurio, venus, terra, marte, jupiter,
saturno, urano, netuno, lua. "t" (segundos) faz o planeta girar e as nuvens andarem."""
import math
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from .globo import _ruido, terra

TW, TH = 1024, 512
LAT = (0.5 - (np.arange(TH, dtype=np.float32)[:, None] + 0.5) / TH) * math.pi      # +pi/2 no topo
LON = ((np.arange(TW, dtype=np.float32)[None, :] + 0.5) / TW * 2 - 1) * math.pi
LAT, LON = np.broadcast_arrays(LAT, LON)


def _mistura(a, b, f):
    f = np.clip(f, 0, 1)[..., None]
    return np.asarray(a, np.float32) * (1 - f) + np.asarray(b, np.float32) * f


def _crateras(base, n, seed, rmin, rmax, fundo=-28, borda=30):
    rnd = np.random.RandomState(seed)
    for _ in range(n):
        cx, cy = rnd.rand() * TW, TH * (0.12 + 0.76 * rnd.rand())
        r = rmin * (rmax / rmin) ** (rnd.rand() ** 2.2)
        esc = 1 / max(0.25, math.cos((0.5 - cy / TH) * math.pi))        # mais largas perto dos polos (projeção)
        x0, x1 = int(cx - r * esc * 1.4), int(cx + r * esc * 1.4) + 1
        y0, y1 = max(0, int(cy - r * 1.4)), min(TH, int(cy + r * 1.4) + 1)
        xs = np.arange(x0, x1) % TW
        if y1 <= y0 or x1 <= x0:
            continue
        sub = np.sqrt((((np.arange(x0, x1)[None, :] - cx) / esc) ** 2) + ((np.arange(y0, y1)[:, None] - cy) ** 2)) / r
        efeito = np.where(sub < 0.85, fundo, 0) + np.where((sub >= 0.85) & (sub < 1.1), borda, 0)
        base[y0:y1][:, xs] += efeito[..., None]
    return base


@lru_cache(maxsize=None)
def textura(nome: str) -> np.ndarray:
    n1, n2, n3 = _ruido(TW, TH, 60, 3), _ruido(TW, TH, 24, 11), _ruido(TW, TH, 10, 19)
    alat = np.abs(LAT)
    if nome == "mercurio":
        cor = _mistura([118, 112, 108], [168, 160, 152], n1 * 1.3 - 0.15)
        cor += ((n3 - 0.5) * 40)[..., None]
        cor = _crateras(cor, 420, 7, 3, 34)
    elif nome == "lua":
        cor = _mistura([150, 150, 156], [205, 205, 210], n1 * 1.4 - 0.2)
        mares = np.clip((n2 - 0.56) * 8, 0, 1) * (alat < 1.0)
        cor = _mistura(cor, [92, 92, 100], mares * 0.85)
        cor = _crateras(cor, 260, 5, 3, 26, fundo=-20, borda=26)
    elif nome == "venus":
        torce = (n1 - 0.5) * 0.9
        faixa = np.sin(LAT * 7 + torce * 4 + np.abs(LON) * 0.4)
        cor = _mistura([226, 196, 132], [246, 226, 178], 0.5 + faixa * 0.35 + (n2 - 0.5) * 0.8)
        cor = _mistura(cor, [200, 160, 100], np.clip((n3 - 0.62) * 3, 0, 0.4))
    elif nome == "marte":
        cor = _mistura([196, 98, 52], [222, 140, 86], n1 * 1.5 - 0.3)
        escuro = np.clip((n2 - 0.55) * 5, 0, 1) * (alat < 1.05)
        cor = _mistura(cor, [112, 58, 38], escuro * 0.8)
        vale = np.exp(-((LAT + 0.14) / 0.022) ** 2) * ((LON > -1.6) & (LON < -0.5))   # Valles Marineris
        cor = _mistura(cor, [96, 44, 28], vale * 0.9)
        olimpo = np.exp(-(((LAT - 0.32) / 0.07) ** 2 + ((LON + 2.3) / 0.09) ** 2))    # Monte Olimpo
        cor = _mistura(cor, [236, 170, 120], olimpo)
        cor = _mistura(cor, [248, 244, 240], np.clip((alat - 1.3 - (n3 - 0.5) * 0.15) * 18, 0, 1))
        cor += ((n3 - 0.5) * 26)[..., None]
    elif nome in ("jupiter", "saturno"):
        y = LAT + (n2 - 0.5) * (0.06 if nome == "jupiter" else 0.03) + np.sin(LON * 3 + LAT * 20) * 0.006
        if nome == "jupiter":
            tons = [[236, 222, 196], [186, 128, 84], [222, 186, 146], [160, 104, 72], [240, 230, 210], [200, 150, 110]]
            freq = 9.0
        else:
            tons = [[236, 214, 160], [214, 186, 128], [242, 226, 180], [204, 174, 118], [230, 206, 150]]
            freq = 7.0
        k = np.clip((np.sin(y * freq) * 0.5 + 0.5) * (len(tons) - 1) + (n3 - 0.5) * 0.35, 0, len(tons) - 1)
        T = np.asarray(tons, np.float32)
        xs = np.arange(len(tons), dtype=np.float32)
        cor = np.stack([np.interp(k, xs, T[:, c]) for c in range(3)], -1)   # paleta contínua entre as faixas
        cor = _mistura(cor, [215, 200, 180], np.clip((alat - 1.15) * 3, 0, 0.6))      # polos mais apagados
        if nome == "jupiter":                                                         # Grande Mancha Vermelha
            m = np.sqrt(((LAT + 0.39) / 0.085) ** 2 + ((LON - 0.6) / 0.22) ** 2)
            cor = _mistura(cor, [206, 92, 58], np.clip((1 - m) * 1.3, 0, 1))
            cor = _mistura(cor, [240, 220, 200], np.clip(1 - np.abs(m - 1.12) * 6, 0, 1) * 0.6)
    elif nome == "urano":
        cor = _mistura([150, 214, 222], [178, 232, 236], 0.5 + np.sin(LAT * 6) * 0.15 + (n2 - 0.5) * 0.3)
    elif nome == "netuno":
        cor = _mistura([40, 78, 196], [78, 126, 230], 0.5 + np.sin(LAT * 8 + (n2 - 0.5) * 2) * 0.35)
        mancha = np.sqrt(((LAT + 0.36) / 0.07) ** 2 + ((LON + 0.4) / 0.17) ** 2)
        cor = _mistura(cor, [14, 24, 78], np.clip((1 - mancha) * 1.6, 0, 1))
        cor = _mistura(cor, [236, 244, 255], np.clip((1.35 - np.sqrt(((LAT + 0.44) / 0.03) ** 2 + ((LON + 0.32) / 0.1) ** 2)) * 2, 0, 0.85))   # nuvem branca ao lado
        nuvem = np.exp(-((LAT + 0.27 + (n1 - 0.5) * 0.05) / 0.035) ** 2) * np.clip((n2 - 0.45) * 3, 0, 1)
        cor = _mistura(cor, [236, 244, 255], nuvem * 0.9)
        cor = _mistura(cor, [230, 240, 255], np.exp(-((LAT - 0.45 + (n1 - 0.5) * 0.05) / 0.03) ** 2) * np.clip((n1 - 0.48) * 3, 0, 1) * 0.6)
    else:
        raise ValueError(nome)
    return cor.clip(0, 255).astype(np.uint8)


ATMOSFERA = {"venus": (255, 230, 170, 150), "marte": (255, 160, 120, 70), "jupiter": (255, 230, 200, 70),
             "saturno": (255, 230, 180, 70), "urano": (170, 240, 255, 120), "netuno": (90, 150, 255, 140)}
GIRO = {"mercurio": 0.05, "lua": 0.05, "venus": 0.08, "marte": 0.3, "jupiter": 0.5, "saturno": 0.45,
        "urano": 0.3, "netuno": 0.35}


@lru_cache(maxsize=16)
def _esfera(R: int, inclina: float, rola: float):
    S = int(R * 2.6)
    c = S / 2
    X = (np.arange(S, dtype=np.float32)[None, :] - c) / R
    Y = (np.arange(S, dtype=np.float32)[:, None] - c) / R
    X, Y = np.broadcast_arrays(X, Y)
    Xr = X * math.cos(rola) + Y * math.sin(rola)                     # "rola": eixo deitado (Urano)
    Yr = -X * math.sin(rola) + Y * math.cos(rola)
    r2 = X ** 2 + Y ** 2
    dentro = r2 < 1.0
    Z = np.sqrt(np.clip(1 - r2, 0, 1))
    yw = -Yr * math.cos(inclina) + Z * math.sin(inclina)
    zw = Yr * math.sin(inclina) + Z * math.cos(inclina)
    lat = np.arcsin(np.clip(yw, -1, 1))
    lon = np.arctan2(Xr, zw)
    L = np.array([-0.62, -0.42, 0.66], np.float32)
    L /= np.linalg.norm(L)
    luz = np.clip(X * L[0] + Y * L[1] + Z * L[2], 0, 1)
    alfa = (np.clip((1 - np.sqrt(r2)) * R * 1.5, 0, 1) * 255).astype(np.uint8)
    return S, dentro, lat[dentro], lon[dentro], luz[dentro], ((1 - Z) ** 3)[dentro], alfa


def _globo(nome, R, t, inclina=0.2, rola=0.0):
    S, dentro, lat, lon, luz, borda, alfa = _esfera(R, round(inclina, 3), round(rola, 3))
    tex = textura(nome)
    lo = (lon + t * GIRO.get(nome, 0.2) + math.pi) % (2 * math.pi)
    uf = lo / (2 * math.pi) * (TW - 1)
    vf = ((math.pi / 2 - lat) / math.pi * (TH - 1)).clip(0, TH - 1)
    if R > 450:                                            # de perto: interpolação suave (sem serrilhado)
        u0, v0 = np.floor(uf).astype(np.int32), np.floor(vf).astype(np.int32)
        du, dv = (uf - u0)[:, None], (vf - v0)[:, None]
        u1, v1 = (u0 + 1) % TW, np.minimum(v0 + 1, TH - 1)
        T = tex.astype(np.float32)
        cor = (T[v0, u0] * (1 - du) * (1 - dv) + T[v0, u1] * du * (1 - dv) + T[v1, u0] * (1 - du) * dv
               + T[v1, u1] * du * dv)
    else:
        cor = tex[vf.astype(np.int32), uf.astype(np.int32)].astype(np.float32)
    amb = 0.16 if nome in ("venus", "urano", "netuno") else 0.07                # atmosfera espalha um pouco de luz
    cor = cor * (amb + 1.02 * luz ** 0.9)[:, None]
    atm = ATMOSFERA.get(nome)
    if atm:
        cor += np.array(atm[:3], np.float32) * (borda * (0.2 + 0.6 * luz) * atm[3] / 255)[:, None]
    rgb = np.zeros((S, S, 3), np.uint8)
    rgb[dentro] = cor.clip(0, 255).astype(np.uint8)
    pl = Image.fromarray(np.dstack([rgb, alfa]), "RGBA")
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    if atm:
        g = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        c = S / 2
        ImageDraw.Draw(g).ellipse((c - R * 1.08, c - R * 1.08, c + R * 1.08, c + R * 1.08), fill=atm)
        out.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.08)))
    out.alpha_composite(pl)
    return out


def _aneis(R, saturno=True, abre=0.22, ang=-0.12):
    """Anéis em perspectiva. Devolve (atrás, frente) do mesmo tamanho, para pôr o planeta no meio."""
    S = int(R * 5.0)
    c = S / 2
    X = (np.arange(S, dtype=np.float32)[None, :] - c) / R
    Y = (np.arange(S, dtype=np.float32)[:, None] - c) / R
    X, Y = np.broadcast_arrays(X, Y)
    Xr = X * math.cos(ang) + Y * math.sin(ang)
    Yr = -X * math.sin(ang) + Y * math.cos(ang)
    q = np.sqrt(Xr ** 2 + (Yr / abre) ** 2)
    if saturno:                                    # C fraco, B forte, divisão de Cassini, A, divisão de Encke
        dens = (np.where((q > 1.24) & (q < 1.53), 0.25, 0) + np.where((q >= 1.53) & (q < 1.95), 0.95, 0)
                + np.where((q >= 2.03) & (q < 2.27), 0.7, 0))
        dens *= np.where((q > 2.21) & (q < 2.23), 0.2, 1)
        dens *= 0.85 + 0.15 * np.sin(q * 90)
        base = np.stack([228 - (q - 1.2) * 30, 206 - (q - 1.2) * 35, 160 - (q - 1.2) * 40], -1)
    else:                                          # Urano: anéis finos e escuros
        dens = sum(np.exp(-((q - r0) / 0.012) ** 2) * 0.6 for r0 in (1.64, 1.7, 1.78, 1.92, 2.02))
        base = np.stack([np.full_like(q, 190), np.full_like(q, 220), np.full_like(q, 230)], -1)
    luz = np.clip(0.75 + 0.25 * (-Xr / (q + 1e-6)), 0.4, 1)
    sombra = np.where((Yr < 0) & (np.abs(Xr) < 1.0) & (Xr > -0.1), 0.35, 1.0)      # sombra do planeta no anel de trás
    a = (np.clip(dens, 0, 1) * 255).astype(np.uint8)
    rgb = (base * (luz * sombra)[..., None]).clip(0, 255).astype(np.uint8)
    img = np.dstack([rgb, a])
    tras, frente = img.copy(), img.copy()
    tras[Yr > 0, 3] = 0
    frente[Yr <= 0, 3] = 0
    return Image.fromarray(tras, "RGBA"), Image.fromarray(frente, "RGBA")


def planeta(nome: str, R: int, t: float = 0.0) -> Image.Image:
    R = int(R)
    if nome == "terra":
        return terra(R, lon=-0.9 - t * 0.35, nuvens=t * 0.25, inclina=0.3)
    if nome in ("saturno", "urano"):
        tras, frente = _aneis(R, nome == "saturno", abre=0.22 if nome == "saturno" else 0.9,
                              ang=-0.12 if nome == "saturno" else 1.45)
        corpo = _globo(nome, R, t, inclina=0.35 if nome == "saturno" else 0.1, rola=0.0 if nome == "saturno" else 1.5)
        out = tras.copy()
        out.alpha_composite(corpo, (int((out.width - corpo.width) / 2), int((out.height - corpo.height) / 2)))
        out.alpha_composite(frente)
        return out
    return _globo(nome, R, t, inclina=0.25)
