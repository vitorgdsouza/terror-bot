"""O ABISMO animado: criatura desenhada pelo código a cada quadro, no mesmo estilo do boneco.

Silhueta humana toda preta, alta e magra, braços e pernas compridos, dedos longos, rosto pálido com olhos
redondos e arregalados e um sorriso enorme. O que assusta é o jeito de se mexer: fica quase parado, e de repente
a cabeça "estala" para um novo ângulo; anda devagar e duro; agachado, observa; no close, o sorriso vai abrindo.

    img, info = desenhar(pose, altura)   # RGBA; info["pes"] = ponto dos pés na imagem; info["rosto"]
    pose = animar(acao, t, dur)          # parado | andando | observando | ataque | rosto
"""
import math
import random

from PIL import Image, ImageDraw

from .boneco import _Lapis, _rot, _segmento, misturar

S = 2
CORPO = (10, 10, 14)
BORDA = (54, 56, 70, 255)           # contorno levemente mais claro: a silhueta se destaca no escuro
PELE = (198, 194, 186)
PELE_S = (160, 156, 150)

NUMERICOS_A = ["y", "tronco", "cab_inc", "olhar", "sorriso", "ombro_e", "cotovelo_e", "ombro_d", "cotovelo_d",
               "quadril_e", "joelho_e", "quadril_d", "joelho_d", "pe_e", "pe_d", "dedos"]
POSE_A = {"vista": "frente", "y": 0.0, "tronco": 0.0, "cab_inc": 0.0, "olhar": 0.0, "sorriso": 1.0,
          "ombro_e": 6.0, "cotovelo_e": 4.0, "ombro_d": 6.0, "cotovelo_d": 4.0,
          "quadril_e": 2.0, "joelho_e": 0.0, "quadril_d": 2.0, "joelho_d": 0.0, "pe_e": 0.0, "pe_d": 0.0,
          "dedos": 0.0, "espelhar": False}


class _LapisEscuro(_Lapis):
    """Lápis da silhueta: guarda as formas e desenha tudo de uma vez (primeiro o contorno de todas, depois o
    preenchimento), para o corpo virar UMA silhueta lisa, sem divisões entre braço, tronco e perna."""

    def __init__(self, d, u):
        super().__init__(d, u)
        self.formas = []

    def capsula(self, a, b, w, cor):
        self.formas.append(("c", a, b, w))

    def poligono(self, pts, cor, traco=True):
        self.formas.append(("p", pts))

    def finalizar(self):
        d, o = self.d, self.o
        for passo, (cor, extra) in enumerate(((BORDA, o), (CORPO, 0))):
            for f in self.formas:
                if f[0] == "c":
                    _, a, b, w = f
                    larg = w + 2 * extra
                    d.line([a, b], fill=cor, width=int(larg))
                    for p in (a, b):
                        r = larg / 2
                        d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=cor)
                else:
                    pts = f[1]
                    d.polygon(pts, fill=cor)
                    if extra:
                        d.line(pts + [pts[0]], fill=cor, width=int(extra * 2), joint="curve")
        self.formas = []


def _mao(d, L, mao, ang, u, abre):
    """Mão com três dedos longos e finos (abre: 0 = juntos, 1 = abertos como garra)."""
    for k in (-1, 0, 1):
        a = math.radians(ang + k * (8 + 18 * abre))
        ponta = (mao[0] + math.sin(a) * u * 0.065, mao[1] + math.cos(a) * u * 0.065)
        L.capsula(mao, ponta, u * 0.011, CORPO)


