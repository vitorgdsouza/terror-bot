"""Formato "voce": terror minimalista em segunda pessoa, no ritmo dos vídeos que estão indo bem no TikTok.

Visual de 2 ou 3 cores (fundo + figuras chapadas + um destaque), uma imagem nova a cada frase, tudo se mexendo,
interface de celular e relógio na tela, e regras ("REGRA 1") falando com VOCÊ. Não precisa de ilustração:
tudo é desenhado em código. A legenda é grande, com 1 a 3 palavras, e a palavra forte em cor (montagem.py).

Roteiro: "formato": "voce", "paleta": noite | sangue | papel, "hora": "03:14" (relógio do canto, que anda com o vídeo),
         "parte": "PARTE 1" (selo no alto, opcional)
Cena: {"narracao": "...", "quadro": "<tipo>", ...}
  ligacao      celular tocando; "nome" (quem liga, ex.: "VOCÊ", "MÃE"), "estado": tocando | atendida | recusada
  chat         conversa aparecendo; "msgs": [["ele", "abre a porta"], ["voce", "quem é?"]], "nome" no topo
  relogio      relógio grande; "hora": "03:16", "vira": "03:17" (vira no meio da cena, em vermelho)
  andares      prédio em corte; "andares": 12, "voce": 11, "de": 1, "ate": 11 (algo subindo andar por andar)
  mapa         ruas vistas de cima; um ponto vem até VOCÊ; "eta": "12:00" (contagem regressiva), "rotulo": "VIATURA"
  regra        cartão "REGRA n"; "n": 1, "texto": "não abra" (escrita de máquina)
  porta        porta de frente com olho mágico; "luz": true (luz por baixo), "pes": true (sombra de pés),
               "batendo": true (a porta treme), "aberta": true (fresta preta)
  olho_magico  a visão pelo olho mágico; "figura": pessoa | oco | ninguem, "vapor": true (sai vapor da boca),
               "embaca": true (o vidro embaça), "geada": true (geada no cabelo; "derrete": true ela some)
  silhueta     você no cômodo; "acao": parado | andando | tremendo | escondido, "outra": true (outra figura no canto)
  texto        palavras grandes no meio, escrita de máquina; "texto": "NÃO ATENDA" ("|" quebra a linha)
  preto        tela preta
Ciência (paleta "ciencia", canal E Se Fosse Real?):
  planeta      a Terra girando no espaço; "eixo": true (mostra o eixo), "balanca": true (eixo bamboleando), "lua": false, "some_lua": true, "para": true (rotação freia), "vento": true, "ponto" (ponto pulsando), "seta" (seta empurrando para baixo), "rotulo"
  terra_corte  a Terra em corte com o buraco; "de"/"ate" (0 a 1: posição de quem cai), "rotulo" (ex.: "5.400 °C")
  espaco       astronauta flutuando; "sem_capacete": true, "segundos": 15 (contagem regressiva)
  numero       número grande contando; "de", "ate", "antes" (ex.: "QUASE"), "ano": true (sem ponto de milhar), "unidade" (km/h), "rotulo"
  comparar     barras crescendo; "itens": [["Furacão", 300], ["Sem rotação", 1670]], "unidade": "km/h", "numeros": false (só as barras)
  multidao     multidão em fileiras pulando; "pulando": false, "ondas" (som se espalhando), "celulares" (+ "sem_sinal"), "andando", "transito" (estrada lotada de carros), "rotulo"
  sol          o Sol e a Terra em órbita; "apaga", "apagado", "onda" (a última luz indo até a Terra), "tangente" (a Terra sai em linha reta), "so_terra" + "congela" (a Terra virando gelo), "rotulo"
  buraco_negro buraco negro com disco de gás; "de"/"ate" (0 longe, 1 na borda: astronauta caindo), "congela" (parece parar na borda, avermelhando), "atravessa", "dentro" (o céu vira um círculo que encolhe), "estica" (espaguetificação; com "pequeno": true estica antes da borda), "rotulo"
  aneis        a Terra com anel; "asteroide", "quebra", "forma" (o anel se fecha), "faixa" + "crateras" (faixa de 30° do equador), "cai", "sombra", "gelo", "some", "ceu" (arco no céu visto do chão), "rotulo"
  astro        qualquer planeta no visual novo; "nome", "com" (outro planeta ao lado), "zoom", "nave", "brilho" (calor), "rotulo"
  pouso        o você no chão de um planeta (igual ao vídeo longo); "nome" (mercurio, venus, marte, terra, lua), "efeitos" (calor, frio, pressao, vento, poeira, noite, sol_nasce), "traje" (0 a 1), "pose"
  perfuracao   poço de sondagem em corte; "de"/"ate" (metros), "medidor": false, "termometro": [de, ate] °C, "calor", "treme", "fosseis", "agua", "lama"; modos "boca" (+ "medida"), "perfil" (você ao lado do poço), "planeta" (a marca minúscula na Terra em corte), "rotulo"
  impacto      o asteroide dos dinossauros; "espaco" (+ "de"/"ate", "impacto"); paisagem com dinossauros e você: "bola", "plumas", "vento", "tsunami", "fogo", "escuro", "frio", "vazio", "ave", "voce": false, "rotulo"
  mergulho     submarino descendo; "de"/"ate" (metros no medidor), "luz", "peixe", "pressao", "fonte" (fonte de calor no fundo), "escala": true (mar em corte com o Everest dentro), "medidor": false, "rotulo"
  apophis      o asteroide que passa em 2029; vista em escala com o anel dos satélites ("de"/"ate", "orbita", "espreme", "medida", "mira"); modos "perto", "data", "tamanho", "risco" (+ "recorde", "valor"), "ceu" (+ "gente"), "mapa"
  estrela      Betelgeuse em Órion ("linhas", "destaca", "explode", "brilha", "apaga", "lua"); modos "tamanho", "neutrinos", "supernova", "dia", "sombra", "longe", "meses" (+ "ate")
  oceano       descida pelas camadas do mar ("de"/"ate" em metros; "peixes", "lulas", "brilho", "cachalote", "paredes", "peixe_caracol", "fundo", "nome_zona": false); modo "zonas" (o mar em corte)
Em qualquer cena: "foco": [x, y, zoom] (close fixo), "seguir": true (close acompanhando quem cai, no terra_corte), "alerta": true (borda vermelha piscando), "susto": true (tremor), "texto_topo": "aviso no alto".
"""
import math
import random
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .util import RAIZ

W, H, FPS = 1080, 1920, 24
PALETAS = {
    "noite": {"fundo": (13, 19, 44), "fundo2": (24, 33, 70), "fig": (238, 240, 248), "acento": (232, 44, 56),
              "acento2": (255, 199, 64), "apagado": (70, 84, 128)},
    "sangue": {"fundo": (128, 8, 18), "fundo2": (60, 2, 8), "fig": (12, 5, 8), "acento": (250, 245, 240),
               "acento2": (255, 210, 90), "apagado": (90, 10, 18)},
    "ciencia": {"fundo": (8, 18, 46), "fundo2": (22, 50, 104), "fig": (245, 247, 252), "acento": (255, 196, 36),
                "acento2": (86, 214, 255), "apagado": (66, 96, 150)},
    "papel": {"fundo": (8, 8, 10), "fundo2": (26, 26, 30), "fig": (236, 236, 236), "acento": (230, 40, 46),
              "acento2": (255, 199, 64), "apagado": (70, 70, 78)},
}
FONTE = str(RAIZ / "assets" / "fontes" / "Poppins-Bold.ttf")
MONO = next((p for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
                         "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf", FONTE) if Path(p).exists()))
_cache: dict = {}


def _f(px, mono=False):
    k = (px, mono)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(MONO if mono else FONTE, px)
    return _cache[k]


def _suave(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def _fundo(p) -> Image.Image:
    k = ("fundo", p["fundo"])
    if k not in _cache:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - H * 0.45) / (H * 0.55)) ** 2).clip(0, 1)[..., None]
        a = np.array(p["fundo2"], np.float32) * (1 - d) + np.array(p["fundo"], np.float32) * d
        _cache[k] = Image.fromarray(a.astype(np.uint8))
    return _cache[k]


def _centro_texto(d, cx, cy, txt, fonte, cor):
    b = d.textbbox((0, 0), txt, font=fonte)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], cy - (b[3] - b[1]) / 2 - b[1]), txt, font=fonte, fill=cor)


# ---------------------------------------------------------------- figuras
def _pessoa(d, cx, chao, alt, cor, t=0.0, acao="parado", oco=False, fundo=(0, 0, 0), olhos=True):
    """Pictograma de pessoa: cabeça redonda e corpo arredondado. O Oco é mais alto e de olhos vazios."""
    if oco:
        alt *= 1.12
    balanco = math.sin(t * 7) * alt * 0.012 if acao == "andando" else 0
    treme = math.sin(t * 47) * alt * 0.006 if acao == "tremendo" else 0
    x = cx + treme
    r = alt * 0.13
    topo = chao - alt
    corpo = (x - alt * 0.17, topo + r * 2.25 + balanco, x + alt * 0.17, chao - alt * 0.36)
    d.rounded_rectangle(corpo, radius=int(alt * 0.12), fill=cor)
    perna = alt * 0.07
    passo = math.sin(t * 7) * alt * 0.05 if acao == "andando" else 0
    d.rounded_rectangle((x - alt * 0.14 + passo, chao - alt * 0.42, x - alt * 0.14 + perna * 2 + passo, chao), radius=int(perna), fill=cor)
    d.rounded_rectangle((x + alt * 0.14 - perna * 2 - passo, chao - alt * 0.42, x + alt * 0.14 - passo, chao), radius=int(perna), fill=cor)
    inclina = math.sin(t * 1.3) * r * 0.25 if oco else 0
    hx, hy = x + inclina, topo + r + balanco
    d.ellipse((hx - r, hy - r, hx + r, hy + r), fill=cor)
    if olhos:
        o = r * 0.16
        for s in (-1, 1):
            ex = hx + s * r * 0.36
            d.ellipse((ex - o, hy - o, ex + o, hy + o), fill=fundo)
            if not oco:                                  # gente tem pupila; o Oco não
                d.ellipse((ex - o * 0.45, hy - o * 0.2, ex + o * 0.45, hy + o * 0.7), fill=cor)
    return hx, hy, r


def _celular(d, cx, cy, w, h, p):
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=int(w * 0.13), fill=p["fundo"],
                        outline=p["fig"], width=8)
    d.rounded_rectangle((cx - w * 0.12, cy - h / 2 + 22, cx + w * 0.12, cy - h / 2 + 40), radius=9, fill=p["apagado"])


# ---------------------------------------------------------------- quadros
def _ligacao(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    cx, cy, w, h = W / 2, H * 0.47, 560, 1040
    estado = cena.get("estado", "tocando")
    sx = math.sin(t * 60) * 6 if estado == "tocando" and (t % 1.2) < 0.6 else 0
    cx += sx
    if estado == "tocando":                              # ondas saindo do celular
        for k in range(3):
            fase = ((t * 0.9 + k / 3) % 1)
            rr = 300 + fase * 380
            cor = tuple(int(c * (1 - fase) + f * fase) for c, f in zip(p["acento"], p["fundo"]))
            d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=cor, width=6)
    _celular(d, cx, cy, w, h, p)
    av = 120
    ay = cy - 230
    d.ellipse((cx - av, ay - av, cx + av, ay + av), fill=p["apagado"])
    _pessoa(d, cx, ay + av * 0.95, av * 1.55, p["fig"], olhos=False)
    _centro_texto(d, cx, cy - 40, cena.get("nome", "DESCONHECIDO"), _f(64), p["fig"])
    if estado == "atendida":
        seg = int(t)
        _centro_texto(d, cx, cy + 40, f"00:{seg:02d}", _f(40, True), p["acento2"])
        for k in range(14):                              # ondas de voz
            a = abs(math.sin(t * 9 + k * 0.8)) * 60 + 8
            x = cx - 210 + k * 32
            d.rounded_rectangle((x, cy + 150 - a, x + 16, cy + 150 + a), radius=8, fill=p["fig"])
    else:
        _centro_texto(d, cx, cy + 40, "chamando..." if estado == "tocando" else "recusada", _f(38, True), p["apagado"])
    by = cy + h / 2 - 150
    for bx, cor in ((cx - 140, p["acento"]), (cx + 140, (60, 190, 90))):
        if estado == "recusada" and bx > cx:
            continue
        pulsa = 1 + 0.08 * math.sin(t * 8) if estado == "tocando" else 1
        rb = 62 * pulsa
        d.ellipse((bx - rb, by - rb, bx + rb, by + rb), fill=cor)
    if estado == "recusada":
        d.line((cx - 220, cy - 360, cx + 220, cy + 360), fill=p["acento"], width=18)


