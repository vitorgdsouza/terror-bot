"""Rufus, o cão farejador da policial (pastor grande), e o "falso Rufus": algo vestido com a pele dele.

Desenho de perfil (virado para a direita; espelhar vira para a esquerda), mesmo traço do boneco.
    img, info = desenhar(pose, altura, falso=False)   # info["pes"] = ponto do chão
    pose = animar(acao, t, dur)    # parado | andando | correndo | sentado | deitado | brincando | de_pe (só o falso)
O falso tem as pernas compridas demais e dobradas do jeito errado, mãos humanas no lugar das patas da frente,
pele frouxa com dobras, orelhas caídas, olho humano e um sorriso de dentes de gente.
"""
import math

from PIL import Image, ImageDraw

from .boneco import TRACO, _Lapis

S = 2
COR = {"pelo": (186, 132, 74), "pelo_s": (150, 102, 56), "sela": (40, 32, 28), "barriga": (214, 176, 120),
       "nariz": (24, 20, 20), "lingua": (206, 92, 104), "pele": (212, 168, 150), "olho_h": (236, 232, 222)}

POSE_BASE = {"modo": "quatro", "espelhar": False, "fd": 0.0, "fe": 0.0, "td": 0.0, "te": 0.0, "corpo_y": 0.0,
             "cab_y": 0.0, "cab_inc": 0.0, "rabo": 0.0, "rabo_alto": 0.5, "boca": 0.0, "lingua": 0.0, "olhos": 1.0,
             "respira": 0.0}