def desenhar(pose: dict, altura: int):
    p = {**POSE_A, **pose}
    altura_real = altura
    altura = min(altura, 1500)
    u = altura * S
    img = Image.new("RGBA", (int(u * 1.3), int(u * 1.12)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    L = _LapisEscuro(d, u)
    L.o = max(2.0, u * 0.0035)
    gx, gy = img.width / 2, img.height - u * 0.04
    lado = p["vista"] == "lado"
    info = {}

    quadril = (gx, gy - u * 0.47 - p["y"] * u)
    pescoco = _rot((quadril[0], quadril[1] - u * 0.28), quadril, p["tronco"])
    coxa, canela, braco, antebraco = u * 0.235, u * 0.235, u * 0.2, u * 0.2
    wp, wb = u * 0.042, u * 0.034

    def perna(orig, q, j, pe_sobe, de_lado):
        if de_lado:
            joelho = _segmento(orig, q, coxa)
            pe = _segmento(joelho, q - abs(j), canela)
        else:
            joelho = _segmento(orig, q, coxa * (1 - pe_sobe * 0.45))
            pe = _segmento(joelho, q + (j if not de_lado else 0) * 0.0, canela * (1 - pe_sobe * 0.45))
        L.capsula(orig, joelho, wp, CORPO)
        L.capsula(joelho, pe, wp * 0.85, CORPO)
        # pé fino e comprido
        frente = u * (0.06 if de_lado else 0.0)
        L.capsula((pe[0] - (0 if de_lado else u * 0.02), pe[1] + u * 0.012), (pe[0] + frente + u * 0.02, pe[1] + u * 0.014), u * 0.022, CORPO)

    def braco_(orig, o, c, sinal):
        a1 = o * sinal
        cot = _segmento(orig, a1, braco)
        mao = _segmento(cot, a1 + c * sinal, antebraco)
        L.capsula(orig, cot, wb, CORPO)
        L.capsula(cot, mao, wb * 0.85, CORPO)
        _mao(d, L, mao, a1 + c * sinal, u, p["dedos"])

    def tronco():
        larg_o, larg_q = u * (0.075 if lado else 0.085), u * (0.05 if lado else 0.06)
        pts = [(quadril[0] - larg_q, quadril[1] + u * 0.02), (pescoco[0] - larg_o, pescoco[1] + u * 0.03),
               (pescoco[0] - larg_o * 0.5, pescoco[1]), (pescoco[0] + larg_o * 0.5, pescoco[1]),
               (pescoco[0] + larg_o, pescoco[1] + u * 0.03), (quadril[0] + larg_q, quadril[1] + u * 0.02)]
        L.poligono(pts, CORPO)

    def costelas():
        for k in range(4):
            y = pescoco[1] + u * (0.07 + 0.04 * k)
            xc = pescoco[0] + (quadril[0] - pescoco[0]) * ((y - pescoco[1]) / (quadril[1] - pescoco[1]))
            d.arc((xc - u * 0.05, y - u * 0.012, xc + u * 0.05, y + u * 0.012), 200, 340, fill=(26, 26, 34), width=int(L.o))

    if lado:
        perna(quadril, p["quadril_e"], p["joelho_e"], 0, True)
        ombro = (pescoco[0], pescoco[1] + u * 0.03)
        braco_(ombro, p["ombro_e"], p["cotovelo_e"], 1)
        tronco()
        perna(quadril, p["quadril_d"], p["joelho_d"], 0, True)
    else:
        for sx, q, j, pe_ in ((-1, p["quadril_e"], p["joelho_e"], p["pe_e"]), (1, p["quadril_d"], p["joelho_d"], p["pe_d"])):
            perna((quadril[0] + sx * u * 0.04, quadril[1]), q * sx, j, pe_, False)
        tronco()
    # pescoço comprido e braços
    cab = _rot((pescoco[0], pescoco[1] - u * 0.11), pescoco, p["cab_inc"] * 0.4)
    L.capsula(pescoco, cab, u * 0.03, CORPO)
    if lado:
        braco_((pescoco[0], pescoco[1] + u * 0.03), p["ombro_d"], p["cotovelo_d"], 1)
    else:
        for sx, o, c in ((-1, p["ombro_e"], p["cotovelo_e"]), (1, p["ombro_d"], p["cotovelo_d"])):
            braco_((pescoco[0] + sx * u * 0.085, pescoco[1] + u * 0.04), o, c, sx)
    L.finalizar()
    costelas()
    _cabeca(d, L, cab, u, p, lado, info, p.get("cab_escala", 1.0))

    if p.get("espelhar"):
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        info["rosto"] = (img.width - info["rosto"][0], info["rosto"][1])
    img = img.reduce(S)
    fator = altura_real / altura
    if abs(fator - 1) > 0.01:
        img = img.resize((int(img.width * fator), int(img.height * fator)), Image.BICUBIC)
    esc = fator / S
    info["pes"] = (gx * esc if not p.get("espelhar") else (img.width - gx * esc), gy * esc)
    info["rosto"] = (info["rosto"][0] * esc, info["rosto"][1] * esc)
    return img, info


def _cabeca(d, L, pos, u, p, lado, info, escala=1.0):
    cx, cy = pos[0], pos[1] - u * 0.07 * escala
    rx, ry = u * 0.075 * escala, u * 0.092 * escala
    info["rosto"] = (cx, cy)
    cab = Image.new("RGBA", (int(rx * 3.2), int(ry * 3.2)), (0, 0, 0, 0))
    dc = ImageDraw.Draw(cab)
    Lc = _LapisEscuro(dc, u)
    Lc.o = L.o
    ccx, ccy = cab.width / 2, cab.height / 2
    _rosto(dc, Lc, ccx, ccy, rx, ry, u * escala, p, lado)
    if p["cab_inc"]:
        cab = cab.rotate(-p["cab_inc"], resample=Image.BICUBIC, center=(ccx, ccy + ry * 0.6))
    d._image.alpha_composite(cab, (int(cx - ccx), int(cy - ccy)))


def _rosto(d, L, cx, cy, rx, ry, u, p, lado):
    o = L.o
    if p.get("silhueta"):                              # identidade escondida: só a forma escura da cabeça
        d.ellipse((cx - rx - o, cy - ry - o, cx + rx + o, cy + ry + o), fill=BORDA)
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=CORPO)
        return
    d.ellipse((cx - rx - o, cy - ry - o, cx + rx + o, cy + ry + o), fill=BORDA)
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=PELE)
    d.chord((cx - rx, cy - ry, cx + rx, cy + ry), 290, 70, fill=PELE_S)        # sombra de um lado
    d.chord((cx - rx, cy - ry, cx + rx, cy + ry), 20, 160, fill=PELE_S)        # queixo mais escuro
    # olhos fundos e vazios: órbita escura e pupila enorme, sem brilho
    olhar = p["olhar"] * rx * 0.08
    olhos = [(cx + rx * 0.45, cy - ry * 0.12)] if lado else [(cx - rx * 0.4, cy - ry * 0.14), (cx + rx * 0.4, cy - ry * 0.14)]
    for ex, ey in olhos:
        R = rx * 0.3
        d.ellipse((ex - R * 1.3, ey - R * 1.25, ex + R * 1.3, ey + R * 1.35), fill=(62, 58, 58))
        d.ellipse((ex - R, ey - R, ex + R, ey + R), fill=(214, 212, 206), outline=(20, 20, 24), width=int(o))
        pr = R * 0.72
        d.ellipse((ex + olhar - pr, ey - pr, ex + olhar + pr, ey + pr), fill=(6, 6, 8))
    # sorriso enorme, de bochecha a bochecha (abre conforme "sorriso" de 0 a 1)
    s = max(0.0, min(1.2, p["sorriso"]))
    larg = rx * (0.3 + 0.62 * s)
    alt = ry * (0.06 + 0.4 * s)
    by = cy + ry * 0.3
    bx = cx + (rx * 0.35 if lado else 0)
    sobe = alt * 0.55                                  # cantos da boca puxados para cima
    d.chord((bx - larg, by - alt * 0.9 - sobe * 0.3, bx + larg, by + alt), 0, 180, fill=(12, 8, 10), outline=(20, 20, 24))
    for sx in (-1, 1):                                 # vincos nos cantos do sorriso
        x0 = bx + sx * larg
        d.line((x0, by - alt * 0.15, x0 + sx * rx * 0.08, by - alt * 0.15 - sobe), fill=(70, 66, 64), width=int(o))
    if s > 0.35:                                       # dentes finos
        n = 11
        for i in range(n):
            x = bx - larg * 0.85 + i * (larg * 1.7 / (n - 1))
            d.line((x, by + alt * 0.02, x, by + alt * 0.22), fill=(140, 136, 130), width=int(max(1, o * 0.8)))