def _chat(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    cx, cy, w, h = W / 2, H * 0.43, 880, 1180
    _celular(d, cx, cy, w, h, p)
    _centro_texto(d, cx, cy - h / 2 + 95, cena.get("nome", "DESCONHECIDO"), _f(50), p["fig"])
    d.line((cx - w / 2 + 30, cy - h / 2 + 140, cx + w / 2 - 30, cy - h / 2 + 140), fill=p["apagado"], width=3)
    msgs = cena.get("msgs") or []
    passo = max(0.5, dur * 0.75 / max(1, len(msgs)))
    y = cy - h / 2 + 180
    fonte = _f(56)
    for i, (lado, txt) in enumerate(msgs):
        if t < 0.2 + i * passo:
            if t > 0.2 + i * passo - 0.5:                 # "digitando..."
                pts = "•" * (1 + int(t * 4) % 3)
                x0 = cx - w / 2 + 50 if lado != "voce" else cx + w / 2 - 170
                d.rounded_rectangle((x0, y, x0 + 140, y + 84), radius=36, fill=p["apagado"])
                d.text((x0 + 26, y + 6), pts, font=fonte, fill=p["fig"])
            break
        linhas, atual = [], ""
        for pal in str(txt).split():
            teste = (atual + " " + pal).strip()
            if d.textlength(teste, font=fonte) > w * 0.68:
                linhas.append(atual)
                atual = pal
            else:
                atual = teste
        linhas.append(atual)
        bw = max(d.textlength(lin, font=fonte) for lin in linhas) + 60
        bh = 76 * len(linhas) + 34
        meu = lado == "voce"
        x0 = cx + w / 2 - 50 - bw if meu else cx - w / 2 + 50
        cor = p["acento"] if lado in ("ele", "oco") else (p["apagado"] if not meu else p["fig"])
        d.rounded_rectangle((x0, y, x0 + bw, y + bh), radius=32, fill=cor)
        for k, lin in enumerate(linhas):
            d.text((x0 + 30, y + 12 + 76 * k), lin, font=fonte, fill=p["fundo"] if meu else p["fig"])
        y += bh + 30


def _relogio(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    hora, vira = cena.get("hora", "03:16"), cena.get("vira")
    virou = bool(vira) and t > dur * 0.5
    txt = vira if virou else hora
    if not virou and (t % 1) < 0.5:
        txt = txt.replace(":", " ")
    cor = p["acento"] if virou else p["fig"]
    escala = 1.0 + (0.12 * max(0, 1 - (t - dur * 0.5) * 4) if virou else 0)
    _centro_texto(d, W / 2, H * 0.43, txt, _f(int(250 * escala), True), cor)


def _andares(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    total, voce = int(cena.get("andares", 12)), int(cena.get("voce", 11))
    de, ate = int(cena.get("de", 1)), int(cena.get("ate", voce))
    x0, x1, base, alt = W * 0.3, W * 0.62, H * 0.82, H * 0.62
    h1 = alt / total
    for k in range(total):
        y = base - (k + 1) * h1
        d.rectangle((x0, y, x1, y + h1 - 6), outline=p["apagado"], width=3)
        d.text((x0 - 70, y + h1 * 0.25), f"{k + 1}º", font=_f(30, True), fill=p["apagado"])
        if k + 1 == voce:
            d.rounded_rectangle((x1 - 150, y + 12, x1 - 20, y + h1 - 18), radius=10, fill=p["acento2"])
            d.text((x1 - 140, y + 14), "VOCÊ", font=_f(30), fill=p["fundo"])
    prog = _suave(t / max(0.1, dur * 0.85))
    atual = de + (ate - de) * prog
    y = base - atual * h1 + h1 * 0.15
    d.rounded_rectangle((x0 + 30, y, x0 + 110, y + h1 * 0.7), radius=8, fill=p["acento"])
    _centro_texto(d, W * 0.82, H * 0.22, f"{int(round(atual)):02d}", _f(150, True), p["acento"])
    d.polygon([(W * 0.82 - 30, H * 0.13), (W * 0.82 + 30, H * 0.13), (W * 0.82, H * 0.13 - 40)], fill=p["acento"])


def _mapa(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    for k in range(-2, 9):                               # ruas
        y = H * 0.2 + k * 190
        d.line((0, y, W, y), fill=p["fundo2"], width=40)
        x = k * 190 + 60
        d.line((x, H * 0.12, x, H * 0.85), fill=p["fundo2"], width=40)
    destino = (W * 0.7, H * 0.32)
    origem = (W * 0.18, H * 0.78)
    pts = [origem, (origem[0], H * 0.5), (destino[0], H * 0.5), destino]
    d.line(pts, fill=p["apagado"], width=10)
    prog = _suave(t / max(0.1, dur * 0.95))
    segs = [math.dist(pts[i], pts[i + 1]) for i in range(3)]
    alvo = prog * sum(segs)
    pos = pts[0]
    for i, s in enumerate(segs):
        if alvo <= s:
            f = alvo / s
            pos = (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)
            break
        alvo -= s
        pos = pts[i + 1]
    r = 26 + 6 * math.sin(t * 6)
    d.ellipse((pos[0] - r, pos[1] - r, pos[0] + r, pos[1] + r), fill=p["acento"])
    d.ellipse((destino[0] - 30, destino[1] - 30, destino[0] + 30, destino[1] + 30), fill=p["acento2"])
    d.text((destino[0] - 60, destino[1] - 95), "VOCÊ", font=_f(44), fill=p["acento2"])
    if cena.get("eta"):
        mm, ss = (int(x) for x in str(cena["eta"]).split(":"))
        resto = max(0, mm * 60 + ss - int(t * 7))
        caixa = (W / 2 - 230, H * 0.86, W / 2 + 230, H * 0.86 + 150)
        d.rounded_rectangle(caixa, radius=24, fill=p["fundo"], outline=p["acento"], width=5)
        _centro_texto(d, W / 2, H * 0.86 + 45, cena.get("rotulo", "CHEGANDO EM"), _f(32), p["fig"])
        _centro_texto(d, W / 2, H * 0.86 + 105, f"{resto // 60:02d}:{resto % 60:02d}", _f(56, True), p["acento"])


def _regra(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    entra = _suave(t / 0.35)
    y = H * 0.36 - (1 - entra) * 120
    caixa = (W / 2 - 300, y, W / 2 + 300, y + 190)
    d.rounded_rectangle(caixa, radius=20, fill=p["fig"])
    _centro_texto(d, W / 2, y + 95, f"REGRA {cena.get('n', 1)}", _f(96), p["fundo"])
    texto = str(cena.get("texto", "")).upper()
    mostra = texto[:int(len(texto) * min(1.0, max(0.0, (t - 0.3) / max(0.3, dur * 0.5))))]
    for k, lin in enumerate(mostra.split("|")):
        _centro_texto(d, W / 2, y + 300 + k * 80, lin.strip(), _f(60, True), p["acento2"])


def _porta(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    sx = 0
    if cena.get("batendo"):
        fase = t % 1.1
        if fase < 0.45 and int(fase / 0.15) % 2 == 0:
            sx = 7
    x0, y0, x1, y1 = W * 0.29 + sx, H * 0.16, W * 0.71 + sx, H * 0.7
    d.rectangle((x0 - 26, y0 - 26, x1 + 26, y1), fill=p["apagado"])
    if cena.get("aberta"):
        d.rectangle((x0, y0, x1, y1), fill=(0, 0, 0))
        d.rectangle((x0 + (x1 - x0) * 0.3, y0, x1, y1), fill=p["fig"])
    else:
        d.rectangle((x0, y0, x1, y1), fill=p["fig"])
        for yy in (0.18, 0.55):
            d.rectangle((x0 + 50, y0 + (y1 - y0) * yy, x1 - 50, y0 + (y1 - y0) * (yy + 0.3)), outline=p["fundo2"], width=5)
        d.ellipse((W / 2 - 22 + sx, y0 + 150, W / 2 + 22 + sx, y0 + 194), fill=p["fundo"])     # olho mágico
        d.ellipse((x1 - 90, H * 0.5, x1 - 50, H * 0.5 + 40), fill=p["acento2"])                # maçaneta
    d.rectangle((0, y1, W, H), fill=p["fundo"])
    if cena.get("luz"):
        brilho = 0.75 + 0.25 * math.sin(t * 3)
        cor = tuple(int(c * brilho) for c in p["acento2"])
        d.rectangle((x0, y1, x1, y1 + 14), fill=cor)
        if cena.get("pes"):
            for px in (W / 2 - 80, W / 2 + 20):
                d.rectangle((px, y1, px + 60, y1 + 14), fill=(0, 0, 0))


def _olho_magico(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    cx, cy, r = W / 2, H * 0.44, 470
    d.rectangle((0, 0, W, H), fill=(0, 0, 0))
    lente = Image.new("RGB", (W, H), p["fundo2"])
    dl = ImageDraw.Draw(lente)
    for k in range(40):                                   # neve caindo
        rnd = random.Random(k)
        x = rnd.random() * W
        y = (rnd.random() * H + t * (80 + rnd.random() * 80)) % H
        dl.ellipse((x - 4, y - 4, x + 4, y + 4), fill=p["apagado"])
    fig = cena.get("figura", "pessoa")
    if fig != "ninguem":
        oco = fig == "oco"
        hx, hy, rr = _pessoa(dl, cx, cy + r * 1.25, r * 1.55, p["fig"] if not oco else (190, 200, 220), t, "parado", oco, p["fundo2"])
        if cena.get("vapor") and not oco:                 # gente solta vapor no frio
            fase = (t * 0.8) % 1
            vx = hx + rr * 0.2 + fase * 110
            dl.ellipse((vx - 30 - fase * 40, hy + rr * 0.55 - fase * 60, vx + 30 + fase * 40, hy + rr * 0.55 - fase * 60 + 60 + fase * 40),
                       outline=(220, 228, 240), width=4)
        if cena.get("geada"):
            derrete = cena.get("derrete") and not oco
            a = 1 - _suave((t - dur * 0.3) / max(0.3, dur * 0.5)) if derrete else 1
            if a > 0.05:
                for k in range(16):
                    ang = math.pi + k * math.pi / 15
                    gx, gy = hx + math.cos(ang) * rr * 1.02, hy + math.sin(ang) * rr * 1.02
                    tam = 10 * a
                    dl.line((gx - tam, gy, gx + tam, gy), fill=(255, 255, 255), width=3)
                    dl.line((gx, gy - tam, gx, gy + tam), fill=(255, 255, 255), width=3)
            elif derrete:
                for k in range(5):
                    gx = hx - rr * 0.8 + k * rr * 0.4
                    gy = hy - rr * 0.6 + ((t * 120 + k * 40) % 140)
                    dl.ellipse((gx - 7, gy - 10, gx + 7, gy + 10), fill=(170, 200, 255))
    mascara = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mascara).ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    if cena.get("embaca"):
        a = _suave((t - 0.3) / max(0.3, dur * 0.6))
        lente = Image.blend(lente, Image.new("RGB", (W, H), (200, 205, 215)), 0.55 * a)
    img.paste(lente, (0, 0), mascara)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=p["apagado"], width=26)


def _silhueta(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    chao = H * 0.74
    d.line((0, chao, W, chao), fill=p["apagado"], width=6)
    acao = cena.get("acao", "parado")
    x = W * 0.45
    if acao == "andando":
        x = W * 0.2 + W * 0.5 * _suave(t / max(0.1, dur))
    if acao == "escondido":
        d.rectangle((W * 0.18, chao - 520, W * 0.5, chao), fill=p["apagado"])
        x = W * 0.42
    _pessoa(d, x, chao, 560, p["fig"], t, acao, False, p["fundo"])
    if cena.get("outra"):
        a = _suave(t / max(0.1, dur * 0.6))
        cor = tuple(int(f + (c - f) * a) for c, f in zip(p["fig"], p["fundo"]))
        _pessoa(d, W * 0.84, chao, 560, cor, t, "parado", True, p["fundo"])


def _texto(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    texto = str(cena.get("texto", "")).upper()
    mostra = texto[:int(len(texto) * min(1.0, t / max(0.3, dur * 0.45)))]
    linhas = mostra.split("|")
    tam = 104                                           # diminui a letra até a linha mais longa caber na tela
    while tam > 56 and max(d.textlength(lin.strip(), font=_f(tam)) for lin in texto.split("|")) > W * 0.88:
        tam -= 6
    for k, lin in enumerate(linhas):
        _centro_texto(d, W / 2, H * 0.42 + (k - (len(texto.split("|")) - 1) / 2) * tam * 1.25, lin.strip(), _f(tam),
                      p["acento"] if k == len(linhas) - 1 else p["fig"])


QUADROS = {"ligacao": _ligacao, "chat": _chat, "relogio": _relogio, "andares": _andares, "mapa": _mapa,
           "regra": _regra, "porta": _porta, "olho_magico": _olho_magico, "silhueta": _silhueta, "texto": _texto}


# ---------------------------------------------------------------- quadros de ciência (canal E Se Fosse Real?)
OCEANO, TERRA_COR = (38, 112, 206), (72, 170, 96)


def _globo(d, cx, cy, r, t, gira=1.0):
    from . import globo
    if globo.tem_mapa():                                # Terra com os continentes de verdade (começa no Brasil)
        tr = globo.terra(r, lon=-0.9 - t * 0.35 * gira, nuvens=t * 0.25, inclina=0.3)
        d._image.paste(tr, (int(cx - tr.width / 2), int(cy - tr.height / 2)), tr)
        return
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=OCEANO)
    for k in range(5):                                  # continentes simples andando com a rotação
        rnd = random.Random(k * 7)
        lat = (rnd.random() - 0.5) * 1.4
        lon = (rnd.random() * 2 * math.pi + t * 0.6 * gira) % (2 * math.pi)
        if math.cos(lon) < 0:
            continue
        x = cx + r * math.sin(lon) * math.cos(lat)
        y = cy - r * math.sin(lat)
        tam = r * (0.18 + rnd.random() * 0.14) * (0.4 + 0.6 * math.cos(lon))
        d.ellipse((x - tam, y - tam * 0.7, x + tam, y + tam * 0.7), fill=TERRA_COR)
    for k in range(1, 4):                               # paralelos
        yy = cy - r + k * r / 2
        meia = math.sqrt(max(0, r * r - (yy - cy) ** 2))
        d.line((cx - meia, yy, cx + meia, yy), fill=(255, 255, 255, 60), width=2)


def _planeta(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img, "RGBA")
    for k in range(90):                                 # estrelas
        rnd = random.Random(k)
        x, y = rnd.random() * W, rnd.random() * H
        b = 120 + int(120 * abs(math.sin(t * 2 + k)))
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(b, b, b))
    cx, cy, r = W / 2, H * 0.45, 330
    gira = 1.0
    if cena.get("para"):                                # a rotação freia até parar
        gira = max(0.0, 1 - t / max(0.1, dur * 0.6))
    _globo(d, cx, cy, r, t if not cena.get("para") else min(t, dur * 0.6) * 0.5, gira)
    if cena.get("lua", True) is not False and not cena.get("sem_terra_lua"):
        a = t * 0.5
        lx, ly = cx + math.cos(a) * 470, cy + math.sin(a) * 160
        alfa = 255
        if cena.get("some_lua"):
            alfa = int(255 * max(0.0, 1 - t / max(0.1, dur * 0.6)))
        if alfa > 5:
            d.ellipse((lx - 60, ly - 60, lx + 60, ly + 60), fill=(220, 220, 228, alfa))
    if cena.get("balanca") or cena.get("eixo"):         # eixo da Terra; "balanca": true faz ele bambolear
        ang = math.radians(23.5 + (math.sin(t * 2.2) * 18 if cena.get("balanca") else 0))
        dx, dy = math.sin(ang) * r * 1.35, math.cos(ang) * r * 1.35
        d.line((cx - dx, cy + dy, cx + dx, cy - dy), fill=p["acento"], width=10)
    if cena.get("vento"):                               # linhas de vento varrendo para leste
        for k in range(10):
            y = cy - r * 0.8 + k * r * 0.18
            x = (t * 900 + k * 170) % (W + 400) - 200
            d.line((x, y, x + 160, y), fill=p["acento2"], width=8)
    if cena.get("ponto"):                               # um ponto pulsando: "todo mundo aqui"
        px_, py_ = cx - r * 0.28, cy - r * 0.32
        pul = 1 + 0.25 * math.sin(t * 6)
        d.ellipse((px_ - 16, py_ - 16, px_ + 16, py_ + 16), fill=p["acento"])
        for k in range(2):
            rr = (40 + k * 30) * pul
            d.ellipse((px_ - rr, py_ - rr, px_ + rr, py_ + rr), outline=p["acento"][:3] + (200 - k * 80,), width=6)
    if cena.get("seta"):                                # seta empurrando a Terra para baixo (quase nada)
        y0 = cy - r - 230 + math.sin(t * 5) * 14
        d.rectangle((cx - 22, y0, cx + 22, y0 + 120), fill=p["acento"])
        d.polygon([(cx - 60, y0 + 115), (cx + 60, y0 + 115), (cx, y0 + 190)], fill=p["acento"])
    if cena.get("rotulo"):
        _centro_texto(d, W / 2, H * (0.7 if cena.get("seta") else 0.16), str(cena["rotulo"]).upper(),
                      _fit(d, str(cena["rotulo"]).upper(), 60), p["acento"])


def _terra_corte(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    cx, cy, r = W / 2, H * 0.46, 470
    camadas = [(1.0, (150, 96, 60)), (0.97, (205, 90, 40)), (0.55, (240, 150, 40)), (0.19, (255, 230, 120))]
    for f, cor in camadas:
        d.ellipse((cx - r * f, cy - r * f, cx + r * f, cy + r * f), fill=cor)
    if cena.get("buraco", True):
        d.rectangle((cx - 22, cy - r - 30, cx + 22, cy + r + 30), fill=(10, 10, 14))
        prog = cena.get("de", 0.0) + (cena.get("ate", 1.0) - cena.get("de", 0.0)) * _suave(t / max(0.1, dur * 0.9))
        y = cy - r + prog * 2 * r
        cena["_alvo"] = (cx / W, y / H)                  # para a câmera seguir quem cai ("seguir": true)
        d.ellipse((cx - 18, y - 18, cx + 18, y + 18), fill=p["fig"])
        d.ellipse((cx - 7, y - 30, cx + 7, y - 16), fill=p["fig"])
    if cena.get("rotulo"):
        _centro_texto(d, W / 2, H * 0.83, str(cena["rotulo"]).upper(), _f(64), p["acento"])


def _espaco(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    for k in range(120):
        rnd = random.Random(k)
        x, y = rnd.random() * W, rnd.random() * H
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(200, 205, 220))
    _globo(d, W * 0.8, H * 0.95, 520, t * 0.3)
    ax, ay = W / 2 + math.sin(t * 0.8) * 40, H * 0.44 + math.cos(t * 0.6) * 30
    branco, cinza, sombra = (240, 243, 250), (190, 198, 214), (150, 158, 178)
    braco = math.sin(t * 1.4) * 18
    d.rounded_rectangle((ax - 150, ay - 40, ax - 70, ay + 150), radius=30, fill=cinza)          # mochila
    d.rounded_rectangle((ax - 110, ay - 30, ax + 110, ay + 210), radius=70, fill=branco)        # corpo
    d.rounded_rectangle((ax - 60, ay + 40, ax + 60, ay + 110), radius=14, fill=sombra)           # painel
    for k, cor in enumerate(((232, 44, 56), (86, 214, 255), (255, 196, 36))):
        d.ellipse((ax - 40 + k * 30, ay + 62, ax - 22 + k * 30, ay + 80), fill=cor)
    d.rounded_rectangle((ax - 175, ay - 10 + braco, ax - 95, ay + 150 + braco), radius=40, fill=branco)  # braços
    d.rounded_rectangle((ax + 95, ay - 10 - braco, ax + 175, ay + 150 - braco), radius=40, fill=branco)
    d.rounded_rectangle((ax - 95, ay + 180, ax - 15, ay + 330), radius=40, fill=branco)         # pernas
    d.rounded_rectangle((ax + 15, ay + 180, ax + 95, ay + 330), radius=40, fill=branco)
    d.rounded_rectangle((ax - 100, ay + 300, ax - 10, ay + 345), radius=20, fill=cinza)
    d.rounded_rectangle((ax + 10, ay + 300, ax + 100, ay + 345), radius=20, fill=cinza)
    hx, hy, hr = ax, ay - 120, 125
    if cena.get("sem_capacete"):                                                                # rosto à mostra
        d.ellipse((hx - hr * 0.78, hy - hr * 0.8, hx + hr * 0.78, hy + hr * 0.8), fill=(240, 200, 170))
        d.pieslice((hx - hr * 0.82, hy - hr * 0.88, hx + hr * 0.82, hy + hr * 0.5), 180, 360, fill=(70, 45, 30))
        for s_ in (-1, 1):
            d.ellipse((hx + s_ * 32 - 14, hy - 4, hx + s_ * 32 + 14, hy + 30), fill=(255, 255, 255))
            d.ellipse((hx + s_ * 32 - 7, hy + 6, hx + s_ * 32 + 7, hy + 22), fill=(20, 20, 30))
        d.ellipse((hx - 22, hy + 48, hx + 22, hy + 80), fill=(120, 40, 40))                       # boca aberta
    else:
        d.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=branco)
        d.rounded_rectangle((hx - hr * 0.72, hy - hr * 0.5, hx + hr * 0.72, hy + hr * 0.5), radius=60, fill=p["fundo2"])
        d.ellipse((hx - hr * 0.5, hy - hr * 0.35, hx - hr * 0.2, hy - hr * 0.1), fill=p["acento2"])
    if cena.get("segundos"):
        resto = max(0, int(cena["segundos"]) - int(t * 3))
        _centro_texto(d, W / 2, H * 0.2, f"{resto:02d}s", _f(130, True), p["acento"])


def _numero(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    de, ate = float(cena.get("de", 0)), float(cena.get("ate", 100))
    v = de + (ate - de) * _suave(t / max(0.1, dur * 0.7))
    inteiro = float(ate).is_integer() and float(de).is_integer()
    txt = f"{v:.0f}" if cena.get("ano") else f"{v:,.0f}".replace(",", ".") if inteiro else f"{v:,.1f}".replace(",", "#").replace(".", ",").replace("#", ".")
    if cena.get("antes"):                                  # palavra pequena antes do número ("QUASE", "MAIS DE")
        _centro_texto(d, W / 2, H * 0.3, str(cena["antes"]).upper(), _f(64), p["acento2"])
    _centro_texto(d, W / 2, H * 0.38, txt, _f(230, True), p["acento"])
    if cena.get("unidade"):
        _centro_texto(d, W / 2, H * 0.49, str(cena["unidade"]).upper(), _f(70), p["fig"])
    if cena.get("rotulo"):
        _centro_texto(d, W / 2, H * 0.58, str(cena["rotulo"]).upper(), _f(48), p["acento2"])


def _comparar(img, cena, t, dur, n, p):
    d = ImageDraw.Draw(img)
    itens = cena.get("itens") or []
    if not itens:
        return
    maior = max(float(v) for _, v in itens)
    x0, larg = W * 0.12, W * 0.76
    y = H * 0.3
    for k, (nome, v) in enumerate(itens):
        cresce = _suave((t - k * 0.35) / max(0.2, dur * 0.5))
        w = larg * float(v) / maior * cresce
        cor = p["acento"] if k == len(itens) - 1 else p["apagado"]
        d.text((x0, y), str(nome).upper(), font=_f(46), fill=p["fig"])
        d.rounded_rectangle((x0, y + 70, x0 + max(20, w), y + 160), radius=20, fill=cor)
        if cena.get("numeros", True):                     # "numeros": false quando a narração não fala os valores
            num = f"{float(v) * cresce:,.0f}".replace(",", ".") + " " + str(cena.get("unidade", ""))
            d.text((x0 + 10, y + 175), num, font=_f(44, True), fill=cor)
        y += 330


def _carro(d, x, y, w, cor, freio=False):
    h = w * 0.42
    d.rounded_rectangle((x - w / 2, y - h, x + w / 2, y), radius=int(w * 0.12), fill=cor)
    d.rounded_rectangle((x - w * 0.32, y - h * 1.55, x + w * 0.3, y - h * 0.9), radius=int(w * 0.1), fill=cor)
    d.rounded_rectangle((x - w * 0.26, y - h * 1.42, x + w * 0.24, y - h * 1.0), radius=int(w * 0.06), fill=(30, 50, 90))
    for s_ in (-1, 1):
        d.ellipse((x + s_ * w * 0.3 - w * 0.1, y - w * 0.1, x + s_ * w * 0.3 + w * 0.1, y + w * 0.1), fill=(20, 20, 26))
    if freio:                                                      # luz de freio acesa
        d.rectangle((x - w / 2, y - h * 0.75, x - w / 2 + w * 0.08, y - h * 0.45), fill=(255, 40, 40))
        d.rectangle((x + w / 2 - w * 0.08, y - h * 0.75, x + w / 2, y - h * 0.45), fill=(255, 40, 40))


def _multidao(img, cena, t, dur, n, p):
    """Multidão em fileiras (do fundo, pequenas, à frente, grandes), cada pessoa de uma cor. "pulando" (padrão: sim),
    "ondas": o som do pulo se espalhando; "celulares": todo mundo com o celular aceso e "SEM SINAL";
    "andando": a multidão se arrastando para o lado; "transito": estrada lotada de carros parados; "rotulo"."""
    d = ImageDraw.Draw(img, "RGBA")
    if cena.get("transito"):
        hz = H * 0.3
        d.rectangle((0, hz, W, H), fill=(40, 70, 50))
        d.polygon([(W * 0.44, hz), (W * 0.56, hz), (W * 1.25, H), (-W * 0.25, H)], fill=(52, 56, 66))
        for k in range(14):                                        # fileiras de carros até o horizonte
            f_ = (k / 14) ** 1.6
            y = H - f_ * (H - hz) - 40
            esc = 1 - f_ * 0.92
            larg_pista = (W * 1.5) * esc
            for faixa in range(-2, 3):
                x = W / 2 + faixa * larg_pista / 5 + math.sin(k * 3 + faixa) * 8 * esc
                rnd = random.Random(k * 10 + faixa)
                cor = [p["acento"], p["acento2"], (235, 235, 240), (200, 60, 60), (90, 120, 200)][rnd.randrange(5)]
                _carro(d, x, y, 150 * esc, cor, freio=(math.sin(t * 4 + k + faixa) > 0))
        if cena.get("rotulo"):
            _centro_texto(d, W / 2, H * 0.17, str(cena["rotulo"]).upper(), _fit(d, str(cena["rotulo"]).upper(), 62), p["acento"])
        return
    chao = H * 0.72
    d.rectangle((0, chao, W, H), fill=tuple(int(c * 0.6) for c in p["fundo2"]))
    cores = [p["acento"], p["acento2"], p["fig"], (232, 90, 80), (150, 220, 140), (200, 160, 255)]
    pulando = cena.get("pulando", True)
    desloca = (t * 40) if cena.get("andando") else 0
    filas = 7
    for linha in range(filas):                                     # do fundo para a frente
        prof = linha / (filas - 1)                                 # 0 = fundo, 1 = frente
        alt = 90 + 170 * prof
        y_base = H * 0.5 + (chao - H * 0.5) * prof
        passo = alt * 0.62
        qtd = int(W / passo) + 3
        for k in range(qtd):
            rnd = random.Random(linha * 100 + k)
            x = (k * passo + (linha % 2) * passo / 2 + desloca * (0.5 + prof) - passo) % (W + passo * 2) - passo
            fase = rnd.random() * 0.25
            pulo = max(0.0, math.sin((t - fase) * 3.2)) * alt * 0.45 if pulando else 0
            cor = cores[rnd.randrange(len(cores))]
            cor = tuple(int(c * (0.55 + 0.45 * prof)) for c in cor)
            hx, hy, r = _pessoa(d, x, y_base - pulo, alt, cor, t, "andando" if cena.get("andando") else "parado",
                                False, p["fundo"], olhos=prof > 0.6)
            if cena.get("celulares"):                              # celular aceso na frente do rosto
                cw, ch = r * 0.9, r * 1.5
                d.rounded_rectangle((hx - cw / 2, hy + r * 0.2, hx + cw / 2, hy + r * 0.2 + ch), radius=int(cw * 0.2),
                                    fill=(20, 20, 30), outline=(120, 200, 255), width=max(2, int(r * 0.08)))
                d.rectangle((hx - cw * 0.35, hy + r * 0.35, hx + cw * 0.35, hy + r * 0.05 + ch), fill=(120, 200, 255, 200))
    if cena.get("ondas"):                                          # o barulho se espalhando
        for k in range(4):
            f_ = ((t * 0.7 + k / 4) % 1)
            rr = 80 + f_ * 700
            yc = H * 0.47
            d.arc((W / 2 - rr, yc - rr * 0.7, W / 2 + rr, yc + rr * 0.7), 195, 345,
                  fill=p["acento"][:3] + (int(255 * (1 - f_)),), width=14)
    if cena.get("celulares") and cena.get("sem_sinal"):           # ícone de sinal riscado
        cx, cy = W / 2, H * 0.3
        for k in range(4):
            hh = 40 + k * 40
            d.rounded_rectangle((cx - 110 + k * 60, cy + 80 - hh, cx - 70 + k * 60, cy + 80), radius=8, fill=p["apagado"])
        if (t % 0.8) < 0.55:
            d.line((cx - 140, cy - 110, cx + 140, cy + 110), fill=(232, 44, 56), width=18)
    if cena.get("rotulo"):
        _centro_texto(d, W / 2, H * (0.42 if cena.get("sem_sinal") else 0.3), str(cena["rotulo"]).upper(),
                      _fit(d, str(cena["rotulo"]).upper(), 70), p["acento"])


def _estrelas(d, t, n=110):
    for k in range(n):
        rnd = random.Random(k)
        x, y = rnd.random() * W, rnd.random() * H
        b = 120 + int(120 * abs(math.sin(t * 2 + k)))
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(b, b, b))


def _sol(img, cena, t, dur, n, p):
    """O Sol no meio e a Terra em órbita. "apaga": o Sol se apaga; "apagado": já começa apagado;
    "onda": a última luz sai do Sol e chega à Terra; "tangente": a Terra sai pela tangente, em linha reta;
    "so_terra": só a Terra, grande; "congela": a Terra vai ficando branca de gelo; "rotulo"."""
    d = ImageDraw.Draw(img, "RGBA")
    _estrelas(d, t)
    cx, cy, ro = W / 2, H * 0.47, 370
    if cena.get("so_terra"):
        r = 300
        _globo(d, cx, cy, r, t * 0.6)
        if cena.get("congela"):
            gelo = _suave(t / max(0.1, dur * 0.8))
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(235, 245, 255, int(215 * gelo)))
            for k in range(14):                            # rachaduras de gelo aparecendo
                rnd = random.Random(k * 3)
                if rnd.random() > gelo:
                    continue
                a0, l0 = rnd.random() * 2 * math.pi, rnd.random() * r * 0.8
                x1, y1 = cx + math.cos(a0) * l0, cy + math.sin(a0) * l0
                a1 = a0 + (rnd.random() - 0.5) * 2
                d.line((x1, y1, x1 + math.cos(a1) * 90, y1 + math.sin(a1) * 90), fill=(150, 190, 230, 255), width=5)
    else:
        luz = 1.0
        if cena.get("apagado"):
            luz = 0.0
        elif cena.get("apaga"):
            luz = 1 - _suave((t - dur * 0.4) / max(0.1, dur * 0.3))   # brilha um pouco antes de apagar
        rs = 120
        if luz > 0.02:                                     # brilho em camadas
            for k in range(6, 0, -1):
                rr = rs * (1 + k * 0.22)
                d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=p["acento"][:3] + (int(30 * luz),))
        base = tuple(int(40 + (c - 40) * luz) for c in p["acento"])
        d.ellipse((cx - rs, cy - rs, cx + rs, cy + rs), fill=base,
                  outline=(90, 100, 130) if luz < 0.5 else None, width=4)
        a0 = cena.get("angulo", math.pi / 2 if cena.get("tangente") else -0.6)
        for k in range(0, 360, 6):                         # a órbita, tracejada
            d.arc((cx - ro, cy - ro, cx + ro, cy + ro), k, k + 3, fill=(120, 140, 190, 150), width=3)
        if cena.get("onda"):                               # a última luz viajando até a Terra
            rw = rs + (ro - rs) * min(1.0, t / max(0.1, dur * 0.75))
            d.ellipse((cx - rw, cy - rw, cx + rw, cy + rw), outline=p["acento"][:3] + (230,), width=10)
        if cena.get("tangente"):                           # sai em linha reta, para onde estava indo
            ex, ey = cx + math.cos(a0) * ro, cy + math.sin(a0) * ro
            tx, ty = -math.sin(a0), math.cos(a0)
            s_ = t * 90
            for k in range(0, int(s_), 30):
                d.ellipse((ex + tx * k - 4, ey + ty * k - 4, ex + tx * k + 4, ey + ty * k + 4), fill=p["acento2"])
            ex, ey = ex + tx * s_, ey + ty * s_
        else:
            a = a0 + t * 0.35
            ex, ey = cx + math.cos(a) * ro, cy + math.sin(a) * ro
        _globo(d, ex, ey, 62, t)
    if cena.get("rotulo"):
        _centro_texto(d, W / 2, H * 0.17, str(cena["rotulo"]).upper(), _fit(d, str(cena["rotulo"]).upper(), 64), p["acento"])


def _fit(d, txt, px):
    """Fonte que cabe na largura da tela (com margem)."""
    while px > 30 and d.textlength(txt, font=_f(px)) > W * 0.86:
        px -= 4
    return _f(px)


def _mergulho(img, cena, t, dur, n, p):
    """Submarino descendo no mar. "de"/"ate": profundidade em metros (aparece no medidor); "luz": farol aceso;
    "peixe": um peixe pálido passa no farol; "pressao": setas apertando o casco; "fonte": fonte de calor no fundo;
    "escala": o mar em corte com o Everest dentro; "rotulo"."""
    d = ImageDraw.Draw(img, "RGBA")
    if cena.get("escala"):
        sup, fundo = H * 0.22, H * 0.86
        d.rectangle((0, 0, W, sup), fill=(140, 200, 255))
        for y in range(int(sup), int(fundo), 6):           # água escurecendo com a fundura
            f_ = (y - sup) / (fundo - sup)
            c = tuple(int(a + (b - a) * min(1, f_ * 2.2)) for a, b in zip((40, 120, 210), (3, 6, 18)))
            d.rectangle((0, y, W, y + 6), fill=c)
        d.rectangle((0, fundo, W, H), fill=(40, 34, 30))
        sobe = 1.0 if cena.get("rotulo") else _suave(t / max(0.1, dur * 0.6))
        topo = fundo - (fundo - sup) * (8.8 / 10.9) * sobe   # Everest ~8,8 km na fossa de ~10,9 km
        d.polygon([(W * 0.18, fundo), (W * 0.5, topo), (W * 0.82, fundo)], fill=(150, 150, 160))
        d.polygon([(W * 0.5, topo), (W * 0.44, topo + 90 * sobe), (W * 0.56, topo + 90 * sobe)], fill=(250, 250, 255))
        if sobe > 0.95:
            for k in range(0, int(topo - sup), 26):         # régua da água que sobra em cima
                d.line((W * 0.5 + 60, sup + k, W * 0.5 + 60, sup + k + 14), fill=p["acento"], width=6)
        if cena.get("rotulo"):
            _centro_texto(d, W / 2, sup + (topo - sup) / 2, str(cena["rotulo"]).upper(),
                          _fit(d, str(cena["rotulo"]).upper(), 58), p["acento"])
        return
    de, ate = float(cena.get("de", 0)), float(cena.get("ate", 0))
    prof = de + (ate - de) * _suave(t / max(0.1, dur * 0.8))
    esc = min(1.0, prof / 1000)
    c = tuple(int(a + (b - a) * esc) for a, b in zip((40, 120, 210), (2, 5, 14)))
    d.rectangle((0, 0, W, H), fill=c)
    vel = 1.0 if ate > de else 0.25
    for k in range(70):                                    # neve marinha subindo: dá a sensação de descer
        rnd = random.Random(k * 11)
        x = rnd.random() * W
        y = (rnd.random() * H - t * (260 * vel + rnd.random() * 80)) % H
        d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(200, 220, 240, 110))
    sx, sy = W / 2 + math.sin(t * 1.1) * 12, H * 0.44 + math.sin(t * 1.7) * 14
    if cena.get("pressao"):
        sx += math.sin(t * 40) * 5
    if cena.get("fonte"):                                  # chaminé no fundo soltando fumaça quente
        bx, by = W * 0.7, H * 0.9
        d.polygon([(bx - 90, H), (bx - 30, by - 180), (bx + 30, by - 180), (bx + 90, H)], fill=(60, 50, 44))
        for k in range(9):
            f_ = ((t * 0.5 + k / 9) % 1)
            rr = 30 + f_ * 90
            d.ellipse((bx - rr + math.sin(k + t) * 30, by - 200 - f_ * 600 - rr, bx + rr + math.sin(k + t) * 30,
                       by - 200 - f_ * 600 + rr), fill=(255, 140, 60, int(120 * (1 - f_))))
        d.rectangle((0, H * 0.94, W, H), fill=(40, 34, 30))
    if cena.get("luz", prof > 400):                        # farol: cone de luz para baixo
        d.polygon([(sx - 30, sy + 70), (sx + 30, sy + 70), (sx + 260, sy + 640), (sx - 260, sy + 640)],
                  fill=(255, 240, 170, 66))
    if cena.get("peixe"):
        fx = W + 160 - ((t * 220) % (W + 400))
        fy = sy + 380 + math.sin(t * 3) * 20
        d.ellipse((fx - 90, fy - 34, fx + 60, fy + 34), fill=(236, 214, 220))
        d.polygon([(fx + 50, fy), (fx + 120, fy - 40 + math.sin(t * 9) * 10), (fx + 120, fy + 40 + math.sin(t * 9) * 10)],
                  fill=(236, 214, 220))
        d.ellipse((fx - 70, fy - 12, fx - 52, fy + 6), fill=(20, 20, 30))
    _submarino(d, sx, sy, p, t, luz=False)                 # submarino com volume (o farol já foi desenhado)
    for k in range(0 if cena.get("rotulo") or cena.get("pressao") else 6):       # bolhas (sem rótulo, para não brigar com ele)
        f_ = ((t * 0.9 + k / 6) % 1)
        bx_ = sx - 60 + math.sin(k * 2 + t * 3) * 40
        d.ellipse((bx_ - 12, sy - 160 - f_ * 160 - 12, bx_ + 12, sy - 160 - f_ * 160 + 12), outline=(220, 240, 255, 180), width=4)
    if cena.get("pressao"):                                # setas apertando de todos os lados
        aperta = 30 * abs(math.sin(t * 3))
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            r1, r2 = 420 - aperta, 330 - aperta
            x1, y1 = sx + math.cos(a) * r1, sy + math.sin(a) * r1 * 0.75
            x2, y2 = sx + math.cos(a) * r2, sy + math.sin(a) * r2 * 0.75
            d.line((x1, y1, x2, y2), fill=(232, 44, 56), width=14)
            px_, py_ = -math.sin(a) * 26, math.cos(a) * 26 * 0.75
            d.polygon([(x2 - math.cos(a) * 10, y2 - math.sin(a) * 10), (x2 + math.cos(a) * 40 + px_, y2 + math.sin(a) * 30 + py_),
                       (x2 + math.cos(a) * 40 - px_, y2 + math.sin(a) * 30 - py_)], fill=(232, 44, 56))
    if cena.get("medidor", True):                          # "medidor": false esconde a fundura
        _centro_texto(d, W / 2, H * 0.2, f"{prof:,.0f} m".replace(",", "."), _f(150, True), p["fig"])
        _centro_texto(d, W / 2, H * 0.27, "DE PROFUNDIDADE", _f(44), p["acento2"])
    if cena.get("rotulo"):
        if cena.get("medidor", True):
            _centro_texto(d, W / 2, H * 0.32, str(cena["rotulo"]).upper(), _fit(d, str(cena["rotulo"]).upper(), 60), p["acento"])
        else:
            _rotulo_caixa(d, H * 0.16, str(cena["rotulo"]).upper(), p)


def _astro_sprite(alt, t, cor, visor, medo=False):
    """Astronauta de pé (cabeça para cima), desenhado em 4x e reduzido: capacete com viseira e reflexo,
    mochila, painel no peito, braços e pernas articulados se debatendo, luvas e botas, contorno escuro."""
    k = 4
    u = alt * k / 100.0
    cw, ch = int(80 * u), int(104 * u)
    sp = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(sp)
    ox = cw / 2 - 50 * u                                       # x em unidades 0..100, centro em 50
    oy = 2 * u

    def P(x, y):
        return ox + x * u, oy + y * u

    branco = tuple(cor[:3])
    sombra = tuple(int(c * 0.78) for c in branco)
    cinza = tuple(int(c * 0.58) for c in branco)
    linha = (14, 18, 36)
    vis = tuple(visor[:3])
    vidro = tuple(int(10 + c * 0.22) for c in vis)
    laranja = (255, 168, 72)

    def membro(a, b, c_, larg, o, cor_):
        pts = [P(*a), P(*b), P(*c_)]
        w_ = (larg + 2 * o) * u
        d.line(pts, fill=cor_, width=int(w_), joint="curve")
        for q in pts:
            r_ = w_ / 2
            d.ellipse((q[0] - r_, q[1] - r_, q[0] + r_, q[1] + r_), fill=cor_)

    def bola(x, y, r, o, cor_):
        x, y = P(x, y)
        r = (r + o) * u
        d.ellipse((x - r, y - r, x + r, y + r), fill=cor_)

    def caixa(x0, y0, x1, y1, rr, o, cor_):
        a, b = P(x0 - o, y0 - o)
        c_, e = P(x1 + o, y1 + o)
        d.rounded_rectangle((a, b, c_, e), radius=int((rr + o) * u), fill=cor_)

    def ang(x, y, graus, comp):
        r_ = math.radians(graus)
        return (x + math.cos(r_) * comp, y + math.sin(r_) * comp)

    s1, s2 = math.sin(t * 2.3), math.sin(t * 1.7 + 1.1)
    # braços se debatendo (graus com y para baixo: 180 = esquerda, 270 = para cima)
    omb_e, omb_d = (37, 43), (63, 43)
    cot_e = ang(*omb_e, 200 + 22 * s1, 15)
    mao_e = ang(*cot_e, 245 + 25 * s1, 13)
    cot_d = ang(*omb_d, 340 - 22 * s2, 15)
    mao_d = ang(*cot_d, 295 - 25 * s2, 13)
    # pernas pedalando de leve
    qua_e, qua_d = (44, 66), (56, 66)
    joe_e = ang(*qua_e, 100 + 10 * s2, 15)
    pe_e = ang(*joe_e, 80 + 8 * s2, 14)
    joe_d = ang(*qua_d, 75 - 10 * s1, 15)
    pe_d = ang(*joe_d, 95 - 8 * s1, 14)

    for o, fase in ((1.8, "linha"), (0.0, "cor")):
        c = (lambda x: linha) if fase == "linha" else (lambda x: x)
        caixa(27, 36, 57, 64, 6, o, c(cinza))                           # mochila (aparece de lado)
        membro(qua_e, joe_e, pe_e, 11, o, c(branco))
        membro(qua_d, joe_d, pe_d, 11, o, c(branco))
        for pe in (pe_e, pe_d):                                         # botas
            bola(pe[0], pe[1] + 1, 6.5, o, c(cinza))
        caixa(34, 37, 66, 69, 10, o, c(branco))                         # tronco
        membro(omb_e, cot_e, mao_e, 9.5, o, c(branco))
        membro(omb_d, cot_d, mao_d, 9.5, o, c(branco))
        for m in (mao_e, mao_d):                                        # luvas
            bola(m[0], m[1], 5.8, o, c(cinza))
        bola(50, 22, 19, o, c(branco))                                  # capacete
        bola(31.5, 23, 3.4, o, c(cinza))
        bola(68.5, 23, 3.4, o, c(cinza))
    # detalhes por cima
    caixa(59, 40, 66, 67, 6, 0, sombra)                                 # sombra no lado do tronco
    caixa(34, 63, 66, 66.5, 1.5, 0, cinza)                              # cinto
    for m, cot in ((mao_e, cot_e), (mao_d, cot_d)):                     # faixa laranja no antebraço
        mx, my = cot[0] + (m[0] - cot[0]) * 0.45, cot[1] + (m[1] - cot[1]) * 0.45
        bola(mx, my, 4.9, 0, laranja)
    caixa(42, 46, 58, 56, 2.5, 0, cinza)                                # painel do peito
    for i, cc in enumerate(((232, 44, 56), vis, (255, 196, 36))):
        bola(45.5 + i * 4.5, 51, 1.6, 0, cc)
    # viseira: vidro escuro com borda da cor do visor, reflexo laranja do disco e brilho branco
    a, b = P(36, 12)
    c_, e = P(66, 33)
    d.ellipse((a - 1.2 * u, b - 1.2 * u, c_ + 1.2 * u, e + 1.2 * u), fill=vis)
    d.ellipse((a, b, c_, e), fill=vidro)
    d.arc((a + 1.5 * u, b + 1.5 * u, c_ - 1.5 * u, e - 1.5 * u), -20, 40, fill=laranja, width=int(2.2 * u))   # reflexo do disco na borda
    if medo:                                                            # rosto apavorado atrás da viseira (thumb)
        for ex in (45.5, 56):
            x_, y_ = P(ex, 21)
            d.ellipse((x_ - 4.2 * u, y_ - 4.8 * u, x_ + 4.2 * u, y_ + 4.8 * u), fill=(255, 255, 255))
            d.ellipse((x_ - 1.5 * u, y_ - 1.2 * u, x_ + 1.5 * u, y_ + 1.8 * u), fill=(10, 12, 24))
            d.line((x_ - 4 * u, y_ - 7.5 * u, x_ + 3 * u, y_ - 6 * u if ex < 50 else y_ - 8.5 * u), fill=(10, 12, 24), width=int(1.3 * u))
        x_, y_ = P(51, 29)
        d.ellipse((x_ - 2.6 * u, y_ - 2.4 * u, x_ + 2.6 * u, y_ + 2.6 * u), fill=(60, 14, 24))
    hx, hy = P(43, 16.5)
    d.ellipse((hx - 3.6 * u, hy - 2.2 * u, hx + 3.6 * u, hy + 2.2 * u), fill=(255, 255, 255))
    hx, hy = P(48.5, 15)
    d.ellipse((hx - 1.3 * u, hy - 1.0 * u, hx + 1.3 * u, hy + 1.0 * u), fill=(255, 255, 255))
    pe_y = oy + (max(pe_e[1], pe_d[1]) + 7.5) * u                       # ponto dos pés (pivô)
    return sp, k, pe_y


def _astro_mini(img, x, y, ang, tam, estica=1.0, cor=(240, 243, 250, 255), visor=(86, 214, 255, 255), t=0.0, centro=False, medo=False):
    """Astronauta visto de longe, com os pés em (x, y) e a cabeça na direção "ang" (para fora do buraco).
    "estica" > 1 alonga e afina o corpo (espaguetificação); "centro": (x, y) é o meio do corpo, não os pés."""
    alt = tam * 1.75
    sp, k, pe_y = _astro_sprite(alt, t, cor, visor, medo)
    lw = max(4, int(sp.width / k / math.sqrt(estica)))
    lh = max(6, int(sp.height / k * estica))
    sy = lh / sp.height
    sp = sp.resize((lw, lh), Image.LANCZOS)
    if cor[3] < 255:
        a = sp.getchannel("A").point(lambda v: v * cor[3] // 255)
        sp.putalpha(a)
    piv_y = (sp.height / 2) if centro else pe_y * sy                    # pivô no corte já reduzido
    dx, dy = 0.0, piv_y - sp.height / 2                                 # do centro até o pivô
    teta = -90 - math.degrees(ang) + math.sin(t * 1.1) * 6              # gira o "para cima" até "ang", balançando
    rot = sp.rotate(teta, resample=Image.BICUBIC, expand=True)
    r_ = math.radians(teta)
    rx = dx * math.cos(r_) + dy * math.sin(r_)
    ry = -dx * math.sin(r_) + dy * math.cos(r_)
    px = x - (rot.width / 2 + rx)
    py = y - (rot.height / 2 + ry)
    img.paste(rot, (int(px), int(py)), rot)


def _buraco_negro(img, cena, t, dur, n, p):
    """Buraco negro com o disco de gás. "de"/"ate" (0 longe, 1 na borda): um astronauta caindo;
    "congela": quem cai parece parar na beirada, ficando vermelho e apagando; "atravessa": passa a borda e some;
    "dentro": visão de dentro, o céu virando um círculo cada vez menor; "estica": o astronauta esticando feito macarrão
    (com "pequeno": true, um buraco negro pequeno que estica antes da borda); "rotulo"."""
    d = ImageDraw.Draw(img, "RGBA")
    if cena.get("dentro"):
        d.rectangle((0, 0, W, H), fill=(0, 0, 0))
        fecha = _suave(t / max(0.1, dur * 0.9))
        rr = 640 - 420 * fecha
        cx, cy = W / 2, H * 0.3
        for k in range(5, 0, -1):                                  # brilho do disco visto de dentro, em volta do furo
            r2 = rr * (1 + k * 0.05)
            d.ellipse((cx - r2, cy - r2, cx + r2, cy + r2), fill=(255, 150, 50, 26))
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=p["fundo2"])
        for k in range(80):                                        # estrelas só dentro do círculo do céu
            rnd = random.Random(k)
            a, r_ = rnd.random() * 2 * math.pi, math.sqrt(rnd.random()) * rr * 0.92
            x, y = cx + math.cos(a) * r_, cy + math.sin(a) * r_
            b = 150 + int(100 * abs(math.sin(t * 2 + k)))
            d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(b, b, b))
        if cena.get("rotulo"):
            _centro_texto(d, W / 2, H * 0.66, str(cena["rotulo"]).upper(), _fit(d, str(cena["rotulo"]).upper(), 60), p["acento"])
        return
    _estrelas(d, t)
    pequeno = cena.get("pequeno")
    cx, cy = W / 2, H * 0.47
    R = 62 if pequeno else 140
    from .buraco_negro import desenhar
    desenhar(img, cx, cy, R, t, 1.25 if pequeno else 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    ang = math.radians(-58)                                        # o astronauta vem do alto, à direita
    if cena.get("estica") and not pequeno:                         # close: o corpo esticando
        f_ = _suave(t / max(0.1, dur * 0.85))
        d.rectangle((0, 0, W, H), fill=(0, 0, 0, int(200 * min(1, f_ * 2))))
        for k in range(18):                                        # riscos de velocidade
            rnd = random.Random(k * 5)
            x = rnd.random() * W
            y = (rnd.random() * H + t * 1400) % (H + 300) - 300
            d.line((x, y, x, y + 220), fill=(255, 170, 70, 120), width=5)
        _astro_mini(img, W / 2, H * 0.48, -math.pi / 2, 150, 1 + 2.2 * f_, t=t, centro=True)
        d = ImageDraw.Draw(img, "RGBA")
    elif "de" in cena or cena.get("congela") or cena.get("atravessa"):
        longe = 3.9 if not pequeno else 7.0
        if cena.get("congela"):                                    # quase parando: aproxima cada vez mais devagar
            prog = 0.88 + 0.1 * (1 - math.exp(-t * 0.9))
        elif cena.get("atravessa"):
            prog = 0.92 + 0.28 * _suave(t / max(0.1, dur * 0.8))
        else:
            de, ate = float(cena.get("de", 0)), float(cena.get("ate", 1))
            prog = de + (ate - de) * _suave(t / max(0.1, dur * 0.9))
        dist = R * (longe - (longe - 1.0) * prog)
        x, y = cx + math.cos(ang) * dist, cy + math.sin(ang) * dist
        tam = 95 * (0.6 + 0.4 * (dist / (R * longe)))
        estica = 1.0
        if pequeno and cena.get("estica"):                         # no pequeno, estica bem antes da borda
            estica = 1 + 3.2 * _suave(prog / 0.7)
        cor, visor = (240, 243, 250, 255), (86, 214, 255, 255)
        if cena.get("congela"):                                    # vai ficando vermelho e apagado
            f_ = _suave(t / max(0.1, dur * 0.9))
            a_ = int(255 * (1 - 0.8 * f_))
            cor = (240, int(243 - 170 * f_), int(250 - 210 * f_), a_)
            visor = (120, 60, 60, a_)
        if dist < R * 1.02:                                        # passou da borda: some no escuro
            a_ = int(255 * max(0.0, (dist - R * 0.8) / (R * 0.22)))
            cor, visor = cor[:3] + (a_,), visor[:3] + (a_,)
        _astro_mini(img, x, y, ang, tam, estica, cor, visor, t=t)
        d = ImageDraw.Draw(img, "RGBA")
    if cena.get("rotulo"):                                         # embaixo do disco, longe de quem cai (que vem do alto)
        _centro_texto(d, W / 2, H * (0.17 if cena.get("estica") and not pequeno else 0.62), str(cena["rotulo"]).upper(), _fit(d, str(cena["rotulo"]).upper(), 62), p["acento"])


def _anel_pontos(d, cx, cy, rx, ry, t, metade, alfa=255, espalha=1.0, a0=0.0, faixas=5):
    """Partículas do anel em perspectiva. "espalha" (0 a 1): o quanto o anel já se fechou a partir do ângulo a0."""
    for j in range(faixas):
        for k in range(150):
            rnd = random.Random(j * 1000 + k)
            frac = rnd.random()
            a = a0 + (frac - 0.5) * 2 * math.pi * espalha + t * 0.25
            if (math.sin(a) < 0) != (metade == "tras"):
                continue
            f_r = 1 + j * 0.06 + rnd.random() * 0.04
            x, y = cx + math.cos(a) * rx * f_r, cy + math.sin(a) * ry * f_r
            tom = 190 + int(50 * rnd.random())
            s = 3 + rnd.random() * 4
            d.ellipse((x - s, y - s, x + s, y + s), fill=(tom, tom - 15, tom - 45, alfa))


def _aneis(img, cena, t, dur, n, p):
    """A Terra com um anel. "asteroide": uma rocha chegando perto; "quebra": a rocha se despedaçando;
    "forma": o anel se fechando a partir dos pedaços; "faixa": a faixa de 30° do equador com crateras aparecendo
    ("crateras": 21); "cai": pedaços caindo do anel no equador; "sombra": o Sol de lado e a sombra do anel na Terra;
    "gelo": a Terra esfriando; "some": o anel se apagando; "ceu": visto do chão, um arco cruzando o céu; "rotulo"."""
    d = ImageDraw.Draw(img, "RGBA")
    if cena.get("ceu"):
        chao = H * 0.72
        for y in range(0, int(chao), 8):                           # céu do fim de tarde
            f_ = y / chao
            c = tuple(int(a + (b - a) * f_) for a, b in zip((14, 30, 80), (90, 140, 200)))
            d.rectangle((0, y, W, y + 8), fill=c)
        _estrelas(d, t, 40)
        sobe = _suave(t / max(0.1, dur * 0.7))
        topo = chao - (chao - H * 0.2) * sobe                      # o arco vai subindo do horizonte
        for j in range(7):                                         # faixas do anel em arco
            rx = W * 0.75 - j * 18
            ry = (chao - topo) - j * 14
            if ry <= 10:
                continue
            tom = 215 - j * 12
            d.arc((W / 2 - rx, chao - ry, W / 2 + rx, chao + ry), 180, 360, fill=(tom, tom - 10, tom - 40, 230), width=14)
        for k in range(30):                                        # brilho correndo no anel
            a = math.radians(180 + ((k * 6 + t * 12) % 180))
            x, y = W / 2 + math.cos(a) * (W * 0.7), chao + math.sin(a) * (chao - topo - 40)
            d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(255, 250, 230, 200))
        d.rectangle((0, chao, W, H), fill=(20, 40, 30))
        _pessoa(d, W / 2, chao + 6, 260, (10, 18, 14), t, "parado", olhos=False)
        if cena.get("rotulo"):
            _centro_texto(d, W / 2, H * 0.13, str(cena["rotulo"]).upper(), _fit(d, str(cena["rotulo"]).upper(), 60), p["acento"])
        return
    _estrelas(d, t)
    cx, cy, r = W / 2, H * 0.46, 235
    rx, ry = r * 1.75, r * 0.4                                     # o anel cabe na largura da tela
    tem_anel = not (cena.get("asteroide") or cena.get("quebra")) or cena.get("forma")
    alfa = 255
    if cena.get("some"):
        alfa = int(255 * max(0.0, 1 - t / max(0.1, dur * 0.8)))
    espalha = _suave(t / max(0.1, dur * 0.85)) if cena.get("forma") else 1.0
    a0 = -1.15                                                     # onde a rocha se quebrou (atrás, à direita)
    if cena.get("sombra"):                                         # Sol à esquerda
        for k in range(6, 0, -1):
            rr = 90 * (1 + k * 0.3)
            d.ellipse((30 - rr, cy - 530 - rr, 30 + rr, cy - 530 + rr), fill=p["acento"][:3] + (34,))
        d.ellipse((-60, cy - 620, 120, cy - 440), fill=p["acento"])
    if tem_anel:
        _anel_pontos(d, cx, cy, rx, ry, t, "tras", alfa, espalha, a0)
    _globo(d, cx, cy, r, t)
    if cena.get("sombra"):                                         # a sombra do anel cai em faixa sobre um hemisfério
        f_ = _suave(t / max(0.1, dur * 0.6))
        for k in range(3):
            yy = cy + r * (0.32 + k * 0.1)
            meia = math.sqrt(max(0, r * r - (yy - cy) ** 2))
            d.line((cx - meia, yy, cx + meia, yy), fill=(0, 0, 20, int(200 * f_)), width=30)
    if cena.get("gelo"):
        g = _suave(t / max(0.1, dur * 0.8))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(235, 245, 255, int(170 * g)))
        h_ = r * (0.3 + 0.45 * g)                                  # calotas de gelo crescendo dos polos
        for yy in range(int(cy - r), int(cy + r), 3):
            if abs(yy - cy) < r - h_:
                continue
            meia = math.sqrt(max(0, r * r - (yy - cy) ** 2))
            d.line((cx - meia, yy, cx + meia, yy), fill=(250, 252, 255, 235), width=3)
    if cena.get("faixa") or cena.get("cai"):                       # faixa de 30° para cada lado do equador
        meia_f = r * math.sin(math.radians(30))
        for yy in (cy - meia_f, cy + meia_f):
            meia = math.sqrt(max(0, r * r - (yy - cy) ** 2))
            d.line((cx - meia, yy, cx + meia, yy), fill=p["acento"], width=6)
    if cena.get("faixa"):
        total = int(cena.get("crateras", 21))
        mostra = int(total * _suave(t / max(0.1, dur * 0.8)) + 0.5)
        for k in range(mostra):
            rnd = random.Random(k * 13)
            lat = (rnd.random() - 0.5) * 2 * math.radians(28)
            yy = cy - r * math.sin(lat)
            meia = math.sqrt(max(0, r * r - (yy - cy) ** 2))
            xx = cx + (rnd.random() - 0.5) * 2 * meia * 0.85
            d.ellipse((xx - 11, yy - 11, xx + 11, yy + 11), fill=(232, 44, 56), outline=(255, 230, 220), width=3)
    if tem_anel:
        _anel_pontos(d, cx, cy, rx, ry, t, "frente", alfa, espalha, a0)
    if cena.get("cai"):                                            # pedaços descendo até o equador, com clarão
        for k in range(8):
            f_ = ((t * 0.6 + k / 8) % 1)
            rnd = random.Random(k * 7)
            sx_ = cx + (rnd.random() - 0.5) * rx * 1.6
            sy_ = cy + ry * (0.4 if k % 2 else -0.4)
            ex_ = cx + (rnd.random() - 0.5) * r * 1.2
            ey_ = cy + (rnd.random() - 0.5) * r * 0.6
            x, y = sx_ + (ex_ - sx_) * f_, sy_ + (ey_ - sy_) * f_
            d.line((x, y, x - (ex_ - sx_) * 0.08, y - (ey_ - sy_) * 0.08), fill=(255, 170, 70, 200), width=6)
            d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(255, 220, 160))
            if f_ > 0.9:
                d.ellipse((ex_ - 26, ey_ - 26, ex_ + 26, ey_ + 26), fill=(255, 200, 90, 180))
    if cena.get("asteroide") or cena.get("quebra"):
        px_, py_ = cx + math.cos(a0) * rx, cy + math.sin(a0) * ry
        if cena.get("asteroide") and not cena.get("quebra"):
            f_ = _suave(t / max(0.1, dur * 0.85))
            x, y = W * 0.86 + (px_ - W * 0.86) * f_, H * 0.24 + (py_ - H * 0.24) * f_
            for k in range(6):                                     # rastro
                d.ellipse((x + k * 18 - 6, y - k * 30 - 6, x + k * 18 + 6, y - k * 30 + 6), fill=(255, 196, 36, 150 - k * 22))
            d.polygon([(x - 44, y - 10), (x - 18, y - 42), (x + 30, y - 36), (x + 46, y + 6), (x + 14, y + 40), (x - 34, y + 30)],
                      fill=(150, 130, 112))
            d.ellipse((x - 10, y - 14, x + 8, y + 2), fill=(110, 94, 80))
        else:
            f_ = _suave(t / max(0.1, dur * 0.8))
            for k in range(14):                                    # pedaços se afastando ao longo da órbita
                rnd = random.Random(k * 3)
                aa = a0 + (rnd.random() - 0.5) * 1.4 * f_
                x, y = cx + math.cos(aa) * rx * (1 + (rnd.random() - 0.5) * 0.12), cy + math.sin(aa) * ry
                s = 22 * (1 - 0.6 * f_) + rnd.random() * 10
                d.polygon([(x - s, y), (x, y - s * 0.8), (x + s, y - s * 0.2), (x + s * 0.4, y + s * 0.8)], fill=(150, 130, 112))
            if f_ < 0.35:
                d.ellipse((px_ - 70, py_ - 70, px_ + 70, py_ + 70), outline=(255, 220, 150, int(255 * (1 - f_ / 0.35))), width=8)
    if cena.get("rotulo"):
        _centro_texto(d, W / 2, H * 0.17, str(cena["rotulo"]).upper(), _fit(d, str(cena["rotulo"]).upper(), 62), p["acento"])


