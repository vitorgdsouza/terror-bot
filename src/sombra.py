"""Formato "sombra": animação minimalista em silhuetas pretas sobre vermelho, com identidade própria.

Fundo vermelho com um halo no meio; tudo é silhueta preta com contorno vermelho-escuro; olhos brancos.
Sem legenda: só palavras-chave no alto da tela ("texto"), como avisos.

Cena: {"narracao": "...", "quadro": "<tipo>", ...opções}
  quadro:
    relogio   relógio digital; "hora": "03:17"
    quarto    a cama com você deitado e a porta à direita; "porta": fechada|entreaberta|aberta,
              "luz": true/false (luz do corredor por baixo da porta), "ondas": true (a voz vindo da porta),
              "olhos": abertos|fechados (seus olhos na cama)
    rosto     close do seu rosto; "olhos": abertos|fechados|arregalados|apertados, "boca": reta|aberta|tremendo,
              "olhar": -1..1 (para onde as pupilas olham)
    porta     close da porta; "porta", "luz", "pes": true (sombra de pés na luz por baixo), "ondas"
    portas    três portas numeradas; "pes": 1|2|3 (pés debaixo dessa porta), "entreaberta": 1|2|3
    abismo    close do Abismo: cabeça comprida, olhos brancos de íris vermelha, sorriso enorme; "maos": true
    destaque  uma palavra grande no meio ("destaque": "primeiro")
    preto     tela preta
  "texto": aviso curto no alto da tela ("|" quebra a linha)
  "batidas": N batidas na porta (com som e contador de bolinhas); "x": true = a última é a errada (X vermelho);
  "batidas_apos_voz": true = as batidas vêm depois da fala, no silêncio
  "susto": true = tremor de câmera
"""
import math
import random
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .util import RAIZ

W, H, FPS = 1080, 1920, 24
PRETO = (10, 4, 6)
ARO = (96, 8, 14)
BRANCO = (242, 232, 232)
TEXTO = (240, 206, 206)
VERM_VIVO = (255, 48, 48)
MONO = next((p for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
                         "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
                         str(RAIZ / "assets" / "fontes" / "Poppins-Bold.ttf")) if Path(p).exists()))
HZ = int(H * 0.70)             # linha do chão
_cache: dict = {}


def _f(px):
    if ("f", px) not in _cache:
        _cache[("f", px)] = ImageFont.truetype(MONO, px)
    return _cache[("f", px)]


# ---------------------------------------------------------------- fundos
def _gradiente(cx, cy, c_in, c_out, raio):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = np.sqrt(((xx - cx) / raio) ** 2 + ((yy - cy) / raio) ** 2).clip(0, 1)[..., None]
    a = np.array(c_in, np.float32) * (1 - dist) + np.array(c_out, np.float32) * dist
    return a


def _fundo(tipo: str) -> Image.Image:
    if ("fundo", tipo) in _cache:
        return _cache[("fundo", tipo)]
    if tipo == "comodo":
        a = _gradiente(W * 0.5, H * 0.42, (176, 16, 24), (58, 2, 6), H * 0.62)
        chao = _gradiente(W * 0.5, H * 0.74, (112, 8, 14), (34, 0, 4), H * 0.45)
        a[HZ:] = chao[HZ:]
        img = Image.fromarray(a.clip(0, 255).astype(np.uint8))
        d = ImageDraw.Draw(img)
        d.line((0, HZ, W, HZ), fill=(46, 2, 6), width=6)
    else:
        a = _gradiente(W * 0.5, H * 0.46, (190, 18, 26), (52, 2, 6), H * 0.6)
        img = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    _cache[("fundo", tipo)] = img
    return img


def _vinheta():
    if "vin" not in _cache:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
        _cache["vin"] = (1 - 0.55 * (r.clip(0.45, 1.25) - 0.45) / 0.8)[..., None].astype(np.float32)
    return _cache["vin"]


# ---------------------------------------------------------------- peças
def _circulo(d, cx, cy, r, cor=PRETO, aro=ARO, larg=6):
    d.ellipse((cx - r - larg, cy - r - larg, cx + r + larg, cy + r + larg), fill=aro)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=cor)


