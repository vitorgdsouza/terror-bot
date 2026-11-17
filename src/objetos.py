"""Objetos de pista da história (mesmo traço do boneco e do gato), desenhados pelo código.

Na cena: "objeto": {"tipo": ..., "posicao": "esquerda|centro|direita", "tamanho": "medio|perto"}
(ou uma lista com até 2). "perto" = close do objeto no chão, com a luz da lanterna em cima.

Tipos:
  coleira     coleira vermelha do gato com guizo dourado e plaquinha
  tigela      tigela de ração virada, ração espalhada
  pelo        tufo de pelo laranja no chão
  novelo      novelo de lã desenrolado, o fio indo para fora da cena
  ratinho     o ratinho de brinquedo do gato
  pegadas     trilha de patinhas de poeira indo para o fundo do cômodo
  arranhoes   arranhões fundos na porta ou na parede
  marcas_mao  marcas de mãos compridas e escuras na parede/janela (o Abismo esteve aqui)
  arma        a pistola de serviço (de perfil)
  caixa_arma  maleta da arma aberta, com o recorte da pistola na espuma... vazio
"""
import math

from PIL import Image, ImageDraw, ImageFilter

TRACO = (24, 22, 30, 255)
TIPOS = ["coleira", "tigela", "pelo", "novelo", "ratinho", "pegadas", "arranhoes", "marcas_mao",
         "foto", "bilhete", "jornal", "desenho"]
ESCALA = {"coleira": 0.26, "ratinho": 0.8, "pelo": 0.8, "foto": 0.9, "bilhete": 0.8, "jornal": 1.0, "desenho": 1.0}
NO_CHAO = {"coleira", "tigela", "pelo", "novelo", "ratinho"}
S = 2


