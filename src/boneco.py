"""Boneco articulado, desenhado pelo código a cada quadro, no estilo de desenho animado simples.

Visual (inspirado na folha do Lucas, simplificado): cabeça redonda, cabelo bagunçado, olhos de bolinha,
moletom aberto sobre camiseta listrada, jeans com barra dobrada e tênis vermelho. Traço fino e cores chapadas.

O corpo tem articulações (ombro, cotovelo, quadril, joelho), expressões e objetos. Como é desenhado
a cada quadro, anda, corre, senta, segura coisas e muda a cara sem deformar, com movimento contínuo.

    img, info = desenhar(pose, altura, quem)   # imagem RGBA; info["pes"] = (x, y) dos pés na imagem
    pose = animar(acao, t, ...)                # pose pronta de cada ação no instante t
    pose = misturar(pose_a, pose_b, k)         # transição suave entre duas poses (k de 0 a 1)
"""
import math

from PIL import Image, ImageDraw

S = 2                                   # desenha no dobro do tamanho e reduz (traço liso)
ALTURA_MAX_DESENHO = 1400               # acima disso desenha neste tamanho e amplia (economiza tempo)
TRACO = (24, 22, 30, 255)

VISUAIS = {
    "homem": {"pele": (240, 205, 172), "pele_s": (214, 176, 146), "cabelo": (92, 58, 36), "cabelo_s": (70, 42, 26),
              "moletom": (66, 128, 72), "moletom_s": (48, 100, 56), "camiseta": (238, 238, 240), "listra": (56, 66, 104),
              "calca": (52, 74, 118), "calca_s": (40, 58, 96), "barra": (78, 102, 148), "tenis": (190, 52, 48),
              "sola": (240, 240, 240), "cabelo_tipo": "baguncado"},
    # elenco extra (vídeos de fatos e outras histórias)
    "adulto": {"pele": (226, 186, 150), "pele_s": (198, 158, 124), "cabelo": (34, 30, 30), "cabelo_s": (20, 18, 18),
               "moletom": (96, 98, 110), "moletom_s": (72, 74, 86), "camiseta": (214, 206, 186), "listra": (214, 206, 186),
               "calca": (58, 52, 46), "calca_s": (44, 40, 36), "barra": (74, 68, 60), "tenis": (60, 40, 30),
               "sola": (40, 32, 28), "cabelo_tipo": "baguncado"},
    "idosa": {"pele": (236, 204, 180), "pele_s": (210, 178, 154), "cabelo": (200, 200, 206), "cabelo_s": (168, 168, 176),
              "moletom": (130, 70, 92), "moletom_s": (104, 52, 72), "camiseta": (236, 228, 214), "listra": (236, 228, 214),
              "calca": (80, 74, 92), "calca_s": (62, 58, 74), "barra": (96, 90, 110), "tenis": (70, 60, 56),
              "sola": (230, 226, 220), "cabelo_tipo": "chanel"},
    "garota": {"pele": (176, 124, 92), "pele_s": (150, 102, 74), "cabelo": (40, 26, 20), "cabelo_s": (26, 16, 12),
               "moletom": (60, 110, 170), "moletom_s": (44, 88, 140), "camiseta": (240, 236, 240), "listra": (210, 80, 100),
               "calca": (40, 44, 58), "calca_s": (30, 32, 44), "barra": (60, 64, 80), "tenis": (240, 240, 240),
               "sola": (190, 190, 196), "cabelo_tipo": "chanel"},
    "policial": {"pele": (224, 182, 150), "pele_s": (196, 154, 124), "cabelo": (58, 34, 24), "cabelo_s": (40, 22, 14),
                 "moletom": (36, 52, 92), "moletom_s": (26, 38, 70), "camiseta": (52, 70, 116), "listra": (52, 70, 116),
                 "calca": (30, 34, 48), "calca_s": (22, 24, 36), "barra": (40, 44, 60), "tenis": (24, 22, 24),
                 "sola": (16, 14, 16), "cabelo_tipo": "chanel"},
    "mulher": {"pele": (242, 208, 178), "pele_s": (216, 180, 150), "cabelo": (34, 28, 34), "cabelo_s": (22, 18, 24),
               "moletom": (206, 160, 52), "moletom_s": (172, 128, 36), "camiseta": (238, 238, 240), "listra": (56, 66, 104),
               "calca": (52, 74, 118), "calca_s": (40, 58, 96), "barra": (78, 102, 148), "tenis": (190, 52, 48),
               "sola": (240, 240, 240), "cabelo_tipo": "chanel"},
}

NUMERICOS = ["y", "tronco", "cab_inc", "cab_vira", "olhar", "ombro_e", "cotovelo_e", "ombro_d", "cotovelo_d",
             "quadril_e", "joelho_e", "quadril_d", "joelho_d", "pe_e", "pe_d", "respira", "luz", "mao_boca"]