def _astro(img, cena, t, dur, n, p):
    """Qualquer planeta no visual novo (src/planetas.py). "nome"; "com": outro planeta ao lado (ex.: "terra"),
    "zoom": [z0, z1]; "nave": nave chegando; "brilho": brilho de calor em volta; "rotulo"."""
    from .planetas import planeta
    d = ImageDraw.Draw(img, "RGBA")
    _estrelas(d, t)
    z0, z1 = cena.get("zoom", [1.0, 1.15])
    z = z0 + (z1 - z0) * _suave(t / max(0.1, dur))
    cx, cy = W / 2, H * 0.47
    R = int(330 * z)
    if cena.get("com"):                                 # um em cima do outro, para comparar
        cy, R = H * 0.33, int(230 * z)
        outro = planeta(cena["com"], int(R * cena.get("proporcao", 1.0)), t)
        img.paste(outro, (int(W / 2 - outro.width / 2), int(H * 0.66 - outro.height / 2)), outro)
    if cena.get("brilho"):
        for k in range(10, 0, -1):
            rr = R * (1.05 + k * 0.05) * (1 + 0.02 * math.sin(t * 4))
            d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(255, 120, 30, 14))
    sp = planeta(cena["nome"], R, t)
    img.paste(sp, (int(cx - sp.width / 2), int(cy - sp.height / 2)), sp)
    d = ImageDraw.Draw(img, "RGBA")
    if cena.get("nave"):
        f = _suave(t / max(0.1, dur * 0.9))
        x, y = W * 0.1 + (cx - R * 0.8 - W * 0.1) * f, H * 0.2 + (cy - R * 0.6 - H * 0.2) * f
        for k in range(8):
            d.ellipse((x - 40 - k * 20, y - 30 - k * 16, x - 22 - k * 20, y - 12 - k * 16), fill=p["acento"][:3] + (150 - k * 17,))
        d.polygon([(x + 50, y + 40), (x - 40, y - 10), (x - 50, y + 20), (x - 20, y + 60)], fill=p["fig"])
    if cena.get("rotulo"):
        _centro_texto(d, W / 2, H * 0.16, str(cena["rotulo"]).upper(), _fit(d, str(cena["rotulo"]).upper(), 64), p["acento"])


