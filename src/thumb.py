"""Thumbs automáticas de cada episódio (vertical 1080x1920 para TikTok/Shorts e horizontal 1280x720 para o YouTube).

Usa a cena mais forte do clímax (a última com o Abismo), sempre com ele em silhueta para não entregar o rosto,
o título do episódio em duas linhas (a segunda na caixa roxa das legendas), uma pergunta-gancho e o selo "EP. N".
    from .thumb import gerar_thumbs; vertical, horizontal = gerar_thumbs(roteiro, pasta)
"""
import json
import sys

import numpy as np
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from .util import RAIZ

FONTE = RAIZ / "assets" / "fontes" / "Poppins-Bold.ttf"
ROXO, VERMELHO = (124, 58, 237), (200, 30, 40)


def _cena_chave(r: dict) -> dict:
    cenas = r.get("cenas", [])
    com_abismo = [c for c in cenas if (c.get("ameaca") or {}).get("tipo") and c.get("cenario") != "celular_cftv"]
    if com_abismo:
        c = dict(com_abismo[-1])
    else:
        c = dict(next((c for c in reversed(cenas) if c.get("personagem") and c.get("cenario") != "celular_cftv"), cenas[-1]))
    c = json.loads(json.dumps(c))
    c.update(camera="parada", efeito="nenhum", _silhueta=True)
    a = c.get("ameaca")
    if a and a.get("tamanho") == "perto":            # na thumb ele fica inteiro, ao fundo
        a.update(tamanho="longe", acao="encarando")
    return c


def _linhas(titulo: str) -> tuple[str, str]:
    p = titulo.upper().split()
    if len(p) == 1:
        return "", p[0]
    melhor = min(range(1, len(p)), key=lambda i: abs(len(" ".join(p[:i])) - len(" ".join(p[i:]))))
    return " ".join(p[:melhor]), " ".join(p[melhor:])


def _fonte(texto: str, larg: float, max_px: int) -> ImageFont.FreeTypeFont:
    px = max_px
    while px > 30 and ImageFont.truetype(str(FONTE), px).getlength(texto) > larg:
        px -= 4
    return ImageFont.truetype(str(FONTE), px)


def _texto(d, x, y, txt, f, caixa=None):
    if caixa:
        w = f.getlength(txt)
        d.rounded_rectangle((x - 24, y + f.size * 0.1, x + w + 24, y + f.size * 1.2), radius=int(f.size * 0.15), fill=caixa)
    d.text((x + 5, y + 6), txt, font=f, fill=(0, 0, 0))
    d.text((x, y), txt, font=f, fill=(255, 255, 255))


def _pergunta(r: dict) -> str:
    if r.get("pergunta_thumb"):
        return r["pergunta_thumb"].strip()
    return "E você, escaparia?" if not r.get("final") else "Como tudo termina?"


VERM_T = (225, 25, 35)


