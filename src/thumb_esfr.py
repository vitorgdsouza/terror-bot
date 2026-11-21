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


ARTE_HORIZONTAL = {"lua_some"}                               # artes que têm composição própria em 16:9


def arte(r: dict, W: int = 1080, H: int = 1920) -> Image.Image:
    """A imagem principal da thumb: um desenho feito para ela (thumb_arte) ou um quadro do vídeo com zoom."""
    tipo = r.get("thumb_arte", "")
    if not tipo:
        img = quadro_do_video(r)
        z = float(r.get("thumb_zoom", 1.0))
        if z > 1:
            fx, fy = r.get("thumb_centro", [0.5, 0.55])
            cw, ch = W / z, H / z
            x0, y0 = min(max(0, fx * W - cw / 2), W - cw), min(max(0, fy * H - ch / 2), H - ch)
            img = img.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
        return img
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
        hz = Image.new("RGB", (1280, 720))
        fundo = cena.resize((1280, int(1280 * H / W))).crop((0, 600, 1280, 1320)).filter(ImageFilter.GaussianBlur(28))
        hz.paste(ImageEnhance.Brightness(fundo).enhance(0.4), (0, 0))
        hz.paste(cena.resize((470, 836)).crop((0, 58, 470, 778)), (810, 0))
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
    tex, tex2, tex3 = _ruido(1024, 512, 75, seed), _ruido(1024, 512, 35, 8), _ruido(1024, 512, 20, 30)
    iu = ((u / np.pi + 0.5) * 1023 * 0.98).astype(int).clip(0, 1023)
    iv = ((v / np.pi + 0.5) * 511).astype(int).clip(0, 511)
    ct = np.clip((tex[iv, iu] - 0.565) * 60, 0, 1)[..., None]
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