def _olhos(d, cx, cy, r, tipo, olhar, t, n):
    piscando = tipo == "abertos" and (t % 3.1) < 0.13
    for lado in (-1, 1):
        ox, oy = cx + lado * r * 0.38, cy - r * 0.06
        if tipo in ("fechados", "apertados") or piscando:
            curva = 0.06 * r if tipo == "fechados" or piscando else 0.02 * r
            d.arc((ox - r * 0.16, oy - curva - r * 0.05, ox + r * 0.16, oy + curva + r * 0.05), 15, 165,
                  fill=(210, 70, 80), width=max(4, int(r * 0.035)))
            if tipo == "apertados":                               # sobrancelhas tensas
                d.line((ox - lado * r * 0.2, oy - r * 0.2, ox + lado * r * 0.14, oy - r * 0.13), fill=(210, 70, 80),
                       width=max(4, int(r * 0.035)))
            continue
        ro = r * (0.2 if tipo == "arregalados" else 0.16)
        tremor = (random.Random(n * 3 + lado).random() - 0.5) * r * 0.02 if tipo == "arregalados" else 0
        d.ellipse((ox - ro, oy - ro, ox + ro, oy + ro), fill=BRANCO)
        rp = ro * (0.28 if tipo == "arregalados" else 0.5)
        px = ox + olhar * (ro - rp) * 0.9 + tremor
        d.ellipse((px - rp, oy - rp, px + rp, oy + rp), fill=PRETO)


def _boca(d, cx, cy, r, tipo, t):
    y = cy + r * 0.45
    cor = (150, 22, 32)
    if tipo == "aberta":
        d.ellipse((cx - r * 0.1, y - r * 0.08, cx + r * 0.1, y + r * 0.12), fill=(60, 4, 8), outline=cor, width=5)
    elif tipo == "tremendo":
        pts = [(cx - r * 0.2 + k * r * 0.05, y + math.sin(k * 1.7 + t * 18) * r * 0.02) for k in range(9)]
        d.line(pts, fill=cor, width=6)
    elif tipo != "nenhuma":
        d.line((cx - r * 0.18, y, cx + r * 0.18, y), fill=cor, width=6)


def _rosto(img, cena, t, dur, n):
    d = ImageDraw.Draw(img)
    cx, cy, r = W * 0.5, H * 0.46, W * 0.27
    respira = math.sin(t * 1.6) * 6
    d.ellipse((W * 0.06, H * 0.6 + respira, W * 0.94, H * 1.15), fill=ARO)           # ombros
    d.ellipse((W * 0.06 + 6, H * 0.6 + 6 + respira, W * 0.94 - 6, H * 1.15), fill=PRETO)
    _circulo(d, cx, cy + respira * 0.5, r)
    _olhos(d, cx, cy + respira * 0.5, r, cena.get("olhos", "abertos"), float(cena.get("olhar", 0)), t, n)
    _boca(d, cx, cy + respira * 0.5, r, cena.get("boca", "reta"), t)
    if cena.get("cobertor", True):                                                   # cobertor até o peito
        d.polygon([(0, H * 0.83), (W * 0.3, H * 0.8), (W * 0.65, H * 0.82), (W, H * 0.79), (W, H), (0, H)], fill=(24, 2, 6))
        d.line([(0, H * 0.83), (W * 0.3, H * 0.8), (W * 0.65, H * 0.82), (W, H * 0.79)], fill=ARO, width=6)


