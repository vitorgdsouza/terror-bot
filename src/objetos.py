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
"""
import math

from PIL import Image, ImageDraw, ImageFilter

TRACO = (24, 22, 30, 255)
TIPOS = ["coleira", "tigela", "pelo", "novelo", "ratinho", "pegadas", "arranhoes", "marcas_mao"]
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
            for i in range(4):
                x0 = (rx + rw * (0.25 + i * 0.12)) * cw
                y0 = (ry + rh * 0.45) * ch
                d.line((x0, y0, x0 + cw * 0.03, y0 + ch * 0.09), fill=(210, 200, 186, 210), width=max(3, int(cw * 0.006)))
                d.line((x0 + 3, y0 + 2, x0 + cw * 0.03 + 3, y0 + ch * 0.09 + 2), fill=(30, 26, 32, 200), width=max(2, int(cw * 0.003)))
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
    # objetos no chão
    if tam == "perto":
        u = cw * 0.55
        cx, cy = cw * 0.5, ch * 0.74
        # luz da lanterna em cima do objeto
        luz = Image.new("L", quadro.size, 0)
        ImageDraw.Draw(luz).ellipse((cx - cw * 0.42, cy - ch * 0.16, cx + cw * 0.42, cy + ch * 0.16), fill=110)
        luz = luz.filter(ImageFilter.GaussianBlur(cw * 0.06))
        quadro.paste(Image.new("RGBA", quadro.size, (255, 236, 190, 255)), (0, 0), luz.point(lambda v: int(v * 0.38)))
    else:
        u = cw * 0.2 * meta.get("escala", 1.0)
        cx, cy = x * cw, ch * (piso - 0.075)          # um pouco acima da borda (a câmera corta o rodapé)
    img, brilho = DESENHOS[tipo](u, t)
    img = noite(img, 0.35 if tam != "perto" else 0.28)
    ox, oy = int(cx - img.width * 0.45), int(cy - img.height * 0.55)
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
