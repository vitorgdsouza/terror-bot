"""Formato "voce": terror minimalista em segunda pessoa, no ritmo dos vídeos que estão indo bem no TikTok.

Visual de 2 ou 3 cores (fundo + figuras chapadas + um destaque), uma imagem nova a cada frase, tudo se mexendo,
interface de celular e relógio na tela, e regras ("REGRA 1") falando com VOCÊ. Não precisa de ilustração:
tudo é desenhado em código. A legenda é grande, com 1 a 3 palavras, e a palavra forte em cor (montagem.py).

Roteiro: "formato": "voce", "paleta": noite | sangue | papel, "hora": "03:14" (relógio do canto, que anda com o vídeo),
         "parte": "PARTE 1" (selo no alto, opcional)
Cena: {"narracao": "...", "quadro": "<tipo>", ...}
  ligacao      celular tocando; "nome" (quem liga, ex.: "VOCÊ", "MÃE"), "estado": tocando | atendida | recusada
  chat         conversa aparecendo; "msgs": [["ele", "abre a porta"], ["voce", "quem é?"]], "nome" no topo
  relogio      relógio grande; "hora": "03:16", "vira": "03:17" (vira no meio da cena, em vermelho)
  andares      prédio em corte; "andares": 12, "voce": 11, "de": 1, "ate": 11 (algo subindo andar por andar)
  mapa         ruas vistas de cima; um ponto vem até VOCÊ; "eta": "12:00" (contagem regressiva), "rotulo": "VIATURA"
  regra        cartão "REGRA n"; "n": 1, "texto": "não abra" (escrita de máquina)
  porta        porta de frente com olho mágico; "luz": true (luz por baixo), "pes": true (sombra de pés),
               "batendo": true (a porta treme), "aberta": true (fresta preta)
  olho_magico  a visão pelo olho mágico; "figura": pessoa | oco | ninguem, "vapor": true (sai vapor da boca),
               "embaca": true (o vidro embaça), "geada": true (geada no cabelo; "derrete": true ela some)
  silhueta     você no cômodo; "acao": parado | andando | tremendo | escondido, "outra": true (outra figura no canto)
  texto        palavras grandes no meio, escrita de máquina; "texto": "NÃO ATENDA" ("|" quebra a linha)
  preto        tela preta
Ciência (paleta "ciencia", canal E Se Fosse Real?):
  planeta      a Terra girando no espaço; "lua": false, "some_lua": true, "para": true (rotação freia), "vento": true, "rotulo"
  terra_corte  a Terra em corte com o buraco; "de"/"ate" (0 a 1: posição de quem cai), "rotulo" (ex.: "5.400 °C")
  espaco       astronauta flutuando; "sem_capacete": true, "segundos": 15 (contagem regressiva)
  numero       número grande contando; "de", "ate", "unidade" (km/h), "rotulo"
  comparar     barras crescendo; "itens": [["Furacão", 300], ["Sem rotação", 1670]], "unidade": "km/h"
  multidao     muita gente pulando; "rotulo"
Em qualquer cena: "foco": [x, y, zoom] (close fixo), "seguir": true (close acompanhando quem cai, no terra_corte), "alerta": true (borda vermelha piscando), "susto": true (tremor), "texto_topo": "aviso no alto".
"""
import math
import random
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .util import RAIZ

W, H, FPS = 1080, 1920, 24
PALETAS = {
    "noite": {"fundo": (13, 19, 44), "fundo2": (24, 33, 70), "fig": (238, 240, 248), "acento": (232, 44, 56),
              "acento2": (255, 199, 64), "apagado": (70, 84, 128)},
    "sangue": {"fundo": (128, 8, 18), "fundo2": (60, 2, 8), "fig": (12, 5, 8), "acento": (250, 245, 240),
               "acento2": (255, 210, 90), "apagado": (90, 10, 18)},
    "ciencia": {"fundo": (8, 18, 46), "fundo2": (22, 50, 104), "fig": (245, 247, 252), "acento": (255, 196, 36),
                "acento2": (86, 214, 255), "apagado": (66, 96, 150)},
    "papel": {"fundo": (8, 8, 10), "fundo2": (26, 26, 30), "fig": (236, 236, 236), "acento": (230, 40, 46),
              "acento2": (255, 199, 64), "apagado": (70, 70, 78)},
}
FONTE = str(RAIZ / "assets" / "fontes" / "Poppins-Bold.ttf")
MONO = next((p for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
                         "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf", FONTE) if Path(p).exists()))