def _abismo_rosto(d, cx, cy, rx, ry, abre, t, n, fresta=False):
    """O Abismo: cabeça comprida, olhos brancos de íris vermelha, um sorriso que não cabe no rosto."""
    if not fresta:
        d.ellipse((cx - rx - 7, cy - ry - 7, cx + rx + 7, cy + ry + 7), fill=ARO)
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=PRETO)
    for lado in (-1, 1):
        ox = cx + lado * rx * 0.42 + (random.Random(n // 2 + lado).random() - 0.5) * rx * 0.03
        oy = cy - ry * 0.22 + lado * ry * 0.04
        ro = rx * 0.16
        d.ellipse((ox - ro, oy - ro * 1.1, ox + ro, oy + ro * 1.1), fill=BRANCO)
        d.ellipse((ox - ro * 0.42, oy - ro * 0.42, ox + ro * 0.42, oy + ro * 0.42), fill=(200, 20, 26))
        d.ellipse((ox - ro * 0.16, oy - ro * 0.16, ox + ro * 0.16, oy + ro * 0.16), fill=PRETO)
    if abre <= 0:
        return
    # sorriso: lua crescente branca, cheia de dentes
    largura = rx * (0.5 + 0.42 * abre)
    alto = ry * (0.1 + 0.32 * abre)
    by = cy + ry * 0.28
    caixa = (cx - largura, by - alto, cx + largura, by + alto)
    d.chord(caixa, 0, 180, fill=BRANCO)
    d.chord((cx - largura * 0.9, by - alto * 0.5, cx + largura * 0.9, by + alto * 0.62), 0, 180, fill=(70, 4, 10))
    for k in range(1, 22):
        x = cx - largura + k * (2 * largura / 22)
        d.line((x, by, x, by + alto * 0.95 * math.sin(math.pi * k / 22)), fill=(120, 30, 36), width=3)
    d.line((cx - largura, by, cx + largura, by), fill=(120, 30, 36), width=3)


def _abismo(img, cena, t, dur, n):
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    abre = min(1.0, t / max(0.8, dur * 0.55))
    d.ellipse((W * -0.05, H * 0.74, W * 1.05, H * 1.3), fill=ARO)
    d.ellipse((W * -0.05 + 7, H * 0.74 + 7, W * 1.05 - 7, H * 1.3), fill=PRETO)
    _abismo_rosto(d, W * 0.5, H * 0.46, W * 0.33, H * 0.25, abre, t, n)
    inclina = -14 * min(1.0, t / max(1.0, dur * 0.8))                 # a cabeça vai tombando de lado
    camada = camada.rotate(inclina, center=(W * 0.5, H * 0.75), resample=Image.BICUBIC)
    img.paste(camada, (0, 0), camada)
    if cena.get("maos"):
        _maos(img, t, dur)


def _maos(img, t, dur):
    d = ImageDraw.Draw(img)
    sobe = min(1.0, t / max(1.0, dur * 0.7))
    for lado in (-1, 1):
        bx = W * (0.5 + lado * 0.42)
        by = H * (1.05 - 0.22 * sobe)
        d.ellipse((bx - 70, by - 60, bx + 70, by + 90), fill=PRETO, outline=ARO, width=5)
        for k in range(4):
            ang = math.radians(-90 + lado * (-30 + k * 18))
            comp = 260 + 40 * (k in (1, 2))
            x2, y2 = bx + math.cos(ang) * comp, by + math.sin(ang) * comp
            mx, my = bx + math.cos(ang) * comp * 0.55 + lado * 10, by + math.sin(ang) * comp * 0.55
            d.line([(bx, by - 30), (mx, my), (x2, y2)], fill=ARO, width=26, joint="curve")
            d.line([(bx, by - 30), (mx, my), (x2, y2)], fill=PRETO, width=18, joint="curve")


def _porta(d, x0, y0, x1, y1, estado, luz, pes, t, n, abre_t=0.0):
    """Porta com batente; luz do corredor por baixo; entreaberta = fresta preta com os olhos dele."""
    d.rectangle((x0 - 16, y0 - 16, x1 + 16, y1), fill=(40, 2, 6))
    d.rectangle((x0, y0, x1, y1), fill=(8, 2, 4))
    larg = x1 - x0
    if estado == "fechada":
        fresta = 0
    elif estado == "entreaberta":
        fresta = larg * 0.16 * min(1.0, 0.3 + abre_t)
    else:
        fresta = larg * 0.92
    folha = (x0 + fresta, y0, x1, y1)
    if folha[2] - folha[0] > 4:
        d.rectangle(folha, fill=(70, 6, 10), outline=PRETO, width=6)
        for py in (0.12, 0.55):                                          # almofadas da porta
            d.rectangle((folha[0] + (folha[2] - folha[0]) * 0.16, y0 + (y1 - y0) * py,
                         folha[2] - (folha[2] - folha[0]) * 0.16, y0 + (y1 - y0) * (py + 0.33)), outline=(46, 2, 6), width=5)
        kx, ky = folha[0] + (folha[2] - folha[0]) * 0.12, y0 + (y1 - y0) * 0.52
        d.ellipse((kx - 12, ky - 12, kx + 12, ky + 12), fill=(150, 110, 90))
    if estado == "entreaberta" and fresta > 10:                          # os olhos dele na fresta
        cx = x0 + fresta / 2
        oy = y0 + (y1 - y0) * 0.3
        for lado in (-1, 1):
            ox = cx + lado * fresta * 0.22
            ro = max(6, fresta * 0.13)
            d.ellipse((ox - ro, oy - ro * 1.1, ox + ro, oy + ro * 1.1), fill=BRANCO)
            d.ellipse((ox - ro * 0.4, oy - ro * 0.4, ox + ro * 0.4, oy + ro * 0.4), fill=(200, 20, 26))
        if abre_t > 0.5:                                                 # e o começo do sorriso
            sy = oy + (y1 - y0) * 0.09
            d.chord((cx - fresta * 0.42, sy - 18, cx + fresta * 0.42, sy + 26), 0, 180, fill=BRANCO)
    if luz and estado == "fechada":                                      # luz do corredor por baixo da porta
        brilho = Image.new("RGBA", (int(x1 - x0) + 120, 90), (0, 0, 0, 0))
        ImageDraw.Draw(brilho).rectangle((60, 40, brilho.width - 60, 52), fill=(255, 190, 150, 230))
        brilho = brilho.filter(ImageFilter.GaussianBlur(10))
        d._image.paste(brilho, (int(x0 - 60), int(y1 - 46)), brilho)
        d.line((x0, y1 - 2, x1, y1 - 2), fill=(255, 214, 180), width=5)
        if pes:                                                          # alguém parado do outro lado
            for k in (0.36, 0.6):
                px = x0 + (x1 - x0) * k
                d.rectangle((px - 34, y1 - 8, px + 34, y1 + 2), fill=PRETO)


def _ondas(img, ox, oy, direcao, t):
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    for k in range(3):
        fase = (t * 0.9 + k / 3) % 1.0
        r = 40 + fase * 230
        alfa = int(220 * (1 - fase))
        a0, a1 = (150, 210) if direcao < 0 else (-30, 30)
        d.arc((ox - r, oy - r, ox + r, oy + r), a0, a1, fill=(255, 220, 220, alfa), width=8)
    img.paste(camada, (0, 0), camada)


def _cama(d, olhos, t, n):
    x0, x1, topo = W * 0.04, W * 0.6, H * 0.6
    d.rectangle((x0, H * 0.5, x0 + 26, HZ), fill=PRETO, outline=ARO, width=4)                    # cabeceira
    d.rectangle((x0, topo + 40, x1, HZ - 30), fill=PRETO, outline=ARO, width=5)
    d.rectangle((x1 - 22, topo + 40, x1, HZ), fill=PRETO)
    resp = math.sin(t * 1.6) * 5
    d.chord((x0 + 120, topo - 40 + resp, x1 + 20, topo + 110), 180, 360, fill=PRETO, outline=ARO, width=5)  # corpo coberto
    d.rounded_rectangle((x0 + 30, topo + 8, x0 + 170, topo + 50), radius=18, fill=(40, 4, 8))          # travesseiro
    cx, cy, r = x0 + 100, topo - 6 + resp * 0.3, 58
    _circulo(d, cx, cy, r, larg=5)
    if olhos == "abertos":
        for lado in (-1, 1):
            ox = cx + 8 + lado * r * 0.36
            d.ellipse((ox - 11, cy - 15, ox + 11, cy + 7), fill=BRANCO)
            d.ellipse((ox + 1, cy - 8, ox + 9, cy), fill=PRETO)
    else:
        for lado in (-1, 1):
            ox = cx + 8 + lado * r * 0.36
            d.arc((ox - 12, cy - 10, ox + 12, cy + 2), 15, 165, fill=(210, 70, 80), width=4)


def _quarto(img, cena, t, dur, n):
    d = ImageDraw.Draw(img)
    # janela com a lua na parede do fundo
    d.rectangle((W * 0.2, H * 0.24, W * 0.46, H * 0.4), fill=(30, 2, 6), outline=PRETO, width=10)
    d.line((W * 0.33, H * 0.24, W * 0.33, H * 0.4), fill=PRETO, width=8)
    d.line((W * 0.2, H * 0.32, W * 0.46, H * 0.32), fill=PRETO, width=8)
    d.ellipse((W * 0.36, H * 0.26, W * 0.42, H * 0.29), fill=(230, 190, 190))
    _porta(d, W * 0.68, H * 0.33, W * 0.92, HZ, cena.get("porta", "fechada"), cena.get("luz", True), cena.get("pes"),
           t, n, t / max(1.0, dur))
    _cama(d, cena.get("olhos", "fechados"), t, n)
    if cena.get("ondas"):
        _ondas(img, W * 0.68, H * 0.52, -1, t)


def _porta_close(img, cena, t, dur, n):
    d = ImageDraw.Draw(img)
    dx = 0
    for tb in cena.get("_batidas_t", []):
        if 0 <= t - tb < 0.09:
            dx = 9 if int((t - tb) * 100) % 2 else -9
    _porta(d, W * 0.2 + dx, H * 0.24, W * 0.8 + dx, HZ + int(H * 0.08), cena.get("porta", "fechada"),
           cena.get("luz", True), cena.get("pes"), t, n, t / max(1.0, dur))
    for tb in cena.get("_batidas_t", []):                                    # ondinha de cada batida
        k = t - tb
        if 0 <= k < 0.5:
            r = 30 + k * 260
            camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(camada).ellipse((W * 0.5 - r, H * 0.42 - r, W * 0.5 + r, H * 0.42 + r),
                                           outline=(255, 220, 220, int(200 * (1 - k / 0.5))), width=6)
            img.paste(camada, (0, 0), camada)
    if cena.get("ondas"):
        _ondas(img, W * 0.5, H * 0.45, 1, t)


def _relogio(img, cena, t, dur, n):
    d = ImageDraw.Draw(img)
    cx, cy = W * 0.5, H * 0.48
    lw, lh = W * 0.38, W * 0.15
    d.rounded_rectangle((cx - lw - 10, cy - lh - 10, cx + lw + 10, cy + lh + 10), radius=40, fill=ARO)
    d.rounded_rectangle((cx - lw, cy - lh, cx + lw, cy + lh), radius=34, fill=PRETO)
    d.rectangle((cx - lw * 0.9, cy + lh, cx - lw * 0.7, cy + lh + 30), fill=PRETO)
    d.rectangle((cx + lw * 0.7, cy + lh, cx + lw * 0.9, cy + lh + 30), fill=PRETO)
    d.rounded_rectangle((cx - lw * 0.86, cy - lh * 0.72, cx + lw * 0.86, cy + lh * 0.72), radius=12, fill=(40, 2, 4))
    hora = str(cena.get("hora", "03:17"))
    if (t % 1.0) > 0.5:
        hora = hora.replace(":", " ")
    f = _f(190)
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dc = ImageDraw.Draw(camada)
    tx, ty = cx - f.getlength(hora) / 2, cy - 118
    dc.text((tx, ty), hora, font=f, fill=VERM_VIVO + (255,))
    brilho = camada.filter(ImageFilter.GaussianBlur(18))
    img.paste(brilho, (0, 0), brilho)
    img.paste(camada, (0, 0), camada)


def _destaque(img, cena, t, dur, n):
    d = ImageDraw.Draw(img)
    txt = str(cena.get("destaque", "")).upper()
    px = 140
    while px > 50 and _f(px).getlength(txt) > W * 0.84:
        px -= 6
    entra = min(1.0, t / 0.2)
    tremor = (random.Random(n).random() - 0.5) * 6
    x, y = (W - _f(px).getlength(txt)) / 2 + tremor, H * 0.47 - px / 2
    d.text((x + 6, y + 8), txt, font=_f(px), fill=(30, 0, 2))
    d.text((x, y), txt, font=_f(px), fill=tuple(int(c * entra) for c in TEXTO))


def _portas(img, cena, t, dur, n):
    """Três portas lado a lado, numeradas. "pes": n = sombra de pés debaixo da porta n; "entreaberta": n = a fresta com os olhos."""
    d = ImageDraw.Draw(img)
    larg = W * 0.24
    for k in range(3):
        x0 = W * 0.06 + k * (larg + W * 0.08)
        num = k + 1
        estado = "entreaberta" if cena.get("entreaberta") == num else "fechada"
        _porta(d, x0, H * 0.36, x0 + larg, HZ, estado, True, cena.get("pes") == num, t, n, t / max(1.0, dur))
        f = _f(96)
        d.text((x0 + larg / 2 - f.getlength(str(num)) / 2 + 4, H * 0.25 + 5), str(num), font=f, fill=(30, 0, 2))
        d.text((x0 + larg / 2 - f.getlength(str(num)) / 2, H * 0.25), str(num), font=f, fill=TEXTO)


QUADROS = {"portas": _portas, "rosto": _rosto, "abismo": _abismo, "quarto": _quarto, "porta": _porta_close, "relogio": _relogio,
           "destaque": _destaque}


def _aviso(img, txt, t):
    d = ImageDraw.Draw(img)
    linhas = str(txt).upper().split("|")
    f = _f(66)
    a = min(1.0, t / 0.3)
    y = H * 0.1
    for ln in linhas:
        x = (W - f.getlength(ln)) / 2
        d.text((x + 4, y + 5), ln, font=f, fill=(30, 0, 2))
        d.text((x, y), ln, font=f, fill=tuple(int(c * a) for c in TEXTO))
        y += 84


def _contador(img, cena, t):
    tempos = cena.get("_batidas_t", [])
    if not tempos or cena.get("contador") is False:      # contador escondido: o público conta sozinho
        return
    d = ImageDraw.Draw(img)
    n = len(tempos)
    r, gap = 38, 104
    y = H * 0.19 if cena.get("texto") else H * 0.12
    x0 = W / 2 - gap * (n - 1) / 2
    for k, tb in enumerate(tempos):
        cx = x0 + k * gap
        if t < tb:
            d.ellipse((cx - r, y - r, cx + r, y + r), outline=(130, 40, 46), width=4)
            continue
        if cena.get("x") and k == n - 1:
            d.ellipse((cx - r, y - r, cx + r, y + r), fill=(60, 0, 4), outline=VERM_VIVO, width=5)
            d.line((cx - 24, y - 24, cx + 24, y + 24), fill=VERM_VIVO, width=10)
            d.line((cx - 24, y + 24, cx + 24, y - 24), fill=VERM_VIVO, width=10)
            continue
        d.ellipse((cx - r, y - r, cx + r, y + r), fill=TEXTO)
        num = str(k + 1)
        d.text((cx - _f(44).getlength(num) / 2, y - 28), num, font=_f(44), fill=(40, 4, 8))


def quadro(cena: dict, t: float, dur: float, n: int) -> Image.Image:
    tipo = cena.get("quadro", "quarto")
    if tipo == "preto":
        return Image.new("RGB", (W, H), (0, 0, 0))
    img = _fundo("comodo" if tipo in ("quarto", "porta", "portas") else "halo").copy()
    QUADROS.get(tipo, _quarto)(img, cena, t, dur, n)
    if cena.get("texto"):
        _aviso(img, cena["texto"], t)
    _contador(img, cena, t)
    # câmera: aproxima devagar; tremor no susto e nas batidas
    z = 1.02 + 0.05 * min(1.0, t / max(1.0, dur))     # sempre um pouco aproximado: sobra margem para o tremor
    sx = sy = 0.0
    batendo = any(0 <= t - tb < 0.12 for tb in cena.get("_batidas_t", []))
    if cena.get("susto") or batendo:
        rnd = random.Random(n)
        forca = 14 if batendo else 9
        sx, sy = (rnd.random() - 0.5) * forca, (rnd.random() - 0.5) * forca
    if z > 1.001 or sx or sy:
        cw, ch = W / z, H / z
        x0 = min(max(0.0, (W - cw) / 2 + sx), W - cw)
        y0 = min(max(0.0, (H - ch) / 2 + sy), H - ch)
        img = img.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
    a = np.asarray(img).astype(np.float32) * _vinheta()
    rnd = np.random.default_rng(n)
    a += rnd.normal(0, 7, (H // 4, W // 4, 1)).repeat(4, 0).repeat(4, 1)          # grão
    if random.Random(n // 4).random() < 0.04:                                     # a luz falha de vez em quando
        a *= 0.82
    borda = min(t, dur - t)
    if borda < 0.14:
        a *= max(0.0, borda) / 0.14
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


# ---------------------------------------------------------------- som das batidas e render
def _som_batidas(tempos, dur, destino: Path):
    sr = 44100
    out = np.zeros(int(sr * (dur + 0.5)), np.float32)
    rnd = np.random.default_rng(7)
    k = np.arange(int(sr * 0.32)) / sr
    for i, tb in enumerate(tempos):
        tom = 78 + 6 * (i % 2)
        golpe = (np.sin(2 * np.pi * tom * k) * np.exp(-k * 16) * 0.9
                 + rnd.normal(0, 1, k.size) * np.exp(-k * 60) * 0.35
                 + np.sin(2 * np.pi * 190 * k) * np.exp(-k * 30) * 0.3)
        a = int(tb * sr)
        out[a:a + k.size] += golpe[:max(0, out.size - a)]
    pcm = (out.clip(-1, 1) * 32000).astype(np.int16)
    with wave.open(str(destino), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def renderizar_cena_sombra(cena: dict, voz: dict, destino: Path, pausa: float, indice: int) -> float:
    dur = voz["duracao"] + pausa
    nb = int(cena.get("batidas") or 0)
    tempos = []
    if nb:
        intervalo = 0.62 if cena.get("x") else 0.5
        if cena.get("batidas_apos_voz"):
            inicio = voz["duracao"] + 0.35
            dur = inicio + intervalo * nb + max(pausa, 0.9)
        else:
            inicio = 0.3
            intervalo = min(intervalo, max(0.3, (voz["duracao"] - 0.4) / nb))
        tempos = [inicio + k * intervalo for k in range(nb)]
    cena["_batidas_t"] = tempos
    frames = math.ceil(dur * FPS)
    entradas = ["-i", str(voz["arquivo"])]
    filtro = "[1:a]aresample=44100,apad[a]"
    if tempos:
        wav = destino.with_suffix(".batidas.wav")
        _som_batidas(tempos, dur, wav)
        entradas += ["-i", str(wav)]
        filtro = "[1:a]aresample=44100,apad[v];[2:a]aresample=44100,volume=1.6[b];[v][b]amix=inputs=2:normalize=0:duration=first[a]"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", *entradas, "-filter_complex", filtro,
                           "-map", "0:v", "-map", "[a]", "-t", f"{dur:.3f}",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "160k", "-ac", "2", str(destino)], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for k in range(frames):
            ff.stdin.write(quadro(cena, k / FPS, dur, indice * 10000 + k).tobytes())
    finally:
        ff.stdin.close()
        erro = ff.stderr.read().decode(errors="ignore")
        ff.wait()
    if ff.returncode != 0:
        raise RuntimeError(erro[-800:])
    return dur