POSE_BASE = {
    "vista": "frente", "espelhar": False, "sentado": False, "cadeira": True, "objeto": None, "joelhos_peito": False,
    "olhos": "normal", "sobrancelhas": "neutras", "boca": "reta",
    "y": 0.0, "tronco": 0.0, "cab_inc": 0.0, "cab_vira": 0.0, "olhar": 0.0,
    "ombro_e": 4.0, "cotovelo_e": 6.0, "ombro_d": 4.0, "cotovelo_d": 6.0,
    "quadril_e": 0.0, "joelho_e": 0.0, "quadril_d": 0.0, "joelho_d": 0.0, "pe_e": 0.0, "pe_d": 0.0,
    "respira": 0.0, "luz": 1.0, "mao_boca": 0.0,
}


# ---------------------------------------------------------------- formas
class _Lapis:
    def __init__(self, d, u):
        self.d, self.u = d, u
        self.o = max(2.0, u * 0.0042)            # espessura do traço

    def capsula(self, a, b, w, cor):
        d, o = self.d, self.o
        for (cor_, larg) in ((TRACO, w + 2 * o), (cor, w)):
            d.line([a, b], fill=cor_, width=int(larg))
            for p in (a, b):
                r = larg / 2
                d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=cor_)

    def elipse(self, cx, cy, rx, ry, cor, traco=True):
        o = self.o if traco else 0
        if traco:
            self.d.ellipse((cx - rx - o, cy - ry - o, cx + rx + o, cy + ry + o), fill=TRACO)
        self.d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=cor)

    def poligono(self, pts, cor, traco=True):
        self.d.polygon(pts, fill=cor)
        if traco:
            self.d.line(pts + [pts[0]], fill=TRACO, width=int(self.o * 1.6), joint="curve")


def _rot(p, centro, graus):
    a = math.radians(graus)
    x, y = p[0] - centro[0], p[1] - centro[1]
    return (centro[0] + x * math.cos(a) - y * math.sin(a), centro[1] + x * math.sin(a) + y * math.cos(a))


def _segmento(orig, ang, comp):
    a = math.radians(ang)
    return (orig[0] + math.sin(a) * comp, orig[1] + math.cos(a) * comp)


