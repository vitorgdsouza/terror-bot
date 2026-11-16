"""Boneco articulado desenhado pelo código, no estilo de desenho animado simples.

Ele tem cabeça, tronco, braços e pernas com articulações (ombro, cotovelo, quadril, joelho), expressões
(olhos, sobrancelhas e boca) e objetos que segura de verdade (celular, lanterna). Por ser desenhado a cada
quadro, pode andar, virar, sentar, segurar coisas e mudar a cara sem nunca deformar.

Uso:  img = desenhar(pose, altura)  ->  imagem RGBA com os pés no centro da borda de baixo.
A pose é um dicionário (veja POSE_BASE); as animações prontas ficam em animar(acao, t, ...).
"""
import math

from PIL import Image, ImageDraw

S = 2                       # desenha em tamanho dobrado e reduz no fim (bordas suaves)
CONTORNO = (22, 20, 28, 255)

VISUAIS = {
    "homem": {"pele": (236, 206, 178), "cabelo": (58, 40, 30), "blusa": (98, 112, 62), "blusa_esc": (78, 90, 48),
              "calca": (58, 60, 70), "tenis": (232, 232, 236), "cabelo_tipo": "bagunçado"},
    "mulher": {"pele": (238, 210, 186), "cabelo": (24, 22, 28), "blusa": (214, 168, 48), "blusa_esc": (180, 138, 34),
               "calca": (52, 70, 110), "tenis": (232, 232, 236), "cabelo_tipo": "franja"},
}

POSE_BASE = {
    "vista": "frente",          # frente | lado | costas
    "espelhar": False,          # de lado: False olha para a direita, True para a esquerda
    "olhos": "normal",          # normal | arregalados | fechados | apertados
    "sobrancelhas": "neutras",  # neutras | preocupadas | bravas | erguidas
    "boca": "reta",             # reta | aberta | grito | triste | nenhuma
    "olhar": 0.0,               # -1..1: para onde os olhos olham (esq/dir)
    "cabeca_inclina": 0.0,      # graus
    "cabeca_vira": 0.0,         # de lado: 1 = rosto virado para a câmera (olhando para trás)
    "tronco_inclina": 0.0,      # graus (para frente +)
    "respira": 0.0,             # 0..1
    "y": 0.0,                   # sobe/desce o corpo (fração da altura), ex.: passo, agachar
    # ângulos a partir do braço/perna esticado para baixo (graus); + = para frente/para fora
    "ombro_e": 6, "cotovelo_e": 6, "ombro_d": 6, "cotovelo_d": 6,
    "quadril_e": 0, "joelho_e": 0, "quadril_d": 0, "joelho_d": 0,
    "objeto": None,             # None | celular | lanterna
    "luz_objeto": 1.0,
}


def _capsula(d, p1, p2, larg, cor, contorno=True):
    if contorno:
        d.line([p1, p2], fill=CONTORNO, width=int(larg + 5 * S))
        for p in (p1, p2):
            r = (larg + 5 * S) / 2
            d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=CONTORNO)
    d.line([p1, p2], fill=cor, width=int(larg))
    for p in (p1, p2):
        r = larg / 2
        d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=cor)


def _membro(origem, ang1, ang2, l1, l2, sentido=1):
    """Pontas do segmento superior e inferior. Ângulos em graus a partir da vertical para baixo."""
    a1 = math.radians(ang1) * sentido
    j = (origem[0] + math.sin(a1) * l1, origem[1] + math.cos(a1) * l1)
    a2 = a1 + math.radians(ang2) * sentido
    f = (j[0] + math.sin(a2) * l2, j[1] + math.cos(a2) * l2)
    return j, f


def _escurecer(cor, k=0.78):
    return tuple(int(c * k) for c in cor[:3])


