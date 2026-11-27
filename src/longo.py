"""Vídeo longo (16:9) do E Se Fosse Real?: blocos (capítulos) narrados com a voz Puck, câmera sempre andando,
personagem "você" (astronauta) recorrente, placar e barra de capítulos fixos, e legenda discreta embaixo.
Regras do formato em docs/ESFR_LONGO.md. Nada de cartão parado com texto: número vira objeto animado.

Roteiro: {"formato": "longo", "canal": "esfr", "voz": "Puck", "clima": "curioso", "titulo", "titulo_youtube",
          "legenda_post", "capitulos": ["Mercúrio", ...] (barra no alto), "blocos": [{"capitulo": "Mercúrio",
          "cenas": [{"narracao": "...", "quadro": "<tipo>", ...}]}]}
Quadros:
  sistema     os planetas enfileirados; "foco" (nome), "placar": {"mercurio": "texto"} embaixo de cada um, "pan"
  planeta     um planeta grande; "nome", "zoom": [z0, z1], "x" (0 a 1), "nave": true (nave chegando), "rotulo"
  superficie  chão do planeta com o você; "nome", "efeitos": [calor, frio, pressao, vento, poeira, noite, sol_nasce],
              "medidor": {"de", "ate", "unidade", "rotulo"} (termômetro/medidor subindo), "traje": 0 a 1 (dano)
  descida     caindo dentro de um gigante gasoso; "nome", "esmaga": true (fim), "medidores": true (barras subindo)
  escala      "tipo": "terras" ("nome": planeta ao lado da Terra no tamanho real) | "dentro" (a Terra dentro de uma
              mancha: "nome" jupiter/netuno)
  (superficie: "pose": parado | acenando | andando (entra andando) | pulando (pulos lentos, gravidade fraca);
   "inscricao": true em qualquer cena mostra o botão "SE INSCREVE" pulsando)
  placar      quadro com os tempos de sobrevivência; "itens": [["Vênus", "texto"], ...], "destaque"
Em qualquer cena: "camera": {"zoom": [1.0, 1.12], "pan": [[0.5, 0.5], [0.55, 0.5]]}, "rotulo" (faixa embaixo, à esquerda).

python -m src.longo  (lê ROTEIRO_ARQ e, se quiser, BLOCOS="0,1" para renderizar só alguns blocos)
"""
import json
import math
import os
import random
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .util import RAIZ, log

W, H, FPS = 1920, 1080, 24
FONTE = str(RAIZ / "assets" / "fontes" / "Poppins-Bold.ttf")
FUNDO, FUNDO2 = (8, 18, 46), (22, 50, 104)
AMARELO, CIANO, BRANCO, VERMELHO = (255, 196, 36), (86, 214, 255), (245, 247, 252), (232, 60, 60)
NOMES = {"mercurio": "Mercúrio", "venus": "Vênus", "terra": "Terra", "marte": "Marte", "jupiter": "Júpiter",
         "saturno": "Saturno", "urano": "Urano", "netuno": "Netuno"}
ORDEM = ["mercurio", "venus", "terra", "marte", "jupiter", "saturno", "urano", "netuno"]
_cache: dict = {}


def _f(px):
    if px not in _cache:
        _cache[px] = ImageFont.truetype(FONTE, px)
    return _cache[px]


def _suave(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def _texto(d, cx, cy, txt, px, cor, sombra=True):
    f = _f(px)
    b = d.textbbox((0, 0), txt, font=f)
    x, y = cx - (b[2] - b[0]) / 2 - b[0], cy - (b[3] - b[1]) / 2 - b[1]
    if sombra:
        d.text((x + 3, y + 4), txt, font=f, fill=(0, 0, 0, 160))
    d.text((x, y), txt, font=f, fill=cor)


def _fundo_espaco(t, n=260, seed=1, deriva=8.0):
    k = ("espaco", seed)
    if k not in _cache:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        dd = np.sqrt(((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H / 2) / (H * 0.8)) ** 2).clip(0, 1)[..., None]
        a = np.array(FUNDO2, np.float32) * (1 - dd) * 0.6 + np.array(FUNDO, np.float32) * (1 - (1 - dd) * 0.6)
        _cache[k] = Image.fromarray(a.astype(np.uint8))
    img = _cache[k].copy()
    d = ImageDraw.Draw(img)
    for i in range(n):                                    # estrelas com leve paralaxe
        r = random.Random(i * 7 + seed)
        prof = 0.3 + r.random() * 0.7
        x = (r.random() * W - t * deriva * prof) % W
        y = r.random() * H
        b = int(120 + 120 * prof * (0.75 + 0.25 * math.sin(t * 2 + i)))
        s = 1.2 + prof * 1.6
        d.ellipse((x - s, y - s, x + s, y + s), fill=(b, b, min(255, b + 15)))
    return img


def _colar(img, sprite, cx, cy):
    img.paste(sprite, (int(cx - sprite.width / 2), int(cy - sprite.height / 2)), sprite)


# ---------------------------------------------------------------- o "você": astronauta recorrente
def astronauta(d, x, chao, h, t, dano=0.0, pose="parado", visor=CIANO):
    """Astronauta chapado de altura h, pés em (x, chao). dano 0 a 1: traje sujo, rachado, avermelhado."""
    s = h / 400
    bal = math.sin(t * 2.2) * 4 * s if pose == "parado" else 0
    passo = math.sin(t * 7) * 22 * s if pose == "andando" else 0   # pernas alternando
    branco = tuple(int(c * (1 - 0.35 * dano) + v * 0.35 * dano) for c, v in zip((240, 243, 250), (220, 120, 90)))
    cinza = (190, 198, 214)
    y0 = chao - h + bal
    d.rounded_rectangle((x - 95 * s, y0 + 150 * s, x - 40 * s, y0 + 300 * s), radius=int(20 * s), fill=cinza)   # mochila
    d.rounded_rectangle((x - 75 * s, y0 + 140 * s, x + 75 * s, y0 + 300 * s), radius=int(50 * s), fill=branco)   # corpo
    d.rounded_rectangle((x - 38 * s, y0 + 180 * s, x + 38 * s, y0 + 228 * s), radius=int(8 * s), fill=(150, 158, 178))
    for k, cor in enumerate((VERMELHO, CIANO, AMARELO)):
        d.ellipse((x - 26 * s + k * 20 * s, y0 + 196 * s, x - 14 * s + k * 20 * s, y0 + 208 * s), fill=cor)
    aceno = math.sin(t * 6) * 25 * s if pose == "acenando" else 0
    d.rounded_rectangle((x - 112 * s, y0 + 150 * s, x - 62 * s, y0 + 265 * s), radius=int(25 * s), fill=branco)
    if pose == "acenando":
        d.rounded_rectangle((x + 62 * s, y0 + 60 * s + aceno, x + 112 * s, y0 + 175 * s), radius=int(25 * s), fill=branco)
    else:
        d.rounded_rectangle((x + 62 * s, y0 + 150 * s, x + 112 * s, y0 + 265 * s), radius=int(25 * s), fill=branco)
    d.rounded_rectangle((x - 62 * s + passo, y0 + 280 * s, x - 10 * s + passo, chao), radius=int(24 * s), fill=branco)  # pernas
    d.rounded_rectangle((x + 10 * s - passo, y0 + 280 * s, x + 62 * s - passo, chao), radius=int(24 * s), fill=branco)
    d.rounded_rectangle((x - 66 * s + passo, chao - 26 * s, x - 6 * s + passo, chao + 4 * s), radius=int(12 * s), fill=cinza)
    d.rounded_rectangle((x + 6 * s - passo, chao - 26 * s, x + 66 * s - passo, chao + 4 * s), radius=int(12 * s), fill=cinza)
    hx, hy, hr = x, y0 + 80 * s, 82 * s                                                                          # capacete
    d.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=branco)
    d.rounded_rectangle((hx - hr * 0.72, hy - hr * 0.45, hx + hr * 0.72, hy + hr * 0.5), radius=int(40 * s), fill=(24, 40, 80))
    d.ellipse((hx - hr * 0.55, hy - hr * 0.35, hx - hr * 0.2, hy - hr * 0.08), fill=visor)
    if dano > 0.3:                                                                                               # rachaduras
        r = random.Random(3)
        for k in range(int(dano * 6)):
            a = r.random() * math.pi * 2
            x1, y1 = hx + math.cos(a) * hr * 0.2, hy + math.sin(a) * hr * 0.2
            d.line((x1, y1, x1 + math.cos(a) * hr * 0.5, y1 + math.sin(a) * hr * 0.5), fill=(230, 240, 255), width=max(2, int(4 * s)))


