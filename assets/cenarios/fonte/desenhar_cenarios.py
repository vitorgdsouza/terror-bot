"""Desenha os cenários (SVG) no mesmo traço do personagem e grava os metadados usados pela animação.

Uso: python desenhar_cenarios.py   -> cria svg/<nome>.svg e ../cenarios.json
Depois converta para PNG (1188x2112), por exemplo com: rsvg-convert svg/sala.svg -o ../sala.png
"""
import json
from pathlib import Path

W, H = 1188, 2112          # 10% maior que 1080x1920, sobra para a câmera se mexer
L = "#141428"              # contorno
OUT = Path(__file__).parent / "svg"
OUT.mkdir(exist_ok=True)
META = {}

# parede de fundo do "quarto em perspectiva" (um ponto de fuga no centro)
BX0, BY0, BX1, BY1 = 194, 520, 994, 1500


def r(x, y, w, h, fill, rx=0, sw=8, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{L}" stroke-width="{sw}" {extra}/>'


def p(pts, fill, sw=8, extra=""):
    pts = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polygon points="{pts}" fill="{fill}" stroke="{L}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'


def c(x, y, rad, fill, sw=8, extra=""):
    return f'<circle cx="{x}" cy="{y}" r="{rad}" fill="{fill}" stroke="{L}" stroke-width="{sw}" {extra}/>'


def linha(x1, y1, x2, y2, sw=6, cor=L):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{cor}" stroke-width="{sw}" stroke-linecap="round"/>'


def brilho(x, y, rx, ry, cor="#ffd36e", op=0.45, gid="g"):
    return (f'<defs><radialGradient id="{gid}"><stop offset="0%" stop-color="{cor}" stop-opacity="{op}"/>'
            f'<stop offset="100%" stop-color="{cor}" stop-opacity="0"/></radialGradient></defs>'
            f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="url(#{gid})"/>')


def caixa(parede, chao, teto, lado):
    """Sala vista de frente com um ponto de fuga."""
    return (p([(0, 0), (W, 0), (BX1, BY0), (BX0, BY0)], teto, 6)
            + p([(0, 0), (BX0, BY0), (BX0, BY1), (0, H)], lado, 6)
            + p([(W, 0), (BX1, BY0), (BX1, BY1), (W, H)], lado, 6)
            + p([(BX0, BY1), (BX1, BY1), (W, H), (0, H)], chao, 6)
            + r(BX0, BY0, BX1 - BX0, BY1 - BY0, parede, 0, 6))


def janela_noite(x, y, w, h, gid, cortina="#5b3f73"):
    lua = c(x + w * 0.72, y + h * 0.28, w * 0.09, "#f3edc8", 4)
    return (r(x, y, w, h, "#0f1733", 6, 10)
            + f'<g clip-path="url(#cl{gid})">{lua}'
            + "".join(c(x + w * fx, y + h * fy, 4, "#dfe6ff", 0) for fx, fy in ((.2, .2), (.4, .12), (.3, .4), (.85, .6), (.55, .3)))
            + p([(x, y + h), (x + w * .15, y + h * .55), (x + w * .3, y + h * .7), (x + w * .45, y + h * .45),
                 (x + w * .62, y + h * .68), (x + w * .8, y + h * .5), (x + w, y + h * .66), (x + w, y + h)], "#0a0f22", 0)
            + "</g>"
            + f'<defs><clipPath id="cl{gid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath></defs>'
            + linha(x + w / 2, y, x + w / 2, y + h, 10) + linha(x, y + h / 2, x + w, y + h / 2, 10)
            + p([(x - 40, y - 30), (x + w * .22, y - 30), (x + w * .12, y + h + 40), (x - 50, y + h + 40)], cortina, 7)
            + p([(x + w + 40, y - 30), (x + w * .78, y - 30), (x + w * .88, y + h + 40), (x + w + 50, y + h + 40)], cortina, 7)
            + r(x - 60, y - 50, w + 120, 22, "#3b2b2b", 8, 6))


def porta(x, y, w, h, cor="#4a3b5c", aberta=False):
    g = r(x - 18, y - 18, w + 36, h + 18, "#2a2238", 4, 8)
    if aberta:
        g += r(x, y, w, h, "#05050a", 0, 6) + p([(x, y), (x + w * .35, y + 30), (x + w * .35, y + h - 10), (x, y + h)], cor, 7)
    else:
        g += r(x, y, w, h, cor, 4, 8) + c(x + w * .85, y + h * .52, 14, "#d9b45a", 5)
        g += r(x + w * .15, y + h * .1, w * .7, h * .32, "none", 6, 5) + r(x + w * .15, y + h * .52, w * .7, h * .38, "none", 6, 5)
    return g


def salvar(nome, corpo, meta):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{corpo}</svg>'
    (OUT / f"{nome}.svg").write_text(svg, encoding="utf-8")
    META[nome] = meta


def rel(x0, y0, x1, y1):
    """Converte retângulo em frações da tela (para o código de animação)."""
    return [round(x0 / W, 4), round(y0 / H, 4), round((x1 - x0) / W, 4), round((y1 - y0) / H, 4)]


# ---------- SALA ----------
g = caixa("#2e3c6b", "#3b3552", "#1d2547", "#26315a")
g += janela_noite(260, 640, 260, 330, "s")
tv = (560, 860, 900, 1120)
g += r(520, 1120, 420, 170, "#3a2c2c", 6) + linha(560, 1205, 900, 1205, 5)
g += r(tv[0] - 18, tv[1] - 18, tv[2] - tv[0] + 36, tv[3] - tv[1] + 36, "#111118", 10) + r(*tv[:2], tv[2] - tv[0], tv[3] - tv[1], "#1b2440", 0, 5)
g += linha(730, 1138, 730, 1120, 10)
g += r(30, 1560, 420, 230, "#5a3e6e", 40) + r(10, 1500, 90, 330, "#4b335c", 30) + r(380, 1500, 90, 330, "#4b335c", 30) + r(70, 1460, 340, 140, "#5a3e6e", 30)
g += brilho(1040, 1180, 260, 300, gid="ls") + linha(1040, 1290, 1040, 1840, 10) + p([(990, 1840), (1090, 1840), (1070, 1870), (1010, 1870)], "#2a2a33", 6)
g += p([(960, 1150), (1120, 1150), (1090, 1300), (990, 1300)], "#f0c86a", 8)
g += r(380, 1780, 440, 70, "#4e2f3a", 30, 6)
salvar("sala", g, {"piso": 0.89, "tv": rel(*tv), "janela": rel(260, 640, 520, 970), "fundo": [0.5, 0.71, 0.45]})

# ---------- CORREDOR ----------
g = (p([(0, 0), (W, 0), (694, 760), (494, 760)], "#1a2140", 6)
     + p([(0, 0), (494, 760), (494, 1180), (0, H)], "#2b3557", 6)
     + p([(W, 0), (694, 760), (694, 1180), (W, H)], "#2b3557", 6)
     + p([(494, 1180), (694, 1180), (W, H), (0, H)], "#3a3550", 6)
     + r(494, 760, 200, 420, "#05050c", 0, 6))
g += p([(140, 560), (300, 680), (300, 1300), (140, 1520)], "#4a3b5c", 7) + c(275, 1010, 10, "#d9b45a", 4)
g += p([(1048, 560), (888, 680), (888, 1300), (1048, 1520)], "#4a3b5c", 7) + c(913, 1010, 10, "#d9b45a", 4)
g += p([(400, 1500), (788, 1500), (1000, 2112), (188, 2112)], "#5a2f3a", 6)
for i, (yy, rr) in enumerate(((140, 70), (420, 42), (620, 26))):
    g += brilho(594, yy + 120, rr * 4, rr * 3, op=0.35, gid=f"c{i}") + f'<ellipse cx="594" cy="{yy}" rx="{rr * 1.6}" ry="{rr * .45}" fill="#ffe7a3" stroke="{L}" stroke-width="5"/>'
salvar("corredor", g, {"piso": 0.92, "porta": rel(494, 760, 694, 1180), "fundo": [0.5, 0.56, 0.22]})

# ---------- QUARTO ----------
g = caixa("#3a3266", "#3f3550", "#231e46", "#2e285a")
g += janela_noite(470, 640, 250, 300, "q", "#6a3f4f")
g += r(230, 760, 210, 620, "#5c4433", 6) + linha(335, 770, 335, 1370, 6) + c(320, 1070, 9, "#d9b45a", 4) + c(350, 1070, 9, "#d9b45a", 4)
g += p([(338, 772), (360, 772), (360, 1368), (338, 1368)], "#05050a", 4)
g += r(700, 1220, 520, 140, "#e8e2f0", 30) + r(690, 1300, 540, 300, "#7d4b6b", 20) + r(1100, 1080, 60, 520, "#5c4433", 10) + r(760, 1180, 170, 80, "#ffffff", 30)
g += r(560, 1340, 110, 150, "#5c4433", 6) + brilho(615, 1260, 160, 150, gid="lq") + p([(580, 1250), (650, 1250), (640, 1330), (590, 1330)], "#f0c86a", 6)
salvar("quarto", g, {"piso": 0.9, "janela": rel(470, 640, 720, 940), "porta": rel(338, 772, 360, 1368), "fundo": [0.62, 0.71, 0.45]})

# ---------- COZINHA ----------
g = caixa("#26475a", "#33424a", "#17303d", "#1f3c4b")
g += janela_noite(500, 700, 220, 220, "k", "#6b5b3a")
g += r(194, 1180, 800, 320, "#3d5a5f", 0, 7) + r(194, 1150, 800, 40, "#c9c2b8", 0, 7)
for x in (230, 430, 760):
    g += r(x, 1220, 170, 240, "#466a70", 8, 6) + linha(x + 150, 1300, x + 150, 1380, 6)
g += r(194, 560, 260, 300, "#466a70", 6) + r(744, 560, 250, 300, "#466a70", 6)
g += r(40, 900, 230, 1000, "#d7d9df", 18) + linha(40, 1250, 270, 1250, 6) + linha(240, 980, 240, 1180, 8) + linha(240, 1300, 240, 1500, 8)
g += linha(610, 0, 610, 380, 5) + brilho(610, 560, 260, 280, gid="lk") + p([(530, 380), (690, 380), (650, 440), (570, 440)], "#f0c86a", 6)
salvar("cozinha", g, {"piso": 0.9, "janela": rel(500, 700, 720, 920), "fundo": [0.5, 0.71, 0.45]})

# ---------- PORTA DE ENTRADA ----------
g = caixa("#33335e", "#3a3550", "#1f1f45", "#29295a")
g += porta(454, 760, 280, 740, "#5a3e33")
g += c(594, 960, 12, "#0a0a12", 4)
g += r(500, 1520, 190, 50, "#7b3f3f", 12, 6)
g += linha(820, 900, 960, 900, 10) + c(850, 930, 14, "#d9b45a", 4) + c(930, 930, 14, "#d9b45a", 4)
g += p([(830, 940), (880, 940), (900, 1200), (810, 1200)], "#3f5a6e", 6)
g += r(240, 1200, 160, 200, "#5c4433", 6) + brilho(320, 1130, 170, 160, gid="lp") + p([(285, 1110), (355, 1110), (345, 1190), (295, 1190)], "#f0c86a", 6)
salvar("porta_entrada", g, {"piso": 0.89, "porta": rel(454, 760, 734, 1500), "fundo": [0.5, 0.71, 0.45]})

# ---------- JANELA (close) ----------
g = r(0, 0, W, H, "#2a3460", 0, 0)
g += janela_noite(144, 380, 900, 1100, "j", "#5b3f73")
g += r(90, 1480, 1008, 70, "#4a3b3b", 10)
g += p([(0, 1550), (W, 1550), (W, H), (0, H)], "#3a3550", 6)
salvar("janela", g, {"piso": 0.97, "janela": rel(144, 380, 1044, 1480), "fundo": [0.5, 0.66, 0.5]})

# ---------- ESCADA ----------
g = r(0, 0, W, H, "#262f55", 0, 0) + p([(0, 1700), (W, 1700), (W, H), (0, H)], "#3a3550", 6)
degraus = 9
for i in range(degraus):
    x0 = 300 + i * 70
    y0 = 1700 - (i + 1) * 120
    g += r(x0, y0, W - x0, 120, "#4a3b5c" if i % 2 else "#54446a", 0, 6)
g += r(930, 380, 258, 240, "#05050c", 0, 6)
g += linha(240, 1520, 860, 440, 14, "#5c4433") + "".join(linha(240 + k * 78, 1520 - k * 135, 240 + k * 78, 1700 - k * 135 - 20, 8, "#5c4433") for k in range(8))
g += brilho(200, 300, 260, 260, op=0.3, gid="le") + c(200, 260, 40, "#ffe7a3", 6)
salvar("escada", g, {"piso": 0.93, "porta": rel(930, 380, 1188, 620), "fundo": [0.88, 0.29, 0.22]})

# ---------- BANHEIRO ----------
g = caixa("#2c4a5e", "#3f4a55", "#1a3040", "#244050")
for yy in range(560, 1500, 90):
    g += linha(BX0, yy, BX1, yy, 3, "#3b5d73")
g += r(394, 640, 400, 420, "#0d1626", 20, 10) + p([(420, 680), (520, 680), (440, 820)], "#2a3a55", 0)
g += r(434, 1160, 320, 90, "#e8e8ee", 30) + r(514, 1250, 160, 250, "#d0d0da", 10) + linha(594, 1100, 594, 1160, 10)
g += p([(780, 520), (994, 520), (1188, 0), (1188, 2112), (994, 1500), (780, 1500)], "#5f7f8f", 7)
for xx in (840, 900, 960):
    g += linha(xx, 540, xx, 1480, 4)
salvar("banheiro", g, {"piso": 0.9, "espelho": rel(394, 640, 794, 1060), "fundo": [0.42, 0.71, 0.45]})

# ---------- CASA (por fora) ----------
g = r(0, 0, W, H, "#141d3d", 0, 0) + c(930, 300, 90, "#f3edc8", 6)
g += "".join(c(x, y, 5, "#dfe6ff", 0) for x, y in ((120, 200), (330, 140), (520, 260), (700, 120), (1080, 520), (260, 420), (820, 480)))
g += p([(0, 1500), (W, 1460), (W, H), (0, H)], "#1f2f2a", 6)
g += r(250, 900, 700, 620, "#3b3f66", 0, 8) + p([(200, 920), (600, 560), (1000, 920)], "#2a2440", 8)
g += r(530, 1180, 140, 340, "#5a3e33", 4, 8) + c(645, 1350, 9, "#d9b45a", 4)
g += r(320, 1000, 150, 140, "#f0c86a", 4, 8) + linha(395, 1000, 395, 1140, 6) + brilho(395, 1070, 200, 180, gid="lc")
g += r(730, 1000, 150, 140, "#0f1733", 4, 8) + linha(805, 1000, 805, 1140, 6)
g += p([(540, 1520), (660, 1520), (760, H), (440, H)], "#4a4552", 6)
for x in range(0, W, 70):
    g += r(x, 1600, 26, 170, "#2d2a3a", 6, 5)
g += r(0, 1640, W, 18, "#2d2a3a", 0, 5)
g += p([(0, 1500), (60, 900), (130, 760), (210, 900), (260, 1500)], "#0a1210", 6)
salvar("casa_fora", g, {"piso": 0.93, "porta": rel(530, 1180, 670, 1520), "janela": rel(730, 1000, 880, 1140), "fundo": [0.5, 0.72, 0.3]})

# ---------- RUA ----------
g = r(0, 0, W, H, "#121a38", 0, 0) + c(250, 260, 70, "#f3edc8", 6)
g += p([(0, 1150), (W, 1150), (W, H), (0, H)], "#24222f", 6)
g += p([(520, 1150), (668, 1150), (1000, H), (188, H)], "#2e2c3a", 0)
for k in range(5):
    y0 = 1200 + k * 180
    g += p([(588, y0), (600, y0), (606 + k * 8, y0 + 90), (582 - k * 8, y0 + 90)], "#d8d0a8", 0)
for x0, w0, h0 in ((0, 260, 420), (240, 220, 330), (900, 288, 460), (720, 200, 300)):
    g += r(x0, 1150 - h0, w0, h0, "#1b2346", 0, 6) + r(x0 + 40, 1150 - h0 + 60, 60, 70, "#f0c86a" if x0 == 900 else "#0f1733", 4, 5)
g += linha(980, 1700, 980, 700, 16, "#2a2a33") + linha(980, 700, 860, 700, 12, "#2a2a33")
g += p([(820, 700), (900, 700), (1060, 1700), (660, 1700)], "#ffe7a3", 0, 'opacity="0.18"') + c(860, 715, 22, "#ffe7a3", 6)
salvar("rua", g, {"piso": 0.94, "fundo": [0.5, 0.57, 0.18]})

(Path(__file__).parent.parent / "cenarios.json").write_text(json.dumps(META, indent=2), encoding="utf-8")
print("ok", list(META))