def desenhar(pose: dict, altura: int, falso: bool = False):
    p = {**POSE_BASE, **pose}
    u = altura * S / (1.45 if p["modo"] == "de_pe" else 1.0)
    img = Image.new("RGBA", (int(u * 2.2), int(u * 1.7)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    L = _Lapis(d, u * 1.6)
    esp = p["espelhar"]
    o = (img.width / 2, img.height - u * 0.05)

    def P(x, y):
        return (o[0] + (-x if esp else x) * u, o[1] + y * u)

    pelo, sombra, sela = COR["pelo"], COR["pelo_s"], COR["sela"]
    if falso:                                   # pelo opaco e sem vida
        pelo, sombra, sela = (150, 116, 80), (118, 90, 62), (44, 38, 34)
    resp = p["respira"] * 0.01
    perna = 1.35 if falso else 1.0             # pernas compridas demais
    wl = 0.085 * u * (0.8 if falso else 1.0)

    def pata(raiz, ang, frente, cor, mao=False):
        a1 = math.radians(ang)
        joelho = (raiz[0] + math.sin(a1) * 0.2 * perna, raiz[1] + math.cos(a1) * 0.2 * perna)
        dobra = (22 if frente else -28) * (-1 if falso and not frente else 1)   # joelho de trás dobrado ao contrário
        a2 = math.radians(ang + dobra)
        pe = (joelho[0] + math.sin(a2) * 0.21 * perna, min(0.0, joelho[1] + math.cos(a2) * 0.21 * perna))
        L.capsula(P(*raiz), P(*joelho), wl * 1.1, cor)
        L.capsula(P(*joelho), P(*pe), wl, cor if not mao else COR["pele"] if falso else cor)
        if mao:                                   # mão humana: palma e dedos compridos
            cx, cy = P(pe[0] + 0.03, pe[1] - 0.01)
            r = u * 0.045
            d.ellipse((cx - r, cy - r * 0.7, cx + r, cy + r * 0.7), fill=COR["pele"], outline=TRACO, width=max(2, int(L.o)))
            for k in range(4):
                fx = cx + (-1 if esp else 1) * (r * 0.6 + k * r * 0.12)
                d.line((fx, cy, fx + (-1 if esp else 1) * r * 0.9, cy + r * (0.2 + 0.15 * k)), fill=COR["pele"], width=max(3, int(r * 0.32)))
        else:
            L.elipse(*P(pe[0] + 0.035, pe[1] - 0.015), 0.055 * u, 0.03 * u, sela if falso else sombra)

    modo = p["modo"]
    # ------------------------------------------------ rabo
    if modo != "de_pe":
        base = (-0.38, -0.6 - p["corpo_y"]) if modo in ("quatro",) else (-0.3, -0.22)
        pts, ang = [base], (160 - 70 * p["rabo_alto"]) if not falso else 235
        if modo == "deitado":
            ang = 182 if not falso else 190
        for i in range(7):
            ang += (-6 if not falso else 2) + math.sin(p["rabo"] + i * 0.6) * (8 if not falso else 1)
            a = math.radians(ang)
            pts.append((pts[-1][0] + math.cos(a) * 0.07, pts[-1][1] - math.sin(a) * 0.07))
        for i in range(7):
            L.capsula(P(*pts[i]), P(*pts[i + 1]), 0.07 * u * (1 - 0.4 * i / 7), sela if i > 3 else pelo)

    # ------------------------------------------------ corpo
    if modo == "quatro":
        cy = -0.58 * (perna if falso else 1) - p["corpo_y"]
        quadril, ombro = (-0.3, cy), (0.28, cy - 0.04)
        pata((quadril[0] + 0.05, cy + 0.06), p["te"], False, sombra)
        pata((ombro[0] - 0.04, cy + 0.08), p["fe"], True, sombra, mao=falso)
        L.capsula(P(*quadril), P(*ombro), 0.34 * u * (0.82 if falso else 1) * (1 + resp), pelo)
        L.elipse(*P(-0.02, cy - 0.08), 0.28 * u, 0.1 * u, sela, traco=False)                   # sela preta
        L.elipse(*P(0.06, cy + 0.1), 0.24 * u, 0.06 * u, COR["barriga"] if not falso else sombra, traco=False)
        if falso:                                                                               # dobras da pele frouxa
            for k in (-0.2, -0.08, 0.04, 0.16):
                d.arc((*P(k - 0.05, cy - 0.02), *P(k + 0.05, cy + 0.14)) if not esp else
                      (P(k + 0.05, cy - 0.02)[0], P(k + 0.05, cy - 0.02)[1], P(k - 0.05, cy + 0.14)[0], P(k - 0.05, cy + 0.14)[1]),
                      200, 340, fill=sombra, width=max(2, int(u * 0.01)))
        pata((quadril[0] - 0.02, cy + 0.06), p["td"], False, pelo)
        pata((ombro[0] + 0.02, cy + 0.08), p["fd"], True, pelo, mao=falso)
        pesc = (ombro[0] + 0.08, ombro[1] - 0.14)
        cab = (ombro[0] + 0.2 + (0.04 if falso else 0), ombro[1] - (0.22 if not falso else 0.02) + p["cab_y"])
    elif modo == "sentado":
        L.capsula(P(-0.18, -0.18), P(0.1, -0.62 + resp), 0.34 * u, pelo)
        L.elipse(*P(-0.2, -0.16), 0.22 * u, 0.15 * u, pelo)
        L.elipse(*P(-0.05, -0.5), 0.18 * u, 0.12 * u, sela, traco=False)
        for dx, cor in ((0.12, sombra), (0.2, pelo)):
            L.capsula(P(dx, -0.45), P(dx + 0.01, -0.03), wl, cor)
            L.elipse(*P(dx + 0.035, -0.02), 0.055 * u, 0.03 * u, sombra)
        pesc, cab = (0.16, -0.68), (0.24, -0.86 + p["cab_y"])
    elif modo == "deitado":
        L.elipse(*P(-0.05, -0.17), 0.46 * u * (1.15 if falso else 1), 0.15 * u * (1 + resp), pelo)
        L.elipse(*P(-0.08, -0.24), 0.32 * u, 0.07 * u, sela, traco=False)
        if falso:                                    # patas de trás compridas demais esticadas para trás
            L.capsula(P(-0.4, -0.08), P(-0.85, -0.04), wl, pelo)
            L.capsula(P(0.3, -0.06), P(0.62, -0.03), wl * 0.9, COR["pele"])
            cx, cy = P(0.66, -0.035)
            r = u * 0.045
            d.ellipse((cx - r, cy - r * 0.7, cx + r, cy + r * 0.7), fill=COR["pele"], outline=TRACO, width=max(2, int(L.o)))
        else:
            L.capsula(P(0.3, -0.06), P(0.52, -0.04), wl, pelo)
            L.elipse(*P(0.55, -0.035), 0.055 * u, 0.03 * u, sombra)
        pesc, cab = (0.36, -0.22), (0.48, -0.3 + p["cab_y"])
    else:                                            # de_pe: em duas pernas, como gente
        quadril, ombro = (0.0, -0.66), (0.12, -1.12)                     # curvado para a frente
        for dx, cor in ((-0.09, sombra), (0.09, pelo)):              # pernas de gente, afastadas
            L.capsula(P(dx * 0.6, -0.66), P(dx, -0.33), wl * 1.25, cor)
            L.capsula(P(dx, -0.33), P(dx * 1.2, -0.03), wl * 1.1, cor)
            L.elipse(*P(dx * 1.2 + 0.04, -0.02), 0.07 * u, 0.03 * u, sela)
        L.capsula(P(*quadril), P(*ombro), 0.3 * u, pelo)
        L.elipse(*P(0.02, -0.86), 0.1 * u, 0.24 * u, sela, traco=False)
        for k in (-0.95, -0.82, -0.7):
            d.line((*P(-0.09, k), *P(0.1, k + 0.03)), fill=sombra, width=max(2, int(u * 0.01)))
        for dx, cor in ((0.02, sombra), (0.2, pelo)):                # braços compridos pendurados, com mãos
            L.capsula(P(dx, -1.08), P(dx + 0.04, -0.72), wl, cor)
            L.capsula(P(dx + 0.04, -0.72), P(dx + 0.05, -0.38), wl * 0.9, COR["pele"])
            cx, cy = P(dx + 0.05, -0.35)
            r = u * 0.05
            d.ellipse((cx - r * 0.7, cy - r, cx + r * 0.7, cy + r), fill=COR["pele"], outline=TRACO, width=max(2, int(L.o)))
            for k in range(4):
                fx = cx - r * 0.5 + k * r * 0.33
                d.line((fx, cy + r * 0.6, fx, cy + r * 1.9), fill=COR["pele"], width=max(3, int(r * 0.28)))
        pesc, cab = (0.16, -1.16), (0.24 + p["cab_inc"] * 0.002, -1.24 + p["cab_y"])

    # ------------------------------------------------ cabeça de perfil
    L.capsula(P(*pesc), P(*cab), 0.17 * u * (0.8 if falso else 1), pelo)
    hx, hy = cab
    L.elipse(*P(hx, hy), 0.14 * u, 0.12 * u, pelo)
    baixo = modo == "de_pe"                                     # pele vestida: o focinho pende para baixo
    fx1, fy1 = (hx + 0.16, hy + 0.2) if baixo else (hx + 0.24, hy + 0.05)
    L.capsula(P(hx + 0.06, hy + 0.03), P(fx1, fy1), 0.11 * u, pelo)                            # focinho
    L.elipse(*P(hx + 0.02, hy - 0.03), 0.1 * u, 0.06 * u, sela, traco=False)
    if falso:                                                                                   # orelhas caídas
        L.poligono([P(hx - 0.06, hy - 0.08), P(hx - 0.16, hy + 0.1), P(hx - 0.02, hy - 0.02)], sela)
    else:
        L.poligono([P(hx - 0.07, hy - 0.08), P(hx - 0.03, hy - 0.3), P(hx + 0.04, hy - 0.09)], sela)
    L.elipse(*P(fx1 + 0.03, fy1 + 0.0), 0.035 * u, 0.028 * u, COR["nariz"], traco=False)
    ex, ey = P(hx + 0.07, hy - 0.025)
    if falso:                                                                                   # olho humano, branco e fixo
        rx, ry = 0.04 * u, 0.026 * u * max(0.2, p["olhos"])
        d.ellipse((ex - rx, ey - ry, ex + rx, ey + ry), fill=COR["olho_h"], outline=TRACO, width=max(2, int(L.o)))
        d.ellipse((ex - rx * 0.3, ey - ry * 0.6, ex + rx * 0.3, ey + ry * 0.6), fill=(30, 40, 50))
        # sorriso de dentes humanos ao longo do focinho
        mx0, my0 = P(hx + 0.06, hy + 0.08)
        mx1, my1 = P(fx1, fy1 + 0.03)
        d.line((mx0, my0, mx1, my1), fill=TRACO, width=max(3, int(u * 0.012)))
        n = 7
        for k in range(n):
            x = mx0 + (mx1 - mx0) * (k + 0.5) / n
            y = my0 + (my1 - my0) * (k + 0.5) / n
            d.rectangle((x - u * 0.008, y - u * 0.012, x + u * 0.008, y + u * 0.004), fill=(236, 230, 214))
    else:
        r = 0.022 * u * max(0.15, p["olhos"])
        d.ellipse((ex - 0.022 * u, ey - r, ex + 0.022 * u, ey + r), fill=TRACO)
        if p["boca"] > 0.1:
            L.capsula(P(hx + 0.14, hy + 0.08), P(hx + 0.1, hy + 0.16 + 0.05 * p["lingua"]), 0.04 * u, COR["lingua"])

    img = img.resize((img.width // S, img.height // S), Image.LANCZOS)
    return img, {"pes": (img.width / 2, img.height - u * 0.05 / S)}


def animar(acao: str, t: float, dur: float = 4.0, espelhar: bool = False, falso: bool = False) -> dict:
    p = {"espelhar": espelhar, "rabo": t * (6 if not falso else 0.5), "respira": math.sin(t * (3 if not falso else 0.8)),
         "olhos": 1.0 if (t % 3.3) > 0.12 else 0.1}
    if acao in ("andando", "correndo", "brincando"):
        f = t * (11 if acao != "andando" else 6) * (0.55 if falso else 1)
        amp = 38 if acao != "andando" else 24
        p.update(fd=math.sin(f) * amp, te=math.sin(f) * amp, fe=-math.sin(f) * amp, td=-math.sin(f) * amp,
                 corpo_y=abs(math.sin(f)) * (0.05 if acao != "andando" else 0.015), rabo_alto=0.9,
                 boca=1.0 if acao != "andando" else 0.4, lingua=abs(math.sin(f)))
        if acao == "brincando":
            p["corpo_y"] = abs(math.sin(t * 5)) * 0.12
    elif acao == "sentado":
        p.update(modo="sentado", boca=0.6 if not falso else 0, lingua=0.5)
    elif acao == "deitado":
        p.update(modo="deitado", cab_y=(0.0 if not falso else 0.04) + 0.01 * math.sin(t))
    elif acao == "de_pe":
        tomba = 18 * math.sin(min(t, dur) * 0.7)
        p.update(modo="de_pe", cab_inc=tomba, cab_y=0.01 * math.sin(t * 1.3))
    elif acao == "levantando_cabeca":
        k = min(1.0, t / max(0.8, dur * 0.6))
        p.update(modo="deitado", cab_y=0.04 - 0.12 * k * k * (3 - 2 * k))
    else:
        p.update(rabo_alto=0.5)
    return p