def _pouso(img, cena, t, dur, n, p):
    """O você no chão de um planeta (o mesmo do vídeo longo), recortado na vertical. "nome", "efeitos", "traje", "pose"."""
    from .longo import _q_superficie, W as LW, H as LH
    grande = Image.new("RGB", (LW, LH))
    _q_superficie(grande, dict(cena, medidor=None), t, dur)
    larg = LH * W / H
    x0 = LW * 0.42 - larg / 2
    corte = grande.crop((int(x0), 0, int(x0 + larg), LH)).resize((W, H), Image.BICUBIC)
    img.paste(corte)
    if cena.get("rotulo"):
        d = ImageDraw.Draw(img)
        _centro_texto(d, W / 2, H * 0.16, str(cena["rotulo"]).upper(), _fit(d, str(cena["rotulo"]).upper(), 64), p["acento"])


QUADROS.update({"astro": _astro, "pouso": _pouso})
QUADROS.update({"planeta": _planeta, "terra_corte": _terra_corte, "espaco": _espaco, "numero": _numero,
                "comparar": _comparar, "multidao": _multidao, "sol": _sol, "mergulho": _mergulho,
                "buraco_negro": _buraco_negro, "aneis": _aneis})


# ---------------------------------------------------------------- perfuração (buraco mais fundo já cavado)
ROCHA_TOPO, ROCHA_FUNDO = (128, 96, 70), (70, 34, 28)