# ---------------------------------------------------------------- quadros
def _q_sistema(img, c, t, dur):
    from .planetas import planeta
    d = ImageDraw.Draw(img, "RGBA")
    tam = {"mercurio": 50, "venus": 76, "terra": 78, "marte": 60, "jupiter": 150, "saturno": 120, "urano": 96, "netuno": 94}
    xs = np.linspace(150, W - 150, len(ORDEM))
    foco = c.get("foco")
    placar = c.get("placar") or {}
    for i, n in enumerate(ORDEM):
        cy = H * 0.5 + math.sin(t * 0.8 + i) * 6
        R = tam[n] * (1.25 if n == foco else 1.0)
        sp = planeta(n, R, t + i)
        if foco and n != foco:
            sp = sp.copy()
            a = np.asarray(sp).copy()
            a[..., 3] = (a[..., 3] * 0.45).astype(np.uint8)
            sp = Image.fromarray(a, "RGBA")
        _colar(img, sp, xs[i], cy)
        d = ImageDraw.Draw(img, "RGBA")
        _texto(d, xs[i], H * 0.5 + 170, NOMES[n].upper(), 30, AMARELO if n == foco else (170, 185, 215))
        if n in placar:
            _texto(d, xs[i], H * 0.5 + 215, str(placar[n]).upper(), 26, BRANCO if n != "terra" else (120, 230, 140))
        if n == foco:
            p = 0.5 + 0.5 * math.sin(t * 4)
            rr = R * 1.55 + p * 8
            d.ellipse((xs[i] - rr, cy - rr, xs[i] + rr, cy + rr), outline=AMARELO + (200,), width=5)


def _q_planeta(img, c, t, dur):
    from .planetas import planeta
    z0, z1 = c.get("zoom", [1.0, 1.25])
    z = z0 + (z1 - z0) * _suave(t / max(0.1, dur))
    R = int(300 * z)
    cx = W * c.get("x", 0.5)
    _colar(img, planeta(c["nome"], R, t), cx, H * 0.5)
    if c.get("eixo") is not None:                        # eixo de rotação (graus a partir da vertical), tracejado
        d = ImageDraw.Draw(img, "RGBA")
        a = math.radians(float(c["eixo"]))
        dx, dy = math.sin(a), -math.cos(a)
        cresce = _suave(t / max(0.1, dur * 0.5))
        for k in range(-16, 17):
            if k % 2:
                continue
            f0, f1 = k / 16 * 1.45 * R * cresce, (k + 1) / 16 * 1.45 * R * cresce
            d.line((cx + dx * f0, H * 0.5 + dy * f0, cx + dx * f1, H * 0.5 + dy * f1), fill=AMARELO + (230,), width=8)
    if c.get("nave"):                                    # nave chegando pelo canto, com rastro
        d = ImageDraw.Draw(img, "RGBA")
        f = _suave(t / max(0.1, dur * 0.9))
        x, y = W * 0.08 + (cx - R * 0.9 - W * 0.08) * f, H * 0.2 + (H * 0.42 - H * 0.2) * f
        for k in range(10):
            d.ellipse((x - 60 - k * 22, y - 18 - k * 9, x - 40 - k * 22, y + 2 - k * 9), fill=AMARELO + (150 - k * 14,))
        d.polygon([(x + 60, y), (x - 30, y - 34), (x - 52, y), (x - 30, y + 34)], fill=BRANCO)
        d.ellipse((x - 6, y - 12, x + 18, y + 12), fill=CIANO)