def _tela(larg, alt):
    img = Image.new("RGBA", (int(larg * S), int(alt * S)), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def _final(img):
    return img.resize((img.width // S, img.height // S), Image.LANCZOS)


def _coleira(u, t):
    img, d = _tela(u * 1.3, u * 0.8)
    o = max(2, int(u * S * 0.02))
    cx, cy, rx, ry = img.width * 0.45, img.height * 0.55, u * S * 0.42, u * S * 0.2
    # anel achatado (coleira caída no chão)
    d.ellipse((cx - rx - o, cy - ry - o, cx + rx + o, cy + ry + o), fill=TRACO)
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(196, 44, 52))
    d.ellipse((cx - rx * 0.78, cy - ry * 0.6, cx + rx * 0.78, cy + ry * 0.6), fill=TRACO)
    d.ellipse((cx - rx * 0.74, cy - ry * 0.54, cx + rx * 0.74, cy + ry * 0.54), fill=(0, 0, 0, 0))
    # guizo dourado e plaquinha
    bx, by, r = cx + rx * 0.85, cy + ry * 0.55, u * S * 0.12
    d.ellipse((bx - r - o, by - r - o, bx + r + o, by + r + o), fill=TRACO)
    d.ellipse((bx - r, by - r, bx + r, by + r), fill=(232, 186, 64))
    d.line((bx - r * 0.7, by + r * 0.15, bx + r * 0.7, by + r * 0.15), fill=TRACO, width=o)
    d.ellipse((bx - r * 0.12, by + r * 0.3, bx + r * 0.12, by + r * 0.55), fill=TRACO)
    d.ellipse((bx - r * 0.55, by - r * 0.6, bx - r * 0.15, by - r * 0.25), fill=(255, 240, 190))
    px, py = cx - rx * 0.5, cy + ry * 0.95
    d.rounded_rectangle((px - r * 0.8, py - r * 0.5, px + r * 0.8, py + r * 0.7), radius=int(r * 0.3), fill=(200, 205, 214), outline=TRACO, width=o)
    return _final(img), (bx / S, by / S)


def _tigela(u, t):
    img, d = _tela(u * 1.5, u * 0.8)
    o = max(2, int(u * S * 0.02))
    U = u * S
    cx, cy = img.width * 0.45, img.height * 0.55
    # tigela tombada de lado
    pts = [(cx - U * 0.3, cy - U * 0.22), (cx + U * 0.12, cy - U * 0.3), (cx + U * 0.22, cy + U * 0.18), (cx - U * 0.22, cy + U * 0.22)]
    d.polygon(pts, fill=(70, 120, 196), outline=TRACO)
    d.line(pts + [pts[0]], fill=TRACO, width=o, joint="curve")
    d.ellipse((cx + U * 0.02, cy - U * 0.32, cx + U * 0.34, cy + U * 0.22), fill=TRACO)
    d.ellipse((cx + U * 0.05, cy - U * 0.28, cx + U * 0.31, cy + U * 0.18), fill=(50, 90, 160))
    # ração espalhada
    rnd = [(0.45, 0.1), (0.55, 0.0), (0.62, 0.15), (0.7, 0.05), (0.5, 0.2), (0.78, 0.18), (0.66, -0.05), (0.85, 0.1)]
    for dx, dy in rnd:
        x, y = cx + U * dx, cy + U * dy
        d.ellipse((x - U * 0.035, y - U * 0.025, x + U * 0.035, y + U * 0.025), fill=(150, 96, 52), outline=TRACO, width=max(1, o // 2))
    return _final(img), (cx / S, cy / S)


def _pelo(u, t):
    """Chumaço de pelo laranja e branco no chão: fofo (borda macia), com alguns fios soltos."""
    import random
    from PIL import ImageFilter as _F
    img, d = _tela(u * 1.1, u * 0.6)
    U = u * S
    cx, cy = img.width / 2, img.height * 0.6
    rnd = random.Random(3)
    for i in range(16):                                # bolinhas de pelo que se sobrepõem
        x = cx + rnd.uniform(-0.22, 0.22) * U
        y = cy + rnd.uniform(-0.06, 0.06) * U
        r = rnd.uniform(0.07, 0.12) * U
        cor = (226, 136, 56, 235) if i % 4 else (244, 236, 222, 235)
        d.ellipse((x - r * 1.3, y - r * 0.7, x + r * 1.3, y + r * 0.7), fill=cor)
    img = img.filter(_F.GaussianBlur(U * 0.012))
    d = ImageDraw.Draw(img)
    for i in range(22):                                # fios soltos na borda
        a = rnd.uniform(0, 2 * math.pi) + math.sin(t * 1.3 + i) * 0.04
        x0, y0 = cx + math.cos(a) * U * 0.25, cy + math.sin(a) * U * 0.1
        x1, y1 = cx + math.cos(a) * U * 0.36, cy + math.sin(a) * U * 0.15
        d.line((x0, y0, (x0 + x1) / 2 + rnd.uniform(-1, 1) * U * 0.02, (y0 + y1) / 2, x1, y1),
               fill=(230, 146, 64, 220), width=max(1, int(U * 0.008)))
    return _final(img), (cx / S, cy / S)


def _novelo(u, t):
    img, d = _tela(u * 2.2, u * 0.8)
    o = max(2, int(u * S * 0.02))
    U = u * S
    cx, cy, r = img.width * 0.22, img.height * 0.55, U * 0.24
    # fio indo embora para fora do quadro
    pts = [(cx + r * 0.8, cy + r * 0.5)]
    for i in range(1, 12):
        pts.append((cx + r + i * U * 0.14, cy + r * 0.5 + math.sin(i * 1.3) * U * 0.06))
    d.line(pts, fill=(170, 46, 60), width=max(2, int(U * 0.025)), joint="curve")
    d.ellipse((cx - r - o, cy - r - o, cx + r + o, cy + r + o), fill=TRACO)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(200, 60, 74))
    for k in (-0.5, 0.0, 0.5):
        d.arc((cx - r * 0.9, cy - r * (0.9 - abs(k) * 0.3), cx + r * 0.9, cy + r * 0.9), 200 + k * 40, 340 + k * 40, fill=(150, 36, 50), width=max(1, o))
    return _final(img), (cx / S, cy / S)


def _ratinho(u, t):
    img, d = _tela(u * 1.4, u * 0.7)
    o = max(2, int(u * S * 0.02))
    U = u * S
    cx, cy = img.width * 0.5, img.height * 0.6
    d.line([(cx - U * 0.3, cy + U * 0.05), (cx - U * 0.45, cy - U * 0.05), (cx - U * 0.55, cy + U * 0.08)], fill=(236, 150, 160), width=max(2, int(U * 0.02)), joint="curve")
    d.ellipse((cx - U * 0.32 - o, cy - U * 0.15 - o, cx + U * 0.2 + o, cy + U * 0.15 + o), fill=TRACO)
    d.ellipse((cx - U * 0.32, cy - U * 0.15, cx + U * 0.2, cy + U * 0.15), fill=(150, 150, 160))
    d.polygon([(cx + U * 0.12, cy - U * 0.12), (cx + U * 0.36, cy + U * 0.02), (cx + U * 0.12, cy + U * 0.12)], fill=(150, 150, 160), outline=TRACO)
    d.ellipse((cx + U * 0.0, cy - U * 0.24, cx + U * 0.14, cy - U * 0.08), fill=(236, 150, 160), outline=TRACO, width=o)
    d.ellipse((cx + U * 0.2, cy - U * 0.04, cx + U * 0.25, cy + U * 0.01), fill=TRACO)
    return _final(img), (cx / S, cy / S)


DESENHOS = {"coleira": _coleira, "tigela": _tigela, "pelo": _pelo, "novelo": _novelo, "ratinho": _ratinho}


def _pata(d, x, y, r, cor):
    d.ellipse((x - r, y - r * 0.75, x + r, y + r * 0.75), fill=cor)
    for dx, dy in ((-0.9, -1.1), (-0.3, -1.45), (0.3, -1.45), (0.9, -1.1)):
        d.ellipse((x + dx * r - r * 0.32, y + dy * r - r * 0.3, x + dx * r + r * 0.32, y + dy * r + r * 0.3), fill=cor)


def desenhar(quadro: Image.Image, obj: dict, meta: dict, t: float, dur: float, noite) -> None:
    """Desenha o objeto no quadro (cenário CW x CH), antes dos personagens."""
    cw, ch = quadro.size
    tipo, tam = obj["tipo"], obj.get("tamanho", "medio")
    piso = meta.get("piso", 0.93)
    fundo = meta.get("fundo", [0.5, 0.6, 0.3])
    x = {"esquerda": 0.3, "centro": 0.5, "direita": 0.7}.get(obj.get("posicao"), 0.5)
    if tipo == "pegadas":                                    # trilha de patinhas do primeiro plano até o fundo
        camada = Image.new("RGBA", quadro.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(camada)
        n = 9
        mostra = min(n, int(n * min(1.0, t / max(0.8, dur * 0.5))) + 2)   # vão aparecendo, como se o olhar seguisse
        for i in range(mostra):
            k = i / (n - 1)
            px = x * cw + (fundo[0] * cw - x * cw) * k + (1 if i % 2 else -1) * cw * 0.02 * (1 - k)
            py = ch * (piso - 0.02) + (ch * fundo[1] - ch * (piso - 0.02)) * k
            _pata(d, px, py, cw * 0.022 * (1 - 0.7 * k), (205, 196, 176, int(170 * (1 - 0.4 * k))))
        quadro.alpha_composite(camada)
        return
    if tipo in ("arranhoes", "marcas_mao"):                  # na parede, na porta ou na janela
        reg = meta.get("porta") or meta.get("janela") or [x - 0.1, 0.4, 0.2, 0.25]
        rx, ry, rw, rh = reg
        camada = Image.new("RGBA", quadro.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(camada)
        if tipo == "arranhoes":
            # quatro riscos na parte de baixo da porta (altura de um gato), proporcionais ao tamanho da porta
            larg_p, alt_p = rw * cw, rh * ch
            comp, esp = alt_p * 0.16, max(2, int(larg_p * 0.025))
            for i in range(4):
                x0 = rx * cw + larg_p * (0.3 + i * 0.09)
                y0 = ry * ch + alt_p * 0.66 + i * alt_p * 0.008
                d.line((x0, y0, x0 + larg_p * 0.05, y0 + comp), fill=(168, 146, 120, 185), width=esp)
                d.line((x0 + esp, y0 + esp * 0.6, x0 + larg_p * 0.05 + esp, y0 + comp + esp * 0.6), fill=(26, 22, 28, 190),
                       width=max(1, esp // 2))
        else:
            for j, (hx, hy, ang) in enumerate(((0.3, 0.35, -12), (0.62, 0.52, 9))):
                cx, cy = (rx + rw * hx) * cw, (ry + rh * hy) * ch
                r = cw * 0.03
                mao = Image.new("RGBA", (int(r * 6), int(r * 8)), (0, 0, 0, 0))
                dm = ImageDraw.Draw(mao)
                mx, my = mao.width / 2, mao.height * 0.7
                dm.ellipse((mx - r, my - r * 1.1, mx + r, my + r), fill=(10, 10, 14, 220))
                for k, dx in enumerate((-0.9, -0.35, 0.2, 0.75)):               # dedos compridos demais
                    comp = r * (3.0 + 0.4 * (k in (1, 2)))
                    dm.line((mx + dx * r, my - r * 0.6, mx + dx * r * 1.4, my - r * 0.6 - comp), fill=(10, 10, 14, 220), width=int(r * 0.42))
                dm.line((mx + r, my, mx + r * 2.0, my - r * 1.0), fill=(10, 10, 14, 220), width=int(r * 0.45))
                mao = mao.rotate(ang, resample=Image.BICUBIC, expand=True).filter(ImageFilter.GaussianBlur(1.2))
                camada.alpha_composite(mao, (int(cx - mao.width / 2), int(cy - mao.height / 2)))
        quadro.alpha_composite(camada)
        return
    if obj.get("nas_maos") and tipo in COM_TEXTO:         # o Lucas segura o papel bem perto da câmera, as mãos tremendo
        _nas_maos(quadro, obj, t, noite)
        return
    # objetos no chão
    if tam == "perto":
        u = cw * 0.55 * ESCALA.get(tipo, 1.0)
        cx, cy = cw * 0.5, ch * 0.74
        if meta.get("objeto_perto"):                   # lugar certo do cenário (ex.: na cama, perto do travesseiro)
            px, py = meta["objeto_perto"]
            hz = meta.get("horizonte", 0.45)
            u *= max(0.5, (py - hz) / (0.74 - hz))      # mais ao fundo = menor
            cx, cy = cw * px, ch * py
        # luz da lanterna em cima do objeto
        luz = Image.new("L", quadro.size, 0)
        ImageDraw.Draw(luz).ellipse((cx - cw * 0.42, cy - ch * 0.16, cx + cw * 0.42, cy + ch * 0.16), fill=110)
        luz = luz.filter(ImageFilter.GaussianBlur(cw * 0.06))
        quadro.paste(Image.new("RGBA", quadro.size, (255, 236, 190, 255)), (0, 0), luz.point(lambda v: int(v * 0.38)))
    else:
        u = cw * 0.2 * meta.get("escala", 1.0) * ESCALA.get(tipo, 1.0)
        cx, cy = x * cw, ch * (piso - 0.075)          # um pouco acima da borda (a câmera corta o rodapé)
    img, brilho = DESENHOS[tipo](u, t, obj.get("texto", "")) if tipo in COM_TEXTO else DESENHOS[tipo](u, t)
    img = noite(img, 0.35 if tam != "perto" else 0.28)
    ox, oy = int(cx - img.width * 0.45), int(cy - img.height * 0.55)
    # sombra de contato: o objeto fica apoiado na superfície (não "voando")
    bb = img.getbbox()
    if bb:
        sl, sa = int((bb[2] - bb[0]) * 1.05), max(6, int((bb[3] - bb[1]) * 0.35))
        sombra = Image.new("RGBA", (sl + 40, sa + 40), (0, 0, 0, 0))
        ImageDraw.Draw(sombra).ellipse((20, 20, 20 + sl, 20 + sa), fill=(0, 0, 8, 150))
        sombra = sombra.filter(ImageFilter.GaussianBlur(max(3, sa // 4)))
        quadro.alpha_composite(sombra, (int(ox + (bb[0] + bb[2]) / 2 - sombra.width / 2),
                                        int(oy + bb[3] - sa * 0.55 - 20)))
    quadro.alpha_composite(img, (ox, oy))
    # brilho que chama a atenção para a pista (pisca devagar)
    pulso = 0.5 + 0.5 * math.sin(t * 2.4)
    r = int(u * (0.035 + 0.02 * pulso))
    if tipo in ("coleira", "tigela") and r > 2:
        bx, by = ox + brilho[0], oy + brilho[1]
        g = Image.new("RGBA", (r * 4, r * 4), (0, 0, 0, 0))
        dg = ImageDraw.Draw(g)
        dg.line((r * 2, r * 0.4, r * 2, r * 3.6), fill=(255, 245, 210, int(160 * pulso)), width=max(1, r // 6))
        dg.line((r * 0.4, r * 2, r * 3.6, r * 2), fill=(255, 245, 210, int(160 * pulso)), width=max(1, r // 6))
        quadro.alpha_composite(g.filter(ImageFilter.GaussianBlur(1)), (int(bx - r * 2), int(by - r * 2)))


# ---------------------------------------------------------------- pistas sobre a origem do Abismo
COM_TEXTO = {"bilhete", "jornal", "foto", "desenho"}
PELE, PELE_S, MANGA, MANGA_S = (240, 205, 172), (214, 176, 146), (66, 128, 72), (48, 100, 56)


def _nas_maos(quadro, obj, t, noite):
    """Ponto de vista do Lucas: o papel nas mãos dele, perto da câmera, com a lanterna/abajur iluminando."""
    cw, ch = quadro.size
    escuro = Image.new("RGBA", quadro.size, (0, 0, 8, 120))       # o fundo some um pouco: o olhar vai para o papel
    quadro.alpha_composite(escuro)
    u = cw * 0.78
    img, _ = DESENHOS[obj["tipo"]](u, t, obj.get("texto", ""))
    img = noite(img, 0.2)
    bb = img.getbbox() or (0, 0, img.width, img.height)
    img = img.crop(bb)
    tremor = math.sin(t * 9.0) * 0.6 + math.sin(t * 13.7) * 0.4
    img = img.rotate(-3 + tremor, resample=Image.BICUBIC, expand=True)
    cx, cy = cw * 0.5 + tremor * cw * 0.004, ch * 0.6 + math.sin(t * 1.3) * ch * 0.004
    luz = Image.new("L", quadro.size, 0)
    ImageDraw.Draw(luz).ellipse((cx - cw * 0.6, cy - ch * 0.3, cx + cw * 0.6, cy + ch * 0.3), fill=90)
    luz = luz.filter(ImageFilter.GaussianBlur(cw * 0.08))
    quadro.paste(Image.new("RGBA", quadro.size, (255, 230, 180, 255)), (0, 0), luz.point(lambda v: int(v * 0.4)))
    ox, oy = int(cx - img.width / 2), int(cy - img.height / 2)
    quadro.alpha_composite(img, (ox, oy))
    d = ImageDraw.Draw(quadro)
    o = max(3, int(cw * 0.006))
    for lado in (-1, 1):                                          # mangas verdes vindo de baixo e as mãos segurando as bordas
        mx = cx + lado * img.width * 0.47
        my = cy + img.height * 0.12
        base = (cx + lado * cw * 0.62, ch * 1.05)
        larg = cw * 0.13
        d.line((base, (mx, my + cw * 0.05)), fill=(20, 18, 24), width=int(larg + o * 2))
        d.line((base, (mx, my + cw * 0.05)), fill=MANGA if lado < 0 else MANGA_S, width=int(larg))
        r = cw * 0.06
        d.ellipse((mx - r - o, my - r * 1.1 - o, mx + r + o, my + r * 1.1 + o), fill=(20, 18, 24))
        d.ellipse((mx - r, my - r * 1.1, mx + r, my + r * 1.1), fill=PELE)
        polegar = (mx - lado * r * 0.2, my - r * 0.9)                 # o polegar por cima do papel
        d.rounded_rectangle((polegar[0] - r * 0.28 - o, polegar[1] - r * 0.9 - o, polegar[0] + r * 0.28 + o, polegar[1] + r * 0.3 + o),
                            radius=int(r * 0.3), fill=(20, 18, 24))
        d.rounded_rectangle((polegar[0] - r * 0.28, polegar[1] - r * 0.9, polegar[0] + r * 0.28, polegar[1] + r * 0.3),
                            radius=int(r * 0.25), fill=PELE_S)


def _fonte(px):
    from PIL import ImageFont
    from pathlib import Path
    arq = Path(__file__).resolve().parent.parent / "assets" / "fontes" / "Poppins-Bold.ttf"
    try:
        return ImageFont.truetype(str(arq), max(8, int(px)))
    except OSError:
        return ImageFont.load_default()


def _texto_centro(d, cx, y, texto, px, cor, larg_max):
    f = _fonte(px)
    while f.getlength(texto) > larg_max and px > 8:
        px *= 0.9
        f = _fonte(px)
    d.text((cx - f.getlength(texto) / 2, y), texto, font=f, fill=cor)


def _papel(u, prop, inclina):
    """Folha de papel no chão (gira um pouco). Devolve img, draw, área útil."""
    img, d = _tela(u * 1.3, u * 1.3)
    U = u * S
    w, h = U * prop[0], U * prop[1]
    return img, d, ((img.width - w) / 2, (img.height - h) / 2, (img.width + w) / 2, (img.height + h) / 2)


def _girar(img, ang):
    return img.rotate(ang, resample=Image.BICUBIC, expand=False)


def _foto(u, t, texto=""):
    """Foto antiga: uma família na frente desta casa, o rosto de um deles riscado; atrás, um vulto alto."""
    img, d, (x0, y0, x1, y1) = _papel(u, (0.8, 0.95), 0)
    o = max(2, int(u * S * 0.015))
    d.rectangle((x0, y0, x1, y1), fill=(232, 222, 196), outline=TRACO, width=o)
    m = (x1 - x0) * 0.08
    fx0, fy0, fx1, fy1 = x0 + m, y0 + m, x1 - m, y1 - (y1 - y0) * 0.22
    d.rectangle((fx0, fy0, fx1, fy1), fill=(96, 84, 70))
    # casa ao fundo e a família (silhuetas sépia)
    cw_ = fx1 - fx0
    d.polygon([(fx0 + cw_ * 0.15, fy0 + cw_ * 0.45), (fx0 + cw_ * 0.5, fy0 + cw_ * 0.18), (fx0 + cw_ * 0.85, fy0 + cw_ * 0.45)], fill=(70, 60, 50))
    d.rectangle((fx0 + cw_ * 0.2, fy0 + cw_ * 0.45, fx0 + cw_ * 0.8, fy1), fill=(80, 68, 56))
    for k, (px, alt) in enumerate(((0.25, 0.42), (0.45, 0.46), (0.65, 0.3))):
        x = fx0 + cw_ * px
        cab = cw_ * 0.06
        topo = fy1 - cw_ * alt
        d.ellipse((x - cab, topo - cab * 2, x + cab, topo), fill=(196, 176, 146))
        d.rounded_rectangle((x - cab * 1.3, topo, x + cab * 1.3, fy1), radius=int(cab), fill=(150, 130, 104))
        if k == 1:                                            # rosto riscado com caneta
            for j in range(5):
                d.line((x - cab * 1.2, topo - cab * (2 - j * 0.4), x + cab * 1.2, topo - cab * (1.6 - j * 0.4)), fill=(20, 16, 18), width=o)
    # o vulto alto na janela de cima, sorrindo (quase não dá para ver)
    vx, vy = fx0 + cw_ * 0.62, fy0 + cw_ * 0.5
    d.rectangle((vx - cw_ * 0.06, vy - cw_ * 0.08, vx + cw_ * 0.06, vy + cw_ * 0.06), fill=(30, 26, 24))
    d.ellipse((vx - cw_ * 0.025, vy - cw_ * 0.06, vx + cw_ * 0.025, vy - cw_ * 0.01), fill=(210, 205, 196))
    d.arc((vx - cw_ * 0.02, vy - cw_ * 0.045, vx + cw_ * 0.02, vy - cw_ * 0.02), 10, 170, fill=(10, 10, 10), width=max(1, o // 2))
    _texto_centro(d, (x0 + x1) / 2, fy1 + (y1 - fy1) * 0.25, texto or "1987", (y1 - fy1) * 0.42, (60, 50, 44), (x1 - x0) * 0.85)
    return _final(_girar(img, -8)), ((x0 + x1) / 2 / S, y0 / S)


def _bilhete(u, t, texto=""):
    """Bilhete escrito à mão, dobrado ao meio."""
    img, d, (x0, y0, x1, y1) = _papel(u, (0.75, 0.55), 0)
    o = max(2, int(u * S * 0.015))
    d.rectangle((x0, y0, x1, y1), fill=(238, 234, 220), outline=TRACO, width=o)
    d.line(((x0 + x1) / 2, y0, (x0 + x1) / 2, y1), fill=(200, 194, 178), width=o)
    linhas = (texto or "NÃO DESÇA").upper().split("|")[:3]
    alt = (y1 - y0) / (len(linhas) + 1.3)
    for i, ln in enumerate(linhas):
        _texto_centro(d, (x0 + x1) / 2, y0 + alt * (0.55 + i), ln.strip(), alt * 0.55, (30, 34, 70), (x1 - x0) * 0.86)
    return _final(_girar(img, 6)), ((x0 + x1) / 2 / S, y0 / S)


def _jornal(u, t, texto=""):
    """Recorte de jornal velho com a manchete e uma foto da casa."""
    img, d, (x0, y0, x1, y1) = _papel(u, (0.85, 0.9), 0)
    o = max(2, int(u * S * 0.015))
    d.rectangle((x0, y0, x1, y1), fill=(214, 206, 178), outline=TRACO, width=o)
    w = x1 - x0
    _texto_centro(d, (x0 + x1) / 2, y0 + w * 0.06, (texto or "FAMÍLIA DESAPARECE").upper(), w * 0.1, (24, 22, 26), w * 0.9)
    fy0 = y0 + w * 0.26
    d.rectangle((x0 + w * 0.08, fy0, x0 + w * 0.55, fy0 + w * 0.42), fill=(90, 86, 80), outline=TRACO, width=max(1, o // 2))
    d.polygon([(x0 + w * 0.14, fy0 + w * 0.22), (x0 + w * 0.31, fy0 + w * 0.07), (x0 + w * 0.49, fy0 + w * 0.22)], fill=(50, 48, 46))
    d.rectangle((x0 + w * 0.17, fy0 + w * 0.22, x0 + w * 0.46, fy0 + w * 0.42), fill=(60, 58, 54))
    for i in range(9):                                        # colunas de texto (rabiscos)
        yy = fy0 + w * 0.02 + i * w * 0.05
        d.line((x0 + w * 0.6, yy, x1 - w * 0.06, yy), fill=(120, 112, 96), width=max(1, o))
    for i in range(4):
        yy = fy0 + w * 0.47 + i * w * 0.05
        d.line((x0 + w * 0.08, yy, x1 - w * 0.06, yy), fill=(120, 112, 96), width=max(1, o))
    return _final(_girar(img, -4)), ((x0 + x1) / 2 / S, y0 / S)


def _desenho(u, t, texto=""):
    """Desenho de criança feito com giz de cera: uma menina, um gato e um homem alto e preto sorrindo."""
    img, d, (x0, y0, x1, y1) = _papel(u, (0.9, 0.7), 0)
    o = max(2, int(u * S * 0.015))
    d.rectangle((x0, y0, x1, y1), fill=(240, 238, 230), outline=TRACO, width=o)
    w, h = x1 - x0, y1 - y0
    g = max(2, int(w * 0.018))
    chao = y0 + h * 0.85
    d.line((x0 + w * 0.05, chao, x1 - w * 0.05, chao), fill=(70, 150, 70), width=g)
    # menina
    mx = x0 + w * 0.22
    d.ellipse((mx - w * 0.045, chao - h * 0.5, mx + w * 0.045, chao - h * 0.38), outline=(200, 80, 60), width=g)
    d.line((mx, chao - h * 0.38, mx, chao - h * 0.15), fill=(200, 80, 60), width=g)
    d.line((mx - w * 0.05, chao, mx, chao - h * 0.15, mx + w * 0.05, chao), fill=(200, 80, 60), width=g)
    # gatinho laranja
    gx = x0 + w * 0.38
    d.ellipse((gx - w * 0.04, chao - h * 0.12, gx + w * 0.04, chao), outline=(226, 136, 56), width=g)
    d.polygon([(gx - w * 0.035, chao - h * 0.1), (gx - w * 0.02, chao - h * 0.17), (gx - w * 0.005, chao - h * 0.11)], outline=(226, 136, 56))
    # o homem alto e preto, sorriso enorme
    hx = x0 + w * 0.72
    d.rectangle((hx - w * 0.04, chao - h * 0.78 * 0.62, hx + w * 0.04, chao), fill=(18, 18, 22))
    d.line((hx - w * 0.04, chao - h * 0.78 * 0.55, hx - w * 0.16, chao - h * 0.78 * 0.3), fill=(18, 18, 22), width=g * 2)
    d.line((hx + w * 0.04, chao - h * 0.78 * 0.55, hx + w * 0.16, chao - h * 0.78 * 0.3), fill=(18, 18, 22), width=g * 2)
    d.ellipse((hx - w * 0.07, chao - h * 0.78 * 0.82, hx + w * 0.07, chao - h * 0.78 * 0.6), fill=(18, 18, 22))
    d.arc((hx - w * 0.05, chao - h * 0.78 * 0.76, hx + w * 0.05, chao - h * 0.78 * 0.64), 10, 170, fill=(240, 238, 230), width=g)
    for ex in (-0.025, 0.025):
        d.ellipse((hx + w * ex - w * 0.012, chao - h * 0.78 * 0.76, hx + w * ex + w * 0.012, chao - h * 0.78 * 0.72), fill=(240, 238, 230))
    _texto_centro(d, (x0 + x1) / 2, y0 + h * 0.04, (texto or "O MOÇO DO SORRISO").upper(), h * 0.09, (40, 60, 160), w * 0.9)
    return _final(_girar(img, 5)), ((x0 + x1) / 2 / S, y0 / S)


DESENHOS.update({"foto": _foto, "bilhete": _bilhete, "jornal": _jornal, "desenho": _desenho})


# ---------------------------------------------------------------- a arma da policial
COR_ARMA, COR_ARMA_S = (58, 60, 66), (40, 42, 48)


def _pistola(d, ox, oy, U, cor, cor_s, o, contorno=True):
    """Pistola de serviço de perfil, cano para a direita (U = largura)."""
    def P(pts):
        return [(ox + x * U, oy + y * U) for x, y in pts]
    ferrolho = P([(0.04, 0.06), (0.96, 0.06), (0.98, 0.1), (0.98, 0.24), (0.04, 0.24)])
    corpo = P([(0.1, 0.24), (0.86, 0.24), (0.86, 0.31), (0.42, 0.31), (0.1, 0.31)])
    cabo = P([(0.08, 0.28), (0.34, 0.28), (0.3, 0.86), (0.27, 0.9), (0.04, 0.88), (0.02, 0.84)])
    guarda = (ox + 0.33 * U, oy + 0.26 * U, ox + 0.56 * U, oy + 0.5 * U)
    for poly in (cabo, corpo, ferrolho):
        d.polygon(poly, fill=cor, outline=TRACO if contorno else None, width=o if contorno else 0)
    d.arc(guarda, 0, 180, fill=TRACO if contorno else cor, width=max(2, int(o * 1.6)))
    return {"ferrolho": ferrolho, "cabo": cabo}


def _arma(u, t):
    img, d = _tela(u * 1.1, u * 0.75)
    o = max(2, int(u * S * 0.018))
    U = u * S
    ox, oy = U * 0.05, U * 0.05
    _pistola(d, ox, oy, U, COR_ARMA, COR_ARMA_S, o)
    for i in range(6):                                           # estrias do ferrolho
        x = ox + U * (0.1 + i * 0.03)
        d.line((x, oy + U * 0.09, x, oy + U * 0.21), fill=COR_ARMA_S, width=max(1, o // 2))
    d.line((ox + U * 0.46, oy + U * 0.31, ox + U * 0.43, oy + U * 0.42), fill=TRACO, width=o)   # gatilho
    for i in range(5):                                           # textura do cabo
        y = oy + U * (0.4 + i * 0.09)
        d.line((ox + U * 0.08, y, ox + U * 0.27, y - U * 0.02), fill=COR_ARMA_S, width=max(1, o // 2))
    d.line((ox + U * 0.12, oy + U * 0.1, ox + U * 0.9, oy + U * 0.1), fill=(150, 152, 160), width=max(1, o // 2))  # reflexo
    return _final(img), (ox / S + u * 0.9, oy / S + u * 0.12)


def _caixa_arma(u, t):
    """Maleta da arma aberta: o recorte da espuma no formato da pistola... vazio."""
    img, d = _tela(u * 1.3, u * 1.05)
    o = max(2, int(u * S * 0.018))
    U = u * S
    x0, x1 = U * 0.05, U * 1.25
    # tampa aberta (para trás), com espuma ondulada
    d.polygon([(x0 + U * 0.08, U * 0.03), (x1 - U * 0.08, U * 0.03), (x1, U * 0.42), (x0, U * 0.42)], fill=(30, 30, 34), outline=TRACO, width=o)
    d.polygon([(x0 + U * 0.14, U * 0.08), (x1 - U * 0.14, U * 0.08), (x1 - U * 0.06, U * 0.38), (x0 + U * 0.06, U * 0.38)], fill=(70, 70, 78))
    for i in range(9):
        for j in range(3):
            cx, cy = x0 + U * (0.18 + i * 0.11), U * (0.14 + j * 0.09)
            d.ellipse((cx - U * 0.03, cy - U * 0.025, cx + U * 0.03, cy + U * 0.025), fill=(58, 58, 66))
    # base com a espuma lisa
    d.rounded_rectangle((x0, U * 0.42, x1, U * 1.0), radius=int(U * 0.04), fill=(30, 30, 34), outline=TRACO, width=o)
    d.rectangle((x0 + U * 0.06, U * 0.47, x1 - U * 0.06, U * 0.94), fill=(78, 78, 86))
    # recorte vazio da pistola e do carregador
    _pistola(d, x0 + U * 0.2, U * 0.5, U * 0.62, (16, 16, 20), None, o, contorno=False)
    d.rounded_rectangle((x0 + U * 0.92, U * 0.58, x0 + U * 1.04, U * 0.88), radius=int(U * 0.02), fill=(16, 16, 20))
    # fechos
    for fx in (0.3, 0.9):
        d.rectangle((x0 + U * fx, U * 0.4, x0 + U * (fx + 0.06), U * 0.46), fill=(150, 150, 158), outline=TRACO, width=max(1, o // 2))
    return _final(img), (x0 / S + u * 0.5, u * 0.7)


DESENHOS.update({"arma": _arma, "caixa_arma": _caixa_arma})
TIPOS += ["arma", "caixa_arma"]
ESCALA.update({"arma": 0.7, "caixa_arma": 0.85})
NO_CHAO |= {"arma", "caixa_arma"}