def desenhar_rosto(pose: dict, altura: int):
    """Close do rosto (para o susto final)."""
    p = {**POSE_A, **pose}
    u = altura * S
    img = Image.new("RGBA", (int(u * 0.8), int(u)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    L = _LapisEscuro(d, u)
    L.o = max(2.0, u * 0.004)
    cx, cy = img.width / 2, img.height * 0.5
    rx, ry = u * 0.3, u * 0.38
    cab = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dc = ImageDraw.Draw(cab)
    Lc = _LapisEscuro(dc, u)
    Lc.o = L.o
    _rosto(dc, Lc, cx, cy, rx, ry, u, p, False)
    if p["cab_inc"]:
        cab = cab.rotate(-p["cab_inc"], resample=Image.BICUBIC, center=(cx, cy))
    img.alpha_composite(cab)
    img = img.reduce(S)
    # o rosto surge da escuridão: centro iluminado, bordas afundando no preto
    import numpy as np
    a = np.asarray(img).astype(float)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.sqrt(((xx - w / 2) / (w * 0.42)) ** 2 + ((yy - h * 0.46) / (h * 0.5)) ** 2)
    luz = np.clip(0.8 - 0.85 * dist ** 1.3, 0.03, 0.8)[..., None]
    a[..., :3] *= luz
    grao = np.random.default_rng(int(p.get("sorriso", 1) * 1000)).normal(0, 7, (h, w, 1))
    a[..., :3] = np.clip(a[..., :3] + grao * (a[..., 3:] > 0), 0, 255)
    return Image.fromarray(a.astype("uint8")), {"rosto": (cx / S, cy / S)}


# ---------------------------------------------------------------- movimento
def _cabeca_estalando(t, semente=3, amp=22.0):
    rnd = random.Random(semente)
    marcos = [0.0]
    angs = [0.0]
    while marcos[-1] < t + 5:
        marcos.append(marcos[-1] + rnd.uniform(1.3, 3.0))
        angs.append(rnd.choice([-1, 1]) * rnd.uniform(amp * 0.4, amp))
    for i in range(1, len(marcos)):
        if t < marcos[i]:
            return angs[i - 1] + (angs[i] - angs[i - 1]) * max(0.0, (t - (marcos[i] - 0.08)) / 0.08)
    return angs[-1]


def animar(acao: str, t: float, dur: float = 4.0, espelhar: bool = False) -> dict:
    cabeca = _cabeca_estalando(t)
    pose = {"cab_inc": cabeca, "olhar": math.sin(t * 0.4) * 0.3, "espelhar": espelhar, "sorriso": 1.0}
    respira = math.sin(t * 2 * math.pi / 4.5)
    if acao == "andando":                         # caminhada lenta e dura, de frente, vindo na direção da câmera
        c = t * 2 * math.pi / 1.6
        s = math.sin(c)
        pose.update(vista="frente", pe_e=max(0.0, s) * 0.3, pe_d=max(0.0, -s) * 0.3,
                    ombro_e=8 + 6 * s, ombro_d=8 - 6 * s, cotovelo_e=6, cotovelo_d=6,
                    y=abs(math.cos(c)) * 0.008, cab_inc=cabeca * 0.6, dedos=0.3)
    elif acao == "observando":                    # agachado, cabeça torta, espiando
        pose.update(vista="lado", y=-0.2, quadril_e=80, joelho_e=150, quadril_d=70, joelho_d=140, tronco=28,
                    ombro_d=70 + respira * 3, cotovelo_d=-40, ombro_e=40, cotovelo_e=60,
                    cab_inc=cabeca * 1.3 - 10, dedos=0.6)
    elif acao == "ataque":                         # avança curvado, braços abertos como garras
        c = t * 2 * math.pi / 1.0
        s = math.sin(c)
        pose.update(vista="lado", tronco=35, y=-0.06, quadril_e=-28 * s + 10, quadril_d=28 * s + 10,
                    joelho_e=max(0.0, 50 * math.sin(c - 1.1)) + 20, joelho_d=max(0.0, 50 * math.sin(c + math.pi - 1.1)) + 20,
                    ombro_e=95 + 10 * s, cotovelo_e=-25, ombro_d=105 - 10 * s, cotovelo_d=-20, dedos=1.0,
                    cab_inc=-12 + cabeca * 0.3)
    elif acao == "bizarro":                        # de corpo inteiro, encara a câmera: cabeça tomba devagar e estala
        k = min(1.0, t / max(1.0, dur * 0.7))          # o sorriso vai rasgando ao longo da cena
        tomba = 38 * math.sin(min(t, dur) * 0.9) + _cabeca_estalando(t, semente=7, amp=30) * 0.6
        pose.update(vista="frente", sorriso=0.55 + 0.65 * k, cab_inc=tomba, cab_escala=1.18,
                    ombro_e=9 + respira * 1.5, ombro_d=9 - respira * 1.5, cotovelo_e=4, cotovelo_d=4,
                    tronco=4 * math.sin(t * 0.6), y=respira * 0.003, dedos=0.5 + 0.5 * abs(math.sin(t * 5.3)))
    else:                                          # parado: imóvel, só a respiração e a cabeça estalando
        pose.update(vista="frente", ombro_e=7 + respira, ombro_d=7 - respira, cotovelo_e=5, cotovelo_d=5,
                    y=respira * 0.002, dedos=0.15 + 0.1 * math.sin(t * 0.7))
    return pose