SUP = {
    "mercurio": {"ceu": [(4, 4, 8), (14, 14, 22)], "chao": (118, 112, 108), "chao2": (84, 80, 78), "sol": 150, "estrelas": True},
    "venus": {"ceu": [(150, 82, 30), (236, 170, 84)], "chao": (112, 70, 40), "chao2": (82, 50, 30), "sol": 0, "estrelas": False},
    "marte": {"ceu": [(170, 120, 90), (226, 186, 148)], "chao": (176, 84, 46), "chao2": (130, 60, 36), "sol": 34, "estrelas": False},
    "terra": {"ceu": [(70, 140, 220), (170, 215, 250)], "chao": (70, 150, 80), "chao2": (50, 120, 64), "sol": 50, "estrelas": False},
    "lua": {"ceu": [(4, 4, 8), (12, 12, 20)], "chao": (160, 160, 166), "chao2": (120, 120, 128), "sol": 50, "estrelas": True},
}


def _q_superficie(img, c, t, dur):
    cfg = SUP[c["nome"]]
    ef = set(c.get("efeitos") or [])
    a = np.zeros((H, W, 3), np.float32)
    g = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    a[:] = np.array(cfg["ceu"][0], np.float32) * (1 - g) + np.array(cfg["ceu"][1], np.float32) * g
    if "noite" in ef:
        a *= 0.25
    img.paste(Image.fromarray(a.astype(np.uint8)))
    d = ImageDraw.Draw(img, "RGBA")
    if cfg["estrelas"] or "noite" in ef:
        for i in range(160):
            r = random.Random(i)
            x, y = r.random() * W, r.random() * H * 0.6
            d.ellipse((x - 1.6, y - 1.6, x + 1.6, y + 1.6), fill=(220, 225, 240, 220))
    sol_r = cfg["sol"]
    if sol_r and "noite" not in ef:                       # o Sol (em Mercúrio, enorme)
        sobe = 1.0
        if "sol_nasce" in ef:
            sobe = _suave(t / max(0.1, dur * 0.8))
        sx, sy = W * 0.16, H * 0.62 - (H * 0.36) * sobe
        for k in range(8, 0, -1):
            rr = sol_r * (1 + k * 0.28)
            d.ellipse((sx - rr, sy - rr, sx + rr, sy + rr), fill=(255, 220, 120, 16))
        d.ellipse((sx - sol_r, sy - sol_r, sx + sol_r, sy + sol_r), fill=(255, 236, 170))
    chao = H * 0.74
    r = random.Random(5)
    pts = [(0, H)]
    for k in range(0, W + 80, 80):                        # morros ao fundo
        pts.append((k, chao - 40 - r.random() * 60 - 50 * math.sin(k / 300)))
    pts.append((W, H))
    d.polygon(pts, fill=cfg["chao2"])
    d.rectangle((0, chao, W, H), fill=cfg["chao"])
    for k in range(14):                                   # crateras e pedras no chão
        rr = random.Random(k * 3)
        x, y, s = rr.random() * W, chao + 30 + rr.random() * (H - chao - 40), 20 + rr.random() * 50
        d.ellipse((x - s, y - s * 0.3, x + s, y + s * 0.3), fill=tuple(int(v * 0.8) for v in cfg["chao"]))
    dano = float(c.get("traje", 0))
    pose = c.get("pose", "parado")
    ax, ay = W * 0.42, chao + 60
    if pose == "andando":                                 # entra andando pela esquerda
        ax = W * 0.12 + (W * 0.42 - W * 0.12) * _suave(t / max(0.1, dur * 0.7))
        if t > dur * 0.7:
            pose = "parado"
    elif pose == "pulando":                               # gravidade fraca: pulos altos e lentos
        ciclo = (t * 0.55) % 1
        ay -= math.sin(ciclo * math.pi) * 260
        sombra_r = 90 * (1 - 0.4 * math.sin(ciclo * math.pi))
        d.ellipse((ax - sombra_r, chao + 50, ax + sombra_r, chao + 72), fill=(0, 0, 0, 70))
        pose = "parado"
    astronauta(d, ax, ay, 430, t, dano, pose)
    if "calor" in ef:                                     # ar tremendo e brilho vermelho
        q = 0.5 + 0.5 * math.sin(t * 3)
        d.rectangle((0, 0, W, H), fill=(255, 80, 20, int(40 + 30 * q)))
        for k in range(40):                               # brasas de calor subindo do chão
            rr = random.Random(k * 17)
            x = rr.random() * W + math.sin(t * 2 + k) * 20
            y = H - (t * (90 + rr.random() * 120) + rr.random() * H) % (H * 0.8)
            s_ = 3 + rr.random() * 5
            d.ellipse((x - s_, y - s_, x + s_, y + s_), fill=(255, 190, 90, 150))
    if "frio" in ef:                                      # vinheta gelada nas bordas e cristais caindo
        k_ = ("vinheta_fria",)
        if k_ not in _cache:
            yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
            dd = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
            a_ = (np.clip((dd - 0.75) * 1.6, 0, 1) * 170).astype(np.uint8)
            v = np.dstack([np.full((H, W), 200, np.uint8), np.full((H, W), 230, np.uint8), np.full((H, W), 255, np.uint8), a_])
            _cache[k_] = Image.fromarray(v, "RGBA")
        img.paste(_cache[k_], (0, 0), _cache[k_])
        d = ImageDraw.Draw(img, "RGBA")
        for k in range(50):
            rr = random.Random(k * 5)
            x = rr.random() * W + math.sin(t + k) * 15
            y = (rr.random() * H + t * (40 + rr.random() * 40)) % H
            s_ = 2 + rr.random() * 3
            d.line((x - s_, y, x + s_, y), fill=(235, 245, 255, 200), width=2)
            d.line((x, y - s_, x, y + s_), fill=(235, 245, 255, 200), width=2)
    if "poeira" in ef or "vento" in ef:
        for k in range(60):
            rr = random.Random(k * 9)
            x = (rr.random() * W + t * (900 if "vento" in ef else 300)) % (W + 200) - 100
            y = rr.random() * H
            d.line((x, y, x + (90 if "vento" in ef else 30), y + 4), fill=(255, 230, 200, 90), width=3)
    if "pressao" in ef:                                   # setas apertando o você de todos os lados
        ap = 20 * abs(math.sin(t * 3))
        cx, cy = W * 0.42, chao - 215
        for ang in range(0, 360, 45):
            aa = math.radians(ang)
            r1, r2 = 360 - ap, 270 - ap
            x1, y1, x2, y2 = cx + math.cos(aa) * r1, cy + math.sin(aa) * r1, cx + math.cos(aa) * r2, cy + math.sin(aa) * r2
            d.line((x1, y1, x2, y2), fill=VERMELHO, width=16)
            px, py = -math.sin(aa) * 26, math.cos(aa) * 26
            d.polygon([(x2 - math.cos(aa) * 8, y2 - math.sin(aa) * 8), (x2 + math.cos(aa) * 40 + px, y2 + math.sin(aa) * 40 + py),
                       (x2 + math.cos(aa) * 40 - px, y2 + math.sin(aa) * 40 - py)], fill=VERMELHO)
    if c.get("medidor"):
        _medidor(d, c["medidor"], t, dur, W * 0.78, H * 0.44)   # mais alto: o rótulo não encosta na legenda