def _perfuracao(img, cena, t, dur, n, p):
    """Poço de sondagem em corte: torre na superfície, rocha em camadas e a broca descendo.
    "de"/"ate": metros (0 a "escala", padrão 12262); "medidor": false esconde a fundura; "termometro": [de, ate] °C;
    "calor": rocha brilhando no fundo; "treme": a broca sacode; "fosseis": plâncton fóssil brilhando em volta da broca;
    "agua": gotas presas na rocha; "lama": bolhas subindo pelo poço; "rotulo".
    Modos: "boca": a tampa de metal enferrujada vista de cima ("medida": régua com o rótulo);
           "perfil": você de pé ao lado da boca do poço (o poço é mais estreito que você);
           "planeta": a Terra em corte com a marca minúscula do poço no alto."""
    d = ImageDraw.Draw(img, "RGBA")
    rot = str(cena.get("rotulo", "")).upper()
    if cena.get("boca"):
        d.rectangle((0, 0, W, H), fill=(92, 94, 98))
        for k in range(260):                                # concreto granulado
            rnd = random.Random(k * 3)
            x, y = rnd.random() * W, rnd.random() * H
            c = 70 + int(rnd.random() * 50)
            d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(c, c, c + 4))
        d.line((W * 0.1, H * 0.15, W * 0.35, H * 0.3, W * 0.3, H * 0.42), fill=(60, 60, 64), width=5)
        d.line((W * 0.75, H * 0.7, W * 0.9, H * 0.62), fill=(60, 60, 64), width=5)
        cx, cy, r = W / 2, H * 0.45, 300 + 12 * math.sin(t * 0.8)
        d.ellipse((cx - r - 40, cy - r - 40, cx + r + 40, cy + r + 40), fill=(64, 64, 68))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(150, 76, 36))
        for k in range(40):                                 # manchas de ferrugem
            rnd = random.Random(k * 17)
            a, rr = rnd.random() * 6.283, rnd.random() * r * 0.9
            x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr
            tam = 14 + rnd.random() * 40
            d.ellipse((x - tam, y - tam * 0.7, x + tam, y + tam * 0.7), fill=(110 + int(rnd.random() * 60), 50, 24, 180))
        for k in range(12):                                 # parafusos
            a = k / 12 * 6.283
            x, y = cx + math.cos(a) * (r - 34), cy + math.sin(a) * (r - 34)
            d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=(70, 50, 40), outline=(40, 30, 26), width=4)
        d.ellipse((cx - r * 0.35, cy - r * 0.35, cx + r * 0.35, cy + r * 0.35), outline=(96, 46, 24), width=10)
        if cena.get("medida"):
            ab = _suave(t / max(0.1, dur * 0.5))
            meia = r * 0.35 * ab
            y = cy + r + 110
            d.line((cx - meia, y, cx + meia, y), fill=p["acento"], width=10)
            for s_ in (-1, 1):
                d.line((cx + s_ * meia, y - 30, cx + s_ * meia, y + 30), fill=p["acento"], width=10)
        if rot:
            _centro_texto(d, W / 2, H * 0.16, rot, _fit(d, rot, 64), p["acento"])
        return
    if cena.get("planeta"):
        _estrelas(d, t)
        cx, cy, r = W / 2, H * 0.5, 430
        for f_, cor in [(1.0, (150, 96, 60)), (0.97, (205, 90, 40)), (0.55, (240, 150, 40)), (0.19, (255, 230, 120))]:
            d.ellipse((cx - r * f_, cy - r * f_, cx + r * f_, cy + r * f_), fill=cor)
        d.line((cx, cy - r, cx, cy), fill=(255, 255, 255, 70), width=3)        # caminho até o centro
        d.line((cx, cy - r, cx, cy - r + 4), fill=(10, 10, 14), width=10)      # o poço: quase nada
        pul = 40 + 25 * abs(math.sin(t * 3))
        d.ellipse((cx - pul, cy - r - pul, cx + pul, cy - r + pul), outline=p["acento"], width=8)
        d.line((cx + 70, cy - r - 170, cx + 22, cy - r - 40), fill=p["acento"], width=10)
        d.polygon([(cx + 14, cy - r - 22), (cx + 2, cy - r - 70), (cx + 46, cy - r - 54)], fill=p["acento"])
        if rot:
            _centro_texto(d, W / 2, H * 0.16, rot, _fit(d, rot, 64), p["acento"])
        return
    sup = H * 0.30
    if cena.get("perfil"):                                  # você ao lado da boca do poço, em escala
        d.rectangle((0, 0, W, H * 0.62), fill=(150, 190, 225))
        chao = H * 0.62
        for y in range(int(chao), H, 8):
            f_ = (y - chao) / (H - chao)
            d.rectangle((0, y, W, y + 8), fill=tuple(int(a + (b - a) * f_) for a, b in zip(ROCHA_TOPO, ROCHA_FUNDO)))
        alt = 620                                           # você (~1,70 m); o poço tem ~23 cm
        poco = alt * 0.23 / 1.7
        px_ = W * 0.62
        d.rectangle((px_ - poco / 2, chao, px_ + poco / 2, H), fill=(14, 10, 10))
        d.rectangle((px_ - poco / 2 - 22, chao - 26, px_ + poco / 2 + 22, chao), fill=(150, 76, 36))
        _pessoa(d, W * 0.36, chao, alt, (30, 40, 70), t, "parado", fundo=(150, 190, 225))
        seta = 20 * abs(math.sin(t * 3))
        d.line((px_, chao - 220 - seta, px_, chao - 60 - seta), fill=p["acento"], width=12)
        d.polygon([(px_ - 30, chao - 80 - seta), (px_ + 30, chao - 80 - seta), (px_, chao - 40 - seta)], fill=p["acento"])
        if rot:
            _centro_texto(d, W / 2, H * 0.2, rot, _fit(d, rot, 64), p["acento"])
        return
    fim = H * 0.75                                          # a legenda fica embaixo disso
    escala = float(cena.get("escala", 12262))
    d.rectangle((0, 0, W, sup), fill=(20, 40, 80))
    for y in range(int(sup), H, 6):                         # rocha escurecendo e avermelhando com a fundura
        f_ = min(1.0, (y - sup) / (fim - sup))
        d.rectangle((0, y, W, y + 6), fill=tuple(int(a + (b - a) * f_) for a, b in zip(ROCHA_TOPO, ROCHA_FUNDO)))
    for k in range(9):                                      # estratos
        rnd = random.Random(k * 5)
        y = sup + (k + 0.5) * (H - sup) / 9
        pts = [(x, y + math.sin(x / 140 + k) * 16 + rnd.random() * 6) for x in range(0, W + 60, 60)]
        d.line(pts, fill=(40, 20, 16, 90), width=4)
    de, ate = float(cena.get("de", 0)), float(cena.get("ate", 0))
    prof = de + (ate - de) * _suave(t / max(0.1, dur * 0.85))
    by = sup + (fim - sup) * min(1.0, prof / escala)
    calor = cena.get("calor") or cena.get("termometro")
    if calor:
        for k in range(12, 0, -1):                          # rocha brilhando em volta da ponta
            rr = 60 + k * 34
            a_ = int(10 + 8 * math.sin(t * 3 + k))
            d.ellipse((W / 2 - rr * 1.6, by - rr, W / 2 + rr * 1.6, by + rr), fill=(255, 110, 30, a_))
    cx = W / 2
    treme = math.sin(t * 50) * 6 if cena.get("treme") else 0
    d.rectangle((cx - 9, sup, cx + 9, by), fill=(12, 8, 8))                     # o poço
    d.polygon([(cx - 120, sup), (cx - 26, sup - 190), (cx + 26, sup - 190), (cx + 120, sup)], outline=p["fig"], width=8)
    for k in range(1, 4):                                   # torre de sondagem
        yy = sup - k * 47
        meia = 120 - (120 - 26) * k / 4
        d.line((cx - meia, yy, cx + meia, yy), fill=p["fig"], width=5)
    d.rectangle((cx - 160, sup - 10, cx + 160, sup + 6), fill=p["apagado"])
    giro = (t * 8) % 1
    bx = cx + treme
    d.polygon([(bx - 24, by - 46), (bx + 24, by - 46), (bx, by + 8)], fill=p["acento"])  # broca
    for k in range(3):
        yy = by - 40 + ((giro + k / 3) % 1) * 44
        meia = 24 * (1 - (yy - (by - 46)) / 54)
        d.line((bx - meia, yy, bx + meia, yy), fill=(150, 110, 20), width=4)
    if cena.get("fosseis"):
        for k in range(9):
            rnd = random.Random(k * 13)
            x = cx + (rnd.random() - 0.5) * 760
            y = by + (rnd.random() - 0.5) * 360
            if abs(x - cx) < 80:
                x += 160 * (1 if x >= cx else -1)
            ap = _suave((t - k * 0.25) / 0.6)
            if ap <= 0:
                continue
            rr = (22 + rnd.random() * 18) * ap * (1 + 0.08 * math.sin(t * 4 + k))
            d.ellipse((x - rr * 2.2, y - rr * 2.2, x + rr * 2.2, y + rr * 2.2), fill=p["acento2"][:3] + (40,))
            d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=p["acento2"], width=5)
            for j in range(8):
                a = j / 8 * 6.283 + t * 0.6
                d.line((x + math.cos(a) * rr, y + math.sin(a) * rr, x + math.cos(a) * rr * 1.5, y + math.sin(a) * rr * 1.5),
                       fill=p["acento2"], width=3)
    if cena.get("agua"):
        for k in range(16):
            rnd = random.Random(k * 29)
            x = cx + (rnd.random() - 0.5) * 820
            y = by - 260 + rnd.random() * 420
            if abs(x - cx) < 60:
                continue
            br = 0.6 + 0.4 * math.sin(t * 3 + k)
            d.polygon([(x, y - 26), (x - 15, y + 4), (x + 15, y + 4)], fill=(90, 180, 255, int(220 * br)))
            d.ellipse((x - 15, y - 10, x + 15, y + 18), fill=(90, 180, 255, int(220 * br)))
    if cena.get("lama"):
        for k in range(14):
            f_ = ((t * 0.7 + k / 14) % 1)
            y = by - f_ * (by - sup)
            x = cx + math.sin(k * 1.7 + t * 5) * 6
            rr = 7 + (k % 3) * 3
            d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(200, 230, 255, 200))
        for k in range(7):                                  # espuma saindo na boca
            f_ = ((t * 0.9 + k / 7) % 1)
            x = cx + (k - 3) * 30 * f_
            y = sup - 20 - f_ * 120
            rr = 12 + f_ * 20
            d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(150, 120, 100, int(200 * (1 - f_))))
    if cena.get("termometro"):
        t0, t1 = cena["termometro"]
        temp = t0 + (t1 - t0) * _suave(t / max(0.1, dur * 0.75))
        tx, ty0, ty1 = W * 0.84, H * 0.40, H * 0.66
        d.rounded_rectangle((tx - 26, ty0, tx + 26, ty1), radius=26, fill=(240, 240, 245), outline=(40, 40, 50), width=5)
        d.ellipse((tx - 50, ty1 - 30, tx + 50, ty1 + 70), fill=(232, 44, 56), outline=(40, 40, 50), width=5)
        nivel = ty1 - (ty1 - ty0 - 20) * min(1.0, temp / 200)
        d.rounded_rectangle((tx - 13, nivel, tx + 13, ty1 + 10), radius=12, fill=(232, 44, 56))
        _centro_texto(d, tx - 20, ty0 - 60, f"{temp:.0f} °C", _f(64, True), p["acento"])
    if cena.get("medidor", True):
        _centro_texto(d, W / 2, H * 0.085, f"{prof:,.0f} m".replace(",", "."), _f(120, True), p["fig"])
    if rot:
        _centro_texto(d, W / 2, H * 0.175 if cena.get("medidor", True) else H * 0.12, rot, _fit(d, rot, 58), p["acento"])


# ---------------------------------------------------------------- impacto (o asteroide dos dinossauros)
def _dino(d, x, chao, s, cor, t, vira=1):
    """Saurópode genérico (pescoço longo) em silhueta, andando devagar."""
    bal = math.sin(t * 2 + x) * s * 0.02
    corpo = (x - s * 0.5, chao - s * 0.75 + bal, x + s * 0.5, chao - s * 0.3 + bal)
    for k, dx in enumerate((-0.36, -0.2, 0.2, 0.36)):        # pernas
        pa = math.sin(t * 2 + k * 1.6) * s * 0.03
        d.rounded_rectangle((x + dx * s - s * 0.06 + pa, chao - s * 0.45, x + dx * s + s * 0.06 + pa, chao), radius=int(s * 0.05), fill=cor)
    d.ellipse(corpo, fill=cor)
    pes = [(x + vira * s * 0.35, chao - s * 0.62 + bal), (x + vira * s * 0.62, chao - s * 1.05), (x + vira * s * 0.78, chao - s * 1.32),
           (x + vira * s * 0.86, chao - s * 1.3), (x + vira * s * 0.72, chao - s * 1.0), (x + vira * s * 0.45, chao - s * 0.45 + bal)]
    d.polygon(pes, fill=cor)
    hx, hy = x + vira * s * 0.86, chao - s * 1.34
    d.ellipse((hx - s * 0.09, hy - s * 0.06, hx + s * 0.09, hy + s * 0.06), fill=cor)
    cauda = math.sin(t * 1.5) * s * 0.05
    d.polygon([(x - vira * s * 0.42, chao - s * 0.66 + bal), (x - vira * s * 1.05, chao - s * 0.36 + cauda),
               (x - vira * s * 0.42, chao - s * 0.42 + bal)], fill=cor)


def _palmeira(d, x, chao, s, cor, t, vento=0.0):
    curva = vento * s * 0.4 + math.sin(t * 1.3 + x) * s * 0.02
    d.line((x, chao, x + curva * 0.5, chao - s * 0.5, x + curva, chao - s), fill=cor, width=max(4, int(s * 0.06)))
    for k in range(6):
        a = math.pi + k * math.pi / 5 + vento * 0.6
        d.line((x + curva, chao - s, x + curva + math.cos(a) * s * 0.4 + vento * s * 0.25, chao - s + math.sin(a) * s * 0.25 + s * 0.12),
               fill=cor, width=max(4, int(s * 0.05)))


def _ave(d, x, y, s, cor, t):
    asa = math.sin(t * 9) * s * 0.5
    d.line((x - s, y - asa, x, y, x + s, y - asa), fill=cor, width=max(4, int(s * 0.18)), joint="curve")


def _rotulo_caixa(d, y, txt, p):
    """Rótulo com caixa escura atrás (para ler em céu claro)."""
    fonte = _fit(d, txt, 64)
    b = d.textbbox((0, 0), txt, font=fonte)
    w_, h_ = b[2] - b[0], b[3] - b[1]
    d.rounded_rectangle((W / 2 - w_ / 2 - 30, y - h_ / 2 - 22, W / 2 + w_ / 2 + 30, y + h_ / 2 + 22), radius=24, fill=(8, 18, 46, 200))
    _centro_texto(d, W / 2, y, txt, fonte, p["acento"])