_cache: dict = {}


def _f(px, mono=False):
    k = (px, mono)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(MONO if mono else FONTE, px)
    return _cache[k]


def _suave(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def _fundo(p) -> Image.Image:
    k = ("fundo", p["fundo"])
    if k not in _cache:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - H * 0.45) / (H * 0.55)) ** 2).clip(0, 1)[..., None]
        a = np.array(p["fundo2"], np.float32) * (1 - d) + np.array(p["fundo"], np.float32) * d
        _cache[k] = Image.fromarray(a.astype(np.uint8))
    return _cache[k]


def _centro_texto(d, cx, cy, txt, fonte, cor):
    b = d.textbbox((0, 0), txt, font=fonte)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], cy - (b[3] - b[1]) / 2 - b[1]), txt, font=fonte, fill=cor)


# ---------------------------------------------------------------- figuras
def _pessoa(d, cx, chao, alt, cor, t=0.0, acao="parado", oco=False, fundo=(0, 0, 0), olhos=True):
    """Pictograma de pessoa: cabeça redonda e corpo arredondado. O Oco é mais alto e de olhos vazios."""
    if oco:
        alt *= 1.12
    balanco = math.sin(t * 7) * alt * 0.012 if acao == "andando" else 0
    treme = math.sin(t * 47) * alt * 0.006 if acao == "tremendo" else 0
    x = cx + treme
    r = alt * 0.13
    topo = chao - alt
    corpo = (x - alt * 0.17, topo + r * 2.25 + balanco, x + alt * 0.17, chao - alt * 0.36)
    d.rounded_rectangle(corpo, radius=int(alt * 0.12), fill=cor)
    perna = alt * 0.07
    passo = math.sin(t * 7) * alt * 0.05 if acao == "andando" else 0
    d.rounded_rectangle((x - alt * 0.14 + passo, chao - alt * 0.42, x - alt * 0.14 + perna * 2 + passo, chao), radius=int(perna), fill=cor)
    d.rounded_rectangle((x + alt * 0.14 - perna * 2 - passo, chao - alt * 0.42, x + alt * 0.14 - passo, chao), radius=int(perna), fill=cor)
    inclina = math.sin(t * 1.3) * r * 0.25 if oco else 0
    hx, hy = x + inclina, topo + r + balanco
    d.ellipse((hx - r, hy - r, hx + r, hy + r), fill=cor)
    if olhos:
        o = r * 0.16
        for s in (-1, 1):
            ex = hx + s * r * 0.36
            d.ellipse((ex - o, hy - o, ex + o, hy + o), fill=fundo)
            if not oco:                                  # gente tem pupila; o Oco não
                d.ellipse((ex - o * 0.45, hy - o * 0.2, ex + o * 0.45, hy + o * 0.7), fill=cor)
    return hx, hy, r


def _celular(d, cx, cy, w, h, p):
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=int(w * 0.13), fill=p["fundo"],
                        outline=p["fig"], width=8)
    d.rounded_rectangle((cx - w * 0.12, cy - h / 2 + 22, cx + w * 0.12, cy - h / 2 + 40), radius=9, fill=p["apagado"])