def _medidor(d, m, t, dur, cx, cy):
    """Termômetro/medidor que enche contando até o valor (o número anda junto com a barra)."""
    de, ate = float(m.get("de", 0)), float(m["ate"])
    f = _suave(t / max(0.1, dur * 0.7))
    v = de + (ate - de) * f
    alto, larg = 470, 70
    topo = cy - alto / 2
    d.rounded_rectangle((cx - larg / 2, topo, cx + larg / 2, topo + alto), radius=35, fill=(255, 255, 255, 50),
                        outline=BRANCO, width=5)
    d.ellipse((cx - 70, topo + alto - 40, cx + 70, topo + alto + 100), fill=VERMELHO if ate > de else CIANO, outline=BRANCO, width=5)
    lo, hi = min(de, ate, 0), max(de, ate, 1)
    frac = (v - lo) / (hi - lo)
    y = topo + alto - frac * (alto - 30)
    d.rounded_rectangle((cx - larg / 2 + 12, y, cx + larg / 2 - 12, topo + alto + 20), radius=20,
                        fill=VERMELHO if ate > de else CIANO)
    txt = f"{v:,.0f}".replace(",", ".") + " " + m.get("unidade", "")
    _texto(d, cx, topo - 70, txt, 76, AMARELO)
    if m.get("rotulo"):
        _texto(d, cx, topo + alto + 135, str(m["rotulo"]).upper(), 32, BRANCO)


CAMADAS = {"jupiter": [(236, 222, 196), (222, 186, 146), (186, 128, 84), (160, 104, 72), (120, 60, 40), (70, 30, 24)],
           "saturno": [(242, 226, 180), (230, 206, 150), (214, 186, 128), (180, 150, 96), (120, 90, 60), (60, 40, 30)],
           "urano": [(190, 236, 240), (160, 220, 228), (120, 196, 210), (80, 150, 170), (40, 90, 110), (20, 40, 60)],
           "netuno": [(110, 160, 240), (78, 126, 230), (50, 90, 200), (34, 62, 160), (20, 36, 110), (10, 16, 50)]}


def _q_descida(img, c, t, dur):
    cores = CAMADAS[c["nome"]]
    prog = _suave(t / max(0.1, dur)) * 0.6 + float(c.get("de", 0))
    a = np.zeros((H, W, 3), np.float32)
    y = np.arange(H, dtype=np.float32)[:, None]
    fundo = (prog + y / H * 0.35) * (len(cores) - 1)
    fundo = np.clip(fundo, 0, len(cores) - 1.001)
    i0 = fundo.astype(int)
    fr = (fundo - i0)[..., None]
    C = np.asarray(cores, np.float32)
    a[:] = (C[i0] * (1 - fr) + C[np.minimum(i0 + 1, len(cores) - 1)] * fr)
    img.paste(Image.fromarray(a.clip(0, 255).astype(np.uint8)))
    d = ImageDraw.Draw(img, "RGBA")
    for k in range(26):                                   # nuvens subindo (dá a sensação de cair)
        r = random.Random(k * 13)
        cy = (r.random() * H * 1.4 - t * (380 + r.random() * 200)) % (H * 1.4) - H * 0.2
        cx = r.random() * W
        s = 120 + r.random() * 260
        cor = cores[min(len(cores) - 1, int(prog * len(cores) + r.random() * 2))]
        d.ellipse((cx - s * 1.8, cy - s * 0.35, cx + s * 1.8, cy + s * 0.35), fill=tuple(int(v * 1.08) for v in cor) + (110,))
    esmaga = c.get("esmaga")
    enc = 1 - 0.55 * _suave((t - dur * 0.3) / max(0.1, dur * 0.6)) if esmaga else 1.0
    tom = int(255 * (1 - enc)) if esmaga else 0
    camada = Image.new("RGBA", (700, 700), (0, 0, 0, 0))     # o você numa camada própria, girando enquanto cai
    astronauta(ImageDraw.Draw(camada), 350, 350 + 215 * enc, int(430 * enc), t, 0.3 if esmaga else 0.0, "parado",
               visor=(255, 120, 90) if esmaga else CIANO)
    camada = camada.rotate(math.sin(t * 1.1) * 28 + t * 6, resample=Image.BICUBIC)
    img.paste(camada, (int(W * 0.5 - 350), int(H * 0.55 - 350 + math.sin(t * 1.7) * 18)), camada)
    d = ImageDraw.Draw(img, "RGBA")
    if esmaga:
        d.rectangle((0, 0, W, H), fill=(255, 60, 20, min(140, tom)))
    if c.get("medidores", True):
        for k, (nome, cor) in enumerate((("PRESSÃO", VERMELHO), ("CALOR", AMARELO))):
            x = W * 0.86 + k * 110
            nivel = min(1.0, prog * 1.4 + 0.05)
            d.rounded_rectangle((x - 30, H * 0.22, x + 30, H * 0.78), radius=30, fill=(0, 0, 0, 90), outline=BRANCO, width=4)
            topo = H * 0.78 - (H * 0.56) * nivel
            d.rounded_rectangle((x - 20, topo, x + 20, H * 0.78 - 10), radius=20, fill=cor)
            _texto(d, x, H * 0.83, nome, 26, BRANCO)


