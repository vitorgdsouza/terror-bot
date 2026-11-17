"""Formato "protocolo": comunicado de alerta em pictogramas vermelhos (estilo terror analógico), com identidade própria.

Tela preta com uma faixa vermelho-escura e um anel; ao fundo, pictogramas apagados do universo da série
(casa, cama, janela com lua, porta, relógio, olho); no centro, o pictograma da frase em vermelho vivo, com
cintilação, linhas de TV e glitch. O texto aparece palavra por palavra no ritmo da narração (sem legenda extra).

Cena: {"narracao": "...", "icones": ["cama", "gato:deitado"], "destaque": "preste atenção"}
  - "icones": 1 ou 2 pictogramas (lista em ICONES; "gato:<ação>" e "pessoa:<pose>" usam o gato e o boneco)
  - "destaque": em vez de pictograma, uma palavra grande no centro (ex.: "primeiro", "trate como anormal")
"""
import math
import random
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .util import RAIZ

W, H, FPS = 1080, 1920, 24
VERM = (226, 26, 30)
VERM_ESC = (86, 6, 8)
FAIXA = (34, 2, 3)
MONO = next((p for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
                         "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
                         str(RAIZ / "assets" / "fontes" / "Poppins-Bold.ttf")) if Path(p).exists()))
Y0, Y1 = int(H * 0.30), int(H * 0.64)        # faixa vermelha
_cache: dict = {}


# ---------------------------------------------------------------- pictogramas (desenhados em branco; colore depois)
def _tela(n=400):
    img = Image.new("L", (n, n), 0)
    return img, ImageDraw.Draw(img)