# ---------------------------------------------------------------- quadros
def _ligacao(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    cx, cy, w, h = W / 2, H * 0.47, 560, 1040
    estado = cena.get("estado", "tocando")
    sx = math.sin(t * 60) * 6 if estado == "tocando" and (t % 1.2) < 0.6 else 0
    cx += sx
    if estado == "tocando":                              # ondas saindo do celular
        for k in range(3):
            fase = ((t * 0.9 + k / 3) % 1)
            rr = 300 + fase * 380
            cor = tuple(int(c * (1 - fase) + f * fase) for c, f in zip(p["acento"], p["fundo"]))
            d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=cor, width=6)
    _celular(d, cx, cy, w, h, p)
    av = 120
    ay = cy - 230
    d.ellipse((cx - av, ay - av, cx + av, ay + av), fill=p["apagado"])
    _pessoa(d, cx, ay + av * 0.95, av * 1.55, p["fig"], olhos=False)
    _centro_texto(d, cx, cy - 40, cena.get("nome", "DESCONHECIDO"), _f(64), p["fig"])
    if estado == "atendida":
        seg = int(t)
        _centro_texto(d, cx, cy + 40, f"00:{seg:02d}", _f(40, True), p["acento2"])
        for k in range(14):                              # ondas de voz
            a = abs(math.sin(t * 9 + k * 0.8)) * 60 + 8
            x = cx - 210 + k * 32
            d.rounded_rectangle((x, cy + 150 - a, x + 16, cy + 150 + a), radius=8, fill=p["fig"])
    else:
        _centro_texto(d, cx, cy + 40, "chamando..." if estado == "tocando" else "recusada", _f(38, True), p["apagado"])
    by = cy + h / 2 - 150
    for bx, cor in ((cx - 140, p["acento"]), (cx + 140, (60, 190, 90))):
        if estado == "recusada" and bx > cx:
            continue
        pulsa = 1 + 0.08 * math.sin(t * 8) if estado == "tocando" else 1
        rb = 62 * pulsa
        d.ellipse((bx - rb, by - rb, bx + rb, by + rb), fill=cor)
    if estado == "recusada":
        d.line((cx - 220, cy - 360, cx + 220, cy + 360), fill=p["acento"], width=18)