def _q_escala(img, c, t, dur):
    from .planetas import planeta
    d = ImageDraw.Draw(img, "RGBA")
    if c.get("tipo") == "dentro":                         # a Terra dentro de uma mancha do planeta (perto, em close)
        nome = c["nome"]
        f = _suave(t / max(0.1, dur * 0.6))
        R = 1500
        from .planetas import GIRO
        lat, lon = (-0.39, 0.6) if nome == "jupiter" else (-0.36, -0.4)
        meia = 0.22 if nome == "jupiter" else 0.17                       # meia largura da mancha (radianos)
        fi = 0.25
        Ys = -math.sin(lat) * math.cos(fi) + math.cos(lat) * math.sin(fi)   # mancha virada de frente (lon 0)
        sp = planeta(nome, R, lon / GIRO[nome])
        _colar(img, sp, W / 2, H / 2 - Ys * R)
        larg = 2 * meia * R * math.cos(lat)
        # Júpiter: a mancha tem 2 vezes a largura da Terra; Netuno: a mancha cabia a Terra inteira
        rt = larg / 4 if nome == "jupiter" else larg * 0.3
        terra = planeta("terra", int(rt), t)
        f2 = _suave((t - dur * 0.15) / max(0.1, dur * 0.6))        # a mancha aparece primeiro; a Terra entra depois
        _colar(img, terra, W / 2 + (1 - f2) * W * 0.75, H / 2)
        return
    nome = c["nome"]
    diam = {"mercurio": 4879, "venus": 12104, "terra": 12756, "marte": 6792, "jupiter": 142984, "saturno": 120536,
            "urano": 51118, "netuno": 49528}
    maior = max(diam[nome], diam["terra"])
    escala = (300 if maior == diam["terra"] else 400) / maior       # raio do maior em pixels / diâmetro real
    f = _suave(t / max(0.1, dur * 0.5))
    Rp, Rt = diam[nome] * escala * f, diam["terra"] * escala
    xp = W * 0.66
    _colar(img, planeta(nome, max(4, int(Rp)), t), xp, H * 0.5)
    _colar(img, planeta("terra", max(4, int(Rt)), t), W * 0.28, H * 0.5)
    d = ImageDraw.Draw(img, "RGBA")
    _texto(d, W * 0.28, H * 0.5 + Rt + 60, "TERRA", 34, (170, 185, 215))
    _texto(d, xp, min(H - 60, H * 0.5 + Rp + 60), NOMES[nome].upper(), 34, AMARELO)


def _q_placar(img, c, t, dur):
    d = ImageDraw.Draw(img, "RGBA")
    _texto(d, W / 2, 190, str(c.get("titulo", "TEMPO DE SOBREVIVÊNCIA")).upper(), 56, AMARELO)
    itens = c.get("itens") or []
    for k, (nome, txt) in enumerate(itens):
        f = _suave((t - k * 0.25) / 0.6)
        if f <= 0:
            continue
        y = 270 + k * 84
        x0 = W * 0.2 - (1 - f) * 200
        cor = AMARELO if nome == c.get("destaque") else BRANCO
        d.rounded_rectangle((x0, y, x0 + W * 0.6, y + 74), radius=20, fill=(255, 255, 255, int(30 * f)))
        d.text((x0 + 30, y + 10), str(nome).upper(), font=_f(44), fill=cor)
        tw = d.textlength(str(txt), font=_f(40))
        d.text((x0 + W * 0.6 - 30 - tw, y + 14), str(txt), font=_f(40), fill=cor)


QUADROS = {"sistema": _q_sistema, "planeta": _q_planeta, "superficie": _q_superficie, "descida": _q_descida,
           "escala": _q_escala, "placar": _q_placar}


def _hud(img, c, t):
    d = ImageDraw.Draw(img, "RGBA")
    caps = c.get("_capitulos") or []
    atual = c.get("_capitulo")
    if caps:                                              # barra de capítulos no alto
        larg = 1100
        x0 = (W - larg) / 2
        passo = larg / max(1, len(caps) - 1) if len(caps) > 1 else 0
        idx = caps.index(atual) if atual in caps else -1
        d.line((x0, 58, x0 + larg, 58), fill=(255, 255, 255, 70), width=4)
        if idx >= 0:
            d.line((x0, 58, x0 + passo * idx, 58), fill=AMARELO, width=6)
        for k, nome in enumerate(caps):
            x = x0 + passo * k
            r = 11 if k == idx else 7
            d.ellipse((x - r, 58 - r, x + r, 58 + r), fill=AMARELO if k <= idx else (120, 130, 160))
            if k == idx:
                _texto(d, x, 96, nome.upper(), 26, AMARELO)
    d.rounded_rectangle((W - 230, 30, W - 40, 82), radius=14, fill=AMARELO)                        # selo do canal
    d.text((W - 215, 36), "E SE...", font=_f(32), fill=FUNDO)
    if c.get("_titulo_cap") and t < 2.4:                  # abertura do capítulo: o nome entra grande e sai
        f = _suave(t / 0.5) * (1 - _suave((t - 1.8) / 0.6))
        nome = str(c["_titulo_cap"]).upper()
        px = int(150 * (1.25 - 0.25 * _suave(t / 0.5)))
        cam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dc = ImageDraw.Draw(cam)
        dc.rectangle((0, H * 0.38, W, H * 0.62), fill=(8, 18, 46, int(150 * f)))
        _texto(dc, W / 2, H * 0.47, nome, px, AMARELO + (int(255 * f),), sombra=False)
        larg = 520 * _suave((t - 0.2) / 0.6)
        dc.rectangle((W / 2 - larg / 2, H * 0.56, W / 2 + larg / 2, H * 0.56 + 8), fill=BRANCO + (int(255 * f),))
        img.paste(cam, (0, 0), cam)
        d = ImageDraw.Draw(img, "RGBA")
    if c.get("inscricao"):                                # botão genérico pulsando no fim do vídeo
        f = _suave((t - 0.6) / 0.5)
        pul = 1 + 0.06 * math.sin(t * 6)
        bw, bh = 520 * pul * f, 120 * pul * f
        if f > 0.05:
            cx, cy = W / 2, H * 0.78
            d.rounded_rectangle((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), radius=int(bh / 2), fill=AMARELO)
            _texto(d, cx + 30 * f, cy, "SE INSCREVE", int(56 * f), FUNDO, sombra=False)
            sx = cx - bw / 2 + 60 * f
            d.ellipse((sx - 26 * f, cy - 30 * f, sx + 26 * f, cy + 22 * f), fill=FUNDO)       # sininho
            d.rectangle((sx - 30 * f, cy + 12 * f, sx + 30 * f, cy + 22 * f), fill=FUNDO)
            d.ellipse((sx - 8 * f, cy + 22 * f, sx + 8 * f, cy + 36 * f), fill=FUNDO)
    t_rot = t - (2.4 if c.get("_titulo_cap") else 0.0)       # com título de capítulo, a faixa entra depois dele
    if c.get("rotulo") and t_rot >= 0:                    # faixa de documentário embaixo, à esquerda
        f = _suave(t_rot / 0.4)
        txt = str(c["rotulo"]).upper()
        tw = d.textlength(txt, font=_f(40))
        x0 = 70 - (1 - f) * 400
        d.rounded_rectangle((x0, H - 250, x0 + tw + 60, H - 180), radius=14, fill=(8, 18, 46, 210))
        d.rectangle((x0, H - 250, x0 + 10, H - 180), fill=AMARELO)
        d.text((x0 + 34, H - 244), txt, font=_f(40), fill=BRANCO)