def _impacto(img, cena, t, dur, n, p):
    """O asteroide dos dinossauros. Modo "espaco": a Terra e o asteroide chegando ("de"/"ate" de 0 a 1; com "impacto",
    clarão no ponto de impacto). Sem "espaco": paisagem com dinossauros e você no morro. Opções: "bola" (risco de
    fogo no céu), "plumas" (rocha derretida subindo do horizonte), "vento" (tudo envergando, poeira), "tsunami" (o mar
    com a onda gigante subindo), "fogo" (incêndio), "escuro" (poeira tapando o Sol), "frio" (céu cinza e flocos caindo),
    "vazio" (sem dinossauros), "ave" (aves voando), "voce": false (sem você), "rotulo"."""
    d = ImageDraw.Draw(img, "RGBA")
    rot = str(cena.get("rotulo", "")).upper()
    if cena.get("espaco"):
        _estrelas(d, t)
        cx, cy, r = W / 2, H * 0.6, 340
        _globo(d, cx, cy, r, t * 0.4)
        d = ImageDraw.Draw(img, "RGBA")
        de, ate = cena.get("de", 0.0), cena.get("ate", 0.85)
        f_ = de + (ate - de) * _suave(t / max(0.1, dur * 0.9))
        ix, iy = cx - r * 0.25, cy - r * 0.92                 # ponto de impacto
        ox, oy = W * 1.05, -H * 0.05
        ax, ay = ox + (ix - ox) * f_, oy + (iy - oy) * f_
        ux, uy = (ox - ix), (oy - iy)
        L = math.hypot(ux, uy)
        ux, uy = ux / L, uy / L
        tam = 26 + 18 * f_
        for k in range(14, 0, -1):                            # rastro de fogo
            rr = tam * (1 - k / 16)
            x, y = ax + ux * k * 26, ay + uy * k * 26
            d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(255, 140 + k * 6, 40, 200 - k * 12))
        d.ellipse((ax - tam, ay - tam, ax + tam, ay + tam), fill=(90, 80, 74), outline=(255, 200, 90), width=5)
        if cena.get("impacto"):
            g = _suave((t - dur * 0.15) / max(0.1, dur * 0.6))
            for k in range(8, 0, -1):
                rr = 30 + g * 260 * k / 8
                d.ellipse((ix - rr, iy - rr * 0.6, ix + rr, iy + rr * 0.6), fill=(255, 230, 160, int(40 * (1 - k / 9))))
            rr = 40 + g * 320
            d.ellipse((ix - rr, iy - rr * 0.6, ix + rr, iy + rr * 0.6), outline=(255, 250, 220, int(255 * (1 - g))), width=10)
        if rot:
            _centro_texto(d, W / 2, H * 0.2, rot, _fit(d, rot, 64), p["acento"])
        return
    escuro = _suave(t / max(0.1, dur * 0.8)) if cena.get("escuro") else 0.0
    ceu1, ceu2 = (96, 160, 220), (190, 220, 240)
    if cena.get("fogo"):
        ceu1, ceu2 = (120, 40, 26), (230, 110, 40)
    if cena.get("frio"):
        ceu1, ceu2 = (70, 76, 86), (120, 126, 134)
        escuro = 0.3
    horiz = H * 0.55
    for y in range(0, int(horiz), 8):
        f_ = y / horiz
        c = [a + (b - a) * f_ for a, b in zip(ceu1, ceu2)]
        c = [v * (1 - escuro) + q * escuro for v, q in zip(c, (40, 34, 30))]
        d.rectangle((0, y, W, y + 8), fill=tuple(int(v) for v in c))
    sx, sy = W * 0.8, H * 0.3                                     # o Sol (longe do rótulo)
    sol_a = int(255 * (1 - escuro * 0.85))
    d.ellipse((sx - 70, sy - 70, sx + 70, sy + 70), fill=(255, 240, 180, sol_a))
    vento = (0.9 + 0.2 * math.sin(t * 7)) if cena.get("vento") else 0.0
    if cena.get("plumas"):                                         # rocha derretida subindo no horizonte
        for k in range(26):
            rnd = random.Random(k * 7)
            f_ = ((t * 0.35 + rnd.random()) % 1)
            x = W * 0.5 + (rnd.random() - 0.5) * 300 * (0.3 + f_)
            y = horiz - f_ * horiz * 0.9
            rr = 14 + rnd.random() * 18
            d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(255, 120 + int(rnd.random() * 80), 30, int(230 * (1 - f_ * 0.6))))
        g = 0.6 + 0.4 * math.sin(t * 5)
        d.ellipse((W * 0.5 - 260, horiz - 120, W * 0.5 + 260, horiz + 120), fill=(255, 200, 90, int(160 * g)))
    if cena.get("tsunami"):
        d.rectangle((0, horiz, W, H), fill=(26, 80, 140))
        sobe = _suave(t / max(0.1, dur * 0.8))
        topo = horiz - sobe * horiz * 0.75
        pts = [(0, horiz + 20)]
        for x in range(0, W + 40, 40):
            pts.append((x, topo + math.sin(x / 120 + t * 3) * 26 + (x / W) * 60))
        pts.append((W, horiz + 20))
        d.polygon(pts, fill=(22, 70, 126))
        for x in range(0, W + 40, 40):
            y = topo + math.sin(x / 120 + t * 3) * 26 + (x / W) * 60
            d.ellipse((x - 26, y - 18, x + 26, y + 18), fill=(235, 245, 255, 220))
        d.rectangle((0, H * 0.72, W, H), fill=(170, 150, 110))  # praia onde você está
        if cena.get("voce", True):
            _pessoa(d, W * 0.5, H * 0.72, 230, (30, 30, 40), t, "tremendo", fundo=(170, 150, 110))
        if rot:
            _rotulo_caixa(d, H * 0.16, rot, p)
        return
    for k in range(3):                                             # morros
        rnd = random.Random(k * 31)
        x = W * (0.15 + k * 0.4)
        d.ellipse((x - 520, horiz - 80 - rnd.random() * 60, x + 520, horiz + 600), fill=(60 + k * 12, 100 + k * 10, 58))
    d.rectangle((0, horiz + 60, W, H), fill=(70, 112, 62))
    mato = (24, 44, 30) if not cena.get("fogo") else (30, 20, 16)
    for k, (x, s) in enumerate(((W * 0.08, 300), (W * 0.9, 340), (W * 0.62, 220))):
        _palmeira(d, x, horiz + 70 + k * 30, s, mato, t, vento)
    if not cena.get("vazio"):
        cor_dino = (30, 40, 36) if not cena.get("fogo") else (24, 16, 14)
        recua = math.sin(t * 20) * 8 if vento else 0
        _dino(d, W * 0.38 + recua, horiz + 150, 330, cor_dino, t, vira=1)
        _dino(d, W * 0.78 + recua, horiz + 110, 200, cor_dino, t + 1, vira=-1)
    if cena.get("voce", True):
        _pessoa(d, W * 0.12, horiz + 220, 170, (20, 26, 40), t, "tremendo" if (vento or cena.get("fogo")) else "parado",
                fundo=(70, 112, 62))
    if cena.get("bola"):                                           # risco de fogo cruzando o céu
        f_ = _suave(t / max(0.1, dur * 0.95))
        ax, ay = W * 0.95 - f_ * W * 0.55, H * 0.05 + f_ * H * 0.42
        for k in range(16, 0, -1):
            rr = 34 * (1 - k / 18)
            x, y = ax + k * 22, ay - k * 17
            d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(255, 160 + k * 5, 60, 230 - k * 13))
        d.ellipse((ax - 30, ay - 30, ax + 30, ay + 30), fill=(255, 250, 220))
    if vento:                                                      # poeira varrendo
        for k in range(40):
            rnd = random.Random(k * 9)
            y = rnd.random() * H * 0.9
            x = ((rnd.random() * W + t * (900 + rnd.random() * 500)) % (W + 300)) - 150
            d.line((x, y, x + 120, y), fill=(200, 170, 130, 120), width=6)
    if cena.get("fogo"):
        for k in range(22):
            rnd = random.Random(k * 3)
            x = rnd.random() * W
            base = horiz + 40 + rnd.random() * (H * 0.2)
            alt = (90 + rnd.random() * 160) * (0.8 + 0.3 * math.sin(t * 8 + k))
            d.polygon([(x - 45, base), (x + math.sin(t * 6 + k) * 20, base - alt), (x + 45, base)], fill=(255, 120, 20, 210))
            d.polygon([(x - 22, base), (x + math.sin(t * 6 + k) * 12, base - alt * 0.6), (x + 22, base)], fill=(255, 220, 80, 230))
    if cena.get("escuro") or cena.get("frio"):
        dens = 40 if cena.get("frio") else int(40 * escuro)
        for k in range(dens):
            rnd = random.Random(k * 41)
            x = (rnd.random() * W + math.sin(t + k) * 30) % W
            y = (rnd.random() * H + t * (60 + rnd.random() * 60)) % H
            cor = (235, 240, 250, 200) if cena.get("frio") else (90, 80, 70, 170)
            d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=cor)
    if cena.get("ave"):
        for k in range(3):
            x = ((t * 160 + k * 260) % (W + 300)) - 150
            _ave(d, x, H * (0.26 + k * 0.06), 74 - k * 12, (30, 30, 40), t + k)
    if escuro or cena.get("frio"):                                 # a paisagem inteira escurece/esfria, não só o céu
        cor = (200, 214, 230, 70) if cena.get("frio") else (30, 24, 20, int(150 * escuro))
        d.rectangle((0, 0, W, H), fill=cor)
    if rot:
        _rotulo_caixa(d, H * 0.16, rot, p)


QUADROS.update({"perfuracao": _perfuracao, "impacto": _impacto})


def _hud(img, cena, t, p):
    d = ImageDraw.Draw(img)
    h0 = cena.get("_hora")
    if h0:
        hh, mm = (int(x) for x in h0.split(":"))
        seg = int(cena.get("_t0", 0) + t)
        m = mm + seg // 60
        d.text((70, 110), f"{(hh + m // 60) % 24:02d}:{m % 60:02d} AM", font=_f(44, True), fill=p["fig"])
    if cena.get("_parte"):
        b = d.textbbox((0, 0), cena["_parte"], font=_f(38))
        d.rounded_rectangle((W - 110 - (b[2] - b[0]), 104, W - 70, 166), radius=12, fill=p["acento"])
        d.text((W - 90 - (b[2] - b[0]), 108), cena["_parte"], font=_f(38), fill=p["fundo"])
    if cena.get("texto_topo"):
        _centro_texto(d, W / 2, H * 0.1, str(cena["texto_topo"]).upper(), _f(52), p["acento2"])
    if cena.get("alerta") and (t % 0.8) < 0.45:
        d.rectangle((0, 0, W - 1, H - 1), outline=p["acento"], width=22)


