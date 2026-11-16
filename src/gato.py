"""O gato do protagonista, desenhado pelo código a cada quadro (mesmo traço do boneco).

Gato laranja com peito e patas brancas, cabeça de frente (dois olhos, como nos desenhos) e corpo de lado.
    img, info = desenhar(pose, altura)   # info["pes"] = ponto do chão (entre as patas)
    pose = animar(acao, t, dur)          # parado | andando | correndo | sentado | deitado | escondido | assustado | miando
"""
import math

from PIL import Image, ImageDraw

from .boneco import TRACO, _Lapis

S = 2
COR = {"pelo": (228, 138, 56), "pelo_s": (196, 110, 40), "listra": (170, 88, 30), "branco": (246, 240, 230),
       "rosa": (236, 150, 160), "olho": (250, 250, 246), "pupila": (20, 18, 24), "iris": (168, 200, 84)}

POSE_BASE = {"modo": "em_pe", "espelhar": False, "arco": 0.0, "corpo_y": 0.0, "cab_y": 0.0, "cab_inc": 0.0,
             "fd": 0.0, "fe": 0.0, "td": 0.0, "te": 0.0, "rabo": 0.0, "rabo_alto": 0.4, "rabo_eriçado": 0.0,
             "olhos": 1.0, "pupila": 0.45, "olhar": 0.0, "orelhas": 0.0, "boca": 0.0, "respira": 0.0}


def _pt(o, x, y, u, esp):
    return (o[0] + (-x if esp else x) * u, o[1] + y * u)