def quadro(c: dict, t: float, dur: float, n: int) -> Image.Image:
    tipo = c.get("quadro", "planeta")
    img = _fundo_espaco(t) if tipo in ("sistema", "planeta", "escala", "placar") else Image.new("RGB", (W, H), FUNDO)
    QUADROS[tipo](img, c, t, dur)
    cam = c.get("camera") or {}
    z0, z1 = cam.get("zoom", [1.0, 1.06])
    z = z0 + (z1 - z0) * _suave(t / max(0.1, dur))
    (px0, py0), (px1, py1) = cam.get("pan", [[0.5, 0.5], [0.5, 0.5]])
    f = _suave(t / max(0.1, dur))
    px, py = px0 + (px1 - px0) * f, py0 + (py1 - py0) * f
    cw, ch = W / z, H / z
    x0 = min(max(0.0, px * W - cw / 2), W - cw)
    y0 = min(max(0.0, py * H - ch / 2), H - ch)
    img = img.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch))
    _hud(img, c, t)
    a = np.asarray(img).astype(np.float32)
    if c.get("_fade"):                                    # escurece só na virada de capítulo
        borda = min(t, dur - t)
        if borda < 0.25:
            a *= max(0.0, borda) / 0.25
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def renderizar_cena(c: dict, voz: dict, destino: Path, pausa: float, n: int) -> float:
    dur = voz["duracao"] + pausa
    frames = math.ceil(dur * FPS)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", str(voz["arquivo"]),
                           "-filter_complex", "[1:a]aresample=44100,apad[a]", "-map", "0:v", "-map", "[a]",
                           "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "160k", "-ac", "2", str(destino)], stdin=subprocess.PIPE)
    try:
        for k in range(frames):
            ff.stdin.write(quadro(c, k / FPS, dur, n * 100000 + k).tobytes())
    finally:
        ff.stdin.close()
        ff.wait()
    return dur


def _legendas(frases: list, destino: Path) -> None:
    """Legenda discreta embaixo (frase inteira, 1 linha): ajuda quem assiste sem som."""
    def tt(s):
        h, m = int(s // 3600), int(s % 3600 // 60)
        return f"{h}:{m:02d}:{s % 60:05.2f}"
    linhas = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "", "[V4+ Styles]",
              "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,"
              "StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
              "Style: L,Poppins,46,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,4,2,2,160,160,70,1",
              "", "[Events]", "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text"]
    for ini, fim, txt in frases:
        linhas.append(f"Dialogue: 0,{tt(ini)},{tt(fim)},L,,0,0,0,,{txt}")
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")