def quadro(cena: dict, t: float, dur: float, n: int) -> Image.Image:
    p = PALETAS.get(cena.get("_paleta", "noite"), PALETAS["noite"])
    tipo = cena.get("quadro", "texto")
    if tipo == "preto":
        return Image.new("RGB", (W, H), (0, 0, 0))
    img = _fundo(p).copy()
    QUADROS.get(tipo, _texto)(img, cena, t, dur, n, p)
    _hud(img, cena, t, p)
    z = 1.02 + 0.06 * _suave(t / max(1.0, dur))          # sempre aproximando devagar: o quadro nunca fica parado
    cx_, cy_ = 0.5, 0.5
    if cena.get("seguir") and cena.get("_alvo"):        # close acompanhando o alvo (ex.: quem cai no buraco)
        z = 2.2
        cx_, cy_ = cena["_alvo"]
    elif cena.get("foco"):
        cx_, cy_, z = cena["foco"]
    sx = sy = 0.0
    if cena.get("susto"):
        rnd = random.Random(n)
        sx, sy = (rnd.random() - 0.5) * 16, (rnd.random() - 0.5) * 16
    cw, ch = W / z, H / z
    x0 = min(max(0.0, cx_ * W - cw / 2 + sx), W - cw)
    y0 = min(max(0.0, cy_ * H - ch / 2 + sy), H - ch)
    img = img.resize((W, H), Image.BILINEAR, box=(x0, y0, min(W, x0 + cw), min(H, y0 + ch)))
    a = np.asarray(img).astype(np.float32)
    a += np.random.default_rng(n).normal(0, 5, (H // 4, W // 4, 1)).repeat(4, 0).repeat(4, 1)   # grão
    borda = min(t, dur - t)
    if borda < 0.08:
        a *= max(0.0, borda) / 0.08
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def renderizar_cena_voce(cena: dict, voz: dict, destino: Path, pausa: float, indice: int) -> float:
    dur = voz["duracao"] + pausa
    frames = math.ceil(dur * FPS)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", str(voz["arquivo"]),
                           "-filter_complex", "[1:a]aresample=44100,apad[a]", "-map", "0:v", "-map", "[a]",
                           "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "160k", "-ac", "2", str(destino)], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for k in range(frames):
            ff.stdin.write(quadro(cena, k / FPS, dur, indice * 10000 + k).tobytes())
    finally:
        ff.stdin.close()
        erro = ff.stderr.read().decode(errors="ignore")
        ff.wait()
    if ff.returncode != 0:
        raise RuntimeError(erro[-800:])
    return dur


# ---------------------------------------------------------------- Apophis (asteroide que passa raspando em 2029)
def _rocha(d, x, y, r, ang=0.0, aperta=1.0, cor=(128, 116, 104)):
    """Asteroide em forma de amendoim (dois lóbulos irregulares), com luz de lado e crateras."""
    def lobulo(ox, rr, seed, c, enc=1.0):
        pts = []
        for k in range(24):
            a = k / 24 * 2 * math.pi
            rad = r * rr * enc * (1 + 0.11 * math.sin(a * 3 + seed) + 0.07 * math.cos(a * 5 + seed * 2))
            px_, py_ = ox * r * aperta + math.cos(a) * rad * aperta, math.sin(a) * rad / aperta
            pts.append((x + px_ * math.cos(ang) - py_ * math.sin(ang), y + px_ * math.sin(ang) + py_ * math.cos(ang)))
        d.polygon(pts, fill=c)
    escuro = tuple(int(v * 0.55) for v in cor)
    lobulo(-0.42, 0.72, 1, escuro)
    lobulo(0.5, 0.6, 4, escuro)
    claro = tuple(min(255, int(v * 1.08)) for v in cor)
    lobulo(-0.47, 0.6, 1, claro)                     # parte iluminada (deslocada para cima e à esquerda)
    lobulo(0.44, 0.5, 4, claro)
    for k in range(7):
        rnd = random.Random(k * 13)
        cx_ = (rnd.random() - 0.5) * 1.5 * r * aperta
        cy_ = (rnd.random() - 0.5) * 0.6 * r / aperta
        cr = r * (0.06 + rnd.random() * 0.08)
        xx, yy = x + cx_ * math.cos(ang) - cy_ * math.sin(ang), y + cx_ * math.sin(ang) + cy_ * math.cos(ang)
        d.ellipse((xx - cr, yy - cr, xx + cr, yy + cr), fill=escuro)


def _torre(d, x, chao, alt, cor):
    """Torre de treliça genérica (silhueta), para comparar tamanhos."""
    base = alt * 0.42
    for k in range(4):                                  # quatro trechos, cada um mais fino
        y0, y1 = chao - alt * (k / 4) ** 0.8, chao - alt * ((k + 1) / 4) ** 0.8
        w0 = base * (1 - (k / 4) ** 0.55) / 2 + 6
        w1 = base * (1 - ((k + 1) / 4) ** 0.55) / 2 + 6
        d.line((x - w0, y0, x - w1, y1), fill=cor, width=10)
        d.line((x + w0, y0, x + w1, y1), fill=cor, width=10)
        d.line((x - w0, y0, x + w1, y1), fill=cor, width=4)
        d.line((x + w0, y0, x - w1, y1), fill=cor, width=4)
        d.line((x - w1, y1, x + w1, y1), fill=cor, width=8)
    d.arc((x - base * 0.32, chao - alt * 0.16, x + base * 0.32, chao + alt * 0.1), 180, 360, fill=cor, width=8)
    d.line((x, chao - alt, x, chao - alt - alt * 0.06), fill=cor, width=6)


def _ceu_noite(d, t, horiz):
    for y in range(0, int(horiz), 8):
        f_ = y / horiz
        c = tuple(int(a + (b - a) * f_) for a, b in zip((6, 10, 30), (30, 46, 92)))
        d.rectangle((0, y, W, y + 8), fill=c)
    for k in range(150):
        rnd = random.Random(k + 500)
        x, y = rnd.random() * W, rnd.random() * horiz * 0.95
        b = 140 + int(110 * abs(math.sin(t * 1.5 + k)))
        rr = 1.5 + rnd.random() * 1.8
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(b, b, min(255, b + 20)))


def _morro_gente(d, t, horiz, n=5, cor=(10, 14, 28)):
    d.polygon([(0, H), (0, horiz + 60), (W * 0.3, horiz - 10), (W * 0.62, horiz + 30), (W, horiz - 30), (W, H)], fill=cor)
    for k in range(n):
        x = W * (0.16 + k * 0.17)
        chao = horiz + 90 + (k % 2) * 20
        alt = 240 + (k % 3) * 20
        _pessoa(d, x, chao, alt, cor, t + k, olhos=False)
        if k % 2 == 0:                                   # braço apontando para o céu
            d.line((x + alt * 0.12, chao - alt * 0.62, x + alt * 0.4, chao - alt * 1.05), fill=cor, width=18)


def _apophis(img, cena, t, dur, n, p):
    """O asteroide Apophis. Sem modo: a Terra (em escala), o anel dos satélites geoestacionários e o asteroide
    passando por dentro dele ("de"/"ate" de 0 a 1 no caminho; "orbita": o caminho entorta depois da passagem;
    "espreme": o asteroide sendo apertado, com pedras soltando). Modos: "data" (calendário virando para sexta 13 de
    abril de 2029), "tamanho" (o asteroide ao lado de uma torre), "risco" (medidor da chance de bater; "de"/"ate" em %,
    "recorde": escala de perigo acendendo até o nível mais alto já dado), "ceu" (de noite, gente no morro e um pontinho
    andando entre as estrelas; "gente": quantas pessoas), "mapa" (a Terra virada para o Atlântico, com os lugares que veem
    a passagem), "perto" (close fora de escala: a Terra embaixo, os satélites e o asteroide grande passando), "medida"
    (régua da Terra ao asteroide), "mira" (a rota parecendo apontar para a Terra), "valor" (texto fixo no medidor), "rotulo"."""
    d = ImageDraw.Draw(img, "RGBA")
    rot = str(cena.get("rotulo", "")).upper()
    prog = _suave(t / max(0.1, dur * 0.9))
    if cena.get("data"):
        _estrelas(d, t)
        cx, cy, cw, ch = W / 2, H * 0.5, 820, 900
        d.rounded_rectangle((cx - cw / 2 + 14, cy - ch / 2 + 18, cx + cw / 2 + 14, cy + ch / 2 + 18), radius=40, fill=(0, 0, 0, 120))
        d.rounded_rectangle((cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), radius=40, fill=(246, 246, 250))
        d.rounded_rectangle((cx - cw / 2, cy - ch / 2, cx + cw / 2, cy - ch / 2 + 190), radius=40, fill=p["acento"])
        d.rectangle((cx - cw / 2, cy - ch / 2 + 140, cx + cw / 2, cy - ch / 2 + 190), fill=p["acento"])
        _centro_texto(d, cx, cy - ch / 2 + 95, "ABRIL 2029", _f(92), p["fundo"])
        sem = "DSTQQSS"
        x0, y0, cel = cx - cw / 2 + 50, cy - ch / 2 + 250, (cw - 100) / 7
        for k, s_ in enumerate(sem):
            _centro_texto(d, x0 + cel * (k + 0.5), y0, s_, _f(46), (120, 130, 150))
        mostrar = int(1 + _suave(t / max(0.1, dur * 0.55)) * 12.5)   # os dias vão aparecendo até o 13
        for dia in range(1, 31):
            col, lin = (dia - 1) % 7, (dia - 1) // 7      # 1º de abril de 2029 é domingo
            x, y = x0 + cel * (col + 0.5), y0 + 100 + lin * 115
            cor = (40, 48, 70) if dia <= mostrar else (210, 214, 224)
            if dia == 13 and mostrar >= 13:
                pulsa = 1 + 0.08 * math.sin(t * 8)
                rr = 56 * pulsa
                d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=(232, 44, 56), width=10)
                cor = (232, 44, 56)
            _centro_texto(d, x, y, str(dia), _f(54), cor)
        if mostrar >= 13:
            _rotulo_caixa(d, H * 0.18, rot or "SEXTA-FEIRA 13", p)
        return
    if cena.get("tamanho"):
        horiz = H * 0.74
        for y in range(0, int(horiz), 8):
            f_ = y / horiz
            d.rectangle((0, y, W, y + 8), fill=tuple(int(a + (b - a) * f_) for a, b in zip((18, 30, 70), (70, 110, 170))))
        d.rectangle((0, horiz, W, H), fill=(24, 30, 44))
        alt = 820
        _torre(d, W * 0.3, horiz, alt, (16, 20, 34))
        s_ = _suave(t / max(0.1, dur * 0.35))
        ax, ay = W * 0.72 + (1 - s_) * 500, horiz - alt / 2
        _rocha(d, ax, ay, alt * 0.36, ang=1.45 + t * 0.15)
        if s_ > 0.95:                                    # régua: as duas alturas iguais
            d.line((W * 0.08, horiz - alt, W * 0.94, horiz - alt), fill=p["acento"] + (200,), width=5)
        if rot:
            _rotulo_caixa(d, H * 0.13, rot, p)
        return
    if cena.get("risco"):
        _estrelas(d, t, 70)
        de, ate = float(cena.get("de", 0)), float(cena.get("ate", 2.7))
        v = de + (ate - de) * _suave(t / max(0.1, dur * 0.35))
        if cena.get("recorde"):                          # escala de perigo de 0 a 10, acende até o nível 4
            nivel = int(prog * 4.99)
            x0, y0, bw = W * 0.08, H * 0.42, W * 0.84 / 11
            cores = [(240, 240, 245)] + [(80, 200, 110)] + [(250, 220, 60)] * 3 + [(255, 150, 40)] * 3 + [(232, 44, 56)] * 3
            for k in range(11):
                a_ = 255 if k <= nivel else 60
                h_ = 160 + k * 26
                d.rounded_rectangle((x0 + k * bw + 6, y0 + 300 - h_, x0 + (k + 1) * bw - 6, y0 + 300), radius=10,
                                    fill=cores[k] + (a_,))
            if nivel >= 4:
                x = x0 + 4.5 * bw
                yy = y0 + 300 - (160 + 4 * 26) - 60 + math.sin(t * 6) * 10
                d.polygon([(x - 30, yy - 40), (x + 30, yy - 40), (x, yy)], fill=p["acento"])
            _centro_texto(d, W / 2, y0 + 380, "ESCALA DE PERIGO", _f(56), p["acento2"])
            _rotulo_caixa(d, H * 0.2, rot or "RECORDE", p)
            return
        cx, cy, R = W / 2, H * 0.55, 360                 # medidor de ponteiro
        d.arc((cx - R, cy - R, cx + R, cy + R), 180, 360, fill=(60, 80, 120), width=60)
        fr = min(1.0, v / 3.0)
        cor = (232, 44, 56) if v > 0.5 else (80, 200, 110)
        if fr > 0.002:
            d.arc((cx - R, cy - R, cx + R, cy + R), 180, 180 + 180 * fr, fill=cor, width=60)
        a = math.pi + math.pi * fr
        d.line((cx, cy, cx + math.cos(a) * (R - 70), cy + math.sin(a) * (R - 70)), fill=p["fig"], width=16)
        d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), fill=p["fig"])
        if v < 0.05:
            txt = "ZERO"
        elif cena.get("valor"):
            txt = str(cena["valor"])
        elif ate < de:                                   # descendo: sem número no caminho, só o ponteiro (nada que a narração não diga)
            txt = "..."
        else:
            txt = f"{v:.1f}%".replace(".", ",")
        _centro_texto(d, cx, cy + 150, txt, _fit(d, txt, 150), cor)
        _centro_texto(d, cx, cy + 270, "CHANCE DE BATER", _f(50), p["acento2"])
        _rocha(d, W * 0.78, H * 0.22, 80, ang=t * 0.6)
        if rot:
            _centro_texto(d, W / 2, H * 0.3, rot, _fit(d, rot, 60), p["acento"])
        return
    if cena.get("ceu"):
        horiz = H * 0.7
        _ceu_noite(d, t, horiz)
        x = W * 0.12 + (W * 0.76) * (0.15 + 0.7 * (t / max(0.1, dur)))
        y = H * 0.32 - math.sin((x / W) * math.pi) * 140
        for k in range(18, 0, -1):                       # rastro fraco
            xx = x - k * 9
            yy = H * 0.32 - math.sin((xx / W) * math.pi) * 140
            d.ellipse((xx - 3, yy - 3, xx + 3, yy + 3), fill=(255, 240, 200, 120 - k * 6))
        brilho = 7 + 2 * math.sin(t * 5)
        d.ellipse((x - brilho * 3, y - brilho * 3, x + brilho * 3, y + brilho * 3), fill=(255, 230, 160, 50))
        d.ellipse((x - brilho, y - brilho, x + brilho, y + brilho), fill=(255, 250, 230))
        if cena.get("seta", True):
            d.ellipse((x - 60, y - 60, x + 60, y + 60), outline=p["acento"] + (170,), width=5)
        _morro_gente(d, t, horiz, n=int(cena.get("gente", 5)))
        if rot:
            _rotulo_caixa(d, H * 0.12, rot, p)
        return
    if cena.get("mapa"):
        _estrelas(d, t)
        from . import globo
        cx, cy, R = W / 2, H * 0.55, 400
        lon_c, inc = -0.30, 0.3
        if globo.tem_mapa():
            tr = globo.terra(R, lon=lon_c, nuvens=t * 0.25, inclina=inc)
            img.paste(tr, (int(cx - tr.width / 2), int(cy - tr.height / 2)), tr)
            d = ImageDraw.Draw(img, "RGBA")
        else:
            _globo(d, cx, cy, R, 0, 0)
        # leste da América do Sul, norte da África e Europa (Live Science, mapas da passagem)
        for k, (la, lo) in enumerate([(-10, -40), (-20, -44), (-5, -36), (15, 5), (25, 15), (10, 20), (30, -5),
                                      (45, 5), (48, 15), (40, -4)]):
            la_, lo_ = math.radians(la), math.radians(lo) - lon_c
            X, yw, zw = math.cos(la_) * math.sin(lo_), math.sin(la_), math.cos(la_) * math.cos(lo_)
            Y = -yw * math.cos(inc) + zw * math.sin(inc)
            Z = yw * math.sin(inc) + zw * math.cos(inc)
            if Z <= 0.05:
                continue
            px_, py_ = cx + X * R, cy + Y * R
            f_ = _suave((t - k * 0.12) / 0.5)
            pul = (t * 1.2 + k * 0.3) % 1
            d.ellipse((px_ - 12 * f_, py_ - 12 * f_, px_ + 12 * f_, py_ + 12 * f_), fill=p["acento"] + (int(255 * f_),))
            rr = 12 + pul * 40
            d.ellipse((px_ - rr, py_ - rr, px_ + rr, py_ + rr), outline=p["acento"] + (int(200 * (1 - pul) * f_),), width=4)
        ax = W * 1.1 - (W * 1.3) * prog
        ay = cy - R - 160 + prog * 60
        for k in range(10, 0, -1):
            d.ellipse((ax + k * 14 - 4, ay - k * 2 - 4, ax + k * 14 + 4, ay - k * 2 + 4), fill=(255, 240, 200, 150 - k * 13))
        _rocha(d, ax, ay, 42, ang=t)
        if rot:
            _rotulo_caixa(d, H * 0.15, rot, p)
        return
    if cena.get("perto"):                                # close (fora de escala): a Terra embaixo, satélites e o asteroide passando
        _estrelas(d, t)
        cx, cy, re = W / 2, H * 1.12, 700
        _globo(d, cx, cy, re, t * 0.2)
        d = ImageDraw.Draw(img, "RGBA")
        rs = re * 1.9
        d.arc((cx - rs, cy - rs, cx + rs, cy + rs), 200, 340, fill=(86, 214, 255, 150), width=4)
        for k in range(9):
            a = math.radians(205 + k * 16.5 + t * 2)
            sx, sy = cx + math.cos(a) * rs, cy + math.sin(a) * rs
            d.rectangle((sx - 9, sy - 9, sx + 9, sy + 9), fill=(230, 236, 250))
            d.rectangle((sx - 34, sy - 4, sx - 11, sy + 4), fill=(86, 160, 255))
            d.rectangle((sx + 11, sy - 4, sx + 34, sy + 4), fill=(86, 160, 255))
        de, ate = float(cena.get("de", 0.0)), float(cena.get("ate", 1.0))
        u = de + (ate - de) * prog
        ax = W * 1.15 - u * W * 1.3
        ay = H * 0.64 - (1 - 4 * (u - 0.5) ** 2) * 60
        for k in range(16, 0, -1):
            d.ellipse((ax + k * 22 - 14, ay - k * 4 - 14, ax + k * 22 + 14, ay - k * 4 + 14), fill=(255, 220, 160, 110 - k * 6))
        _rocha(d, ax, ay, 95, ang=t * 0.5)
        if rot:
            _rotulo_caixa(d, H * 0.13, rot, p)
        return
    # visão de cima, em escala: Terra, anel geoestacionário (~6,6 raios do centro) e a passagem (~5,7 raios)
    _estrelas(d, t)
    cx, cy, re = W / 2, H * 0.56, 72
    _globo(d, cx, cy, re, t * 0.5)
    d = ImageDraw.Draw(img, "RGBA")
    rg = re * 6.6
    for k in range(72):                                  # anel tracejado
        a0, a1 = k * 5, k * 5 + 3
        d.arc((cx - rg, cy - rg, cx + rg, cy + rg), a0, a1, fill=(86, 214, 255, 150), width=4)
    for k in range(14):                                  # satélites
        a = k / 14 * 2 * math.pi + t * 0.15
        sx, sy = cx + math.cos(a) * rg, cy + math.sin(a) * rg
        d.rectangle((sx - 6, sy - 6, sx + 6, sy + 6), fill=(230, 236, 250))
        d.rectangle((sx - 22, sy - 3, sx - 8, sy + 3), fill=(86, 160, 255))
        d.rectangle((sx + 8, sy - 3, sx + 22, sy + 3), fill=(86, 160, 255))
    dmin = re * 5.7
    de, ate = float(cena.get("de", 0.0)), float(cena.get("ate", 1.0))
    s_ = de + (ate - de) * prog

    def caminho(u, curva):
        # u de 0 a 1: entra pela direita, passa por cima da Terra a dmin do centro (u = 0,5) e sai pela esquerda;
        # "curva" entorta a saída (a órbita muda depois da passagem)
        k = (u - 0.5) * 2
        return cx - k * 640, cy - dmin - k * k * 420 + curva * 520 * max(0.0, k) ** 1.6
    if cena.get("orbita"):
        pts0 = [caminho(u / 40, 0) for u in range(41)]
        for k in range(0, 40, 2):
            d.line(pts0[k] + pts0[k + 1], fill=(200, 205, 220, 120), width=4)
        curva = _suave(t / max(0.1, dur * 0.7))
        pts = [caminho(u / 40, curva) for u in range(41)]
        d.line(pts, fill=p["acento"] + (230,), width=7)
    else:
        pts = [caminho(u / 40 * s_, 0) for u in range(41)]
        if len(pts) > 1:
            d.line(pts, fill=p["acento"] + (180,), width=5)
    ax, ay = caminho(s_, 1.0 if cena.get("orbita") else 0)
    if cena.get("orbita"):
        ax, ay = caminho(0.5 + 0.5 * _suave(t / max(0.1, dur)), _suave(t / max(0.1, dur * 0.7)))
    aperta = 1.0
    if cena.get("espreme"):
        aperta = 1.0 + 0.22 * abs(math.sin(t * 3))
        for k in range(10):                              # pedrinhas soltando
            rnd = random.Random(k * 3)
            f_ = (t * 0.6 + rnd.random()) % 1
            a = rnd.random() * 2 * math.pi
            px_, py_ = ax + math.cos(a) * (50 + f_ * 120), ay + math.sin(a) * (50 + f_ * 120)
            d.ellipse((px_ - 5, py_ - 5, px_ + 5, py_ + 5), fill=(170, 160, 150, int(255 * (1 - f_))))
        for k in range(3):                               # linhas da gravidade puxando para a Terra
            f_ = (t * 0.8 + k / 3) % 1
            x1, y1 = ax + (cx - ax) * f_ * 0.7, ay + (cy - ay) * f_ * 0.7
            d.line((x1, y1, x1 + (cx - ax) * 0.08, y1 + (cy - ay) * 0.08), fill=(86, 214, 255, int(220 * (1 - f_))), width=6)
    d.ellipse((ax - 80, ay - 80, ax + 80, ay + 80), outline=p["acento"] + (150,), width=5)
    _rocha(d, ax, ay, 56 if cena.get("espreme") else 46, ang=t * 0.8, aperta=aperta)
    if cena.get("medida"):                               # régua da Terra até o asteroide
        d.line((cx, cy - re, ax, ay + 50), fill=(255, 255, 255, 200), width=5)
    if cena.get("mira"):                                 # a rota que parecia apontar para a Terra
        for k in range(0, 20, 2):
            f0, f1 = k / 20, (k + 1) / 20
            d.line((ax + (cx - ax) * f0, ay + (cy - ay) * f0, ax + (cx - ax) * f1, ay + (cy - ay) * f1), fill=(232, 44, 56, 220), width=7)
        rr = re + 20 + 12 * math.sin(t * 6)
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=(232, 44, 56), width=8)
    if rot:
        _rotulo_caixa(d, H * 0.13, rot, p)


QUADROS.update({"apophis": _apophis})


# ---------------------------------------------------------------- Betelgeuse (a estrela que vai virar supernova)
ORION = {"betelgeuse": (0.30, 0.30), "bellatrix": (0.70, 0.33), "alnitak": (0.42, 0.52), "alnilam": (0.50, 0.505),
         "mintaka": (0.58, 0.49), "saiph": (0.35, 0.72), "rigel": (0.71, 0.70)}
ORION_LINHAS = [("betelgeuse", "bellatrix"), ("betelgeuse", "alnitak"), ("bellatrix", "mintaka"), ("alnitak", "alnilam"),
                ("alnilam", "mintaka"), ("alnitak", "saiph"), ("mintaka", "rigel"), ("saiph", "rigel")]


def _brilho_estrela(d, x, y, r, cor, t, raios=True):
    for k in range(9, 0, -1):
        rr = r * (1 + k * 0.6)
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=cor + (int(26 * (1 - k / 10)),))
    if raios:
        L = r * 5 * (1 + 0.06 * math.sin(t * 5))
        for a in (0, 90):
            ra = math.radians(a + 10)
            d.line((x - math.cos(ra) * L, y - math.sin(ra) * L, x + math.cos(ra) * L, y + math.sin(ra) * L),
                   fill=cor + (150,), width=max(2, int(r * 0.18)))
    d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255))