def _arte_porta_pes(W, H, horizontal=False, circulo=True, aberta=False):
    """Porta vista de dentro, no escuro: luz forte vazando por baixo cortada por duas sombras de pés; olho mágico aceso.
    aberta=True (Parte 2): a mesma porta entreaberta, a luz do corredor entrando e a sombra comprida de alguém no chão."""
    yy, xx = np.mgrid[0:H, 0:W].astype("float32")
    if horizontal:
        px0, px1, chao = W * 0.62, W * 0.93, H * 0.80
        ptop = H * 0.02
    else:
        px0, px1, chao = W * 0.17, W * 0.83, H * 0.90
        ptop = H * 0.40
    if aberta:                                                 # a porta sobe para caber a sombra no chão
        ptop, chao = (H * 0.02, H * 0.56) if horizontal else (H * 0.41, H * 0.71)
    cxp = (px0 + px1) / 2
    # fundo: parede escura com brilho quente vindo do chão
    d_chao = np.clip((yy - (chao - H * 0.35)) / (H * 0.35), 0, 1)
    base = np.array([10, 7, 9]) + np.array([60, 30, 14]) * (d_chao ** 2.2)[..., None] * np.exp(-((xx - cxp) / (W * 0.45)) ** 2)[..., None]
    img = Image.fromarray(base.clip(0, 255).astype("uint8")).convert("RGBA")
    d = ImageDraw.Draw(img)
    # batente e porta
    d.rectangle((px0 - 26, ptop - 26, px1 + 26, chao), fill=(22, 16, 16))
    d.rectangle((px0, ptop, px1, chao - 30), fill=(40, 30, 30))
    pw = px1 - px0
    for (a, b) in ((0.08, 0.06), (0.08, 0.52)):          # almofadas da porta
        x0, x1 = px0 + pw * a, px1 - pw * a
        h_ = (chao - ptop)
        y0 = ptop + h_ * b
        y1 = y0 + h_ * 0.40
        d.rectangle((x0, y0, x1, y1), outline=(48, 38, 38), width=6)
    # maçaneta
    mx, my = px1 - pw * 0.13, ptop + (chao - ptop) * 0.55
    d.rounded_rectangle((mx - 16, my - 50, mx + 16, my + 50), radius=12, fill=(120, 96, 60))
    if aberta:
        return _abre_porta(img, W, H, px0, px1, ptop, chao, circulo)
    # olho mágico aceso
    oy = ptop + (chao - ptop) * 0.2 if not horizontal else ptop + (chao - ptop) * 0.3
    halo = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse((cxp - 60, oy - 60, cxp + 60, oy + 60), fill=(255, 190, 110, 150))
    img.alpha_composite(halo.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(img)
    d.ellipse((cxp - 20, oy - 20, cxp + 20, oy + 20), fill=(255, 225, 170), outline=(90, 70, 50), width=6)
    # fresta de luz debaixo da porta e o leque de luz no chão
    fy0, fy1 = chao - 30, chao
    luz = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(luz)
    ld.polygon([(px0, fy1), (px1, fy1), (px1 + pw * 0.5, H), (px0 - pw * 0.5, H)], fill=(255, 175, 90, 170))
    img.alpha_composite(luz.filter(ImageFilter.GaussianBlur(40)))
    brilho = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(brilho).rectangle((px0, fy0 - 6, px1, fy1 + 6), fill=(255, 210, 130, 255))
    img.alpha_composite(brilho.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(img)
    d.rectangle((px0, fy0, px1, fy1), fill=(255, 244, 210))
    # as duas sombras de pés cortando a luz (e se esticando pelo chão)
    sombra = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sombra)
    for k in (-1, 1):
        cx = cxp + k * pw * 0.085
        w = pw * 0.05
        sd.rounded_rectangle((cx - w, fy0 - 4, cx + w, fy1 + 4), radius=6, fill=(0, 0, 0, 255))
        L = H * 0.12
        for j in range(30):                                     # sombra comprida no chão, sumindo
            y = fy1 + L * j / 30
            ww = w * (1 + 1.4 * j / 30)
            sd.rectangle((cx - ww + k * j * 1.5, y, cx + ww + k * j * 1.5, y + L / 30 + 1), fill=(0, 0, 0, int(230 * (1 - j / 30))))
    img.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(3)))
    # vinheta vermelha
    g = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(g).rectangle((0, 0, W, H), outline=(200, 10, 20, 170), width=90)
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(70)))

    if circulo:                                                # círculo vermelho "à mão" em volta dos pés
        d = ImageDraw.Draw(img)
        rx, ry = pw * 0.24, (chao - fy0) + H * 0.035
        for k, (dx, dy, wd) in enumerate(((0, 0, 12), (6, -5, 8))):
            d.ellipse((cxp - rx + dx, fy0 - ry * 0.9 + dy, cxp + rx + dx, fy1 + ry * 1.1 + dy), outline=VERM_T, width=wd)
    return img