def _efeitos(eventos: list, total: float, destino: Path) -> Path:
    """Efeitos sonoros sintetizados (sem bipes): "whoosh" na virada de capítulo e na chegada da nave,
    ronco grave nas descidas, vento nas cenas de vento/poeira e um rumor quente nas cenas de calor."""
    import wave
    sr = 44100
    n = int(total * sr) + sr
    out = np.zeros(n, np.float32)
    rnd = np.random.RandomState(9)

    def ruido(seg, corte):                               # ruído filtrado (passa-baixa simples no espectro)
        m = int(seg * sr)
        x = rnd.randn(m).astype(np.float32)
        X = np.fft.rfft(x)
        fr = np.fft.rfftfreq(m, 1 / sr)
        X *= 1 / np.sqrt(1 + (fr / corte) ** 4)
        y = np.fft.irfft(X, m).astype(np.float32)
        return y / (np.abs(y).max() + 1e-9)

    for t0, dur, quadro_, ef, inicio in eventos:
        a = int(t0 * sr)
        if inicio:                                        # whoosh: ruído que sobe e desce em 1,4 s
            w = ruido(1.4, 1800)
            env = np.sin(np.linspace(0, np.pi, len(w))) ** 2
            seg = w * env * 0.55
            out[a:a + len(seg)] += seg[:max(0, min(len(seg), n - a))]
        m = int(dur * sr)
        env = np.minimum(1, np.minimum(np.arange(m) / (0.4 * sr), (m - np.arange(m)) / (0.4 * sr))).astype(np.float32)
        if quadro_ == "descida":
            seg = ruido(dur, 120) * env * 0.5
        elif "vento" in ef or "poeira" in ef:
            seg = ruido(dur, 900) * env * 0.22 * (0.7 + 0.3 * np.sin(np.arange(m) / sr * 1.3))
        elif "calor" in ef:
            seg = ruido(dur, 250) * env * 0.25
        else:
            continue
        out[a:a + m] += seg[:max(0, min(m, n - a))]
    out = np.clip(out, -1, 1)
    est = np.stack([out, np.roll(out, 300)], -1)
    with wave.open(str(destino), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((est * 32767 * 0.8).astype("<i2").tobytes())
    return destino


def _narracao(sub: dict, cfg: dict, pasta: Path, bi: int, narrar) -> list:
    """Narra o bloco, ou reaproveita a narração de um render anterior (NARRACAO_CACHE) se o texto for o mesmo.
    Assim dá para refazer o visual do longo sem gastar a cota de voz. Sempre salva vozes.json para a próxima vez."""
    import hashlib
    texto = "\n".join(c["narracao"].strip() for c in sub["cenas"])
    assinatura = hashlib.sha1(texto.encode("utf-8")).hexdigest()
    cache = os.environ.get("NARRACAO_CACHE", "").strip()
    if cache:
        mudou = False
        candidatos = []                                   # pode haver vários renders no cache: fica com a melhor nota
        for achado in Path(cache).rglob(f"audio_{bi:02d}/vozes.json"):
            dados = json.loads(achado.read_text(encoding="utf-8"))
            candidatos.append((-(dados.get("nota") or 0), str(achado), achado, dados))
        for _, _, achado, dados in sorted(candidatos):
            if dados.get("assinatura") != assinatura:
                mudou = True
                continue
            pasta.mkdir(parents=True, exist_ok=True)
            vozes = []
            for v in dados["vozes"]:
                destino = pasta / v["arquivo"]
                shutil.copy(achado.parent / v["arquivo"], destino)
                vozes.append({"arquivo": destino, "duracao": v["duracao"], "palavras": v.get("palavras", [])})
            shutil.copy(achado, pasta / "vozes.json")     # guarda de novo: o próximo render também pode reaproveitar
            log(f"  narração reaproveitada de {achado.parent.parent.name} ({len(vozes)} falas, nota {dados.get('nota', '?')})")
            return vozes
        if mudou:
            log("  o texto do bloco mudou: narrando de novo")
    vozes = narrar(sub, cfg, pasta)
    (pasta / "vozes.json").write_text(json.dumps({
        "assinatura": assinatura, "nota": sub.get("_nota"),
        "vozes": [{"arquivo": Path(v["arquivo"]).name, "duracao": v["duracao"], "palavras": v.get("palavras", [])}
                  for v in vozes]}, ensure_ascii=False), encoding="utf-8")
    return vozes


def _variar(cenas: list) -> None:
    """Planeta em várias cenas seguidas cansa: alterna o enquadramento (lado e direção da câmera) quando o roteiro
    não pediu um. Não muda nada que o roteiro já definiu."""
    seq = 0
    for i, c in enumerate(cenas):
        ant = cenas[i - 1] if i else {}
        if c.get("quadro") == "planeta" and ant.get("quadro") == "planeta" and ant.get("nome") == c.get("nome"):
            seq += 1
        else:
            seq = 0
        if c.get("quadro") != "planeta" or seq == 0:
            continue
        if "x" not in c:
            c["x"] = (0.36, 0.64, 0.5)[seq % 3]
        if "camera" not in c:
            lado = 0.42 if c["x"] < 0.5 else 0.58 if c["x"] > 0.5 else 0.5
            c["camera"] = ({"zoom": [1.0, 1.12], "pan": [[0.5, 0.5], [lado, 0.5]]} if seq % 2 else
                           {"zoom": [1.15, 1.0], "pan": [[lado, 0.48], [0.5, 0.5]]})


def montar(r: dict, pasta: Path) -> tuple[Path, list]:
    from .util import carregar_config, duracao
    from .voz_gemini import narrar_roteiro
    from .montagem import _trilha, FONTES
    cfg = carregar_config()
    pasta.mkdir(parents=True, exist_ok=True)
    so = [int(x) for x in os.environ.get("BLOCOS", "").replace(" ", "").split(",") if x != ""]
    clipes, frases, capitulos, eventos, t0 = [], [], [], [], 0.0
    caps = r.get("capitulos") or [b["capitulo"] for b in r["blocos"]]
    for bi, b in enumerate(r["blocos"]):
        if so and bi not in so:
            continue
        log(f"Bloco {bi + 1}/{len(r['blocos'])}: {b['capitulo']} ({len(b['cenas'])} cenas)")
        sub = {"cenas": b["cenas"], "voz": r.get("voz", "Puck"), "clima": r.get("clima", "curioso"), "canal": "esfr",
               "formato": "voce", "tomadas": b.get("tomadas", r.get("tomadas", 2))}
        vozes = _narracao(sub, cfg, pasta / f"audio_{bi:02d}", bi, narrar_roteiro)
        capitulos.append((t0, b["capitulo"]))
        _variar(b["cenas"])
        for ci, (cena, voz) in enumerate(zip(b["cenas"], vozes)):
            cena.update(_capitulos=caps, _capitulo=b.get("marca", b["capitulo"]), _fade=ci in (0, len(b["cenas"]) - 1),
                        _titulo_cap=b["capitulo"] if ci == 0 and bi > 0 else None)
            pausa = 0.35 if ci < len(b["cenas"]) - 1 else 0.9
            destino = pasta / f"clip_{bi:02d}_{ci:02d}.mp4"
            dur = renderizar_cena(cena, voz, destino, pausa, bi * 100 + ci)
            frases.append((t0, t0 + voz["duracao"], cena["narracao"]))
            eventos.append((t0, dur, cena.get("quadro"), set(cena.get("efeitos") or []), ci == 0))
            t0 += dur
            clipes.append(destino)
    lista = pasta / "lista.txt"
    lista.write_text("".join(f"file '{c.name}'\n" for c in clipes), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "lista.txt", "-c", "copy",
                    "juntos.mp4"], check=True, cwd=pasta)
    _legendas(frases, pasta / "legendas.ass")
    total = duracao(pasta / "juntos.mp4")
    if r.get("trilha") == "propria":                      # trilha sintetizada do canal (src/trilha_esfr.py)
        from .trilha_esfr import gerar
        arq = gerar(pasta / "trilha.wav")
        vol = float(r.get("trilha_volume", 0.22))
        log("Trilha: própria do canal (sintetizada)")
        extras = ["-stream_loop", "-1", "-i", str(arq)]
        filtro_bg = (f"[1:a]aformat=channel_layouts=stereo,volume={vol},afade=t=in:d=2,"
                     f"afade=t=out:st={max(total - 3, 0):.2f}:d=3[bg]")
    else:
        extras, filtro_bg = _trilha(total, cfg, r)
    sfx = _efeitos(eventos, total, pasta / "efeitos.wav")
    idx = 1 + (1 if extras else 0)
    extras = [*extras, "-i", str(sfx)]
    mistura = (f"[0:a]asplit=3[voz][chave][chave2];[{idx}:a]aformat=channel_layouts=stereo,volume=0.55[sfx];"
               "[sfx][chave2]sidechaincompress=threshold=0.04:ratio=2.5:attack=30:release=400[sfxd];"
               "[bg][chave]sidechaincompress=threshold=0.05:ratio=2.5:attack=40:release=600[bgd];"
               "[voz][bgd][sfxd]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "juntos.mp4", *extras, "-filter_complex",
                    f"[0:v]ass=legendas.ass:fontsdir={FONTES}[v];{filtro_bg};{mistura}", "-map", "[v]", "-map", "[a]",
                    "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "video_longo.mp4"], check=True, cwd=pasta)
    log(f"Vídeo longo pronto: {total / 60:.1f} min")
    return pasta / "video_longo.mp4", capitulos


def main():
    from . import telegram
    arq = os.environ.get("ROTEIRO_ARQ", "").strip()
    r = json.loads((RAIZ / arq).read_text(encoding="utf-8"))
    trab = RAIZ / "trabalho"
    shutil.rmtree(trab, ignore_errors=True)
    final, capitulos = montar(r, trab / "longo")
    def mmss(s):
        return f"{int(s // 60)}:{int(s % 60):02d}"
    caps_txt = "\n".join(f"{mmss(t)} {nome}" for t, nome in capitulos)
    (trab / "capitulos.txt").write_text(caps_txt, encoding="utf-8")
    log("Capítulos:\n" + caps_txt)
    previas = RAIZ / "data" / "previas"
    previas.mkdir(parents=True, exist_ok=True)
    nome = Path(arq).stem
    from .util import duracao as _dur
    passo = max(4.0, _dur(final) / 64)                  # a folha cobre o vídeo inteiro (64 quadros)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(final), "-vf", f"fps=1/{passo:.2f},scale=320:-1,tile=8x8",
                    "-frames:v", "1", "-q:v", "4", str(previas / f"{nome}.jpg")])
    try:
        capa = thumb(r, trab / "thumb_longo.jpg")
        telegram.enviar_foto(capa, "[E Se Fosse Real?] Thumb do vídeo longo: toque e salve na galeria")
        telegram.enviar_arquivo(capa, "Thumb do vídeo longo: arquivo original, sem compressão")
    except Exception as e:  # noqa: BLE001
        log(f"Thumb no Telegram falhou: {e}")
    try:
        telegram.enviar_mensagem(f"[E Se Fosse Real?] Vídeo longo pronto: {r['titulo']}\n\nCapítulos:\n{caps_txt}")
        envio = final
        if final.stat().st_size > 48 * 1024 * 1024:       # o bot do Telegram só manda até 50 MB: cópia mais leve
            from .util import duracao
            dur = duracao(final)
            kbps = int((45 * 8 * 1024) / dur - 128)
            envio = final.with_name("video_longo_telegram.mp4")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(final), "-c:v", "libx264", "-preset", "medium",
                            "-b:v", f"{kbps}k", "-maxrate", f"{int(kbps * 1.3)}k", "-bufsize", f"{kbps * 2}k",
                            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(envio)], check=True)
            log(f"Cópia para o Telegram: {envio.stat().st_size / 1e6:.0f} MB ({kbps} kbps)")
        telegram.enviar_video(envio, f"[E Se Fosse Real?] {r['titulo']}", W, H)
        if envio != final:
            telegram.enviar_mensagem("Essa cópia foi comprimida para caber no Telegram. O arquivo em qualidade máxima "
                                     "está no GitHub Actions (artefato video-longo).")
    except Exception as e:  # noqa: BLE001
        log(f"Telegram falhou: {e}")