# ---------------------------------------------------------------- desenho
def desenhar(pose: dict, altura: int, quem: str = "homem"):
    """Desenha o boneco. Devolve (imagem RGBA, info) com info["pes"], info["rosto"], info["lanterna"]."""
    p = {**POSE_BASE, **pose}
    v = VISUAIS.get(quem, VISUAIS["homem"])
    alt_real = altura
    altura = min(altura, ALTURA_MAX_DESENHO)
    u = altura * S
    img = Image.new("RGBA", (int(u * 1.25), int(u * 1.18)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    L = _Lapis(d, u)
    gx, gy = img.width / 2, img.height - u * 0.05      # ponto no chão, entre os pés
    vista = p["vista"]
    lado = vista == "lado"
    info = {}

    resp = p["respira"] * u * 0.005
    quadril = (gx, gy - u * 0.37 - p["y"] * u)
    if p["sentado"]:
        quadril = (gx, gy - u * 0.26)
    pescoco = _rot((quadril[0], quadril[1] - u * 0.25 - resp), quadril, p["tronco"] if lado else 0)
    if not lado:
        pescoco = (pescoco[0] + math.sin(math.radians(p["tronco"])) * u * 0.02, pescoco[1])
    coxa, canela = u * 0.175, u * 0.16
    braco, antebraco = u * 0.13, u * 0.12
    wp, wb = u * 0.078, u * 0.064

    # ------------------------------------------------ partes
    def perna(orig, q, j, pe_sobe, cor, cor_barra, cor_tenis, de_lado):
        if de_lado:
            joelho = _segmento(orig, q, coxa)
            pe = _segmento(joelho, q - abs(j), canela)
        else:
            joelho = _segmento(orig, q, coxa * (1 - pe_sobe * 0.5))
            pe = _segmento(joelho, q, canela * (1 - pe_sobe * 0.5))
        L.capsula(orig, joelho, wp, cor)
        L.capsula(joelho, pe, wp * 0.95, cor)
        # barra dobrada do jeans
        bx = (pe[0] - joelho[0], pe[1] - joelho[1])
        n = math.hypot(*bx) or 1
        b1 = (pe[0] - bx[0] / n * u * 0.03, pe[1] - bx[1] / n * u * 0.03)
        L.capsula(b1, pe, wp * 1.12, cor_barra)
        # tênis
        if de_lado:
            ang = math.radians(q - abs(j))
            frente = (math.cos(ang), -math.sin(ang)) if False else (1, 0)
            cx_, cy_ = pe[0] + u * 0.025, pe[1] + u * 0.02
            L.elipse(cx_, cy_, u * 0.055, u * 0.026, cor_tenis)
            d.rectangle((cx_ - u * 0.055, cy_ + u * 0.008, cx_ + u * 0.058, cy_ + u * 0.024), fill=v["sola"])
            d.line((cx_ - u * 0.055, cy_ + u * 0.024, cx_ + u * 0.058, cy_ + u * 0.024), fill=TRACO, width=int(L.o))
        else:
            cx_, cy_ = pe[0], pe[1] + u * 0.018
            L.elipse(cx_, cy_, u * 0.04, u * 0.028, cor_tenis)
            d.rectangle((cx_ - u * 0.04, cy_ + u * 0.008, cx_ + u * 0.04, cy_ + u * 0.022), fill=v["sola"])
        return pe

    def braco_(orig, o, c, sinal, cor_manga, cor_mao, objeto=None, de_lado=False):
        a1 = o * sinal
        cot = _segmento(orig, a1, braco)
        mao = _segmento(cot, a1 + c * sinal, antebraco)
        L.capsula(orig, cot, wb, cor_manga)
        L.capsula(cot, mao, wb * 0.95, cor_manga)
        L.elipse(mao[0], mao[1], u * 0.027, u * 0.027, cor_mao)
        if objeto:
            _objeto(objeto, mao, cot)
        return mao

    def _objeto(tipo, mao, cot):
        ang = math.atan2(mao[1] - cot[1], mao[0] - cot[0])
        if tipo == "celular":
            w, h = u * 0.065, u * 0.11
            box = (mao[0] - w / 2, mao[1] - h * 0.8, mao[0] + w / 2, mao[1] + h * 0.2)
            d.rounded_rectangle((box[0] - L.o, box[1] - L.o, box[2] + L.o, box[3] + L.o), radius=int(u * 0.01), fill=TRACO)
            d.rounded_rectangle(box, radius=int(u * 0.008), fill=(28, 30, 38))
            m = u * 0.006
            k = p["luz"]
            d.rectangle((box[0] + m, box[1] + m, box[2] - m, box[3] - m),
                        fill=(int(120 + 70 * k), int(170 + 50 * k), int(220 + 35 * k)))
            L.elipse(mao[0], mao[1] - u * 0.005, u * 0.024, u * 0.022, v["pele"])   # dedos por cima
            info["tela"] = (mao[0], box[1])
        elif tipo == "lanterna":
            dx, dy = math.cos(ang), math.sin(ang)
            a = (mao[0] - dx * u * 0.02, mao[1] - dy * u * 0.02)
            b = (mao[0] + dx * u * 0.085, mao[1] + dy * u * 0.085)
            L.capsula(a, b, u * 0.028, (70, 72, 80))
            r = u * 0.02
            d.ellipse((b[0] - r, b[1] - r, b[0] + r, b[1] + r), fill=(255, 245, 200))
            info["lanterna"] = (b, math.degrees(ang))

    def tronco_frente():
        lq, lo = u * 0.105, u * 0.118                  # meia largura no quadril e nos ombros
        base = quadril[1] + u * 0.03
        topo = pescoco[1] + u * 0.02
        dx = pescoco[0] - quadril[0]
        corpo = [(quadril[0] - lq, base), (pescoco[0] - lo, topo + u * 0.035), (pescoco[0] - lo * 0.7, topo),
                 (pescoco[0] + lo * 0.7, topo), (pescoco[0] + lo, topo + u * 0.035), (quadril[0] + lq, base)]
        L.poligono(corpo, v["moletom"])
        # sombra do lado direito
        d.polygon([(pescoco[0] + lo * 0.55, topo + u * 0.01), (pescoco[0] + lo * 0.95, topo + u * 0.04),
                   (quadril[0] + lq * 0.96, base - L.o), (quadril[0] + lq * 0.55, base - L.o)], fill=v["moletom_s"])
        # camiseta listrada (moletom aberto)
        cam = [(pescoco[0] - u * 0.035, topo), (pescoco[0] + u * 0.035, topo),
               (quadril[0] + u * 0.04, base - L.o), (quadril[0] - u * 0.04, base - L.o)]
        d.polygon(cam, fill=v["camiseta"])
        y = topo + u * 0.02
        while y < base - u * 0.015:
            k = (y - topo) / (base - topo)
            xc = pescoco[0] + (quadril[0] - pescoco[0]) * k
            meia = u * (0.035 + 0.005 * k)
            d.line((xc - meia, y, xc + meia, y), fill=v["listra"], width=int(u * 0.011))
            y += u * 0.03
        for sx in (-1, 1):                              # bordas do zíper
            d.line((pescoco[0] + sx * u * 0.035, topo, quadril[0] + sx * u * 0.04, base - L.o), fill=TRACO, width=int(L.o * 1.3))
        d.line((quadril[0] - lq, base, quadril[0] + lq, base), fill=TRACO, width=int(L.o * 1.6))

    def tronco_lado():
        base = (quadril[0], quadril[1] + u * 0.03)
        pts = [(-0.075, 0.03), (-0.082, -0.12), (-0.06, -0.24), (0.035, -0.25), (0.07, -0.19), (0.072, -0.05), (0.07, 0.03)]
        pts = [_rot((quadril[0] + x * u, quadril[1] + y * u), quadril, p["tronco"]) for x, y in pts]
        L.poligono(pts, v["moletom"])
        frente = [_rot((quadril[0] + x * u, quadril[1] + y * u), quadril, p["tronco"])
                  for x, y in ((0.045, -0.23), (0.068, -0.19), (0.07, 0.025), (0.05, 0.025))]
        d.polygon(frente, fill=v["camiseta"])
        for yy in (-0.2, -0.16, -0.12, -0.08, -0.04, 0.0):
            a = _rot((quadril[0] + 0.05 * u, quadril[1] + yy * u), quadril, p["tronco"])
            b = _rot((quadril[0] + 0.069 * u, quadril[1] + yy * u), quadril, p["tronco"])
            d.line((a, b), fill=v["listra"], width=int(u * 0.01))
        d.line((frente[0], frente[3]), fill=TRACO, width=int(L.o * 1.2))

    def tronco_costas():
        lq, lo = u * 0.105, u * 0.118
        base = quadril[1] + u * 0.03
        topo = pescoco[1] + u * 0.02
        corpo = [(quadril[0] - lq, base), (pescoco[0] - lo, topo + u * 0.035), (pescoco[0] - lo * 0.7, topo),
                 (pescoco[0] + lo * 0.7, topo), (pescoco[0] + lo, topo + u * 0.035), (quadril[0] + lq, base)]
        L.poligono(corpo, v["moletom"])
        d.polygon([(pescoco[0] + lo * 0.5, topo + u * 0.01), (pescoco[0] + lo * 0.95, topo + u * 0.04),
                   (quadril[0] + lq * 0.96, base - L.o), (quadril[0] + lq * 0.5, base - L.o)], fill=v["moletom_s"])
        # capuz caído nas costas
        L.elipse(pescoco[0], topo + u * 0.045, u * 0.075, u * 0.055, v["moletom_s"])

    def cadeira():
        cx_, cy_ = quadril[0] - u * 0.03, quadril[1] + u * 0.03
        cor = (46, 48, 58)
        d.rounded_rectangle((cx_ - u * 0.11, cy_ - u * 0.03, cx_ + u * 0.13, cy_ + u * 0.02), radius=int(u * 0.02), fill=cor, outline=TRACO, width=int(L.o))
        d.rounded_rectangle((cx_ - u * 0.13, cy_ - u * 0.3, cx_ - u * 0.07, cy_ - u * 0.01), radius=int(u * 0.03), fill=cor, outline=TRACO, width=int(L.o))
        d.line((cx_, cy_ + u * 0.02, cx_, gy - u * 0.03), fill=TRACO, width=int(u * 0.02))
        d.line((cx_ - u * 0.09, gy - u * 0.02, cx_ + u * 0.09, gy - u * 0.02), fill=TRACO, width=int(u * 0.016))

    # ------------------------------------------------ ordem de desenho
    escuro = lambda c: tuple(int(x * 0.72) for x in c[:3])
    if lado:
        if p["sentado"] and p["cadeira"]:
            cadeira()
        ombro = _rot((pescoco[0] + u * 0.005, pescoco[1] + u * 0.03), pescoco, 0)
        perna(quadril, p["quadril_e"], p["joelho_e"], 0, escuro(v["calca"]), escuro(v["barra"]), escuro(v["tenis"]), True)
        braco_(ombro, p["ombro_e"], p["cotovelo_e"], 1, escuro(v["moletom"]), escuro(v["pele"]), None, True)
        tronco_lado()
        perna(quadril, p["quadril_d"], p["joelho_d"], 0, v["calca"], v["barra"], v["tenis"], True)
        cabeca_pos = (pescoco[0] + u * 0.01, pescoco[1] - u * 0.14)
        _cabeca(d, L, cabeca_pos, u, p, v, "lado", info)
        braco_(ombro, p["ombro_d"], p["cotovelo_d"], 1, v["moletom"], v["pele"], p["objeto"], True)
    else:
        costas = vista == "costas"
        for sx, q, j, pe_ in (() if p.get("joelhos_peito") else ((-1, p["quadril_e"], p["joelho_e"], p["pe_e"]), (1, p["quadril_d"], p["joelho_d"], p["pe_d"]))):
            perna((quadril[0] + sx * u * 0.055, quadril[1]), q * sx, j, pe_, v["calca"], v["barra"], v["tenis"], False)
        (tronco_costas if costas else tronco_frente)()
        if p.get("joelhos_peito"):
            for sx in (-1, 1):
                q0 = (quadril[0] + sx * u * 0.055, quadril[1])
                joelho = (quadril[0] + sx * u * 0.06, quadril[1] - u * 0.13)
                pe = (quadril[0] + sx * u * 0.07, gy - u * 0.025)
                L.capsula(q0, joelho, wp * 1.05, v["calca"])
                L.capsula(joelho, pe, wp, v["calca"])
                L.capsula((pe[0], pe[1] - u * 0.03), pe, wp * 1.12, v["barra"])
                L.elipse(pe[0], pe[1] + u * 0.015, u * 0.04, u * 0.026, v["tenis"])
        cabeca_pos = (pescoco[0], pescoco[1] - u * 0.14)
        maos = []
        for sx, o, c in ((-1, p["ombro_e"], p["cotovelo_e"]), (1, p["ombro_d"], p["cotovelo_d"])):
            orig = (pescoco[0] + sx * u * 0.105, pescoco[1] + u * 0.05)
            obj = p["objeto"] if (sx == 1 and not costas) else None
            if p["mao_boca"] > 0.01:
                maos.append((orig, o, c, sx, obj))
                continue
            braco_(orig, o, c, sx, v["moletom"] if sx < 0 else v["moletom_s"], v["pele"], obj)
        _cabeca(d, L, cabeca_pos, u, p, v, vista, info)
        for orig, o, c, sx, obj in maos:          # mãos na frente da boca: braços por cima da cabeça
            braco_(orig, o, c, sx, v["moletom"] if sx < 0 else v["moletom_s"], v["pele"], obj)

    if lado and p["espelhar"]:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        for k in ("lanterna", "tela", "rosto"):
            if k in info:
                if k == "lanterna":
                    (bx, by), ang = info[k]
                    info[k] = ((img.width - bx, by), 180 - ang)
                else:
                    info[k] = (img.width - info[k][0], info[k][1])
    fator = alt_real / altura
    img = img.reduce(S) if S > 1 else img
    if abs(fator - 1) > 0.01:
        img = img.resize((int(img.width * fator), int(img.height * fator)), Image.BICUBIC)
    esc = fator / S
    conv = lambda pt: (pt[0] * esc, pt[1] * esc)
    info["pes"] = conv((gx, gy))
    for k in ("tela", "rosto"):
        if k in info:
            info[k] = conv(info[k])
    if "lanterna" in info:
        info["lanterna"] = (conv(info["lanterna"][0]), info["lanterna"][1])
    return img, info


def _cabeca(d, L, pos, u, p, v, vista, info):
    cx, cy = pos
    rx, ry = u * 0.148, u * 0.152
    inc = p["cab_inc"]
    lado = vista == "lado"
    vira = p["cab_vira"] if lado else 0.0
    if lado and vira > 0.5:
        vista, lado = "frente", False
    info["rosto"] = (cx, cy)
    # orelhas
    chanel = v["cabelo_tipo"] == "chanel"
    if vista == "frente" and not chanel:
        for sx in (-1, 1):
            L.elipse(cx + sx * rx * 0.97, cy + u * 0.012, u * 0.022, u * 0.03, v["pele"])
    elif lado or chanel:
        pass
    else:
        for sx in (-1, 1):
            L.elipse(cx + sx * rx * 0.97, cy + u * 0.012, u * 0.02, u * 0.028, v["pele"])
    L.elipse(cx, cy, rx, ry, v["pele"])
    if lado:
        if v["cabelo_tipo"] != "chanel":
            L.elipse(cx - rx * 0.15, cy + u * 0.015, u * 0.02, u * 0.028, v["pele"])     # orelha de perfil
        d.polygon([(cx + rx * 0.96, cy + ry * 0.02), (cx + rx * 1.1, cy + ry * 0.2), (cx + rx * 0.93, cy + ry * 0.26)], fill=v["pele"])
        d.line([(cx + rx * 0.96, cy + ry * 0.02), (cx + rx * 1.1, cy + ry * 0.2), (cx + rx * 0.93, cy + ry * 0.26)], fill=TRACO, width=int(L.o))
    # sombra suave da bochecha (lado direito)
    if vista == "frente":
        d.chord((cx - rx, cy - ry, cx + rx, cy + ry), 300, 60, fill=v["pele_s"])
    _cabelo(d, L, cx, cy, rx, ry, u, v, vista)
    if vista == "costas":
        return
    # olhos
    olhar = p["olhar"] * rx * 0.08
    if lado:
        olhos = [(cx + rx * 0.5, cy + ry * 0.02)]
    else:
        olhos = [(cx - rx * 0.36 + olhar, cy + ry * 0.04), (cx + rx * 0.36 + olhar, cy + ry * 0.04)]
    re = u * 0.016
    for (ex, ey) in olhos:
        tipo = p["olhos"]
        if tipo == "fechados":
            d.arc((ex - re * 1.3, ey - re, ex + re * 1.3, ey + re), 20, 160, fill=TRACO, width=int(L.o * 1.3))
        elif tipo == "arregalados":
            R = re * 1.7
            d.ellipse((ex - R - L.o, ey - R - L.o, ex + R + L.o, ey + R + L.o), fill=TRACO)
            d.ellipse((ex - R, ey - R, ex + R, ey + R), fill=(250, 250, 248))
            px = ex + R * 0.3 * p["olhar"]
            d.ellipse((px - re * 0.55, ey - re * 0.55, px + re * 0.55, ey + re * 0.55), fill=TRACO)
        else:
            h = re * (0.75 if tipo == "apertados" else 1.25)
            d.ellipse((ex - re * 0.95, ey - h, ex + re * 0.95, ey + h), fill=TRACO)
            d.ellipse((ex - re * 0.1, ey - h * 0.65, ex + re * 0.35, ey - h * 0.25), fill=(255, 255, 255))
        # sobrancelhas
        sb = p["sobrancelhas"]
        by = ey - re * (3.0 if tipo == "arregalados" else 2.4)
        lado_olho = -1 if (len(olhos) == 2 and ex < cx) else 1
        inc_s = {"neutras": 0.0, "preocupadas": 1.0, "bravas": -1.0, "erguidas": 0.0}.get(sb, 0.0)
        sobe = re * 1.0 if sb in ("erguidas", "preocupadas") else 0
        x_in, x_out = ex - lado_olho * re * 1.5, ex + lado_olho * re * 1.5
        d.line((x_in, by - sobe - inc_s * re * 0.9, x_out, by - sobe + inc_s * re * 0.5), fill=TRACO, width=int(L.o * 1.5))
    # boca
    bx = cx + (rx * 0.62 if lado else olhar)
    by = cy + ry * 0.5
    b = p["boca"]
    if p["mao_boca"] > 0.5:
        return
    if b == "reta":
        d.line((bx - u * 0.014, by, bx + u * 0.014, by), fill=TRACO, width=int(L.o * 1.3))
    elif b == "sorriso":
        d.arc((bx - u * 0.022, by - u * 0.02, bx + u * 0.022, by + u * 0.012), 20, 160, fill=TRACO, width=int(L.o * 1.3))
    elif b == "triste":
        d.arc((bx - u * 0.02, by - u * 0.002, bx + u * 0.02, by + u * 0.022), 200, 340, fill=TRACO, width=int(L.o * 1.3))
    elif b in ("aberta", "grito"):
        w, h = (u * 0.014, u * 0.016) if b == "aberta" else (u * 0.026, u * 0.036)
        d.ellipse((bx - w - L.o, by - h * 0.5 - L.o, bx + w + L.o, by + h + L.o), fill=TRACO)
        d.ellipse((bx - w, by - h * 0.5, bx + w, by + h), fill=(110, 40, 44))


def _cabelo(d, L, cx, cy, rx, ry, u, v, vista):
    cor, cor_s = v["cabelo"], v["cabelo_s"]
    o = L.o
    if v["cabelo_tipo"] == "chanel":
        if vista == "costas":
            pts = [(cx - rx * 1.08, cy + ry * 0.55), (cx - rx * 1.08, cy - ry * 0.2)]
        else:
            pts = [(cx - rx * 1.06, cy + ry * 0.5), (cx - rx * 1.05, cy - ry * 0.2)]
        n = 14
        topo = [(cx + math.cos(math.pi + i * math.pi / n) * rx * 1.08, cy - ry * 0.05 + math.sin(math.pi + i * math.pi / n) * ry * 1.06)
                for i in range(n + 1)]
        if vista == "frente":
            contorno = [(cx - rx * 1.1, cy + ry * 0.62)] + topo + [(cx + rx * 1.1, cy + ry * 0.62), (cx + rx * 0.84, cy + ry * 0.62),
                        (cx + rx * 0.86, cy - ry * 0.3), (cx - rx * 0.86, cy - ry * 0.3), (cx - rx * 0.84, cy + ry * 0.62)]
        elif vista == "lado":
            contorno = [(cx - rx * 1.07, cy + ry * 0.5)] + topo + [(cx + rx * 0.9, cy - ry * 0.25), (cx + rx * 0.2, cy - ry * 0.25),
                        (cx + rx * 0.05, cy + ry * 0.5)]
        else:
            contorno = [(cx - rx * 1.08, cy + ry * 0.58)] + topo + [(cx + rx * 1.08, cy + ry * 0.58)]
        L.poligono(contorno, cor)
        return
    # cabelo bagunçado (pontas)
    n = 11
    pts = []
    for i in range(n + 1):
        a = math.pi + i * math.pi / n
        r = 1.1 + (0.13 if i % 2 else 0.0)
        pts.append((cx + math.cos(a) * rx * r, cy - ry * 0.08 + math.sin(a) * ry * r))
    if vista == "frente":
        franja = [(cx + rx * 0.98, cy - ry * 0.05), (cx + rx * 0.62, cy - ry * 0.3), (cx + rx * 0.45, cy - ry * 0.08),
                  (cx + rx * 0.2, cy - ry * 0.32), (cx - rx * 0.05, cy - ry * 0.1), (cx - rx * 0.25, cy - ry * 0.34),
                  (cx - rx * 0.5, cy - ry * 0.12), (cx - rx * 0.7, cy - ry * 0.3), (cx - rx * 0.98, cy - ry * 0.02)]
        L.poligono(pts + franja, cor)
        d.polygon([(cx + rx * 0.3, cy - ry * 1.0), (cx + rx * 0.9, cy - ry * 0.55), (cx + rx * 0.62, cy - ry * 0.32)], fill=cor_s)
    elif vista == "lado":
        nuca = [(cx + rx * 0.75, cy - ry * 0.5), (cx + rx * 0.5, cy - ry * 0.32), (cx + rx * 0.3, cy - ry * 0.45),
                (cx + rx * 0.05, cy - ry * 0.25), (cx - rx * 0.25, cy - ry * 0.05), (cx - rx * 0.35, cy + ry * 0.35),
                (cx - rx * 0.75, cy + ry * 0.45), (cx - rx * 1.05, cy + ry * 0.25)]
        L.poligono(pts + nuca, cor)
    else:
        L.poligono(pts + [(cx + rx * 1.05, cy + ry * 0.35), (cx + rx * 0.5, cy + ry * 0.55), (cx, cy + ry * 0.45),
                          (cx - rx * 0.5, cy + ry * 0.58), (cx - rx * 1.05, cy + ry * 0.35)], cor)


# ---------------------------------------------------------------- animação
def misturar(a: dict, b: dict, k: float) -> dict:
    """Transição suave da pose a para a pose b (k de 0 a 1, com aceleração e freio)."""
    k = max(0.0, min(1.0, k))
    k = k * k * (3 - 2 * k)
    pa, pb = {**POSE_BASE, **a}, {**POSE_BASE, **b}
    out = dict(pb if k >= 0.5 else pa)
    for c in NUMERICOS:
        out[c] = pa[c] + (pb[c] - pa[c]) * k
    return out


def _piscar(t, fase=0.0):
    return ((t + fase) % 3.7) < 0.12


EXPRESSOES = {
    "neutro": ("normal", "neutras", "reta"),
    "preocupado": ("normal", "preocupadas", "triste"),
    "assustado": ("arregalados", "preocupadas", "aberta"),
    "aterrorizado": ("arregalados", "preocupadas", "grito"),
    "determinado": ("normal", "bravas", "reta"),
    "confuso": ("normal", "erguidas", "reta"),
    "aliviado": ("normal", "neutras", "sorriso"),
}

ACOES = ["parado", "andando", "correndo", "afastando", "aproximando", "olhando_tras", "celular", "lanterna",
         "sentado", "abrindo_porta", "agachado", "escondido", "costas", "virando"]


def animar(acao: str, t: float, dur: float = 4.0, medo: float = 0.0, expressao: str | None = None,
           espelhar: bool = False) -> dict:
    """Pose do boneco no instante t. medo (0..1) muda a expressão e a respiração; expressao força uma cara."""
    if expressao not in EXPRESSOES:
        expressao = ("aterrorizado" if medo > 0.85 else "assustado" if medo > 0.6 else
                     "preocupado" if medo > 0.3 else "neutro")
    olhos, sobr, boca = EXPRESSOES[expressao]
    if _piscar(t) and olhos != "arregalados":
        olhos = "fechados"
    resp = 0.5 + 0.5 * math.sin(t * 2 * math.pi / (1.5 if medo > 0.5 else 3.3))
    treme = math.sin(t * 47) * 1.6 * max(0.0, medo - 0.6)
    pose = {"olhos": olhos, "sobrancelhas": sobr, "boca": boca, "respira": resp, "espelhar": espelhar}

    if acao in ("andando", "correndo"):
        corre = acao == "correndo"
        per = 0.55 if corre else 0.9
        c = t * 2 * math.pi / per
        s = math.sin(c)
        amp_q, amp_b = (34, 45) if corre else (24, 22)
        pose.update(vista="lado", tronco=(12 if corre else 3),
                    quadril_e=-amp_q * s, quadril_d=amp_q * s,
                    joelho_e=max(0.0, (60 if corre else 38) * math.sin(c - 1.1)),
                    joelho_d=max(0.0, (60 if corre else 38) * math.sin(c + math.pi - 1.1)),
                    ombro_e=amp_b * s, ombro_d=-amp_b * s,
                    cotovelo_e=(85 if corre else 18), cotovelo_d=(85 if corre else 18),
                    y=abs(math.cos(c)) * (0.03 if corre else 0.012), cab_inc=math.sin(c * 2) * 1.0)
    elif acao in ("afastando", "aproximando"):
        c = t * 2 * math.pi / 0.9
        s = math.sin(c)
        pose.update(vista="costas" if acao == "afastando" else "frente",
                    pe_e=max(0.0, s) * 0.35, pe_d=max(0.0, -s) * 0.35,
                    ombro_e=4 + 10 * s, ombro_d=4 - 10 * s, y=abs(math.cos(c)) * 0.01)
    elif acao == "olhando_tras":
        pose.update(vista="lado", cab_vira=1.0, ombro_e=-6, ombro_d=6, tronco=-2,
                    olhos="arregalados" if not _piscar(t) else "fechados", sobrancelhas="preocupadas")
    elif acao == "celular":
        pose.update(vista="frente", objeto="celular", ombro_d=-4, cotovelo_d=-128, ombro_e=-2, cotovelo_e=-30,
                    cab_inc=4, luz=0.85 + 0.15 * math.sin(t * 1.4), olhar=-0.3)
    elif acao == "lanterna":
        varre = math.sin(t * 0.9) * 6
        pose.update(vista="lado", objeto="lanterna", ombro_d=82 + varre, cotovelo_d=4, ombro_e=8, cotovelo_e=16, tronco=3)
    elif acao == "sentado":                     # sentado com as mãos no colo, só respirando (sem computador)
        pose.update(vista="lado", sentado=True, cadeira=False, quadril_e=88, joelho_e=88, quadril_d=84, joelho_d=84,
                    ombro_e=6, cotovelo_e=58, ombro_d=4, cotovelo_d=62, tronco=2, cab_inc=2)
    elif acao == "abrindo_porta":
        k = min(1.0, t / max(0.8, dur * 0.4))
        k = k * k * (3 - 2 * k)
        pose.update(vista="lado", ombro_d=10 + 70 * k, cotovelo_d=30 - 22 * k, tronco=3 + 4 * k, ombro_e=4, cotovelo_e=10)
    elif acao == "agachado":
        pose.update(vista="lado", y=-0.13, quadril_e=78, joelho_e=140, quadril_d=62, joelho_d=125,
                    tronco=22, ombro_d=55 + math.sin(t * 1.2) * 5, cotovelo_d=25, ombro_e=30, cotovelo_e=40, cab_inc=10)
    elif acao == "escondido":
        pose.update(vista="frente", y=-0.24, joelhos_peito=True,
                    ombro_e=-18, cotovelo_e=-150, ombro_d=-18, cotovelo_d=-150, mao_boca=1.0,
                    olhos="arregalados" if not _piscar(t) else "fechados", sobrancelhas="preocupadas")
    elif acao == "costas":
        pose.update(vista="costas", ombro_e=4 + treme, ombro_d=4 - treme)
    else:                                                     # parado / virando
        glance = math.sin(t * 0.6) * 0.7 if medo < 0.5 else math.sin(t * 2.1) * 0.9
        pose.update(vista="frente", olhar=glance, cab_inc=math.sin(t * 0.45) * 2 + treme,
                    ombro_e=4 + treme, ombro_d=4 - treme)
        if medo > 0.6:
            pose.update(ombro_e=-14 + treme, cotovelo_e=-120, ombro_d=-14 - treme, cotovelo_d=-120)
    return pose


def pose_cena(acao: str, t: float, dur: float, medo: float, espelhar: bool, expressao=None,
              depois: str | None = None, troca_em: float | None = None) -> dict:
    """Pose de uma cena, com troca suave para a ação "depois" no instante troca_em (0,4 s de transição)."""
    if acao == "virando":
        troca_em = troca_em if troca_em is not None else dur * 0.45
        a = animar("costas", t, dur, medo, expressao, espelhar)
        b = animar("parado", t, dur, medo, expressao, espelhar)
        return misturar(a, b, (t - troca_em) / 0.45)
    atual = animar(acao, t, dur, medo, expressao, espelhar)
    if depois and troca_em is not None and t > troca_em - 0.05:
        if acao == "sentado" and depois == "olhando_tras":     # vira só a cabeça, continua sentado
            prox = {**animar("sentado", t, dur, max(medo, 0.6), expressao, espelhar), "cab_vira": 1.0,
                    "ombro_e": 30, "ombro_d": 25, "olhos": "arregalados", "sobrancelhas": "preocupadas"}
        else:
            prox = animar(depois, t - troca_em, dur, medo, expressao, espelhar)
        return misturar(atual, prox, (t - troca_em) / 0.4)
    return atual