def _abre_porta(img, W, H, px0, px1, ptop, chao, circulo):
    """Parte 2: a porta entreaberta. Pela fresta entra a luz do corredor, e nela a sombra comprida de alguém parado."""
    pw = px1 - px0
    gx0 = px1 - pw * 0.30                                      # a fresta fica do lado da maçaneta
    d = ImageDraw.Draw(img)
    d.rectangle((gx0, ptop, px1, chao), fill=(255, 226, 170))   # luz do corredor
    d.rectangle((gx0 - 18, ptop, gx0, chao), fill=(70, 54, 46)) # quina da porta
    d.rounded_rectangle((gx0 - 60, ptop + (chao - ptop) * 0.5, gx0 - 30, ptop + (chao - ptop) * 0.5 + 100), radius=12, fill=(120, 96, 60))
    brilho = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(brilho)
    bd.rectangle((gx0, ptop, px1, chao), fill=(255, 200, 120, 200))
    bd.polygon([(gx0, chao), (px1, chao), (px1 + pw * 0.55, H), (gx0 - pw * 0.55, H)], fill=(255, 205, 140, 210))
    img.alpha_composite(brilho.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(img)
    d.polygon([(gx0, chao), (px1, chao), (px1 + pw * 0.45, H), (gx0 - pw * 0.45, H)], fill=(250, 200, 130))
    # sombra de alguém parado no corredor, esticada pelo chão na direção de quem olha
    som = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(som)
    cx = (gx0 + px1) / 2
    L = H - chao
    wb = pw * 0.07
    def pt(f, k):                                              # largura do corpo cresce com a distância (perspectiva)
        return cx + k * wb * (1 + 1.6 * f), chao + L * f
    sombra = (8, 5, 6, 245)
    for k in (-1, 1):                                          # pernas, coladas na fresta
        sd.polygon([pt(0, k * 0.15), pt(0, k * 0.85), pt(0.36, k * 0.95), pt(0.36, k * 0.12)], fill=sombra)
    sd.polygon([pt(0.33, -1.0), pt(0.33, 1.0), pt(0.62, 1.25), pt(0.66, 0.4), pt(0.66, -0.4), pt(0.62, -1.25)], fill=sombra)
    for k in (-1, 1):                                          # braços caídos
        sd.polygon([pt(0.36, k * 1.05), pt(0.36, k * 1.45), pt(0.63, k * 1.6), pt(0.63, k * 1.3)], fill=sombra)
    hx, hy = pt(0.76, 0)
    hr = wb * 1.15
    sd.ellipse((hx - hr, hy - hr * 1.25, hx + hr, hy + hr * 1.25), fill=sombra)       # cabeça
    img.alpha_composite(som.filter(ImageFilter.GaussianBlur(4)))
    g = Image.new("RGBA", img.size, (0, 0, 0, 0))              # vinheta vermelha
    ImageDraw.Draw(g).rectangle((0, 0, W, H), outline=(200, 10, 20, 170), width=90)
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(70)))
    if circulo:
        d = ImageDraw.Draw(img)
        rx, ry = wb * 4.2, L * 0.5
        cy = chao + L * 0.47
        for dx, dy, wd in ((0, 0, 12), (6, -5, 8)):
            d.ellipse((cx - rx + dx, cy - ry + dy, cx + rx + dx, cy + ry + dy), outline=VERM_T, width=wd)
    return img