def thumb(r: dict, destino: Path) -> Path:
    """Thumb 16:9 (1280x720) do vídeo longo: o você em Vênus pegando fogo, os planetas em fila e a pergunta."""
    from .planetas import planeta
    img = _fundo_espaco(0.0).copy()
    d = ImageDraw.Draw(img, "RGBA")
    tam = {"mercurio": 48, "venus": 72, "terra": 74, "marte": 58, "jupiter": 150, "saturno": 120, "urano": 92, "netuno": 90}
    xs = np.linspace(170, W - 170, len(ORDEM))
    for i, n in enumerate(ORDEM):                         # fila de planetas embaixo
        _colar(img, planeta(n, tam[n] * 0.95, 1.0 + i), xs[i], H * 0.86)
    d = ImageDraw.Draw(img, "RGBA")
    ven = planeta("venus", 300, 2.0)
    _colar(img, ven, W * 0.8, H * 0.37)
    d = ImageDraw.Draw(img, "RGBA")
    for k in range(10, 0, -1):                            # brilho de calor em volta de Vênus
        rr = 300 + k * 14
        d.ellipse((W * 0.8 - rr, H * 0.37 - rr, W * 0.8 + rr, H * 0.37 + rr), outline=(255, 120, 30, 10), width=14)
    astronauta(d, W * 0.56, H * 0.66, 330, 0.0, 0.5, "acenando")
    linhas = [(l.strip().upper(), AMARELO if k == 1 else BRANCO)
              for k, l in enumerate(str(r.get("thumb_texto", "DÁ PRA|SOBREVIVER?")).split("|"))]
    y = 120
    for txt, cor in linhas:
        px = 150
        while d.textlength(txt, font=_f(px)) > W * 0.55 and px > 60:
            px -= 6
        for dx, dy in ((5, 6), (0, 0)):
            d.text((80 + dx, y + dy), txt, font=_f(px), fill=(0, 0, 0, 200) if dx else cor)
        y += px * 1.08
    d.rounded_rectangle((80, y + 20, 80 + d.textlength("E SE FOSSE REAL?", font=_f(40)) + 50, y + 92), radius=34, fill=(8, 14, 40))
    d.text((105, y + 30), "E SE FOSSE REAL?", font=_f(40), fill=CIANO)
    destino.parent.mkdir(parents=True, exist_ok=True)
    img.resize((1280, 720), Image.LANCZOS).save(destino, quality=92)
    return destino


if __name__ == "__main__":
    main()