def desenhar(pose: dict, altura: int):
    """altura = altura do gato em pé (do chão ao topo das orelhas), em pixels."""
    p = {**POSE_BASE, **pose}
    u = altura * S / 0.95                       # 1 unidade ~ comprimento do corpo
    img = Image.new("RGBA", (int(u * 2.0), int(u * 1.25)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    L = _Lapis(d, u * 1.9)
    esp = p["espelhar"]
    o = (img.width / 2, img.height - u * 0.06)  # chão, no meio do gato
    P = lambda x, y: _pt(o, x, y, u, esp)       # noqa: E731
    pelo, sombra, branco = COR["pelo"], COR["pelo_s"], COR["branco"]
    modo = p["modo"]
    resp = p["respira"] * 0.008
    w_perna = 0.1 * u

    # ------------------------------------------------ rabo (atrás de tudo)
    if modo == "sentado":
        base = (-0.12, -0.12)
    elif modo in ("deitado", "escondido"):
        base = (-0.38, -0.12)
    else:
        base = (-0.36, -0.46 - p["corpo_y"])
    pts, ang = [base], 200.0 if modo in ("sentado", "deitado", "escondido") else 140.0 - 55 * p["rabo_alto"]
    n = 9
    for i in range(n):
        onda = math.sin(p["rabo"] + i * 0.55) * (10 + 3 * i) * (0.4 if modo in ("deitado", "escondido") else 1.0)
        curva = -14 if modo == "sentado" else (-6 if i < 4 else (-14 if p["rabo_eriçado"] < 0.5 else -2))
        ang += curva + onda * 0.25
        a = math.radians(ang)
        x, y = pts[-1]
        pts.append((x + math.cos(a) * 0.075, y - math.sin(a) * 0.075))
    larg = 0.085 * (1 + 0.9 * p["rabo_eriçado"])
    for i in range(n):
        cor = COR["listra"] if i % 3 == 2 else pelo
        L.capsula(P(*pts[i]), P(*pts[i + 1]), larg * u * (1 - 0.25 * i / n), cor)

    # ------------------------------------------------ corpo e patas
    if modo == "em_pe":
        cy = -0.42 - p["corpo_y"]
        quadril, ombro = (-0.27, cy + 0.02), (0.24, cy)
        meio = ((quadril[0] + ombro[0]) / 2, cy - 0.04 - 0.22 * p["arco"])

        def pata(raiz, ang, frente, cor):
            joelho = (raiz[0] + math.sin(math.radians(ang)) * 0.17, raiz[1] + math.cos(math.radians(ang)) * 0.17)
            dobra = 18 if frente else -22
            pe = (joelho[0] + math.sin(math.radians(ang + dobra)) * 0.2, joelho[1] + math.cos(math.radians(ang + dobra)) * 0.2)
            pe = (pe[0], min(pe[1], 0.0))
            L.capsula(P(*raiz), P(*joelho), w_perna * 1.05, cor)
            L.capsula(P(*joelho), P(*pe), w_perna * 0.9, cor)
            L.elipse(*P(pe[0] + 0.03, pe[1] - 0.02), 0.055 * u, 0.035 * u, branco)

        # patas de trás do lado de lá (mais escuras)
        pata((quadril[0] + 0.04, quadril[1] + 0.06), p["te"], False, sombra)
        pata((ombro[0] - 0.03, ombro[1] + 0.08), p["fe"], True, sombra)
        # corpo: duas cápsulas que formam o arco das costas
        L.capsula(P(*quadril), P(*meio), 0.33 * u * (1 + resp), pelo)
        L.capsula(P(*meio), P(*ombro), 0.32 * u * (1 + resp), pelo)
        d_ = 0.33 * u * 0.5
        d.line([P(*quadril), P(*meio), P(*ombro)], fill=pelo, width=int(d_ * 1.6), joint="curve")
        # listras nas costas
        for k in (0.25, 0.45, 0.65):
            bx = quadril[0] + (ombro[0] - quadril[0]) * k
            by = meio[1] - 0.12 + abs(k - 0.5) * 0.1
            d.line([P(bx - 0.02, by), P(bx + 0.02, by + 0.07)], fill=COR["listra"], width=int(u * 0.03))
        L.elipse(*P(ombro[0] + 0.04, ombro[1] + 0.06), 0.11 * u, 0.12 * u, branco, traco=False)   # peito
        pata((quadril[0] - 0.02, quadril[1] + 0.06), p["td"], False, pelo)
        pata((ombro[0] + 0.02, ombro[1] + 0.08), p["fd"], True, pelo)
        pescoco = (ombro[0] + 0.1, ombro[1] - 0.12)
        cab = (ombro[0] + 0.19, ombro[1] - 0.24 + p["cab_y"])
    elif modo == "sentado":
        L.elipse(*P(-0.08, -0.17), 0.21 * u, 0.17 * u, sombra)                     # coxa de lá
        L.capsula(P(-0.02, -0.2), P(0.08, -0.5 + resp), 0.3 * u, pelo)             # tronco em pé
        L.elipse(*P(-0.04, -0.15), 0.22 * u, 0.16 * u, pelo)                      # coxa de cá
        L.elipse(*P(0.06, -0.03), 0.09 * u, 0.04 * u, branco)                     # pata de trás
        L.elipse(*P(0.12, -0.36), 0.1 * u, 0.15 * u, branco, traco=False)          # peito
        for dx, cor in ((0.1, sombra), (0.17, pelo)):                              # patas da frente retas
            L.capsula(P(dx, -0.36), P(dx + 0.01, -0.03), w_perna * 0.95, cor)
            L.elipse(*P(dx + 0.03, -0.025), 0.05 * u, 0.032 * u, branco)
        pescoco = (0.1, -0.52)
        cab = (0.12, -0.66 + p["cab_y"])
    else:                                                                          # deitado / escondido
        baixo = 0.04 if modo == "escondido" else 0.0
        L.elipse(*P(-0.06, -0.15 + baixo), 0.4 * u, 0.16 * u * (1 + resp), pelo)
        for k in (-0.2, 0.0, 0.18):
            d.line([P(k, -0.29 + baixo), P(k + 0.03, -0.22 + baixo)], fill=COR["listra"], width=int(u * 0.03))
        L.elipse(*P(0.26, -0.03), 0.07 * u, 0.035 * u, branco)
        L.elipse(*P(0.33, -0.03), 0.07 * u, 0.035 * u, branco)
        pescoco = (0.25, -0.22 + baixo)
        cab = (0.33, -0.3 + baixo + p["cab_y"])

    # ------------------------------------------------ cabeça (de frente)
    r = 0.17 * u
    cx, cy = P(*cab)
    inc = p["cab_inc"] * (-1 if esp else 1)
    # orelhas (para trás = abaixadas e abertas)
    for lado in (-1, 1):
        ab = p["orelhas"]
        base1 = (cx + lado * r * 0.25, cy - r * 0.75)
        base2 = (cx + lado * r * 0.95, cy - r * (0.35 + 0.2 * ab))
        topo = (cx + lado * r * (0.75 + 0.45 * ab), cy - r * (1.45 - 0.6 * ab))
        L.poligono([base1, topo, base2], pelo)
        meio_ = ((base1[0] + base2[0]) / 2, (base1[1] + base2[1]) / 2)
        d.polygon([((base1[0] + meio_[0]) / 2, (base1[1] + meio_[1]) / 2), ((topo[0] * 2 + meio_[0]) / 3, (topo[1] * 2 + meio_[1]) / 3),
                   ((base2[0] + meio_[0]) / 2, (base2[1] + meio_[1]) / 2)], fill=COR["rosa"])
    L.elipse(cx, cy, r * 1.08, r * 0.95, pelo)
    # bochechas brancas e focinho
    L.elipse(cx, cy + r * 0.42, r * 0.55, r * 0.38, branco, traco=False)
    for k in (-0.35, 0.0, 0.35):                                                  # listrinhas da testa
        d.line([(cx + k * r, cy - r * 0.92), (cx + k * r * 0.8, cy - r * 0.62)], fill=COR["listra"], width=int(u * 0.022))
    # olhos
    abre = max(0.08, p["olhos"])
    for lado in (-1, 1):
        ex, ey = cx + lado * r * 0.42 + inc * r * 0.1, cy - r * 0.08
        rx, ry = r * 0.27, r * 0.3 * abre
        L.elipse(ex, ey, rx, ry, COR["olho"])
        if abre > 0.3:
            L.elipse(ex + p["olhar"] * rx * 0.3, ey, rx * 0.7, ry * 0.75, COR["iris"], traco=False)
            pr = rx * (0.18 + 0.45 * p["pupila"])
            d.ellipse((ex + p["olhar"] * rx * 0.3 - pr * 0.6, ey - ry * 0.62, ex + p["olhar"] * rx * 0.3 + pr * 0.6, ey + ry * 0.62),
                      fill=COR["pupila"])
            d.ellipse((ex - rx * 0.32, ey - ry * 0.5, ex - rx * 0.08, ey - ry * 0.22), fill=(255, 255, 255))
    # nariz, boca e bigodes
    nx, ny = cx, cy + r * 0.25
    d.polygon([(nx - r * 0.11, ny - r * 0.05), (nx + r * 0.11, ny - r * 0.05), (nx, ny + r * 0.08)], fill=COR["rosa"])
    lw = max(2, int(u * 0.012))
    if p["boca"] > 0.15:
        a = p["boca"]
        d.ellipse((nx - r * 0.16, ny + r * 0.1, nx + r * 0.16, ny + r * (0.18 + 0.35 * a)), fill=(120, 40, 50), outline=TRACO, width=lw)
    else:
        d.arc((nx - r * 0.2, ny, nx, ny + r * 0.2), 0, 160, fill=TRACO, width=lw)
        d.arc((nx, ny, nx + r * 0.2, ny + r * 0.2), 20, 180, fill=TRACO, width=lw)
    for lado in (-1, 1):
        for k in (-0.12, 0.05):
            d.line([(cx + lado * r * 0.45, ny + k * r), (cx + lado * r * 1.25, ny + k * r * 2.2 - r * 0.05)],
                   fill=(250, 245, 235), width=lw)

    img = img.resize((img.width // S, img.height // S), Image.LANCZOS)
    info = {"pes": (img.width / 2, img.height - u * 0.06 / S), "rosto": (cx / S, cy / S)}
    return img, info


def animar(acao: str, t: float, dur: float = 4.0, espelhar: bool = False) -> dict:
    """Pose do gato no instante t."""
    pis = 1.0 if (t % 3.7) > 0.12 else 0.1                  # pisca de vez em quando
    p = {"espelhar": espelhar, "rabo": t * 2.2, "respira": math.sin(t * 2.6), "olhos": pis,
         "olhar": math.sin(t * 0.7) * 0.6}
    if acao in ("andando", "correndo"):
        f = t * (9.0 if acao == "correndo" else 5.2)
        amp = 34 if acao == "correndo" else 22
        p.update(fd=math.sin(f) * amp, te=math.sin(f) * amp, fe=-math.sin(f) * amp, td=-math.sin(f) * amp,
                 corpo_y=abs(math.sin(f)) * (0.03 if acao == "correndo" else 0.012), rabo_alto=0.75,
                 cab_y=math.sin(f * 2) * 0.01, olhar=0.8)
        if acao == "correndo":
            p.update(orelhas=0.6, pupila=0.9, rabo_alto=0.2)
    elif acao == "sentado":
        p.update(modo="sentado", rabo=t * 1.2)
    elif acao == "miando":
        m = max(0.0, math.sin(t * 2.4))                     # abre a boca devagar, como num miado
        p.update(modo="sentado", boca=m, olhos=1.0 - 0.4 * m, cab_y=-0.03 * m, rabo=t * 1.2)
    elif acao == "deitado":
        p.update(modo="deitado", olhos=0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * 0.8)) * pis, rabo=t * 0.8)
    elif acao == "escondido":
        p.update(modo="escondido", pupila=1.0, orelhas=0.7, rabo=t * 3.0)
    elif acao == "assustado":
        tr = math.sin(t * 40) * 0.006
        p.update(arco=1.0, corpo_y=0.06 + tr, rabo_alto=1.0, rabo_eriçado=1.0, orelhas=1.0, pupila=1.0,
                 boca=0.55 + 0.25 * math.sin(t * 5), fd=-8, fe=8, td=10, te=-6, rabo=t * 0.6, olhar=0.0)
    else:                                                    # parado: em pé, rabo balançando
        p.update(rabo_alto=0.6)
    return p
