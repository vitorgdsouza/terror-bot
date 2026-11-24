"""Thumbs do canal E Se Fosse Real? (ciência). Separado do terror: identidade própria, nada de cenário ou frase do outro canal.

Usa um quadro do próprio vídeo (a cena marcada com "thumb": true, ou a primeira cena com desenho) e escreve por cima
a frase curta de "thumb_texto" (ex.: "PULARIA|NESSE BURACO?"), em branco e amarelo, com o selo do canal embaixo.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ / "assets" / "fontes" / "Poppins-Bold.ttf"
AMARELO, BRANCO, AZUL = (255, 196, 40), (250, 250, 252), (90, 215, 255)
SO_TEXTO = {"texto", "preto", "numero", "regra"}


def _cena(r: dict) -> tuple[dict, int]:
    cenas = r["cenas"]
    i = next((k for k, c in enumerate(cenas) if c.get("thumb")), None)
    if i is None:
        i = next((k for k, c in enumerate(cenas) if c.get("quadro") not in SO_TEXTO), 0)
    return cenas[i], i


def _fonte(txt: str, larg: float, max_px: int) -> ImageFont.FreeTypeFont:
    px = max_px
    while px > 40 and ImageFont.truetype(str(FONTE), px).getlength(txt) > larg:
        px -= 4
    return ImageFont.truetype(str(FONTE), px)


def _escreve(d, x, y, txt, f, cor):
    for dx, dy in ((0, 10), (6, 6), (-4, 4), (4, -2)):
        d.text((x + dx, y + dy), txt, font=f, fill=(0, 0, 0))
    d.text((x, y), txt, font=f, fill=cor, stroke_width=4, stroke_fill=(0, 0, 0))


def quadro_do_video(r: dict) -> Image.Image:
    from .voce import quadro
    c, i = _cena(r)
    c = dict(c, _paleta=r.get("paleta", "ciencia"), _hora=None, _parte=None, alerta=False, susto=False, texto_topo=None)
    dur = float(c.get("thumb_t", 3.0))
    img = quadro(c, dur * float(c.get("thumb_momento", 0.7)), dur, 7 + i).convert("RGB")
    return ImageEnhance.Contrast(ImageEnhance.Brightness(img).enhance(1.12)).enhance(1.08)


def _ceu(W: int, H: int) -> Image.Image:
    import random
    yy, xx = np.mgrid[0:H, 0:W].astype("float32")
    d = np.sqrt(((xx / W - 0.5) * 1.2) ** 2 + (yy / H - 0.58) ** 2)
    a = np.array([6, 10, 32]) + np.array([20, 38, 95]) * np.exp(-d * 3.0)[..., None]
    img = Image.fromarray(a.clip(0, 255).astype("uint8"))
    dr, rnd = ImageDraw.Draw(img), random.Random(3)
    for _ in range(260):
        x, y, rr = rnd.random() * W, rnd.random() * H, rnd.choice([1, 1, 2, 2, 3])
        c = rnd.randint(150, 255)
        dr.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(c, c, 255))
    return img


ARTE_HORIZONTAL = {"lua_some", "sem_traje", "buraco_negro"}                               # artes que têm composição própria em 16:9


def arte(r: dict, W: int = 1080, H: int = 1920) -> Image.Image:
    """A imagem principal da thumb: um desenho feito para ela (thumb_arte) ou um quadro do vídeo com zoom."""
    tipo = r.get("thumb_arte", "")
    if not tipo:
        img = quadro_do_video(r)
        if (W, H) != img.size:
            return img
        # o desenho principal dos quadros fica em ~47% da altura; na thumb ele vai para o meio do espaço livre
        # entre o texto (em cima) e o selo (embaixo), em ~58%, com um pouco de zoom
        z = max(1.0, float(r.get("thumb_zoom", 1.25)))
        fx, fy = r.get("thumb_centro", [0.5, 0.47])
        alvo = float(r.get("thumb_alvo", 0.58))
        cw, ch = W / z, H / z
        x0 = min(max(0, fx * W - cw / 2), W - cw)
        y0 = min(max(0, fy * H - alvo * ch), H - ch)
        return img.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
    img = _ceu(W, H).convert("RGBA")
    d = ImageDraw.Draw(img)
    if tipo == "terra_parada":
        t = terra(400)
        img.alpha_composite(t, (W // 2 - t.width // 2, int(H * 0.6) - t.height // 2))
        cx, cy, rr = W * 0.76, H * 0.75, 125                     # selo de "pause" vermelho
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(225, 30, 40), outline=(255, 255, 255), width=12)
        for dx in (-42, 22):
            d.rounded_rectangle((cx + dx, cy - 58, cx + dx + 22, cy + 58), radius=6, fill=(255, 255, 255))
    elif tipo == "lua_some":
        _lua_some(img, W, H)
    elif tipo == "sem_traje":
        _sem_traje(img, W, H)
    elif tipo == "buraco":
        R = 380
        t = terra(R)
        cx, cy = W // 2, int(H * 0.63)
        td = ImageDraw.Draw(t)                                    # o túnel atravessando o planeta de polo a polo
        c = t.width / 2
        td.rectangle((c - 26, c - R + 2, c + 26, c + R - 2), fill=(12, 6, 4, 255))
        td.rectangle((c - 26, c - R + 2, c - 18, c + R - 2), fill=(255, 140, 40, 255))
        td.rectangle((c + 18, c - R + 2, c + 26, c + R - 2), fill=(255, 140, 40, 255))
        img.alpha_composite(t, (cx - t.width // 2, cy - t.height // 2))
        from .voce import _pessoa
        _pessoa(d, cx, cy - R - 40, 150, (245, 245, 250), 0.0, "parado", fundo=(10, 16, 40))
        for k in range(3):                                        # setas amarelas: pra baixo
            y = cy - R - 150 + k * 0
            x = cx + 150
            d.polygon([(x - 40, cy - R - 120), (x + 40, cy - R - 120), (x, cy - R - 50)], fill=(255, 196, 40)) if k == 0 else None
        d.rectangle((cx + 140, cy - R - 230, cx + 160, cy - R - 120), fill=(255, 196, 40))
    elif tipo == "asteroide":
        R = 700
        t = terra(R, seed=33)
        ex, ey = W // 2, int(H * 1.08)                            # Terra enorme, só o topo aparece
        img.alpha_composite(t, (ex - t.width // 2, ey - t.height // 2))
        ax, ay, ar = int(W * 0.56), int(H * 0.5), 125
        ix, iy = int(W * 0.47), ey - R + 20                       # onde vai bater: brilho no planeta
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(gl).ellipse((ix - 170, iy - 60, ix + 170, iy + 60), fill=(255, 120, 30, 200))
        img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(40)))
        cauda = Image.new("RGBA", (W, H), (0, 0, 0, 0))          # rastro de fogo vindo do alto à direita
        cd = ImageDraw.Draw(cauda)
        dx, dy = 1.0, -1.25
        for k in range(46, 0, -1):
            f = k / 46
            x, y = ax + dx * k * 16, ay + dy * k * 16
            rr = ar * (1.05 - 0.75 * f)
            cor = (255, int(240 - 170 * f), int(150 - 140 * f), int(250 * (1 - f) ** 0.7 + 10))
            cd.ellipse((x - rr, y - rr, x + rr, y + rr), fill=cor)
        img.alpha_composite(cauda.filter(ImageFilter.GaussianBlur(14)))
        halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(halo).ellipse((ax - ar * 1.7, ay - ar * 1.7, ax + ar * 1.7, ay + ar * 1.7), fill=(255, 170, 60, 210))
        img.alpha_composite(halo.filter(ImageFilter.GaussianBlur(30)))
        S = ar * 2 + 4                                             # a rocha, com crateras e lado quente
        X = (np.arange(S)[None, :] - S / 2) / ar
        Y = (np.arange(S)[:, None] - S / 2) / ar
        m2 = X ** 2 + Y ** 2
        rug = _ruido(S, S, 18, 5)
        borda = 1 + (rug - 0.5) * 0.25
        Z = np.sqrt(np.clip(1 - m2, 0, 1))
        luz = np.clip(-X * 0.55 + Y * 0.6 + Z * 0.6, 0, 1)
        base = (70 + 80 * rug)[..., None] * np.array([1.0, 0.85, 0.75])
        quente = np.clip((-X * 0.7 + Y * 0.7) - 0.15, 0, 1)[..., None] * 1.3   # frente em brasa (lado da descida)
        quente = np.clip(quente, 0, 1)
        cor = base * (0.35 + 0.9 * luz)[..., None] * (1 - quente) + np.array([255, 150, 50]) * quente
        a = np.clip((borda - np.sqrt(m2)) * ar * 1.2, 0, 1) * 255
        img.alpha_composite(Image.fromarray(np.dstack([cor.clip(0, 255), a]).astype("uint8"), "RGBA"), (ax - S // 2, ay - S // 2))
        img.alpha_composite(_dino_assustado(img.size, ex, ey, R, x=300))
        d = ImageDraw.Draw(img)
        fl = ImageFont.truetype(str(FONTE), 54)                    # rótulos
        for txt, x, y in (("10 KM", ax + 150, ay - 60), ("20 KM/S", ax + 150, ay + 130)):
            d.text((x, y), txt, font=fl, fill=(255, 196, 40), stroke_width=4, stroke_fill=(0, 0, 0))
    elif tipo == "buraco_negro":
        _buraco_negro_thumb(img, W, H)
    elif tipo == "pulo":
        t = terra(380)
        cy = int(H * 0.64)
        for k, rr in enumerate((470, 560, 650)):                 # ondas de impacto
            d.ellipse((W / 2 - rr, cy - rr, W / 2 + rr, cy + rr), outline=(255, 196, 40, 230 - k * 60), width=14 - k * 3)
        img.alpha_composite(t, (W // 2 - t.width // 2, cy - t.height // 2))
        from .voce import _pessoa                                 # bonecos pulando em cima do planeta
        for k, x in enumerate(range(330, 760, 70)):
            _pessoa(d, x, cy - 400 - (k % 2) * 40, 120, (245, 245, 250), 0.0, "parado", fundo=(10, 16, 40))
    return img.convert("RGB")


def gerar(r: dict, pasta: Path) -> tuple[Path, Path]:
    pasta.mkdir(parents=True, exist_ok=True)
    cena = arte(r)
    W, H = cena.size
    linhas = [l.strip().upper() for l in (r.get("thumb_texto") or r.get("titulo", "E se...?")).split("|") if l.strip()][:3]
    selo = "E SE FOSSE REAL?"

    # ---------------- vertical (9:16): texto em cima, desenho no meio, selo embaixo
    v = cena.convert("RGBA")
    som = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(som)
    for k in range(60):                                       # escurece o topo para o texto saltar
        ds.rectangle((0, int(H * 0.36 * k / 60), W, int(H * 0.36 * (k + 1) / 60)), fill=(4, 8, 24, int(215 * (1 - k / 60))))
    v.alpha_composite(som)
    d = ImageDraw.Draw(v)
    y = H * 0.07
    for n, txt in enumerate(linhas):
        f = _fonte(txt, W * 0.9, 170)
        _escreve(d, (W - f.getlength(txt)) / 2, y, txt, f, AMARELO if n == len(linhas) - 1 and len(linhas) > 1 else BRANCO)
        y += f.size * 1.12
    fs = ImageFont.truetype(str(FONTE), 46)
    lw = fs.getlength(selo)
    d.rounded_rectangle(((W - lw) / 2 - 34, H * 0.9, (W + lw) / 2 + 34, H * 0.9 + 78), radius=39, fill=(8, 14, 40))
    d.text(((W - lw) / 2, H * 0.9 + 8), selo, font=fs, fill=AZUL)
    vert = pasta / "thumb_vertical.jpg"
    v.convert("RGB").save(vert, quality=92)

    # ---------------- horizontal (16:9): texto à esquerda, desenho à direita
    if r.get("thumb_arte") in ARTE_HORIZONTAL:                # desenho refeito em 16:9, sem cortar o vertical
        hz = arte(r, 1280, 720).convert("RGBA")
        som = Image.new("RGBA", hz.size, (0, 0, 0, 0))
        ds = ImageDraw.Draw(som)
        for k in range(60):                                   # escurece a esquerda para o texto saltar
            ds.rectangle((int(700 * k / 60), 0, int(700 * (k + 1) / 60), 720), fill=(4, 8, 24, int(200 * (1 - k / 60))))
        hz.alpha_composite(som)
        hz = hz.convert("RGB")
    else:
        hz = _ceu(1280, 720).convert("RGBA")                   # céu limpo; o desenho centrado no painel da direita
        q = quadro_do_video(r)
        qw, qh = q.size
        fx, fy = r.get("thumb_centro", [0.5, 0.47])
        pw, ph = 600, 720
        cw = qw * 0.98
        ch = cw * ph / pw
        x0 = min(max(0, fx * qw - cw / 2), qw - cw)
        y0 = min(max(0, fy * qh - ch / 2), qh - ch)
        painel = q.resize((pw, ph), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch)).convert("RGBA")
        masc = Image.new("L", (pw, ph), 255)
        dm = ImageDraw.Draw(masc)
        for k in range(140):                                  # borda esquerda esfumada, sem emenda
            dm.line((k, 0, k, ph), fill=int(255 * k / 140))
        painel.putalpha(masc)
        hz.alpha_composite(painel, (1280 - pw, 0))
        hz = hz.convert("RGB")
    dz = ImageDraw.Draw(hz)
    y = 150
    for n, txt in enumerate(linhas):
        f = _fonte(txt, 720, 120)
        _escreve(dz, 50, y, txt, f, AMARELO if n == len(linhas) - 1 and len(linhas) > 1 else BRANCO)
        y += f.size * 1.14
    fs = ImageFont.truetype(str(FONTE), 34)
    dz.rounded_rectangle((50, 600, 90 + fs.getlength(selo), 656), radius=28, fill=(8, 14, 40))
    dz.text((70, 606), selo, font=fs, fill=AZUL)
    hor = pasta / "thumb_horizontal.jpg"
    hz.save(hor, quality=92)
    return vert, hor


def _buraco_negro_thumb(img: Image.Image, W: int, H: int) -> None:
    """Buraco negro gigante sugando tudo: riscos de luz entrando, o astronauta apavorado esticando feito macarrão
    a caminho da borda, e a seta vermelha apontando para ele."""
    import math
    import random
    from .buraco_negro import desenhar
    from .voce import _astro_mini
    deitado = W > H
    if deitado:
        R, cx, cy = int(H * 0.18), W * 0.75, H * 0.62
        ang, dist, tam, est = math.radians(-60), 1.5, 0.6, 1.3
    else:
        R, cx, cy = int(W * 0.24), W * 0.5, H * 0.66
        ang, dist, tam, est = math.radians(-58), 1.5, 0.62, 1.35
    riscos = Image.new("RGBA", (W, H), (0, 0, 0, 0))             # luz e poeira caindo em espiral para dentro
    dr, rnd = ImageDraw.Draw(riscos), random.Random(8)
    for _ in range(90):
        a = rnd.random() * 2 * math.pi
        r1 = R * (1.4 + rnd.random() * 3.2)
        r2 = r1 * (0.55 + rnd.random() * 0.2)
        a2 = a + 0.35
        cor = rnd.choice([(255, 170, 70), (255, 220, 150), (120, 200, 255)])
        dr.line((cx + math.cos(a) * r1, cy + math.sin(a) * r1 * 0.8, cx + math.cos(a2) * r2, cy + math.sin(a2) * r2 * 0.8),
                fill=cor + (rnd.randint(60, 150),), width=rnd.choice([3, 4, 6]))
    img.alpha_composite(riscos.filter(ImageFilter.GaussianBlur(1.5)))
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))                  # brilho quente em volta
    ImageDraw.Draw(gl).ellipse((cx - R * 3.2, cy - R * 1.6, cx + R * 3.2, cy + R * 1.6), fill=(255, 130, 40, 120))
    img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(R * 0.6)))
    base = img.convert("RGB")
    desenhar(base, cx, cy, R, 1.3, 1.35)
    img.paste(base.convert("RGBA"))
    # o astronauta: vem do alto, esticando na direção do buraco, com rastro brilhante
    dist *= R
    px, py = cx + math.cos(ang) * dist, cy + math.sin(ang) * dist
    tam *= R
    rastro = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rastro)
    for k in range(14):
        f = k / 14
        x = px + (cx - px) * f * 0.75
        y = py + (cy - py) * f * 0.75
        rr = tam * 0.22 * (1 - f * 0.7)
        rd.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(255, 200, 120, int(120 * (1 - f))))
    img.alpha_composite(rastro.filter(ImageFilter.GaussianBlur(10)))
    _astro_mini(img, px, py, ang, tam, est, t=0.9, medo=True)
    # seta vermelha com contorno branco, vindo de baixo à esquerda até o corpo de quem cai
    meio = tam * 1.75 * est * 0.45
    bcx, bcy = px + math.cos(ang) * meio, py + math.sin(ang) * meio
    bx, by = bcx - tam * 0.75, bcy + tam * 0.15
    ax, ay = bx - tam * 1.7, by + tam * 1.0
    sd = ImageDraw.Draw(img)
    ux, uy = bx - ax, by - ay
    n = math.hypot(ux, uy)
    ux, uy = ux / n, uy / n
    lw = tam * 0.16
    for cor, extra in (((255, 255, 255), lw * 0.5), ((228, 30, 44), 0)):
        sd.line((ax, ay, bx - ux * tam * 0.4, by - uy * tam * 0.4), fill=cor, width=int(lw + extra * 2))
        cab = tam * 0.5 + extra * 1.6
        sd.polygon([(bx + ux * extra, by + uy * extra), (bx - ux * cab - uy * cab * 0.75, by - uy * cab + ux * cab * 0.75),
                    (bx - ux * cab + uy * cab * 0.75, by - uy * cab - ux * cab * 0.75)], fill=cor)


# ---------------- Terra "de verdade" (mesmo desenho do banner do canal), para as thumbs de planeta
import numpy as np


def _ruido(w, h, cel, seed):
    r = np.random.RandomState(seed)
    out, amp, tot = np.zeros((h, w), "float32"), 1.0, 0.0
    for _ in range(5):
        g = r.rand(int(h / cel) + 3, int(w / cel) + 3).astype("float32")
        img = Image.fromarray((g * 255).astype("uint8")).resize((w + int(cel * 2), h + int(cel * 2)), Image.BICUBIC)
        out += np.asarray(img, "float32")[:h, :w] / 255 * amp
        tot += amp
        amp *= 0.5
        cel = max(cel / 2, 2)
    return out / tot


def terra(R: int, seed: int = 21) -> Image.Image:
    """Terra sombreada com continentes, gelo, nuvens, luzes de cidade e atmosfera. Devolve RGBA (2.6R x 2.6R)."""
    S = int(R * 2.6)
    c = S / 2
    X = (np.arange(S)[None, :] - c) / R
    Y = (np.arange(S)[:, None] - c) / R
    r2 = X ** 2 + Y ** 2
    Z = np.sqrt(np.clip(1 - r2, 0, 1))
    with np.errstate(invalid="ignore", divide="ignore"):
        u = np.nan_to_num(np.arcsin(np.clip(X / np.maximum(np.sqrt(np.clip(1 - Y ** 2, 0, 1)), 1e-3), -1, 1)))
        v = np.nan_to_num(np.arcsin(np.clip(Y, -1, 1)))
    TW = 2048 if R > 450 else 1024
    tex, tex2, tex3 = _ruido(TW, TW // 2, TW * 0.073, seed), _ruido(TW, TW // 2, TW * 0.034, 8), _ruido(TW, TW // 2, TW * 0.02, 30)
    iu = ((u / np.pi + 0.5) * (TW - 1) * 0.98).astype(int).clip(0, TW - 1)
    iv = ((v / np.pi + 0.5) * (TW // 2 - 1)).astype(int).clip(0, TW // 2 - 1)
    ct = np.clip((tex[iv, iu] - 0.565) * 60, 0, 1)[..., None]
    from .globo import tem_mapa, _mapa
    if tem_mapa():                                         # continentes de verdade, com o Brasil de frente
        lo = ((u - 0.9 + np.pi) % (2 * np.pi)) / (2 * np.pi) * 2047
        la = ((np.pi / 2 + v) / np.pi * 1023).clip(0, 1023)
        ct = _mapa()[la.astype(int), lo.astype(int)][..., None]
    oceano = np.stack([18 + 20 * Z, 85 + 40 * Z, 190 + 40 * Z], -1)
    mist = np.clip((tex2[iv, iu] - 0.45) * 3, 0, 1)[..., None]
    solo = np.array([62, 160, 80]) * (1 - mist) + np.array([200, 175, 110]) * mist * 0.85
    cor = solo * ct + oceano * (1 - ct)
    pc = np.clip((np.abs(Y) + (tex2[iv, iu] - 0.5) * 0.25 - 0.88) * 40, 0, 1)[..., None]
    cor = cor * (1 - pc) + np.array([235, 242, 250]) * pc
    nuv = np.clip((tex3[iv, iu] - 0.56) * 2.6, 0, 0.7)[..., None]
    cor = cor * (1 - nuv) + 255 * nuv
    L = np.array([-0.6, -0.45, 0.66])
    L /= np.linalg.norm(L)
    luz = np.clip(X * L[0] + Y * L[1] + Z * L[2], 0, 1)
    cor = cor * (0.07 + 1.1 * luz ** 1.1)[..., None]
    noite = np.clip(0.18 - luz, 0, 0.18) / 0.18
    cid = (np.random.RandomState(4).rand(S, S) > 0.985) & (ct[..., 0] > 0.5)
    cor[cid] += np.array([255, 200, 110]) * noite[cid][:, None] * 0.9
    cor += 255 * (luz ** 40 * (ct[..., 0] < 0.5))[..., None] * 0.5
    alfa = np.clip((1 - np.sqrt(r2)) * R * 1.5, 0, 1) * 255
    pl = Image.fromarray(np.dstack([cor.clip(0, 255), alfa]).astype("uint8"), "RGBA")
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    g = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(g).ellipse((c - R * 1.12, c - R * 1.12, c + R * 1.12, c + R * 1.12), fill=(80, 180, 255, 150))
    out.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.12)))
    out.alpha_composite(pl)
    return out


def lua(R: int, apagada: float = 0.0) -> Image.Image:
    S = int(R * 2 + 4)
    X = (np.arange(S)[None, :] - S / 2) / R
    Y = (np.arange(S)[:, None] - S / 2) / R
    m2 = X ** 2 + Y ** 2
    Z = np.sqrt(np.clip(1 - m2, 0, 1))
    L = np.array([-0.6, -0.45, 0.66])
    L /= np.linalg.norm(L)
    sh = 0.15 + 0.95 * np.clip(X * L[0] + Y * L[1] + Z * L[2], 0, 1)
    base = 200 + 40 * (_ruido(S, S, max(4, R // 10), 2) - 0.5)
    for ux, uy, s in [(-0.3, -0.2, 0.25), (0.3, 0.25, 0.18), (0.05, 0.45, 0.12), (-0.4, 0.35, 0.1)]:
        base = np.where((X - ux) ** 2 + (Y - uy) ** 2 < s * s, base - 35, base)
    cor = np.stack([base, base, base + 10], -1) * sh[..., None]
    a = np.clip((1 - np.sqrt(m2)) * R * 1.5, 0, 1) * 255 * (1 - apagada)
    return Image.fromarray(np.dstack([cor.clip(0, 255), a]).astype("uint8"), "RGBA")


def _lua_desfazendo(R: int, seed: int = 5) -> Image.Image:
    """A Lua grande se desfazendo em pedaços para a direita. Devolve RGBA (R*5 x R*3), com a Lua centrada em (1.5R, 1.5R)."""
    import random
    S = R * 2 + 4
    m = lua(R).copy()
    X = (np.arange(S)[None, :] - S / 2) / R
    Y = (np.arange(S)[:, None] - S / 2) / R
    corte = 0.05 + 0.35 * Y ** 2 + 0.28 * (_ruido(S, S, max(4, R // 6), seed) - 0.5)   # borda irregular do corte
    a = np.asarray(m, "float32")[..., 3] * np.clip((corte - X) * R / 6, 0, 1)
    px = np.asarray(m).copy().astype("float32")
    borda = np.clip(1 - (corte - X) / 0.07, 0, 1)[..., None] * (a > 0)[..., None]       # a borda quebrada brilha quente
    px[..., :3] = px[..., :3] * (1 - borda * 0.75) + np.array([255, 170, 70]) * borda * 0.75
    px[..., 3] = a
    px = px.clip(0, 255).astype("uint8")
    lua_cortada = Image.fromarray(px, "RGBA")

    out = Image.new("RGBA", (R * 5, R * 3), (0, 0, 0, 0))
    cx, cy = int(R * 1.5), int(R * 1.5)
    brilho = Image.new("RGBA", out.size, (0, 0, 0, 0))                                  # halo frio da Lua
    ImageDraw.Draw(brilho).ellipse((cx - R * 1.18, cy - R * 1.18, cx + R * 1.18, cy + R * 1.18), fill=(190, 215, 255, 110))
    out.alpha_composite(brilho.filter(ImageFilter.GaussianBlur(R * 0.14)))
    d = ImageDraw.Draw(out)
    rnd = random.Random(seed)
    for _ in range(170):                                       # pedaços e poeira voando, menores quanto mais longe
        ang = rnd.uniform(-0.95, 0.95)
        y0 = rnd.uniform(-0.85, 0.85)
        x0 = 0.05 + 0.35 * y0 ** 2
        dist = rnd.random() ** 1.6 * 3.1
        x = cx + (x0 + dist * np.cos(ang * 0.45)) * R
        y = cy + (y0 + dist * np.sin(ang * 0.45) * 0.9) * R
        tam = max(2.0, R * 0.13 * (1 - dist / 3.3) * rnd.uniform(0.25, 1.0))
        tom = int(rnd.uniform(130, 210) * (1 - 0.35 * dist / 3.1))
        alfa = int(255 * (1 - 0.6 * dist / 3.1))
        pts = [(x + tam * np.cos(t) * rnd.uniform(0.6, 1.1), y + tam * np.sin(t) * rnd.uniform(0.6, 1.1))
               for t in np.linspace(0, 2 * np.pi, rnd.randint(5, 7), endpoint=False)]
        d.polygon(pts, fill=(tom, tom, tom + 8, alfa))
        if tam > R * 0.05:                                    # lado iluminado do pedaço
            d.polygon([(px_ - 0.25 * tam, py_ - 0.25 * tam) for px_, py_ in pts[:3]] + [pts[0]],
                      fill=(min(255, tom + 45),) * 3 + (alfa,))
    out.alpha_composite(lua_cortada, (cx - S // 2, cy - S // 2))
    return out


def _lua_some(img: Image.Image, W: int, H: int) -> None:
    """Thumb da Lua sumindo: a Lua enorme se desfazendo, com a Terra pequena embaixo para dar escala."""
    horizontal = W > H
    if horizontal:
        R, (lx, ly) = 235, (1010, int(H * 0.46))
        Rt, (tx, ty) = 210, (760, 820)
    else:
        R, (lx, ly) = 360, (int(W * 0.44), int(H * 0.56))
        Rt, (tx, ty) = 520, (int(W * 0.5), int(H * 1.17))
    t = terra(Rt)
    img.alpha_composite(t, (tx - t.width // 2, ty - t.height // 2))
    m = _lua_desfazendo(R)
    img.alpha_composite(m, (lx - int(R * 1.5), ly - int(R * 1.5)))


# ---------------- "E se você saísse da nave sem roupa espacial?": pessoa de roupa comum saindo da nave
def _pessoa_sem_traje(alt: int) -> Image.Image:
    """Pessoa de camiseta e jeans, braços e pernas abertos, boca aberta soltando vapor. RGBA, desenhada em 2x e reduzida."""
    k = 2
    A = alt * k
    S = int(A * 1.25)
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = S / 2, S / 2 + A * 0.06
    pele, cabelo = (240, 196, 160), (70, 44, 28)
    camisa, camisa2 = (240, 84, 60), (200, 58, 44)
    jeans, jeans2 = (52, 96, 190), (38, 72, 150)
    tenis = (245, 245, 250)

    def membro(x0, y0, x1, y1, w, cor):
        d.line((x0, y0, x1, y1), fill=cor, width=int(w))
        for x, y in ((x0, y0), (x1, y1)):
            d.ellipse((x - w / 2, y - w / 2, x + w / 2, y + w / 2), fill=cor)

    ombro, quadril = cy - A * 0.14, cy + A * 0.18
    # pernas abertas, joelho dobrado
    membro(cx - A * 0.07, quadril, cx - A * 0.2, quadril + A * 0.2, A * 0.11, jeans2)
    membro(cx - A * 0.2, quadril + A * 0.2, cx - A * 0.3, quadril + A * 0.38, A * 0.1, jeans2)
    membro(cx + A * 0.07, quadril, cx + A * 0.22, quadril + A * 0.17, A * 0.11, jeans)
    membro(cx + A * 0.22, quadril + A * 0.17, cx + A * 0.36, quadril + A * 0.3, A * 0.1, jeans)
    for x, y, ang in ((cx - A * 0.3, quadril + A * 0.38, 0), (cx + A * 0.36, quadril + A * 0.3, 0)):
        d.rounded_rectangle((x - A * 0.07, y - A * 0.04, x + A * 0.07, y + A * 0.05), radius=int(A * 0.04), fill=tenis)
    # braços pra cima, se debatendo
    membro(cx - A * 0.13, ombro + A * 0.02, cx - A * 0.3, ombro - A * 0.12, A * 0.1, camisa2)
    membro(cx - A * 0.3, ombro - A * 0.12, cx - A * 0.36, ombro - A * 0.32, A * 0.085, pele)
    membro(cx + A * 0.13, ombro + A * 0.02, cx + A * 0.32, ombro - A * 0.06, A * 0.1, camisa)
    membro(cx + A * 0.32, ombro - A * 0.06, cx + A * 0.42, ombro - A * 0.25, A * 0.085, pele)
    for x, y in ((cx - A * 0.36, ombro - A * 0.32), (cx + A * 0.42, ombro - A * 0.25)):   # mãos abertas
        d.ellipse((x - A * 0.05, y - A * 0.05, x + A * 0.05, y + A * 0.05), fill=pele)
    # tronco (camiseta) e cinto
    d.rounded_rectangle((cx - A * 0.15, ombro - A * 0.04, cx + A * 0.15, quadril + A * 0.03), radius=int(A * 0.08), fill=camisa)
    d.rounded_rectangle((cx - A * 0.15, quadril - A * 0.02, cx + A * 0.15, quadril + A * 0.06), radius=int(A * 0.03), fill=jeans)
    d.polygon([(cx - A * 0.05, ombro - A * 0.04), (cx + A * 0.05, ombro - A * 0.04), (cx, ombro + A * 0.04)], fill=pele)
    # cabeça
    hr = A * 0.13
    hx, hy = cx, ombro - A * 0.16
    d.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=pele)
    d.pieslice((hx - hr * 1.04, hy - hr * 1.1, hx + hr * 1.04, hy + hr * 0.55), 180, 360, fill=cabelo)
    for s in (-1, 1):                                                       # olhos arregalados
        ex, ey = hx + s * hr * 0.4, hy + hr * 0.05
        d.ellipse((ex - hr * 0.24, ey - hr * 0.26, ex + hr * 0.24, ey + hr * 0.26), fill=(255, 255, 255))
        d.ellipse((ex - hr * 0.1, ey - hr * 0.08, ex + hr * 0.1, ey + hr * 0.12), fill=(20, 20, 30))
        d.line((ex - hr * 0.25, ey - hr * 0.42 - s * hr * 0.04, ex + hr * 0.25, ey - hr * 0.42 + s * hr * 0.04),
               fill=cabelo, width=int(hr * 0.1))
    d.ellipse((hx - hr * 0.2, hy + hr * 0.42, hx + hr * 0.2, hy + hr * 0.82), fill=(110, 32, 36))   # boca em "O"
    # vapor saindo da boca (a água da boca e o ar escapando)
    for j, (dx, dy, rr) in enumerate(((0.28, 0.75, 0.13), (0.5, 0.62, 0.17), (0.76, 0.5, 0.21), (1.02, 0.4, 0.15))):
        x, y, r = hx + hr * dx * 1.6, hy + hr * dy, hr * rr * 1.3
        d.ellipse((x - r, y - r, x + r, y + r), fill=(225, 240, 255, 200 - j * 30))
    return im.resize((S // k, S // k), Image.LANCZOS)


def _nave(w: int) -> Image.Image:
    """Lateral de uma nave (casco branco), com a escotilha aberta e luz quente saindo. RGBA."""
    k = 2
    W2, H2 = w * k, int(w * 1.5) * k
    im = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, W2, H2), radius=int(W2 * 0.18), fill=(214, 220, 232))
    d.rounded_rectangle((W2 * 0.06, 0, W2, H2), radius=int(W2 * 0.18), fill=(236, 240, 247))
    for y in (0.18, 0.82):                                                 # faixas e rebites
        d.rectangle((0, H2 * y - 10 * k, W2, H2 * y + 10 * k), fill=(180, 188, 206))
    d.rectangle((W2 * 0.3, H2 * 0.1, W2 * 0.95, H2 * 0.14), fill=(232, 60, 60))
    porta = (W2 * 0.3, H2 * 0.28, W2 * 0.95, H2 * 0.72)
    d.rounded_rectangle((porta[0] - 14 * k, porta[1] - 14 * k, porta[2] + 14 * k, porta[3] + 14 * k), radius=int(W2 * 0.12),
                        fill=(120, 128, 150))
    d.rounded_rectangle(porta, radius=int(W2 * 0.1), fill=(255, 214, 120))
    d.rounded_rectangle((porta[0] + 12 * k, porta[1] + 12 * k, porta[2] - 12 * k, porta[3] - 12 * k), radius=int(W2 * 0.08),
                        fill=(255, 238, 190))
    return im.resize((W2 // k, H2 // k), Image.LANCZOS)


def _capacete(r: int) -> Image.Image:
    """Capacete de astronauta vazio, flutuando para longe. RGBA."""
    k = 2
    R = r * k
    S = int(R * 2.4)
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = S / 2
    d.ellipse((c - R, c - R, c + R, c + R), fill=(240, 243, 250))
    d.rounded_rectangle((c - R * 0.75, c - R * 0.5, c + R * 0.75, c + R * 0.5), radius=int(R * 0.45), fill=(255, 190, 60))
    d.rounded_rectangle((c - R * 0.62, c - R * 0.38, c + R * 0.62, c + R * 0.38), radius=int(R * 0.35), fill=(40, 60, 120))
    d.ellipse((c - R * 0.48, c - R * 0.3, c - R * 0.12, c - R * 0.08), fill=(150, 200, 255))
    d.rounded_rectangle((c - R * 0.7, c + R * 0.78, c + R * 0.7, c + R * 1.05), radius=int(R * 0.12), fill=(180, 188, 206))
    return im.resize((S // k, S // k), Image.LANCZOS)


def _cronometro(d, cx, cy, r, txt):
    """Selo vermelho de cronômetro com o número de segundos."""
    d.rectangle((cx - r * 0.14, cy - r * 1.28, cx + r * 0.14, cy - r * 1.02), fill=(255, 255, 255))
    d.rounded_rectangle((cx - r * 0.32, cy - r * 1.4, cx + r * 0.32, cy - r * 1.22), radius=int(r * 0.08), fill=(255, 255, 255))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(225, 30, 40), outline=(255, 255, 255), width=max(6, int(r * 0.09)))
    f = _fonte(txt, r * 1.5, int(r * 0.9))
    d.text((cx - f.getlength(txt) / 2, cy - f.size * 0.62), txt, font=f, fill=(255, 255, 255))


def _sem_traje(img: Image.Image, W: int, H: int) -> None:
    d = ImageDraw.Draw(img)
    if W > H:                                    # 16:9: texto à esquerda, cena à direita
        t = terra(250)
        img.alpha_composite(t, (1040 - t.width // 2, 930 - t.height // 2))
        nv = _nave(170)
        img.alpha_composite(nv, (1280 - nv.width + 40, 40))
        cp = _capacete(58).rotate(-25, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(cp, (700, 470))
        ps = _pessoa_sem_traje(430).rotate(18, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(ps, (990 - ps.width // 2, 330 - ps.height // 2))
        _cronometro(d, 1190, 620, 62, "15s")
    else:                                        # 9:16: texto em cima, cena no meio, Terra embaixo
        t = terra(520)
        img.alpha_composite(t, (int(W * 0.5) - t.width // 2, int(H * 1.17) - t.height // 2))
        nv = _nave(300)
        img.alpha_composite(nv, (-110, int(H * 0.41)))
        cp = _capacete(80).rotate(-25, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(cp, (10, int(H * 0.285)))
        ps = _pessoa_sem_traje(720).rotate(14, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(ps, (int(W * 0.56) - ps.width // 2, int(H * 0.56) - ps.height // 2))
        _cronometro(d, int(W * 0.2), int(H * 0.76), 110, "15s")


def _dino_assustado(tam, ex, ey, R, x):
    """Um T-rex de desenho em pé na borda da Terra, olhando para cima, de boca aberta."""
    import math
    L = Image.new("RGBA", (700, 700), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    V, VE, CL, PR = (88, 170, 72), (58, 125, 52), (190, 225, 150), (20, 30, 18)
    o = dict(outline=PR, width=8)
    d.polygon([(250, 470), (60, 560), (40, 590), (90, 585), (270, 520)], fill=V, **o)            # cauda
    d.rounded_rectangle((285, 520, 335, 640), radius=20, fill=VE, **o)                         # perna de trás
    d.ellipse((230, 360, 440, 560), fill=V, **o)                                               # corpo
    d.rounded_rectangle((370, 520, 420, 640), radius=20, fill=V, **o)                          # perna da frente
    d.ellipse((280, 420, 400, 540), fill=CL)                                                   # barriga
    d.polygon([(360, 380), (420, 220), (480, 230), (440, 400)], fill=V, **o)                   # pescoço
    d.polygon([(400, 120), (560, 90), (600, 140), (560, 175), (470, 190), (410, 220)], fill=V, **o)  # cabeça
    d.polygon([(420, 222), (470, 196), (560, 184), (575, 250), (470, 262), (430, 250)], fill=VE, **o)  # mandíbula aberta
    d.polygon([(470, 192), (560, 180), (560, 190), (470, 202)], fill=(120, 20, 20))           # boca
    for k in range(4):                                                                         # dentes
        xx = 485 + k * 20
        d.polygon([(xx, 182), (xx + 8, 196), (xx + 14, 181)], fill=(250, 250, 245))
    d.ellipse((470, 92, 530, 152), fill=(255, 255, 255), **o)                                  # olho arregalado
    d.ellipse((498, 98, 524, 124), fill=PR)
    d.line((462, 80, 520, 70), fill=PR, width=8)                                               # sobrancelha
    d.line((440, 300, 480, 330), fill=PR, width=10)                                            # bracinho
    d.line((480, 330, 500, 315), fill=PR, width=8)
    for k in range(3):                                                                         # tremedeira
        d.arc((560 + k * 22, 30 + k * 10, 640 + k * 22, 110 + k * 10), 300, 30, fill=(255, 255, 255), width=6)
    T = 560
    L = L.resize((T, T), Image.LANCZOS)
    pe = 640 / 700 * T                                                                         # altura dos pés na camada
    dy = math.sqrt(max(R * R - (x - ex) ** 2, 0))
    ang = math.degrees(math.atan2(x - ex, dy)) * 0.6                                           # inclina um pouco com a curva
    G = Image.new("RGBA", (T * 2, T * 2), (0, 0, 0, 0))
    G.alpha_composite(L, (T // 2, int(T - pe)))                                                # pés no centro da camada grande
    G = G.rotate(-ang, resample=Image.BICUBIC, center=(T, T))
    out = Image.new("RGBA", tam, (0, 0, 0, 0))
    out.alpha_composite(G, (int(x - T), int(ey - dy - T + 18)))
    return out