def _chat(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    cx, cy, w, h = W / 2, H * 0.43, 880, 1180
    _celular(d, cx, cy, w, h, p)
    _centro_texto(d, cx, cy - h / 2 + 95, cena.get("nome", "DESCONHECIDO"), _f(50), p["fig"])
    d.line((cx - w / 2 + 30, cy - h / 2 + 140, cx + w / 2 - 30, cy - h / 2 + 140), fill=p["apagado"], width=3)
    msgs = cena.get("msgs") or []
    passo = max(0.5, dur * 0.75 / max(1, len(msgs)))
    y = cy - h / 2 + 180
    fonte = _f(56)
    for i, (lado, txt) in enumerate(msgs):
        if t < 0.2 + i * passo:
            if t > 0.2 + i * passo - 0.5:                 # "digitando..."
                pts = "•" * (1 + int(t * 4) % 3)
                x0 = cx - w / 2 + 50 if lado != "voce" else cx + w / 2 - 170
                d.rounded_rectangle((x0, y, x0 + 140, y + 84), radius=36, fill=p["apagado"])
                d.text((x0 + 26, y + 6), pts, font=fonte, fill=p["fig"])
            break
        linhas, atual = [], ""
        for pal in str(txt).split():
            teste = (atual + " " + pal).strip()
            if d.textlength(teste, font=fonte) > w * 0.68:
                linhas.append(atual)
                atual = pal
            else:
                atual = teste
        linhas.append(atual)
        bw = max(d.textlength(lin, font=fonte) for lin in linhas) + 60
        bh = 76 * len(linhas) + 34
        meu = lado == "voce"
        x0 = cx + w / 2 - 50 - bw if meu else cx - w / 2 + 50
        cor = p["acento"] if lado in ("ele", "oco") else (p["apagado"] if not meu else p["fig"])
        d.rounded_rectangle((x0, y, x0 + bw, y + bh), radius=32, fill=cor)
        for k, lin in enumerate(linhas):
            d.text((x0 + 30, y + 12 + 76 * k), lin, font=fonte, fill=p["fundo"] if meu else p["fig"])
        y += bh + 30


def _relogio(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    hora, vira = cena.get("hora", "03:16"), cena.get("vira")
    virou = bool(vira) and t > dur * 0.5
    txt = vira if virou else hora
    if not virou and (t % 1) < 0.5:
        txt = txt.replace(":", " ")
    cor = p["acento"] if virou else p["fig"]
    escala = 1.0 + (0.12 * max(0, 1 - (t - dur * 0.5) * 4) if virou else 0)
    _centro_texto(d, W / 2, H * 0.43, txt, _f(int(250 * escala), True), cor)


def _andares(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    total, voce = int(cena.get("andares", 12)), int(cena.get("voce", 11))
    de, ate = int(cena.get("de", 1)), int(cena.get("ate", voce))
    x0, x1, base, alt = W * 0.3, W * 0.62, H * 0.82, H * 0.62
    h1 = alt / total
    for k in range(total):
        y = base - (k + 1) * h1
        d.rectangle((x0, y, x1, y + h1 - 6), outline=p["apagado"], width=3)
        d.text((x0 - 70, y + h1 * 0.25), f"{k + 1}º", font=_f(30, True), fill=p["apagado"])
        if k + 1 == voce:
            d.rounded_rectangle((x1 - 150, y + 12, x1 - 20, y + h1 - 18), radius=10, fill=p["acento2"])
            d.text((x1 - 140, y + 14), "VOCÊ", font=_f(30), fill=p["fundo"])
    prog = _suave(t / max(0.1, dur * 0.85))
    atual = de + (ate - de) * prog
    y = base - atual * h1 + h1 * 0.15
    d.rounded_rectangle((x0 + 30, y, x0 + 110, y + h1 * 0.7), radius=8, fill=p["acento"])
    _centro_texto(d, W * 0.82, H * 0.22, f"{int(round(atual)):02d}", _f(150, True), p["acento"])
    d.polygon([(W * 0.82 - 30, H * 0.13), (W * 0.82 + 30, H * 0.13), (W * 0.82, H * 0.13 - 40)], fill=p["acento"])


def _mapa(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    for k in range(-2, 9):                               # ruas
        y = H * 0.2 + k * 190
        d.line((0, y, W, y), fill=p["fundo2"], width=40)
        x = k * 190 + 60
        d.line((x, H * 0.12, x, H * 0.85), fill=p["fundo2"], width=40)
    destino = (W * 0.7, H * 0.32)
    origem = (W * 0.18, H * 0.78)
    pts = [origem, (origem[0], H * 0.5), (destino[0], H * 0.5), destino]
    d.line(pts, fill=p["apagado"], width=10)
    prog = _suave(t / max(0.1, dur * 0.95))
    segs = [math.dist(pts[i], pts[i + 1]) for i in range(3)]
    alvo = prog * sum(segs)
    pos = pts[0]
    for i, s in enumerate(segs):
        if alvo <= s:
            f = alvo / s
            pos = (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)
            break
        alvo -= s
        pos = pts[i + 1]
    r = 26 + 6 * math.sin(t * 6)
    d.ellipse((pos[0] - r, pos[1] - r, pos[0] + r, pos[1] + r), fill=p["acento"])
    d.ellipse((destino[0] - 30, destino[1] - 30, destino[0] + 30, destino[1] + 30), fill=p["acento2"])
    d.text((destino[0] - 60, destino[1] - 95), "VOCÊ", font=_f(44), fill=p["acento2"])
    if cena.get("eta"):
        mm, ss = (int(x) for x in str(cena["eta"]).split(":"))
        resto = max(0, mm * 60 + ss - int(t * 7))
        caixa = (W / 2 - 230, H * 0.86, W / 2 + 230, H * 0.86 + 150)
        d.rounded_rectangle(caixa, radius=24, fill=p["fundo"], outline=p["acento"], width=5)
        _centro_texto(d, W / 2, H * 0.86 + 45, cena.get("rotulo", "CHEGANDO EM"), _f(32), p["fig"])
        _centro_texto(d, W / 2, H * 0.86 + 105, f"{resto // 60:02d}:{resto % 60:02d}", _f(56, True), p["acento"])


def _regra(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    entra = _suave(t / 0.35)
    y = H * 0.36 - (1 - entra) * 120
    caixa = (W / 2 - 300, y, W / 2 + 300, y + 190)
    d.rounded_rectangle(caixa, radius=20, fill=p["fig"])
    _centro_texto(d, W / 2, y + 95, f"REGRA {cena.get('n', 1)}", _f(96), p["fundo"])
    texto = str(cena.get("texto", "")).upper()
    mostra = texto[:int(len(texto) * min(1.0, max(0.0, (t - 0.3) / max(0.3, dur * 0.5))))]
    for k, lin in enumerate(mostra.split("|")):
        _centro_texto(d, W / 2, y + 300 + k * 80, lin.strip(), _f(60, True), p["acento2"])


def _porta(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    sx = 0
    if cena.get("batendo"):
        fase = t % 1.1
        if fase < 0.45 and int(fase / 0.15) % 2 == 0:
            sx = 7
    x0, y0, x1, y1 = W * 0.29 + sx, H * 0.16, W * 0.71 + sx, H * 0.7
    d.rectangle((x0 - 26, y0 - 26, x1 + 26, y1), fill=p["apagado"])
    if cena.get("aberta"):
        d.rectangle((x0, y0, x1, y1), fill=(0, 0, 0))
        d.rectangle((x0 + (x1 - x0) * 0.3, y0, x1, y1), fill=p["fig"])
    else:
        d.rectangle((x0, y0, x1, y1), fill=p["fig"])
        for yy in (0.18, 0.55):
            d.rectangle((x0 + 50, y0 + (y1 - y0) * yy, x1 - 50, y0 + (y1 - y0) * (yy + 0.3)), outline=p["fundo2"], width=5)
        d.ellipse((W / 2 - 22 + sx, y0 + 150, W / 2 + 22 + sx, y0 + 194), fill=p["fundo"])     # olho mágico
        d.ellipse((x1 - 90, H * 0.5, x1 - 50, H * 0.5 + 40), fill=p["acento2"])                # maçaneta
    d.rectangle((0, y1, W, H), fill=p["fundo"])
    if cena.get("luz"):
        brilho = 0.75 + 0.25 * math.sin(t * 3)
        cor = tuple(int(c * brilho) for c in p["acento2"])
        d.rectangle((x0, y1, x1, y1 + 14), fill=cor)
        if cena.get("pes"):
            for px in (W / 2 - 80, W / 2 + 20):
                d.rectangle((px, y1, px + 60, y1 + 14), fill=(0, 0, 0))


def _olho_magico(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    cx, cy, r = W / 2, H * 0.44, 470
    d.rectangle((0, 0, W, H), fill=(0, 0, 0))
    lente = Image.new("RGB", (W, H), p["fundo2"])
    dl = ImageDraw.Draw(lente)
    for k in range(40):                                   # neve caindo
        rnd = random.Random(k)
        x = rnd.random() * W
        y = (rnd.random() * H + t * (80 + rnd.random() * 80)) % H
        dl.ellipse((x - 4, y - 4, x + 4, y + 4), fill=p["apagado"])
    fig = cena.get("figura", "pessoa")
    if fig != "ninguem":
        oco = fig == "oco"
        hx, hy, rr = _pessoa(dl, cx, cy + r * 1.25, r * 1.55, p["fig"] if not oco else (190, 200, 220), t, "parado", oco, p["fundo2"])
        if cena.get("vapor") and not oco:                 # gente solta vapor no frio
            fase = (t * 0.8) % 1
            vx = hx + rr * 0.2 + fase * 110
            dl.ellipse((vx - 30 - fase * 40, hy + rr * 0.55 - fase * 60, vx + 30 + fase * 40, hy + rr * 0.55 - fase * 60 + 60 + fase * 40),
                       outline=(220, 228, 240), width=4)
        if cena.get("geada"):
            derrete = cena.get("derrete") and not oco
            a = 1 - _suave((t - dur * 0.3) / max(0.3, dur * 0.5)) if derrete else 1
            if a > 0.05:
                for k in range(16):
                    ang = math.pi + k * math.pi / 15
                    gx, gy = hx + math.cos(ang) * rr * 1.02, hy + math.sin(ang) * rr * 1.02
                    tam = 10 * a
                    dl.line((gx - tam, gy, gx + tam, gy), fill=(255, 255, 255), width=3)
                    dl.line((gx, gy - tam, gx, gy + tam), fill=(255, 255, 255), width=3)
            elif derrete:
                for k in range(5):
                    gx = hx - rr * 0.8 + k * rr * 0.4
                    gy = hy - rr * 0.6 + ((t * 120 + k * 40) % 140)
                    dl.ellipse((gx - 7, gy - 10, gx + 7, gy + 10), fill=(170, 200, 255))
    mascara = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mascara).ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    if cena.get("embaca"):
        a = _suave((t - 0.3) / max(0.3, dur * 0.6))
        lente = Image.blend(lente, Image.new("RGB", (W, H), (200, 205, 215)), 0.55 * a)
    img.paste(lente, (0, 0), mascara)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=p["apagado"], width=26)


def _silhueta(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    chao = H * 0.74
    d.line((0, chao, W, chao), fill=p["apagado"], width=6)
    acao = cena.get("acao", "parado")
    x = W * 0.45
    if acao == "andando":
        x = W * 0.2 + W * 0.5 * _suave(t / max(0.1, dur))
    if acao == "escondido":
        d.rectangle((W * 0.18, chao - 520, W * 0.5, chao), fill=p["apagado"])
        x = W * 0.42
    _pessoa(d, x, chao, 560, p["fig"], t, acao, False, p["fundo"])
    if cena.get("outra"):
        a = _suave(t / max(0.1, dur * 0.6))
        cor = tuple(int(f + (c - f) * a) for c, f in zip(p["fig"], p["fundo"]))
        _pessoa(d, W * 0.84, chao, 560, cor, t, "parado", True, p["fundo"])


def _texto(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    texto = str(cena.get("texto", "")).upper()
    mostra = texto[:int(len(texto) * min(1.0, t / max(0.3, dur * 0.45)))]
    linhas = mostra.split("|")
    tam = 104                                           # diminui a letra até a linha mais longa caber na tela
    while tam > 56 and max(d.textlength(lin.strip(), font=_f(tam)) for lin in texto.split("|")) > W * 0.88:
        tam -= 6
    for k, lin in enumerate(linhas):
        _centro_texto(d, W / 2, H * 0.42 + (k - (len(texto.split("|")) - 1) / 2) * tam * 1.25, lin.strip(), _f(tam),
                      p["acento"] if k == len(linhas) - 1 else p["fig"])


QUADROS = {"ligacao": _ligacao, "chat": _chat, "relogio": _relogio, "andares": _andares, "mapa": _mapa,
           "regra": _regra, "porta": _porta, "olho_magico": _olho_magico, "silhueta": _silhueta, "texto": _texto}


# ---------------------------------------------------------------- quadros de ciência (canal E Se Fosse Real?)
OCEANO, TERRA_COR = (38, 112, 206), (72, 170, 96)


def _globo(d, cx, cy, r, t, gira=1.0):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=OCEANO)
    for k in range(5):                                  # continentes simples andando com a rotação
        rnd = random.Random(k * 7)
        lat = (rnd.random() - 0.5) * 1.4
        lon = (rnd.random() * 2 * math.pi + t * 0.6 * gira) % (2 * math.pi)
        if math.cos(lon) < 0:
            continue
        x = cx + r * math.sin(lon) * math.cos(lat)
        y = cy - r * math.sin(lat)
        tam = r * (0.18 + rnd.random() * 0.14) * (0.4 + 0.6 * math.cos(lon))
        d.ellipse((x - tam, y - tam * 0.7, x + tam, y + tam * 0.7), fill=TERRA_COR)
    for k in range(1, 4):                               # paralelos
        yy = cy - r + k * r / 2
        meia = math.sqrt(max(0, r * r - (yy - cy) ** 2))
        d.line((cx - meia, yy, cx + meia, yy), fill=(255, 255, 255, 60), width=2)


def _planeta(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img, "RGBA")
    for k in range(90):                                 # estrelas
        rnd = random.Random(k)
        x, y = rnd.random() * W, rnd.random() * H
        b = 120 + int(120 * abs(math.sin(t * 2 + k)))
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(b, b, b))
    cx, cy, r = W / 2, H * 0.45, 330
    gira = 1.0
    if cena.get("para"):                                # a rotação freia até parar
        gira = max(0.0, 1 - t / max(0.1, dur * 0.6))
    _globo(d, cx, cy, r, t if not cena.get("para") else min(t, dur * 0.6) * 0.5, gira)
    if cena.get("lua", True) is not False and not cena.get("sem_terra_lua"):
        a = t * 0.5
        lx, ly = cx + math.cos(a) * 470, cy + math.sin(a) * 160
        alfa = 255
        if cena.get("some_lua"):
            alfa = int(255 * max(0.0, 1 - t / max(0.1, dur * 0.6)))
        if alfa > 5:
            d.ellipse((lx - 60, ly - 60, lx + 60, ly + 60), fill=(220, 220, 228, alfa))
    if cena.get("vento"):                               # linhas de vento varrendo para leste
        for k in range(10):
            y = cy - r * 0.8 + k * r * 0.18
            x = (t * 900 + k * 170) % (W + 400) - 200
            d.line((x, y, x + 160, y), fill=p["acento2"], width=8)
    if cena.get("rotulo"):
        _centro_texto(d, W / 2, H * 0.78, str(cena["rotulo"]).upper(), _f(60), p["acento"])


def _terra_corte(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    cx, cy, r = W / 2, H * 0.46, 470
    camadas = [(1.0, (150, 96, 60)), (0.97, (205, 90, 40)), (0.55, (240, 150, 40)), (0.19, (255, 230, 120))]
    for f, cor in camadas:
        d.ellipse((cx - r * f, cy - r * f, cx + r * f, cy + r * f), fill=cor)
    if cena.get("buraco", True):
        d.rectangle((cx - 22, cy - r - 30, cx + 22, cy + r + 30), fill=(10, 10, 14))
        prog = cena.get("de", 0.0) + (cena.get("ate", 1.0) - cena.get("de", 0.0)) * _suave(t / max(0.1, dur * 0.9))
        y = cy - r + prog * 2 * r
        cena["_alvo"] = (cx / W, y / H)                  # para a câmera seguir quem cai ("seguir": true)
        d.ellipse((cx - 18, y - 18, cx + 18, y + 18), fill=p["fig"])
        d.ellipse((cx - 7, y - 30, cx + 7, y - 16), fill=p["fig"])
    if cena.get("rotulo"):
        _centro_texto(d, W / 2, H * 0.83, str(cena["rotulo"]).upper(), _f(64), p["acento"])


def _espaco(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    for k in range(120):
        rnd = random.Random(k)
        x, y = rnd.random() * W, rnd.random() * H
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(200, 205, 220))
    _globo(d, W * 0.8, H * 0.95, 520, t * 0.3)
    ax, ay = W / 2 + math.sin(t * 0.8) * 40, H * 0.42 + math.cos(t * 0.6) * 30
    ang = t * 0.4
    tam = 240
    d.rounded_rectangle((ax - tam * 0.35, ay - tam * 0.2, ax + tam * 0.35, ay + tam * 0.75), radius=50, fill=p["fig"])
    d.ellipse((ax - tam * 0.42, ay - tam * 0.75, ax + tam * 0.42, ay + tam * 0.05), fill=p["fig"])
    if not cena.get("sem_capacete"):
        d.ellipse((ax - tam * 0.3, ay - tam * 0.6, ax + tam * 0.3, ay - tam * 0.1), fill=p["fundo2"])
        d.ellipse((ax - tam * 0.18, ay - tam * 0.52, ax - tam * 0.05, ay - tam * 0.42), fill=p["acento2"])
    if cena.get("segundos"):
        resto = max(0, int(cena["segundos"]) - int(t * 3))
        _centro_texto(d, W / 2, H * 0.2, f"{resto:02d}s", _f(130, True), p["acento"])


def _numero(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    de, ate = float(cena.get("de", 0)), float(cena.get("ate", 100))
    v = de + (ate - de) * _suave(t / max(0.1, dur * 0.7))
    txt = f"{v:,.0f}".replace(",", ".") if abs(ate) >= 10 else f"{v:.1f}".replace(".", ",")
    _centro_texto(d, W / 2, H * 0.38, txt, _f(230, True), p["acento"])
    if cena.get("unidade"):
        _centro_texto(d, W / 2, H * 0.49, str(cena["unidade"]).upper(), _f(70), p["fig"])
    if cena.get("rotulo"):
        _centro_texto(d, W / 2, H * 0.58, str(cena["rotulo"]).upper(), _f(48), p["acento2"])


def _comparar(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    itens = cena.get("itens") or []
    if not itens:
        return
    maior = max(float(v) for _, v in itens)
    x0, larg = W * 0.12, W * 0.76
    y = H * 0.3
    for k, (nome, v) in enumerate(itens):
        cresce = _suave((t - k * 0.35) / max(0.2, dur * 0.5))
        w = larg * float(v) / maior * cresce
        cor = p["acento"] if k == len(itens) - 1 else p["apagado"]
        d.text((x0, y), str(nome).upper(), font=_f(46), fill=p["fig"])
        d.rounded_rectangle((x0, y + 70, x0 + max(20, w), y + 160), radius=20, fill=cor)
        num = f"{float(v) * cresce:,.0f}".replace(",", ".") + " " + str(cena.get("unidade", ""))
        d.text((x0 + 10, y + 175), num, font=_f(44, True), fill=cor)
        y += 330


def _multidao(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    chao = H * 0.7
    d.line((0, chao, W, chao), fill=p["apagado"], width=6)
    pulo = max(0.0, math.sin(t * 2.4)) * 60 if cena.get("pulando", True) else 0
    for linha in range(4):
        for k in range(9):
            x = 70 + k * 118 + (linha % 2) * 55
            alt = 210 - linha * 30
            y = chao - linha * 26 - pulo * (1 - linha * 0.15)
            cor = tuple(int(c * (1 - linha * 0.18)) for c in p["fig"])
            _pessoa(d, x, y, alt, cor, t, "parado", False, p["fundo"], olhos=False)
    if cena.get("rotulo"):
        _centro_texto(d, W / 2, H * 0.3, str(cena["rotulo"]).upper(), _f(70), p["acento"])


QUADROS.update({"planeta": _planeta, "terra_corte": _terra_corte, "espaco": _espaco, "numero": _numero,
                "comparar": _comparar, "multidao": _multidao})


def _hud(img, cena, t, p):
    d = ImageDraw.Draw(img)
    h0 = cena.get("_hora")
    if h0:
        hh, mm = (int(x) for x in h0.split(":"))
        seg = int(cena.get("_t0", 0) + t)
        m = mm + seg // 60
        d.text((70, 110), f"{(hh + m // 60) % 24:02d}:{m % 60:02d} AM", font=_f(44, True), fill=p["fig"])
    if cena.get("_parte"):
        b = d.textbbox((0, 0), cena["_parte"], font=_f(38))
        d.rounded_rectangle((W - 110 - (b[2] - b[0]), 104, W - 70, 166), radius=12, fill=p["acento"])
        d.text((W - 90 - (b[2] - b[0]), 108), cena["_parte"], font=_f(38), fill=p["fundo"])
    if cena.get("texto_topo"):
        _centro_texto(d, W / 2, H * 0.1, str(cena["texto_topo"]).upper(), _f(52), p["acento2"])
    if cena.get("alerta") and (t % 0.8) < 0.45:
        d.rectangle((0, 0, W - 1, H - 1), outline=p["acento"], width=22)


def quadro(cena: dict, t: float, dur: float, n: int) -> Image.Image:
    p = PALETAS.get(cena.get("_paleta", "noite"), PALETAS["noite"])
    tipo = cena.get("quadro", "texto")
    if tipo == "preto":
        return Image.new("RGB", (W, H), (0, 0, 0))
    img = _fundo(p).copy()
    QUADROS.get(tipo, _texto)(img, cena, t, dur, n, p)
    _hud(img, cena, t, p)
    z = 1.02 + 0.06 * _suave(t / max(1.0, dur))          # sempre aproximando devagar: o quadro nunca fica parado
    cx_, cy_ = 0.5, 0.5
    if cena.get("seguir") and cena.get("_alvo"):        # close acompanhando o alvo (ex.: quem cai no buraco)
        z = 2.2
        cx_, cy_ = cena["_alvo"]
    elif cena.get("foco"):
        cx_, cy_, z = cena["foco"]
    sx = sy = 0.0
    if cena.get("susto"):
        rnd = random.Random(n)
        sx, sy = (rnd.random() - 0.5) * 16, (rnd.random() - 0.5) * 16
    cw, ch = W / z, H / z
    x0 = min(max(0.0, cx_ * W - cw / 2 + sx), W - cw)
    y0 = min(max(0.0, cy_ * H - ch / 2 + sy), H - ch)
    img = img.resize((W, H), Image.BILINEAR, box=(x0, y0, min(W, x0 + cw), min(H, y0 + ch)))
    a = np.asarray(img).astype(np.float32)
    a += np.random.default_rng(n).normal(0, 5, (H // 4, W // 4, 1)).repeat(4, 0).repeat(4, 1)   # grão
    borda = min(t, dur - t)
    if borda < 0.08:
        a *= max(0.0, borda) / 0.08
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def renderizar_cena_voce(cena: dict, voz: dict, destino: Path, pausa: float, indice: int) -> float:
    dur = voz["duracao"] + pausa
    frames = math.ceil(dur * FPS)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", str(voz["arquivo"]),
                           "-filter_complex", "[1:a]aresample=44100,apad[a]", "-map", "0:v", "-map", "[a]",
                           "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p",
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