def desenhar(pose: dict, altura: int, quem: str = "homem") -> Image.Image:
    p = {**POSE_BASE, **pose}
    v = VISUAIS.get(quem, VISUAIS["homem"])
    H = altura * S
    larg_tela = int(H * 1.1)
    img = Image.new("RGBA", (larg_tela, int(H * 1.08)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = larg_tela / 2
    chao = img.height - int(H * 0.03)
    dy = -p["y"] * H
    vista = p["vista"]
    lado = vista == "lado"
    sentido = 1                                     # desenha de lado olhando para a direita e espelha no fim

    quadril = (cx, chao - H * 0.36 + dy)
    resp = p["respira"] * H * 0.006
    tronco_inc = math.radians(p["tronco_inclina"])
    alt_tronco = H * 0.25 + resp
    ombro_c = (quadril[0] + math.sin(tronco_inc) * alt_tronco, quadril[1] - math.cos(tronco_inc) * alt_tronco)
    larg_tronco = H * (0.17 if lado else 0.25)
    coxa, canela = H * 0.175, H * 0.165
    braco, antebraco = H * 0.135, H * 0.125
    w_perna, w_braco = H * 0.085, H * 0.07

    def perna(lado_x, q, jo, cor_calca, cor_tenis):
        orig = (quadril[0] + lado_x, quadril[1])
        j, f = _membro(orig, q, -abs(jo) if lado else jo, coxa, canela, sentido)
        _capsula(d, orig, j, w_perna, cor_calca)
        _capsula(d, j, f, w_perna * 0.92, cor_calca)
        # tênis
        frente = 1 if lado else 0
        pe = (f[0] + (H * 0.035 * frente), f[1] + H * 0.012)
        r = H * 0.032
        d.ellipse((pe[0] - r * 1.5 - 2.5 * S, pe[1] - r - 2.5 * S, pe[0] + r * 1.5 + 2.5 * S, pe[1] + r * 0.7 + 2.5 * S), fill=CONTORNO)
        d.ellipse((pe[0] - r * 1.5, pe[1] - r, pe[0] + r * 1.5, pe[1] + r * 0.7), fill=cor_tenis)

    def bracinho(lado_x, o, c, cor, cor_mao, objeto=None):
        orig = (ombro_c[0] + lado_x, ombro_c[1] + H * 0.02)
        s = sentido if lado else (1 if lado_x > 0 else -1)
        j, f = _membro(orig, o, c, braco, antebraco, s)
        _capsula(d, orig, j, w_braco, cor)
        _capsula(d, j, f, w_braco * 0.95, cor)
        r = H * 0.032
        d.ellipse((f[0] - r - 2.5 * S, f[1] - r - 2.5 * S, f[0] + r + 2.5 * S, f[1] + r + 2.5 * S), fill=CONTORNO)
        d.ellipse((f[0] - r, f[1] - r, f[0] + r, f[1] + r), fill=cor_mao)
        if objeto:
            _objeto(objeto, f, j)
        return f

    def _objeto(tipo, mao, cotovelo):
        ang = math.atan2(mao[1] - cotovelo[1], mao[0] - cotovelo[0])
        if tipo == "celular":
            w, h = H * 0.07, H * 0.12
            box = (mao[0] - w / 2, mao[1] - h * 0.85, mao[0] + w / 2, mao[1] + h * 0.15)
            d.rounded_rectangle((box[0] - 2.5 * S, box[1] - 2.5 * S, box[2] + 2.5 * S, box[3] + 2.5 * S), radius=int(H * 0.01), fill=CONTORNO)
            d.rounded_rectangle(box, radius=int(H * 0.008), fill=(30, 32, 40))
            m = H * 0.006
            luz = int(200 + 55 * p["luz_objeto"])
            d.rectangle((box[0] + m, box[1] + m, box[2] - m, box[3] - m), fill=(170, 215, luz))
        elif tipo == "lanterna":
            comp, gro = H * 0.11, H * 0.032
            dx, dy_ = math.cos(ang), math.sin(ang)
            a = (mao[0] - dx * comp * 0.2, mao[1] - dy_ * comp * 0.2)
            b = (mao[0] + dx * comp * 0.8, mao[1] + dy_ * comp * 0.8)
            _capsula(d, a, b, gro, (55, 55, 62))
            r = gro * 0.75
            d.ellipse((b[0] - r, b[1] - r, b[0] + r, b[1] + r), fill=(255, 246, 205))

    # ------------------------------------------------------------ ordem de desenho
    escuro = lambda c: _escurecer(c, 0.7)
    obj_e = obj_d = None
    if p["objeto"]:
        obj_d = p["objeto"]            # sempre na mão da frente / direita
    if lado:
        perna(0, p["quadril_e"], p["joelho_e"], escuro(v["calca"]), escuro(v["tenis"]))
        bracinho(0, p["ombro_e"], p["cotovelo_e"], escuro(v["blusa"]), escuro(v["pele"]))
    else:
        perna(-H * 0.06, p["quadril_e"], p["joelho_e"], v["calca"], v["tenis"])
        perna(H * 0.06, p["quadril_d"], p["joelho_d"], v["calca"], v["tenis"])

    # tronco (moletom)
    t1, t2 = ombro_c, quadril
    lt, lb = larg_tronco / 2, larg_tronco / 2 * 0.94
    base_y = t2[1] + H * 0.035
    dxi = (t1[0] - t2[0])
    corpo = [(t1[0] - lt * 0.82, t1[1]), (t1[0] + lt * 0.82, t1[1]), (t1[0] + lt, t1[1] + H * 0.04),
             (t2[0] + lb, base_y), (t2[0] - lb, base_y), (t1[0] - lt, t1[1] + H * 0.04)]
    d.polygon(corpo, fill=v["blusa"], outline=CONTORNO)
    d.line(corpo + [corpo[0]], fill=CONTORNO, width=int(2.8 * S), joint="curve")
    # sombra do moletom (luz vindo da esquerda)
    sombra = [(t1[0] + lt * 0.35, t1[1] + H * 0.01), (t1[0] + lt * 0.8, t1[1] + H * 0.01), (t1[0] + lt * 0.97, t1[1] + H * 0.045),
              (t2[0] + lb * 0.97, base_y - 2 * S), (t2[0] + lb * 0.4, base_y - 2 * S)]
    d.polygon(sombra, fill=v["blusa_esc"])
    barra = (t2[0] - lb, base_y - H * 0.03, t2[0] + lb, base_y)
    d.rounded_rectangle(barra, radius=int(H * 0.01), fill=v["blusa_esc"], outline=CONTORNO, width=int(2.5 * S))
    if not lado and vista == "frente":
        bolso = (t2[0] - larg_tronco * 0.3, t2[1] - H * 0.075, t2[0] + larg_tronco * 0.3, t2[1] - H * 0.005)
        d.rounded_rectangle(bolso, radius=int(H * 0.015), outline=_escurecer(v["blusa"], 0.6), width=int(2.5 * S))
        for sx in (-1, 1):
            d.line((t1[0] + sx * H * 0.025, t1[1] + H * 0.04, t1[0] + sx * H * 0.028, t1[1] + H * 0.10),
                   fill=(235, 235, 235), width=int(2 * S))
    if lado:
        perna(0, p["quadril_d"], p["joelho_d"], v["calca"], v["tenis"])

    # braços
    if lado:
        bracinho(0, p["ombro_d"], p["cotovelo_d"], v["blusa"], v["pele"], obj_d)
    else:
        bracinho(-larg_tronco * 0.5, p["ombro_e"], p["cotovelo_e"], v["blusa"], v["pele"], obj_e)
        bracinho(larg_tronco * 0.5, p["ombro_d"], p["cotovelo_d"], v["blusa"], v["pele"], obj_d)

    # capuz atrás do pescoço
    gola = (ombro_c[0], ombro_c[1] + H * 0.005)
    rw, rh = H * (0.08 if lado else 0.11), H * 0.035
    d.ellipse((gola[0] - rw, gola[1] - rh, gola[0] + rw, gola[1] + rh), fill=v["blusa_esc"], outline=CONTORNO, width=int(2.5 * S))

    # cabeça
    cab_c = (ombro_c[0] + math.sin(tronco_inc) * H * 0.02, ombro_c[1] - H * 0.15)
    cab = Image.new("RGBA", (int(H * 0.46), int(H * 0.46)), (0, 0, 0, 0))
    _cabeca(ImageDraw.Draw(cab), cab.width / 2, cab.height / 2, H, p, v, vista)
    if p["cabeca_inclina"]:
        cab = cab.rotate(-p["cabeca_inclina"], resample=Image.BICUBIC, center=(cab.width / 2, cab.height * 0.7))
    img.alpha_composite(cab, (int(cab_c[0] - cab.width / 2), int(cab_c[1] - cab.height / 2)))

    if lado and p["espelhar"]:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    img = img.resize((img.width // S, img.height // S), Image.LANCZOS)
    return noturno(img, p.get("noite", 0.38))


def noturno(img: Image.Image, k: float) -> Image.Image:
    """Escurece e puxa para o azul, para o boneco combinar com os cenários à noite."""
    if k <= 0:
        return img
    r, g, b, a = img.split()
    r = r.point(lambda x: int(x * (1 - 0.52 * k)))
    g = g.point(lambda x: int(x * (1 - 0.45 * k)))
    b = b.point(lambda x: int(x * (1 - 0.25 * k)))
    return Image.merge("RGBA", (r, g, b, a))


def _cabeca(d, cx, cy, H, p, v, vista):
    rx, ry = H * 0.13, H * 0.145
    o = 2.8 * S
    lado = vista == "lado"
    vira = p["cabeca_vira"] if lado else 0.0     # 0 = perfil, 1 = rosto para a câmera
    # orelha
    if vista == "frente" or (lado and vira < 0.5):
        for sx in ((-1, 1) if vista == "frente" else (-0.15,)):
            ox = cx + sx * rx * (0.98 if vista == "frente" else 1)
            d.ellipse((ox - H * 0.022 - o, cy - H * 0.01 - o, ox + H * 0.022 + o, cy + H * 0.035 + o), fill=CONTORNO)
            d.ellipse((ox - H * 0.022, cy - H * 0.01, ox + H * 0.022, cy + H * 0.035), fill=v["pele"])
    d.ellipse((cx - rx - o, cy - ry - o, cx + rx + o, cy + ry + o), fill=CONTORNO)
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=v["pele"])
    if vista == "costas":
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry * 0.75), fill=v["cabelo"])
        return
    # cabelo
    if v["cabelo_tipo"] == "franja":
        d.chord((cx - rx - o, cy - ry - o, cx + rx + o, cy + ry * 0.55), 180, 360, fill=v["cabelo"])
        if not lado:
            d.rectangle((cx - rx * 1.02, cy - ry * 0.25, cx + rx * 1.02, cy - ry * 0.12), fill=v["cabelo"])
        else:
            d.rectangle((cx - rx * 0.6, cy - ry * 0.3, cx + rx * 0.55, cy - ry * 0.2), fill=v["cabelo"])
        if not lado:
            for sx in (-1, 1):
                d.rectangle((cx + sx * rx * 0.82 - H * 0.025, cy - ry * 0.2, cx + sx * rx * 0.82 + H * 0.025, cy + ry * 0.55), fill=v["cabelo"])
        else:
            d.rectangle((cx - rx * 1.02, cy - ry * 0.3, cx - rx * 0.45, cy + ry * 0.62), fill=v["cabelo"])
    else:
        d.chord((cx - rx - o, cy - ry - o, cx + rx + o, cy + ry * 0.35), 180, 360, fill=v["cabelo"])
        pontas = []
        for i in range(7):
            a = math.pi + i * math.pi / 6
            r1 = 1.04 + (0.16 if i % 2 else 0.02)
            pontas.append((cx + math.cos(a) * rx * r1, cy - ry * 0.05 + math.sin(a) * ry * r1))
        d.polygon(pontas + [(cx + rx, cy - ry * 0.1), (cx - rx, cy - ry * 0.1)], fill=v["cabelo"])
        if lado:
            d.rectangle((cx - rx * 1.0, cy - ry * 0.2, cx - rx * 0.5, cy + ry * 0.2), fill=v["cabelo"])
    # rosto
    if lado and vira < 0.5:
        fx, esp = cx + rx * 0.5, 0                   # perfil: um olho só, perto da frente
        olhos = [(fx, cy)]
        d.polygon([(cx + rx * 0.97, cy + ry * 0.05), (cx + rx * 1.12, cy + ry * 0.2), (cx + rx * 0.95, cy + ry * 0.28)],
                  fill=v["pele"], outline=CONTORNO)
    else:
        desloc = rx * 0.15 * p["olhar"]
        olhos = [(cx - rx * 0.4 + desloc, cy), (cx + rx * 0.4 + desloc, cy)]
    r = H * 0.012
    for (ex, ey) in olhos:
        if p["olhos"] == "fechados":
            d.line((ex - r * 1.6, ey + r * 0.3, ex + r * 1.6, ey + r * 0.3), fill=CONTORNO, width=int(3 * S))
        elif p["olhos"] == "arregalados":
            R = r * 2.1
            d.ellipse((ex - R - 2 * S, ey - R - 2 * S, ex + R + 2 * S, ey + R + 2 * S), fill=CONTORNO)
            d.ellipse((ex - R, ey - R, ex + R, ey + R), fill=(250, 250, 250))
            px = ex + R * 0.35 * p["olhar"]
            d.ellipse((px - r * 0.8, ey - r * 0.8, px + r * 0.8, ey + r * 0.8), fill=CONTORNO)
        elif p["olhos"] == "apertados":
            d.ellipse((ex - r, ey - r * 0.5, ex + r, ey + r * 0.5), fill=CONTORNO)
        else:
            d.ellipse((ex - r, ey - r * 1.15, ex + r, ey + r * 1.15), fill=CONTORNO)
        # sobrancelha
        sb = p["sobrancelhas"]
        by = ey - r * (3.2 if p["olhos"] == "arregalados" else 2.6)
        dentro = 1 if (len(olhos) == 2 and ex < cx) else -1
        if len(olhos) == 1:
            dentro = -1
        inc = {"neutras": 0, "preocupadas": -1, "bravas": 1, "erguidas": 0}[sb]
        sobe = r * 1.2 if sb == "erguidas" else 0
        x1, x2 = ex - r * 2 * dentro, ex + r * 2 * dentro
        d.line((x1, by - sobe + inc * r * 0.8, x2, by - sobe - inc * r * 0.8), fill=CONTORNO, width=int(3 * S))
    # boca
    bx = cx + (rx * 0.5 if lado and vira < 0.5 else rx * 0.15 * p["olhar"])
    byc = cy + ry * 0.48
    if p["boca"] == "reta":
        d.line((bx - H * 0.018, byc, bx + H * 0.018, byc), fill=CONTORNO, width=int(3 * S))
    elif p["boca"] == "triste":
        d.arc((bx - H * 0.022, byc, bx + H * 0.022, byc + H * 0.025), 200, 340, fill=CONTORNO, width=int(3 * S))
    elif p["boca"] in ("aberta", "grito"):
        w, h = (H * 0.018, H * 0.016) if p["boca"] == "aberta" else (H * 0.03, H * 0.04)
        d.ellipse((bx - w, byc - h * 0.6, bx + w, byc + h), fill=(70, 25, 30), outline=CONTORNO, width=int(2.5 * S))


# ---------------------------------------------------------------- animações prontas
def _piscar(t, fase=0.0):
    return ((t + fase) % 3.6) < 0.13


def animar(acao: str, t: float, dur: float = 4.0, medo: float = 0.0, objeto=None, espelhar=False) -> dict:
    """Pose do boneco no instante t para uma ação. medo (0..1) muda a expressão e faz tremer."""
    resp = 0.5 + 0.5 * math.sin(t * 2 * math.pi / (1.6 if medo > 0.5 else 3.2))
    pose = {"respira": resp, "objeto": objeto, "espelhar": espelhar}
    olhos = "fechados" if _piscar(t) else ("arregalados" if medo > 0.6 else "normal")
    pose.update(olhos=olhos,
                sobrancelhas="preocupadas" if medo > 0.3 else "neutras",
                boca="aberta" if medo > 0.8 else ("triste" if medo > 0.4 else "reta"))
    treme = math.sin(t * 50) * 1.2 * max(0.0, medo - 0.6)

    if acao in ("andando", "entrando", "saindo"):
        ciclo = t * 2 * math.pi / 0.9                    # um passo a cada 0,45 s
        s = math.sin(ciclo)
        pose.update(vista="lado", quadril_e=-24 * s, quadril_d=24 * s,
                    joelho_e=max(0, 35 * math.sin(ciclo + 1.2)), joelho_d=max(0, 35 * math.sin(ciclo + math.pi + 1.2)),
                    ombro_e=20 * s, ombro_d=-20 * s, cotovelo_e=18, cotovelo_d=18,
                    y=abs(math.cos(ciclo)) * 0.012, tronco_inclina=4)
        if objeto == "lanterna":
            pose.update(ombro_d=75, cotovelo_d=8)
        elif objeto == "celular":
            pose.update(ombro_d=40, cotovelo_d=95, cabeca_inclina=8)
    elif acao == "olhando_tras":
        pose.update(vista="lado", cabeca_vira=1.0, olhos="arregalados" if not _piscar(t) else "fechados",
                    sobrancelhas="preocupadas", ombro_e=-8, ombro_d=8)
    elif acao == "celular":
        pose.update(vista="frente", ombro_d=-12, cotovelo_d=-150, ombro_e=-6, cotovelo_e=-25,
                    cabeca_inclina=5 * (1 - medo), olhar=-0.2, objeto="celular")
    elif acao == "lanterna":
        pose.update(vista="lado", ombro_d=78 + math.sin(t * 1.3) * 4, cotovelo_d=6, ombro_e=10, cotovelo_e=20,
                    objeto="lanterna", tronco_inclina=3)
    elif acao == "encolhido":
        pose.update(vista="frente", y=-0.16, quadril_e=-70, joelho_e=120, quadril_d=70, joelho_d=-120,
                    ombro_e=-30, cotovelo_e=-110, ombro_d=-30, cotovelo_d=-110, olhos="arregalados",
                    sobrancelhas="preocupadas", boca="triste")
    elif acao == "costas":
        pose.update(vista="costas")
    else:                                                # parado
        olhar = math.sin(t * 0.7) * 0.6 if medo < 0.5 else math.sin(t * 2.3) * 0.8
        pose.update(vista="frente", olhar=olhar, ombro_e=6 + treme, ombro_d=6 - treme,
                    cabeca_inclina=math.sin(t * 0.5) * 2)
        if medo > 0.6:
            pose.update(ombro_e=-20 + treme, cotovelo_e=-115, ombro_d=-20 - treme, cotovelo_d=-115)
    pose["cabeca_inclina"] = pose.get("cabeca_inclina", 0) + treme
    return pose