def _gancho(d, cx, y0, larg, r, max_txt=140):
    """Balão de mensagem do grupo + frase grande (branco e vermelho), centrados em cx. Devolve o y final."""
    nome, msg = r.get("thumb_de", "MENSAGEM NOVA"), r.get("thumb_msg", "")
    fm = _fonte(msg, larg * 0.84, int(max_txt * 0.46))
    fn = ImageFont.truetype(str(FONTE), max(22, int(fm.size * 0.55)))
    bw = max(fm.getlength(msg), fn.getlength(nome)) + fm.size * 1.25
    x0 = cx - bw / 2
    alt = fn.size * 1.6 + fm.size * 1.3
    d.rounded_rectangle((x0, y0, x0 + bw, y0 + alt), radius=int(fm.size * 0.55), fill=(242, 242, 246))
    d.ellipse((x0 + bw - fn.size * 1.2, y0 + fn.size * 0.45, x0 + bw - fn.size * 0.6, y0 + fn.size * 1.05), fill=VERM_T)
    d.text((x0 + fm.size * 0.62, y0 + fn.size * 0.5), nome, font=fn, fill=(120, 120, 130))
    d.text((x0 + fm.size * 0.62, y0 + fn.size * 1.55), msg, font=fm, fill=(15, 15, 20))
    y = y0 + alt + fm.size * 0.7
    for k, txt in enumerate([l for l in r.get("thumb_texto", "").upper().split("|") if l]):
        f = _fonte(txt, larg, max_txt)
        x = cx - f.getlength(txt) / 2
        d.text((x + 6, y + 8), txt, font=f, fill=(0, 0, 0))
        d.text((x, y), txt, font=f, fill=VERM_T if k else (255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
        y += f.size * 1.08
    return y


def _thumb_porta_pes(r: dict, pasta: Path) -> tuple[Path, Path]:
    aberta = r.get("thumb_arte") == "porta_aberta"
    """Formato Você com arte própria: a porta no escuro, a luz por baixo e duas sombras de pés (círculo vermelho)."""
    selo = r.get("selo") or f"EP. {r.get('parte') or 1}"
    # vertical
    v = _arte_porta_pes(1080, 1920, aberta=aberta)
    d = ImageDraw.Draw(v)
    fs = ImageFont.truetype(str(FONTE), 46)
    d.rounded_rectangle((50, 60, 90 + fs.getlength(selo), 130), radius=14, fill=VERM_T)
    d.text((70, 64), selo, font=fs, fill=(255, 255, 255))
    _gancho(d, 540, 190, 1080 * 0.9, r, 170)
    vert = pasta / "thumb_vertical.jpg"
    v.convert("RGB").save(vert, quality=92)
    # horizontal
    h = _arte_porta_pes(1280, 720, horizontal=True, aberta=aberta)
    d = ImageDraw.Draw(h)
    fs = ImageFont.truetype(str(FONTE), 32)
    d.rounded_rectangle((40, 34, 72 + fs.getlength(selo), 86), radius=10, fill=VERM_T)
    d.text((56, 38), selo, font=fs, fill=(255, 255, 255))
    _gancho(d, 380, 120, 680, r, 130)
    hor = pasta / "thumb_horizontal.jpg"
    h.convert("RGB").save(hor, quality=92)
    return vert, hor


def _thumb_voce(r: dict, pasta: Path) -> tuple[Path, Path]:
    """Formato Você: a mensagem que dá o gancho (balão de celular) + frase em vermelho + o quadro do vídeo embaixo."""
    from .voce import quadro as quadro_voce
    c = next((c for c in r["cenas"] if c.get("thumb")), None) or next(
        (c for c in r["cenas"] if c.get("quadro") == "olho_magico" and c.get("figura") not in (None, "ninguem")), r["cenas"][0])
    c = dict(c, _paleta=r.get("paleta", "noite"), _hora=None, _parte=None, alerta=False, susto=False, texto_topo=None)
    c.update(r.get("thumb_ajuste") or {})
    q = quadro_voce(c, 2.2, 3.0, 7).convert("RGB")
    W, H = q.size
    q = ImageEnhance.Brightness(q).enhance(0.95)
    base = Image.new("RGB", (W, H), (6, 4, 6))
    base.paste(q.crop((0, int(H * 0.18), W, H)), (0, int(H * 0.36)))           # o desenho desce; o topo fica pro gancho
    v = base.convert("RGBA")
    fade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fade)
    for k in range(40):
        y = H * 0.36 + k * 6
        fd.rectangle((0, y, W, y + 6), fill=(6, 4, 6, int(255 * (1 - k / 40))))
    v.alpha_composite(fade)
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))                               # vinheta vermelha
    ImageDraw.Draw(g).rectangle((0, 0, W, H), outline=(200, 10, 20, 170), width=90)
    v.alpha_composite(g.filter(ImageFilter.GaussianBlur(70)))
    d = ImageDraw.Draw(v)
    selo = r.get("selo") or f"EP. {r.get('parte') or 1}"
    fs = ImageFont.truetype(str(FONTE), 46)
    d.rounded_rectangle((50, 60, 90 + fs.getlength(selo), 130), radius=14, fill=VERM_T)
    d.text((70, 64), selo, font=fs, fill=(255, 255, 255))
    # balão de mensagem
    nome, msg = r.get("thumb_de", "MENSAGEM NOVA"), r.get("thumb_msg", "")
    fm, fn = _fonte(msg, W * 0.74, 64), ImageFont.truetype(str(FONTE), 34)
    bw = max(fm.getlength(msg), fn.getlength(nome)) + 80
    x0, y0 = (W - bw) / 2, H * 0.1
    d.rounded_rectangle((x0, y0, x0 + bw, y0 + 70 + fm.size * 1.25), radius=34, fill=(242, 242, 246))
    d.text((x0 + 40, y0 + 20), nome, font=fn, fill=(120, 120, 130))
    d.text((x0 + 40, y0 + 58), msg, font=fm, fill=(15, 15, 20))
    # frase em vermelho
    y = y0 + 70 + fm.size * 1.25 + 50
    for k, txt in enumerate([l for l in r.get("thumb_texto", "").upper().split("|") if l]):
        f = _fonte(txt, W * 0.88, 140)
        x = (W - f.getlength(txt)) / 2
        d.text((x + 6, y + 8), txt, font=f, fill=(0, 0, 0))
        d.text((x, y), txt, font=f, fill=VERM_T if k else (255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
        y += f.size * 1.1
    vert = pasta / "thumb_vertical.jpg"
    v.convert("RGB").save(vert, quality=92)
    hz = Image.new("RGB", (1280, 720), (6, 4, 6))
    vv = v.convert("RGB")
    hz.paste(vv.resize((405, 720)), (875, 0))
    hz.paste(vv.crop((0, 0, W, int(H * 0.36))).resize((800, int(800 * H * 0.36 / W))), (40, 120))
    hor = pasta / "thumb_horizontal.jpg"
    hz.save(hor, quality=92)
    return vert, hor


def _thumb_celular(r: dict, pasta: Path) -> tuple[Path, Path]:
    """Cenário de fundo em tom de fita + um celular com a conversa do gancho + frase grande. Para histórias de chat."""
    import numpy as np
    W, H = 1080, 1920
    fundo = Image.open(Path(__file__).resolve().parent.parent / "assets" / "cenarios" / f"{r['thumb_cenario']}.png").convert("RGB")
    fw, fh = fundo.size
    esc = max(W / fw, H / fh)
    fundo = fundo.resize((int(fw * esc) + 1, int(fh * esc) + 1), Image.LANCZOS)
    fy, alvo = r.get("thumb_foco_y", [0.5, 0.5])                  # ponto do cenário (fração) que vai para a altura "alvo" da thumb
    topo = int(fy * fundo.height - alvo * H)
    base = Image.new("RGB", (W, H), (5, 3, 5))
    base.paste(fundo.crop(((fundo.width - W) // 2, max(0, topo), (fundo.width - W) // 2 + W, min(fundo.height, topo + H))), (0, max(0, -topo)))
    fundo = base
    a = np.asarray(fundo, "float32") * np.array([1.05, 0.72, 0.75])               # tom vermelho de fita
    a = a + np.random.RandomState(3).normal(0, 9, (H, W, 1))
    a[::4] *= 0.85
    v = Image.fromarray(a.clip(0, 255).astype("uint8")).convert("RGBA")
    som = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(som)
    for k in range(80):
        sd.rectangle((0, k * 12, W, k * 12 + 12), fill=(5, 2, 4, int(235 * (1 - k / 80) ** 1.3)))
    v.alpha_composite(som)
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(g).rectangle((0, 0, W, H), outline=(200, 10, 20, 200), width=80)
    v.alpha_composite(g.filter(ImageFilter.GaussianBlur(60)))
    d = ImageDraw.Draw(v)
    # celular
    px0, py0, pw, ph = 150, 130, 780, int(r.get("thumb_tel_alt", 640))
    d.rounded_rectangle((px0, py0, px0 + pw, py0 + ph), radius=60, fill=(18, 18, 22), outline=(70, 70, 80), width=6)
    tx0, ty0, tx1, ty1 = px0 + 26, py0 + 26, px0 + pw - 26, py0 + ph - 26
    d.rounded_rectangle((tx0, ty0, tx1, ty1), radius=40, fill=(236, 229, 221))
    d.rounded_rectangle((tx0, ty0, tx1, ty0 + 110), radius=40, fill=(32, 44, 51))
    d.rectangle((tx0, ty0 + 60, tx1, ty0 + 110), fill=(32, 44, 51))
    fn, fp = ImageFont.truetype(str(FONTE), 42), ImageFont.truetype(str(FONTE), 28)
    d.ellipse((tx0 + 24, ty0 + 22, tx0 + 90, ty0 + 88), fill=(90, 110, 120))
    d.text((tx0 + 110, ty0 + 16), r.get("thumb_de", "GRUPO"), font=fn, fill=(240, 240, 240))
    d.text((tx0 + 110, ty0 + 64), r.get("thumb_sub", "online"), font=fp, fill=(170, 190, 195))
    y = ty0 + 140
    for quem, txt in r.get("thumb_conversa", []):
        fm = _fonte(txt, (tx1 - tx0) * 0.72, 46)
        bw, bh = fm.getlength(txt) + 60, fm.size + 70
        meu = quem == "eu"
        x = tx1 - 24 - bw if meu else tx0 + 24
        d.rounded_rectangle((x, y, x + bw, y + bh), radius=22, fill=(217, 253, 211) if meu else (255, 255, 255))
        if not meu:
            d.text((x + 30, y + 8), quem, font=fp, fill=(200, 60, 60))
            d.text((x + 30, y + 40), txt, font=fm, fill=(20, 20, 20))
        else:
            d.text((x + 30, y + 14), txt, font=fm, fill=(20, 20, 20))
            d.text((x + bw - 175, y + bh - 36), "03:25", font=fp, fill=(90, 120, 130))
            cx0 = x + bw - 85
            for dx in (0, 16):                                                       # ✓✓ azul de lida
                d.line((cx0 + dx, y + bh - 22, cx0 + dx + 8, y + bh - 14, cx0 + dx + 24, y + bh - 32), fill=(60, 150, 220), width=4)
        y += bh + 22
    if r.get("thumb_circulo"):                                    # círculo vermelho no detalhe (ex.: os pés debaixo da porta)
        cx, cy, rr = r["thumb_circulo"]
        d.ellipse((cx - rr, cy - rr * 0.6, cx + rr, cy + rr * 0.6), outline=VERM_T, width=12)
    # selo e frase
    selo = r.get("selo", "")
    if selo:
        fs = ImageFont.truetype(str(FONTE), 46)
        d.rounded_rectangle((50, 40, 90 + fs.getlength(selo), 108), radius=14, fill=VERM_T)
        d.text((70, 44), selo, font=fs, fill=(255, 255, 255))
    y = py0 + ph + 60
    for k, txt in enumerate([l for l in r.get("thumb_texto", "").upper().split("|") if l]):
        f = _fonte(txt, W * 0.9, 150)
        x = (W - f.getlength(txt)) / 2
        d.text((x + 6, y + 9), txt, font=f, fill=(0, 0, 0))
        d.text((x, y), txt, font=f, fill=VERM_T if k else (255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
        y += f.size * 1.08
    vert = pasta / "thumb_vertical.jpg"
    v.convert("RGB").save(vert, quality=92)
    hz = Image.new("RGB", (1280, 720), (6, 4, 6))
    vv = v.convert("RGB")
    hz.paste(vv.resize((405, 720)), (875, 0))
    hz.paste(vv.crop((0, 0, W, int(py0 + ph + 40))).resize((800, int(800 * (py0 + ph + 40) / W))), (40, 40))
    hor = pasta / "thumb_horizontal.jpg"
    hz.save(hor, quality=92)
    return vert, hor


def gerar_thumbs(r: dict, pasta: Path) -> tuple[Path, Path]:
    if r.get("thumb_modelo") == "celular" and r.get("canal") != "esfr":
        pasta.mkdir(parents=True, exist_ok=True)
        return _thumb_celular(r, pasta)
    if r.get("formato") == "voce" and r.get("canal") != "esfr" and r.get("thumb_msg"):
        pasta.mkdir(parents=True, exist_ok=True)
        if r.get("thumb_arte") in ("porta_pes", "porta_aberta"):
            return _thumb_porta_pes(r, pasta)
        return _thumb_voce(r, pasta)
    if r.get("canal") == "esfr":                       # E Se Fosse Real? tem thumb própria (nada do terror)
        from .thumb_esfr import gerar
        return gerar(r, pasta)
    from .animacao import quadro
    pasta.mkdir(parents=True, exist_ok=True)
    prot = r.get("protagonista", "homem")
    if r.get("formato") == "real":                     # quadro do próprio vídeo (cena marcada com "thumb": true)
        import subprocess
        i = next((k for k, c in enumerate(r["cenas"]) if c.get("thumb")), len(r["cenas"]) // 2)
        clip = RAIZ / "trabalho" / "video" / f"clip_{i:02d}.mp4"
        png = pasta / "quadro.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.0", "-i", str(clip), "-frames:v", "1", str(png)], check=True)
        cena = ImageEnhance.Brightness(Image.open(png).convert("RGB")).enhance(1.15)
    elif r.get("formato") == "protocolo":             # o pictograma vermelho mais forte do vídeo, sem o texto
        from .protocolo import quadro as quadro_prot
        c = next((c for c in r["cenas"] if c.get("thumb")), None) or next(
            (c for c in r["cenas"] if any(i.startswith(("falso:", "gato:")) for i in c.get("icones", []))), r["cenas"][0])
        c = dict(c, narracao="", _palavras=[], _rotulo=r.get("rotulo", "PROTOCOLO STU"), _sombra=r.get("sombra", "abismo"))
        cena = ImageEnhance.Brightness(quadro_prot(c, 1.0, 3.0, 7)).enhance(1.15)
        from .protocolo import icone, VERM, VERM_ESC       # pictogramas grandes embaixo do título (o meio fica pro texto)
        nomes = (c.get("icones") or ["alerta"])[:2]
        tam = 560 if len(nomes) == 1 else 470
        for k, nome in enumerate(nomes):
            ic = icone(nome).resize((tam, tam))
            x = (cena.width - tam) // 2 + (0 if len(nomes) == 1 else (-245 if k == 0 else 245))
            y = int(cena.height * 0.62)
            brilho = ic.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * 0.7))
            cena.paste(Image.new("RGB", (tam, tam), VERM_ESC), (x, y), brilho)
            cena.paste(Image.new("RGB", (tam, tam), VERM), (x, y), ic)
    elif r.get("formato") == "sombra":                 # a cena marcada com "thumb" (ou o close do Abismo)
        from .sombra import quadro as quadro_sombra
        c = next((c for c in r["cenas"] if c.get("thumb")), None) or next(c for c in reversed(r["cenas"]) if c.get("quadro") == "abismo")
        cena = quadro_sombra(dict(c, texto=None), 3.0, 3.2, 1)
    elif r.get("formato") == "voce":                   # quadro do próprio vídeo (cena "thumb": true, ou o olho mágico)
        from .voce import quadro as quadro_voce
        c = next((c for c in r["cenas"] if c.get("thumb")), None) or next(
            (c for c in r["cenas"] if c.get("quadro") == "olho_magico" and c.get("figura") not in (None, "ninguem")), r["cenas"][0])
        c = dict(c, _paleta=r.get("paleta", "noite"), _hora=r.get("hora"), _parte=None, alerta=False, susto=False)
        cena = ImageEnhance.Brightness(quadro_voce(c, 2.2, 3.0, 7).convert("RGB")).enhance(1.15)
    elif r.get("thumb_cenario"):                       # ilustração pronta (cena especial) escolhida para a thumb
        cena = Image.open(RAIZ / "assets" / "cenarios" / f"{r['thumb_cenario']}.png").convert("RGB")
        fx, fy, z = r.get("thumb_foco") or [0.5, 0.5, 1.0]
        if z > 1:                                       # aproxima no ponto [fx, fy], mantendo 9:16
            w, h = cena.width / z, cena.height / z
            x0 = min(max(0, cena.width * fx - w / 2), cena.width - w)
            y0 = min(max(0, cena.height * fy - h / 2), cena.height - h)
            cena = cena.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((1188, 2112), Image.LANCZOS)
        cena = ImageEnhance.Brightness(cena).enhance(1.12)
    else:
        cena = ImageEnhance.Brightness(quadro(_cena_chave(r), 2.2, 4.0, prot).convert("RGB")).enhance(1.25)
    W, H = cena.size
    ty = r.get("thumb_texto_y", 0.38)                   # altura do bloco de título (fração da altura)
    l1, l2 = _linhas(r.get("titulo", "Você escaparia?"))
    pergunta = _pergunta(r)
    selo = r.get("selo") or ("FINAL" if r.get("final") else f"EP. {r.get('parte') or 1}")

    # ---------------- vertical
    v = cena.convert("RGBA")
    faixa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(faixa).rectangle((0, H * (ty - 0.02), W, H * (ty + 0.22)), fill=(3, 4, 12, 130))
    v.alpha_composite(faixa.filter(ImageFilter.GaussianBlur(50)))
    d = ImageDraw.Draw(v)
    y = H * ty
    for txt, cx in ((l1, None), (l2, ROXO)):
        if not txt:
            continue
        f = _fonte(txt, W * 0.84, 150)
        _texto(d, (W - f.getlength(txt)) / 2, y, txt, f, cx)
        y += f.size * 1.18
    f = _fonte(pergunta, W * 0.88, 52)
    _texto(d, (W - f.getlength(pergunta)) / 2, y + 20, pergunta, f)
    fs = ImageFont.truetype(str(FONTE), 46)
    d.rounded_rectangle((40, 60, 80 + fs.getlength(selo), 130), radius=14, fill=VERMELHO)
    d.text((60, 64), selo, font=fs, fill=(255, 255, 255))
    vert = pasta / "thumb_vertical.jpg"
    v.convert("RGB").save(vert, quality=92)

    # ---------------- horizontal
    hz = Image.new("RGB", (1280, 720))
    fundo = cena.resize((1280, int(1280 * H / W))).crop((0, 300, 1280, 1020)).filter(ImageFilter.GaussianBlur(30))
    hz.paste(ImageEnhance.Brightness(fundo).enhance(0.45), (0, 0))
    hz.paste(cena.resize((450, 800)).crop((0, 40, 450, 760)), (830, 0))
    sombra = Image.new("L", (1280, 720), 0)
    ImageDraw.Draw(sombra).rectangle((780, 0, 860, 720), fill=255)
    hz = Image.composite(Image.new("RGB", (1280, 720), (5, 6, 14)), hz,
                         sombra.filter(ImageFilter.GaussianBlur(25)).point(lambda p: int(p * 0.6)))
    dz = ImageDraw.Draw(hz)
    y = 170
    for txt, cx in ((l1, None), (l2, ROXO)):
        if not txt:
            continue
        f = _fonte(txt, 700, 110)
        _texto(dz, 60, y, txt, f, cx)
        y += f.size * 1.18
    f = _fonte(pergunta, 720, 40)
    _texto(dz, 62, y + 20, pergunta, f)
    fs = ImageFont.truetype(str(FONTE), 40)
    dz.rounded_rectangle((60, 80, 96 + fs.getlength(selo), 138), radius=12, fill=VERMELHO)
    dz.text((78, 84), selo, font=fs, fill=(255, 255, 255))
    hor = pasta / "thumb_horizontal.jpg"
    hz.save(hor, quality=92)
    return vert, hor


def enviar_thumbs(r: dict, pasta: Path) -> None:
    """Gera e manda as thumbs no Telegram (como arquivo, sem perder qualidade). Falha aqui não derruba o envio."""
    from . import telegram
    try:
        vert, hor = gerar_thumbs(r, pasta)
        for arq, nome in ((vert, "Thumb vertical (capa do TikTok/Shorts)"), (hor, "Thumb horizontal (YouTube)")):
            telegram.enviar_foto(arq, nome + ": toque e salve na galeria")   # abre em qualquer celular
            telegram.enviar_arquivo(arq, nome + ": arquivo original, sem compressão")
    except Exception as e:  # noqa: BLE001
        print(f"Thumbs falharam: {e}", file=sys.stderr)


if __name__ == "__main__":
    r = json.loads((RAIZ / "trabalho" / "roteiro.json").read_text(encoding="utf-8"))
    print(gerar_thumbs(r, RAIZ / "trabalho" / "thumbs"))