def _estrela(img, cena, t, dur, n, p):
    """Betelgeuse. Sem modo: o céu com Órion ("linhas": as linhas da constelação se desenhando; "destaca": círculo
    na Betelgeuse; "explode": ela vira supernova; "brilha": já explodida; "apaga": explodida e sumindo até deixar o
    ombro vazio; "lua": meia-lua no canto para comparar). Modos: "tamanho" (o Sol, um pontinho, ao lado da gigante
    vermelha), "neutrinos" (partículas atravessando a Terra antes da luz), "supernova" (close da explosão), "dia"
    (céu azul com o ponto brilhando de dia), "sombra" (você de noite com sombra no chão), "longe" (a Terra com a zona de
    perigo e a estrela muito longe), "meses" (12 meses; "ate": quantos acesos fortes), "rotulo"."""
    d = ImageDraw.Draw(img, "RGBA")
    rot = str(cena.get("rotulo", "")).upper()
    vermelho = (255, 110, 60)
    if cena.get("tamanho"):
        _estrelas(d, t, 60)
        cresce = _suave(t / max(0.1, dur * 0.6))
        R = 300 + 1000 * cresce                          # a borda da gigante subindo pela tela
        cx, cy = W / 2, H * 0.98 + R * 0.55
        for k in range(8, 0, -1):
            rr = R * (1 + k * 0.025)
            d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(255, 90, 40, 20))
        d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(214, 70, 40))
        for k in range(30):                              # manchas de convecção
            rnd = random.Random(k)
            a = math.pi + rnd.random() * math.pi
            rr = R * (0.6 + rnd.random() * 0.38)
            x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr
            m = R * (0.05 + rnd.random() * 0.05)
            d.ellipse((x - m, y - m, x + m, y + m), fill=(250, 120 + int(30 * math.sin(t * 2 + k)), 60, 120))
        sx, sy = W * 0.5, H * 0.3                        # o Sol: um pontinho
        d.ellipse((sx - 4, sy - 4, sx + 4, sy + 4), fill=(255, 230, 120))
        d.ellipse((sx - 40, sy - 40, sx + 40, sy + 40), outline=p["acento"], width=5)
        d.line((sx + 30, sy - 30, sx + 140, sy - 140), fill=p["acento"], width=6)
        d.text((sx + 150, sy - 210), "SOL", font=_f(70), fill=p["acento"])
        if rot:
            _rotulo_caixa(d, H * 0.13, rot, p)
        return
    if cena.get("neutrinos"):
        _estrelas(d, t, 70)
        cx, cy, R = W / 2, H * 0.56, 300
        _globo(d, cx, cy, R, t * 0.4)
        d = ImageDraw.Draw(img, "RGBA")
        for k in range(46):                              # passam direto, por fora e por dentro da Terra
            rnd = random.Random(k * 5)
            y = cy - 620 + rnd.random() * 1240
            x = ((t * 900 + rnd.random() * 2000) % 2000) - 400
            d.line((x - 130, y + 40, x, y), fill=(86, 214, 255, 200), width=4)
            d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(200, 245, 255))
        pisca = (t % 0.6) < 0.3
        bx, by = cx, H * 0.24                          # detector no alto (embaixo fica a legenda)
        d.rounded_rectangle((bx - 220, by - 60, bx + 220, by + 60), radius=20, fill=(10, 20, 40, 230), outline=p["acento2"], width=4)
        d.ellipse((bx - 190, by - 18, bx - 154, by + 18), fill=(80, 230, 120) if pisca else (30, 60, 40))
        d.text((bx - 130, by - 30), "DETECTOR", font=_f(50), fill=p["fig"])
        if rot:
            _rotulo_caixa(d, H * 0.13 if by > H * 0.4 else H * 0.33, rot, p)
        return
    if cena.get("supernova"):
        _estrelas(d, t, 90)
        cx, cy = W / 2, H * 0.5
        f_ = t / max(0.1, dur)
        if f_ < 0.25:                                    # a gigante encolhe (o miolo desaba)
            r = 260 * (1 - _suave(f_ / 0.25) * 0.8)
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(214, 70, 40))
        else:
            g = _suave((f_ - 0.25) / 0.6)
            for k in range(6, 0, -1):                    # casca de gás se espalhando
                rr = 60 + g * 520 * k / 6
                d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=(255, 160 - k * 10, 90, int(170 * (1 - g * 0.5))), width=14)
            _brilho_estrela(d, cx, cy, 50 + 60 * g, (190, 220, 255), t)
            flash = max(0.0, 1 - (f_ - 0.25) / 0.2)
            if flash > 0:
                d.rectangle((0, 0, W, H), fill=(255, 255, 255, int(200 * flash)))
        if rot:
            _rotulo_caixa(d, H * 0.13, rot, p)
        return
    if cena.get("dia") or cena.get("sombra"):
        horiz = H * 0.66
        dia = bool(cena.get("dia"))
        c1, c2 = ((60, 130, 220), (170, 210, 245)) if dia else ((8, 12, 34), (26, 40, 84))
        for y in range(0, int(horiz), 8):
            f_ = y / horiz
            d.rectangle((0, y, W, y + 8), fill=tuple(int(a + (b - a) * f_) for a, b in zip(c1, c2)))
        if not dia:
            _ceu_noite(d, t, horiz)
        sx, sy = W * 0.28, H * 0.24
        _brilho_estrela(d, sx, sy, 16, (200, 225, 255) if dia else (210, 230, 255), t)
        if dia:
            d.ellipse((W * 0.78 - 70, H * 0.26 - 70, W * 0.78 + 70, H * 0.26 + 70), fill=(255, 245, 200))
            chao_c = (60, 90, 70)
        else:
            chao_c = (30, 36, 52)
        d.rectangle((0, horiz, W, H), fill=chao_c)
        for k in range(9):                               # prédios e árvores no horizonte
            rnd = random.Random(k * 9)
            x = k * W / 8 - 40
            h_ = 90 + rnd.random() * 220
            d.rectangle((x, horiz - h_, x + 80 + rnd.random() * 40, horiz), fill=(40, 60, 90) if dia else (12, 16, 30))
        if cena.get("sombra"):
            px_, chao = W * 0.66, H * 0.72
            # a sombra cai do lado oposto à estrela
            dx, dy = (px_ - sx), (chao - sy)
            L = math.hypot(dx, dy)
            ux, uy = dx / L, dy / L
            comp = 420 * _suave(t / max(0.1, dur * 0.4))
            d.polygon([(px_ - 40, chao), (px_ + 40, chao), (px_ + 40 + ux * comp, chao + uy * comp * 0.35),
                       (px_ - 40 + ux * comp, chao + uy * comp * 0.35)], fill=(0, 0, 0, 150))
            _pessoa(d, px_, chao, 300, (210, 220, 240), t)
        if rot:
            _rotulo_caixa(d, H * 0.82 if dia else H * 0.12, rot, p)
        return
    if cena.get("longe"):
        _estrelas(d, t, 90)
        ex, ey, R = W * 0.68, H * 0.74, 70
        _globo(d, ex, ey, R, t * 0.4)
        d = ImageDraw.Draw(img, "RGBA")
        zr = 170 + 6 * math.sin(t * 3)
        d.ellipse((ex - zr, ey - zr, ex + zr, ey + zr), fill=(232, 44, 56, 40), outline=(232, 44, 56, 200), width=5)
        bx, by = W * 0.2, H * 0.26
        _brilho_estrela(d, bx, by, 14, vermelho, t)
        f_ = _suave(t / max(0.1, dur * 0.7))
        n_ = int(24 * f_)
        for k in range(n_):
            a0 = k / 24
            x1, y1 = bx + (ex - bx) * a0, by + (ey - by) * a0
            x2, y2 = bx + (ex - bx) * (a0 + 0.022), by + (ey - by) * (a0 + 0.022)
            d.line((x1, y1, x2, y2), fill=(255, 255, 255, 170), width=5)
        if rot:
            _rotulo_caixa(d, H * 0.5, rot, p)
        return
    if cena.get("meses"):
        _estrelas(d, t, 70)
        ate = int(cena.get("ate", 3))
        mostrar = _suave(t / max(0.1, dur * 0.7)) * 12
        nomes = "JFMAMJJASOND"
        x0, y0, cw, ch = W * 0.1, H * 0.5, W * 0.8 / 4, 200
        for k in range(12):
            col, lin = k % 4, k // 4
            x, y = x0 + col * cw, y0 + lin * (ch + 20)
            aceso = k < mostrar
            forte = k < ate
            cor = (255, 240, 200, 255) if (aceso and forte) else ((150, 170, 210, 200) if aceso else (60, 70, 100, 120))
            d.rounded_rectangle((x + 8, y, x + cw - 8, y + ch), radius=18, fill=cor[:3] + (60 if aceso else 30,), outline=cor, width=5)
            if aceso:
                rr = 26 if forte else 12
                d.ellipse((x + cw / 2 - rr, y + ch / 2 - rr, x + cw / 2 + rr, y + ch / 2 + rr), fill=cor)
        _brilho_estrela(d, W / 2, H * 0.3, 26, (200, 225, 255), t)
        if rot:
            _rotulo_caixa(d, H * 0.13, rot, p)
        return
    # céu com Órion
    for y in range(0, H, 8):
        f_ = y / H
        d.rectangle((0, y, W, y + 8), fill=tuple(int(a + (b - a) * f_) for a, b in zip((4, 8, 26), (20, 30, 70))))
    _estrelas(d, t, 90)
    pos = {k: (x * W, y * H) for k, (x, y) in ORION.items()}
    if cena.get("linhas"):
        f_ = _suave(t / max(0.1, dur * 0.8)) * len(ORION_LINHAS)
        for k, (a, b) in enumerate(ORION_LINHAS):
            q = min(1.0, max(0.0, f_ - k))
            if q <= 0:
                continue
            (x1, y1), (x2, y2) = pos[a], pos[b]
            d.line((x1, y1, x1 + (x2 - x1) * q, y1 + (y2 - y1) * q), fill=(140, 180, 255, 140), width=4)
    some = 0.0
    explode = 0.0
    if cena.get("explode"):
        explode = _suave((t - dur * 0.15) / max(0.1, dur * 0.4))
    if cena.get("brilha"):
        explode = 1.0
    if cena.get("apaga"):
        explode, some = 1.0, _suave(t / max(0.1, dur * 0.7))
    for nome, (x, y) in pos.items():
        if nome == "betelgeuse":
            continue
        r = 9 if nome in ("rigel",) else 7
        _brilho_estrela(d, x, y, r, (180, 210, 255), t, raios=False)
    bx, by = pos["betelgeuse"]
    if explode <= 0:
        r = 11 + 1.5 * math.sin(t * 3)
        _brilho_estrela(d, bx, by, r, vermelho, t, raios=False)
        d.ellipse((bx - r * 0.7, by - r * 0.7, bx + r * 0.7, by + r * 0.7), fill=(255, 170, 120))
    elif some < 1:
        r = (11 + 44 * explode) * (1 - some * 0.95)
        cor = tuple(int(a + (b - a) * explode) for a, b in zip(vermelho, (200, 225, 255)))
        _brilho_estrela(d, bx, by, r, cor, t)
    if some > 0.9 or cena.get("vazio"):
        for k in range(0, 360, 30):
            d.arc((bx - 50, by - 50, bx + 50, by + 50), k, k + 15, fill=(255, 255, 255, 160), width=4)
    if cena.get("destaca"):
        rr = 60 + 8 * math.sin(t * 4)
        d.ellipse((bx - rr, by - rr, bx + rr, by + rr), outline=p["acento"], width=6)
    if cena.get("lua"):
        lx, ly, lr = W * 0.75, H * 0.16, 70
        d.ellipse((lx - lr, ly - lr, lx + lr, ly + lr), fill=(60, 64, 80))
        d.pieslice((lx - lr, ly - lr, lx + lr, ly + lr), 90, 270, fill=(240, 236, 220))
    if rot:
        _rotulo_caixa(d, H * 0.13, rot, p)


QUADROS.update({"estrela": _estrela})


# ---------------------------------------------------------------- oceano em camadas (descida até a fossa)
ZONAS_MAR = [(0, 200, "ZONA DO SOL", (40, 130, 215)), (200, 1000, "CREPÚSCULO", (16, 58, 120)),
             (1000, 4000, "MEIA-NOITE", (5, 14, 40)), (4000, 6000, "ABISMO", (3, 8, 22)),
             (6000, 11000, "FOSSA", (2, 4, 12))]          # limites da NOAA (JetStream, "Layers of the Ocean")


def _cor_mar(prof):
    for a, b, _, c in ZONAS_MAR:
        if prof < b:
            prox = next((z[3] for z in ZONAS_MAR if z[0] == b), c)
            f_ = (prof - a) / (b - a)
            return tuple(int(x + (y - x) * f_ ** 2) for x, y in zip(c, prox))
    return ZONAS_MAR[-1][3]


def _submarino(d, sx, sy, p, t, luz=True, esc=1.0):
    """Submarino com volume: casco com sombra embaixo e brilho em cima, janelas com reflexo, hélice girando."""
    am = p["acento"]
    esc_ = lambda v: v * esc
    sombra = tuple(int(v * 0.62) for v in am)
    brilho = tuple(min(255, int(v * 1.12)) for v in am)
    if luz:
        d.polygon([(sx - esc_(200), sy + esc_(40)), (sx - esc_(250), sy + esc_(60)), (sx - esc_(560), sy + esc_(560)),
                   (sx + esc_(80), sy + esc_(560))], fill=(255, 240, 170, 60))
    d.rounded_rectangle((sx - esc_(230), sy - esc_(90), sx + esc_(230), sy + esc_(90)), radius=int(esc_(90)), fill=sombra)
    d.rounded_rectangle((sx - esc_(226), sy - esc_(90), sx + esc_(226), sy + esc_(56)), radius=int(esc_(80)), fill=am)
    d.rounded_rectangle((sx - esc_(170), sy - esc_(76), sx + esc_(150), sy - esc_(50)), radius=int(esc_(14)), fill=brilho)
    d.rounded_rectangle((sx - esc_(70), sy - esc_(150), sx + esc_(70), sy - esc_(70)), radius=int(esc_(30)), fill=am)
    d.rectangle((sx - esc_(52), sy - esc_(140), sx + esc_(40), sy - esc_(126)), fill=brilho)
    for k in range(-3, 4):                               # rebites
        d.ellipse((sx + k * esc_(60) - 5, sy + esc_(66) - 5, sx + k * esc_(60) + 5, sy + esc_(66) + 5), fill=sombra)
    for wx in (-105, 25):
        d.ellipse((sx + esc_(wx - 45), sy - esc_(45), sx + esc_(wx + 45), sy + esc_(45)), fill=(20, 30, 50), outline=(40, 48, 66), width=int(esc_(12)))
        d.ellipse((sx + esc_(wx - 30), sy - esc_(30), sx + esc_(wx + 30), sy + esc_(30)), fill=p["acento2"])
        d.ellipse((sx + esc_(wx - 20), sy - esc_(24), sx + esc_(wx - 4), sy - esc_(8)), fill=(240, 250, 255))
    d.polygon([(sx + esc_(225), sy), (sx + esc_(290), sy - esc_(70)), (sx + esc_(290), sy + esc_(70))], fill=sombra)
    h = math.sin(t * 14) * esc_(40)
    d.line((sx + esc_(300), sy - h, sx + esc_(300), sy + h), fill=(200, 200, 210), width=int(esc_(16)))
    d.ellipse((sx - esc_(250), sy + esc_(20), sx - esc_(214), sy + esc_(56)), fill=(255, 250, 220))   # farol


def _lula(d, x, y, s, cor, t):
    d.polygon([(x, y - s), (x - s * 0.35, y - s * 0.3), (x - s * 0.3, y + s * 0.4), (x + s * 0.3, y + s * 0.4),
               (x + s * 0.35, y - s * 0.3)], fill=cor)
    for k in range(6):
        ox = (k - 2.5) * s * 0.1
        bal = math.sin(t * 4 + k) * s * 0.12
        d.line((x + ox, y + s * 0.4, x + ox + bal, y + s * 1.1), fill=cor, width=max(3, int(s * 0.06)))


def _cachalote(d, x, y, s, cor):
    d.rounded_rectangle((x - s, y - s * 0.32, x + s * 0.3, y + s * 0.32), radius=int(s * 0.3), fill=cor)
    d.ellipse((x - s * 0.1, y - s * 0.26, x + s * 0.9, y + s * 0.26), fill=cor)
    d.polygon([(x + s * 0.8, y), (x + s * 1.25, y - s * 0.3), (x + s * 1.15, y), (x + s * 1.25, y + s * 0.3)], fill=cor)
    d.ellipse((x - s * 0.78, y - s * 0.12, x - s * 0.7, y - s * 0.04), fill=(10, 10, 16))


def _oceano(img, cena, t, dur, n, p):
    """Descida pelas camadas do mar. "de"/"ate": profundidade em metros (o fundo muda de cor com ela e aparece o
    nome da zona). Bichos de cada zona: "peixes" (cardume com raios de sol), "lulas" (lulas e krill), "brilho"
    (bichos que brilham no escuro), "cachalote", "paredes" (as paredes da fossa se fechando), "peixe_caracol"
    (peixe-caracol pálido na luz do farol), "fundo" (o chão da fossa). "zonas": o mar em corte com as cinco camadas
    e o submarino descendo por elas. "rotulo"; "nome_zona": false esconde o nome da zona."""
    d = ImageDraw.Draw(img, "RGBA")
    rot = str(cena.get("rotulo", "")).upper()
    de, ate = float(cena.get("de", 0)), float(cena.get("ate", 0))
    prog = _suave(t / max(0.1, dur * 0.85))
    prof = de + (ate - de) * prog
    if cena.get("zonas"):
        topo, base = H * 0.2, H * 0.96
        esc = lambda m: topo + (base - topo) * (math.log10(1 + m / 50) / math.log10(1 + 11000 / 50))
        d.rectangle((0, 0, W, topo), fill=(150, 205, 250))
        for y in range(int(topo), int(base), 4):
            lo, hi = 0.0, 11000.0                        # inverte a escala por busca simples
            for _ in range(20):
                mid = (lo + hi) / 2
                if esc(mid) < y:
                    lo = mid
                else:
                    hi = mid
            d.rectangle((0, y, W, y + 4), fill=_cor_mar(lo))
        d.rectangle((0, base, W, H), fill=(40, 34, 30))
        for a, b, nome, _ in ZONAS_MAR:
            y0, y1 = esc(a), esc(b)
            d.line((0, y0, W, y0), fill=(255, 255, 255, 60), width=3)
            d.text((W * 0.06, (y0 + y1) / 2 - 30), nome, font=_f(54), fill=(230, 240, 255, 235))
        sy = esc(prof)
        _submarino(d, W * 0.74, min(sy, H * 0.93), p, t, luz=prof > 300, esc=0.42)
        if rot:
            _rotulo_caixa(d, H * 0.1, rot, p)
        return
    d.rectangle((0, 0, W, H), fill=_cor_mar(prof))
    if prof < 220:                                       # raios de sol vindo de cima
        a_ = int(70 * (1 - prof / 220))
        for k in range(6):
            x = W * (0.1 + k * 0.17) + math.sin(t * 0.8 + k) * 30
            d.polygon([(x - 30, 0), (x + 30, 0), (x + 160, H), (x + 40, H)], fill=(255, 255, 220, a_))
    vel = 1.0 if ate > de else 0.25
    for k in range(70):                                  # neve marinha subindo: sensação de descer
        rnd = random.Random(k * 11)
        x = rnd.random() * W
        y = (rnd.random() * H - t * (240 * vel + rnd.random() * 80)) % H
        d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(200, 220, 240, 90 if prof > 200 else 50))
    sx, sy = W / 2 + math.sin(t * 1.1) * 12, H * 0.42 + math.sin(t * 1.7) * 14
    if cena.get("paredes"):                              # paredes da fossa se fechando
        f_ = 0.6 + 0.4 * prog
        for lado in (-1, 1):
            pts = [(W / 2 + lado * W * 0.5, -10)]
            for k in range(12):
                y = k * H / 11
                rnd = random.Random(k * 3 + (lado > 0))
                x = W / 2 + lado * (W * 0.5 - W * 0.16 * f_ - rnd.random() * 50 + ((t * 120 + y) % 60) * 0)
                pts.append((x, y))
            pts.append((W / 2 + lado * W * 0.6, H + 10))
            pts.append((W / 2 + lado * W * 0.6, -10))
            d.polygon(pts, fill=(28, 24, 26))
    if cena.get("peixes"):
        for k in range(16):
            rnd = random.Random(k)
            fx = (W + 200 - ((t * 160 + rnd.random() * W * 1.6) % (W + 400)))
            fy = H * 0.66 + rnd.random() * 380 + math.sin(t * 3 + k) * 14
            s = 26 + rnd.random() * 10
            d.ellipse((fx - s, fy - s * 0.4, fx + s, fy + s * 0.4), fill=(210, 232, 250))
            d.polygon([(fx + s * 0.8, fy), (fx + s * 1.5, fy - s * 0.5), (fx + s * 1.5, fy + s * 0.5)], fill=(210, 232, 250))
    if cena.get("lulas"):
        for k in range(4):
            rnd = random.Random(k * 7)
            x = W * (0.15 + 0.7 * rnd.random())
            y = (H * 0.65 + rnd.random() * 500 - t * 60 * (1 + k % 2)) % H + 300 * (k % 2)
            _lula(d, x, min(y, H * 0.92), 60 + k * 8, (190, 90, 110, 220), t + k)
        for k in range(60):                              # krill
            rnd = random.Random(k * 17)
            x = (rnd.random() * W + t * 30) % W
            y = H * 0.62 + rnd.random() * H * 0.36
            d.ellipse((x - 4, y - 2, x + 4, y + 2), fill=(240, 160, 140, 160))
    if cena.get("brilho") or cena.get("lulas"):
        for k in range(40 if cena.get("brilho") else 14):  # bioluminescência piscando
            rnd = random.Random(k * 29)
            x, y = rnd.random() * W, H * 0.55 + rnd.random() * H * 0.43
            if not cena.get("brilho"):
                y = rnd.random() * H
            a_ = abs(math.sin(t * (1.5 + rnd.random() * 2) + k))
            cor = (80, 240, 255) if k % 3 else (140, 255, 170)
            for rr, al in ((22, 40), (10, 120), (4, 255)):
                d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=cor + (int(al * a_),))
    if cena.get("cachalote"):
        cx_ = W + 520 - ((t * 200) % (W + 1100))
        _cachalote(d, cx_, H * 0.78, 300, (70, 76, 92))
    if cena.get("fundo"):
        d.polygon([(0, H * 0.84), (W * 0.3, H * 0.82), (W * 0.6, H * 0.85), (W, H * 0.83), (W, H), (0, H)], fill=(58, 50, 44))
        for k in range(7):                               # bolotas no chão (seres de uma célula só, xenofióforos)
            rnd = random.Random(k * 41)
            x = W * (0.08 + 0.85 * rnd.random())
            y = H * 0.86 + rnd.random() * 40
            r = 18 + rnd.random() * 16
            d.ellipse((x - r, y - r * 0.7, x + r, y + r * 0.5), fill=(150, 130, 110))
    if cena.get("peixe_caracol"):
        fx = W * 0.62 + math.sin(t * 0.7) * 120
        fy = H * 0.74 + math.sin(t * 1.3) * 16
        d.polygon([(sx - 120, sy + 40), (sx - 60, sy + 40), (fx + 260, fy + 140), (fx - 220, fy + 140)], fill=(255, 240, 170, 40))
        cor = (244, 214, 220)
        d.ellipse((fx - 110, fy - 46, fx + 40, fy + 46), fill=cor)
        d.polygon([(fx + 20, fy - 40), (fx + 200, fy - 8 + math.sin(t * 6) * 10), (fx + 200, fy + 12 + math.sin(t * 6) * 10),
                   (fx + 20, fy + 40)], fill=cor)
        d.ellipse((fx - 86, fy - 20, fx - 64, fy + 2), fill=(30, 30, 50))
    _submarino(d, sx, sy, p, t, luz=cena.get("luz", prof > 300))
    if cena.get("nome_zona", True) and not rot:
        nome = next((z[2] for z in ZONAS_MAR if prof < z[1]), ZONAS_MAR[-1][2])
        _rotulo_caixa(d, H * 0.13, nome, p)
    if rot:
        _rotulo_caixa(d, H * 0.13, rot, p)


QUADROS.update({"oceano": _oceano})