def _silhueta(rgba: Image.Image, n=400) -> Image.Image:
    a = rgba.getchannel("A").point(lambda v: 255 if v > 40 else 0)
    bb = a.getbbox()
    a = a.crop(bb) if bb else a
    a.thumbnail((int(n * 0.92), int(n * 0.92)))
    img = Image.new("L", (n, n), 0)
    img.paste(a, ((n - a.width) // 2, (n - a.height) // 2))
    return img


def _ic_gato(acao):
    from . import gato as G
    return _silhueta(G.desenhar(G.animar(acao or "sentado", 0.6), 360)[0])


def _ic_pessoa(pose):
    from . import boneco as B
    acao = {"medo": "parado", "deitado": "parado"}.get(pose or "", pose or "parado")
    return _silhueta(B.desenhar(B.animar(acao, 1.0, 4, 0.0, None), 380)[0])


def _ic_cama():
    img, d = _tela()
    d.rectangle((40, 210, 360, 250), fill=255)
    d.rectangle((40, 150, 70, 300), fill=255)
    d.rectangle((330, 200, 360, 300), fill=255)
    d.rounded_rectangle((80, 180, 160, 212), radius=12, fill=255)
    return img


def _ic_janela():
    img, d = _tela()
    d.rectangle((70, 60, 330, 340), outline=255, width=14)
    d.line((200, 60, 200, 340), fill=255, width=10)
    d.line((70, 200, 330, 200), fill=255, width=10)
    d.ellipse((215, 80, 305, 170), fill=255)
    d.ellipse((240, 72, 320, 152), fill=0)
    return img


def _ic_olho():
    img, d = _tela()
    d.chord((30, 110, 370, 330), 180, 360, fill=255)
    d.chord((30, 70, 370, 290), 0, 180, fill=255)
    d.ellipse((140, 130, 260, 250), fill=0)
    d.ellipse((172, 162, 228, 218), fill=255)
    return img


def _ic_porta():
    img, d = _tela()
    d.rectangle((110, 40, 290, 370), outline=255, width=14)
    d.ellipse((240, 200, 262, 222), fill=255)
    return img


def _ic_porta_aberta():
    img, d = _tela()
    d.rectangle((110, 40, 290, 370), outline=255, width=12)
    d.polygon([(110, 40), (210, 80), (210, 400), (110, 370)], fill=255)
    return img


def _ic_alerta():
    img, d = _tela()
    d.polygon([(200, 40), (370, 340), (30, 340)], outline=255, width=1)
    d.line([(200, 40), (370, 340), (30, 340), (200, 40)], fill=255, width=18, joint="curve")
    d.rounded_rectangle((188, 130, 212, 260), radius=10, fill=255)
    d.ellipse((186, 280, 214, 308), fill=255)
    return img


def _ic_relogio():
    img, d = _tela()
    d.ellipse((60, 60, 340, 340), outline=255, width=16)
    d.line((200, 200, 200, 105), fill=255, width=14)
    d.line((200, 200, 270, 235), fill=255, width=14)
    return img


def _ic_casa():
    img, d = _tela()
    d.polygon([(200, 50), (360, 190), (40, 190)], fill=255)
    d.rectangle((80, 185, 320, 350), fill=255)
    d.rectangle((170, 250, 230, 350), fill=0)
    return img


def _ic_prancheta():
    img, d = _tela()
    d.rounded_rectangle((90, 60, 310, 360), radius=16, outline=255, width=14)
    d.rectangle((160, 40, 240, 80), fill=255)
    for k in range(4):
        y = 130 + k * 55
        d.line((130, y, 150, y + 15, 175, y - 10), fill=255, width=8)
        d.line((195, y, 280, y), fill=255, width=10)
    return img


def _ic_som():
    img, d = _tela()
    d.polygon([(60, 160), (130, 160), (210, 90), (210, 310), (130, 240), (60, 240)], fill=255)
    for r in (60, 110, 160):
        d.arc((210 - r, 200 - r, 210 + r, 200 + r), -45, 45, fill=255, width=14)
    return img


def _ic_parar():
    img, d = _tela()
    d.ellipse((50, 50, 350, 350), outline=255, width=20)
    d.line((100, 300, 300, 100), fill=255, width=20)
    return img


def _ic_coleira():
    img, d = _tela()
    d.ellipse((60, 120, 340, 280), outline=255, width=22)
    d.ellipse((260, 230, 340, 310), fill=255)
    d.line((270, 270, 330, 270), fill=0, width=8)
    return img


def _ic_pegadas():
    img, d = _tela()
    for k, (x, y) in enumerate(((120, 320), (210, 250), (140, 170), (230, 95))):
        d.ellipse((x - 26, y - 20, x + 26, y + 20), fill=255)
        for dx, dy in ((-24, -28), (-8, -40), (8, -40), (24, -28)):
            d.ellipse((x + dx - 9, y + dy - 9, x + dx + 9, y + dy + 9), fill=255)
    return img


def _ic_escada():
    img, d = _tela()
    pts = [(40, 360)]
    for k in range(6):
        x, y = 40 + k * 55, 360 - k * 50
        pts += [(x, y - 50), (x + 55, y - 50)]
    pts += [(370, 60), (370, 360)]
    d.polygon(pts, fill=255)
    return img


ICONES = {"cama": _ic_cama, "janela": _ic_janela, "olho": _ic_olho, "porta": _ic_porta, "porta_aberta": _ic_porta_aberta,
          "alerta": _ic_alerta, "relogio": _ic_relogio, "casa": _ic_casa, "prancheta": _ic_prancheta, "som": _ic_som,
          "parar": _ic_parar, "coleira": _ic_coleira, "pegadas": _ic_pegadas, "escada": _ic_escada}


def icone(nome: str) -> Image.Image:
    if nome not in _cache:
        base, _, arg = nome.partition(":")
        if base == "gato":
            _cache[nome] = _ic_gato(arg)
        elif base == "pessoa":
            _cache[nome] = _ic_pessoa(arg)
        else:
            _cache[nome] = ICONES.get(base, _ic_alerta)()
    return _cache[nome]


# ---------------------------------------------------------------- composição
def _fundo() -> Image.Image:
    if "fundo" not in _cache:
        img = Image.new("RGB", (W, H), (0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rectangle((0, Y0, W, Y1), fill=FAIXA)
        cx, cy, r = W // 2, (Y0 + Y1) // 2, int(W * 0.47)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(40, 6, 8), width=6)
        # pictogramas apagados ao fundo (o universo da série)
        for k, (nome, x, y, n) in enumerate((("relogio", 0.14, 0.36, 120), ("casa", 0.33, 0.35, 130), ("janela", 0.8, 0.36, 140),
                                             ("porta", 0.08, 0.52, 150), ("escada", 0.9, 0.55, 130),
                                             ("cama", 0.28, 0.58, 150), ("olho", 0.7, 0.6, 110))):
            ic = icone(nome).resize((n, n))
            img.paste(Image.new("RGB", (n, n), (58, 8, 10)), (int(W * x - n / 2), int(H * y - n / 2)), ic)
        # silhueta enorme e apagada no meio (o Abismo observando, sempre presente)
        from . import abismo_anim as AB
        p = AB.animar("parado", 1.0, 4)
        p["silhueta"] = True
        ab = _silhueta(AB.desenhar(p, 900)[0], 700)
        img.paste(Image.new("RGB", (700, 700), (44, 5, 7)), (cx - 350, cy - 350), ab)
        _cache["fundo"] = img
    return _cache["fundo"]


def _linhas_tv(img: Image.Image, n: int) -> Image.Image:
    a = np.asarray(img).astype(np.int16)
    a[::4] = (a[::4] * 0.55).astype(np.int16)
    rnd = np.random.default_rng(n)
    a += rnd.integers(-10, 11, (H, W, 1), dtype=np.int16)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def _glitch(img: Image.Image, n: int) -> Image.Image:
    rnd = random.Random(n)
    a = np.asarray(img).copy()
    for _ in range(rnd.randint(3, 7)):
        y = rnd.randint(Y0, Y1 - 40)
        h = rnd.randint(8, 40)
        a[y:y + h] = np.roll(a[y:y + h], rnd.randint(-60, 60), axis=1)
    return Image.fromarray(a)


def _texto(d: ImageDraw.ImageDraw, palavras: list, t: float, frase: str) -> None:
    """Escreve a frase palavra por palavra (pelo tempo da fala), quebrando em até 2 linhas."""
    ditas = [p["texto"] for p in palavras if p["inicio"] <= t] if palavras else frase.split()
    if not ditas:
        return
    f = ImageFont.truetype(MONO, 44)
    linhas, linha = [], ""
    for w in frase.lower().split()[:len(ditas)]:
        if f.getlength((linha + " " + w).strip()) > W * 0.86:
            linhas.append(linha)
            linha = w
        else:
            linha = (linha + " " + w).strip()
    linhas.append(linha)
    linhas = linhas[-2:]
    y = Y1 - 40 - 58 * len(linhas)
    for ln in linhas:
        x = (W - f.getlength(ln)) / 2
        d.text((x + 3, y + 3), ln, font=f, fill=(20, 0, 0))
        d.text((x, y), ln, font=f, fill=(210, 28, 32))
        y += 58


def quadro(cena: dict, t: float, dur: float, n: int) -> Image.Image:
    img = _fundo().copy()
    d = ImageDraw.Draw(img)
    cx, cy = W // 2, (Y0 + Y1) // 2 - 40
    entra = min(1.0, t / 0.25)
    if cena.get("destaque"):
        txt = cena["destaque"].lower()
        px = 92
        while px > 40 and ImageFont.truetype(MONO, px).getlength(txt) > W * 0.8:
            px -= 4
        f = ImageFont.truetype(MONO, px)
        cor = tuple(int(c * entra) for c in VERM)
        d.text(((W - f.getlength(txt)) / 2, cy - px / 2), txt, font=f, fill=cor)
    else:
        nomes = (cena.get("icones") or ["alerta"])[:2]
        tam = 520 if len(nomes) == 1 else 380
        escala = 0.92 + 0.08 * entra
        for k, nome in enumerate(nomes):
            ic = icone(nome)
            s = int(tam * escala)
            ic = ic.resize((s, s), Image.LANCZOS)
            x = cx - s // 2 + (0 if len(nomes) == 1 else (-200 if k == 0 else 200))
            pulso = 0.85 + 0.15 * math.sin(t * 3 + k)
            if random.Random(n * 7 + k).random() < 0.05:   # cintila de vez em quando
                pulso *= 0.4
            cor = tuple(int(c * pulso * entra) for c in VERM)
            brilho = ic.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.6))
            img.paste(Image.new("RGB", (s, s), VERM_ESC), (x, cy - s // 2), brilho)
            img.paste(Image.new("RGB", (s, s), cor), (x, cy - s // 2), ic)
    _texto(d, cena.get("_palavras") or [], t, cena["narracao"])
    # selo do canal (canto) e "sinal"
    fp = ImageFont.truetype(MONO, 28)
    d.text((40, Y0 - 50), "PROTOCOLO STU", font=fp, fill=(150, 20, 24))
    if (n // 12) % 2 == 0:
        d.ellipse((W - 70, Y0 - 46, W - 46, Y0 - 22), fill=(200, 20, 24))
    if random.Random(n // 3).random() < 0.08 or t < 0.12:
        img = _glitch(img, n)
    img = _linhas_tv(img, n)
    borda = min(t, dur - t)
    if borda < 0.15:
        img = Image.blend(img, Image.new("RGB", (W, H)), 1 - max(0.0, borda) / 0.15)
    return img


def renderizar_cena_protocolo(cena: dict, voz: dict, destino: Path, pausa: float, indice: int) -> float:
    dur = voz["duracao"] + pausa
    cena["_palavras"] = voz.get("palavras") or []
    frames = math.ceil(dur * FPS)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", str(voz["arquivo"]), "-filter_complex",
                           "[1:a]aresample=44100,apad[a]", "-map", "0:v", "-map", "[a]", "-t", f"{dur:.3f}",
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
