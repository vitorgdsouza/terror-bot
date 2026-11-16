"""Recorta os personagens da folha de modelos (folha_modelos.jpg) e gera as figurinhas usadas na animação.
Rode da raiz do repositório:  python assets/personagem/v2/fonte/montar_sprites.py"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as nd

AQUI = Path(__file__).parent
DEST = AQUI.parent
FOLHAS = {n: Image.open(AQUI / f"{n}.jpg").convert("RGB") for n in ("folha_modelos", "folha_modelos_2", "folha_modelos_3")}
TOPO, PES, LARG, ALT = 52, 1115, 1000, 1200

# nome: (folha, caixa na folha, olhos [(x0,y0,x1,y1) em pixels do recorte])
PECAS = {
    "homem/frente": ("folha_modelos", (390, 75, 580, 625), [(73, 40, 88, 48), (96, 40, 111, 48)]),
    "homem/costas": ("folha_modelos", (588, 70, 765, 625), []),
    "homem/gritando": ("folha_modelos_3", (588, 55, 732, 345), []),
    "homem/perfil": ("folha_modelos_3", (462, 345, 535, 628), []),
    "mulher/frente": ("folha_modelos", (30, 70, 225, 630), [(65, 43, 78, 53), (89, 43, 100, 53)]),
    "mulher/perfil": ("folha_modelos", (250, 70, 360, 625), [(14, 43, 23, 50)]),
    "mulher/costas": ("folha_modelos_2", (395, 70, 575, 615), []),
    "mulher/medo": ("folha_modelos_2", (597, 70, 757, 620), []),
    "mulher/encolhida": ("folha_modelos_3", (230, 55, 345, 262), []),
    "sobrenatural": ("folha_modelos", (0, 690, 250, 1250), []),
    "invasor": ("folha_modelos_2", (378, 735, 593, 1305), []),
}


def recortar(folha, caixa):
    FOLHA = FOLHAS[folha]
    sub = np.asarray(FOLHA.crop(caixa)).astype(float)
    FUNDO = np.median(np.concatenate([sub[0], sub[-1], sub[:, 0], sub[:, -1]]), axis=0)   # cor do fundo pelas bordas
    m = np.sqrt(((sub - FUNDO) ** 2).sum(-1)) > 20
    m = nd.binary_closing(m, iterations=2)
    lab, n = nd.label(m)
    m = lab == (1 + int(np.argmax(nd.sum(m, lab, range(1, n + 1)))))   # só a figura maior (tira textos)
    m = nd.binary_opening(nd.binary_fill_holes(m), iterations=1)
    borda = m & ~nd.binary_erosion(m, iterations=2)   # contorno escuro: não sobra o azul do fundo da folha
    arr = np.asarray(FOLHA.crop(caixa)).copy()
    arr[borda] = (arr[borda] * 0.3).astype("uint8")
    alfa = Image.fromarray((nd.binary_erosion(m, iterations=1) * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.8))
    img = Image.fromarray(arr).convert("RGBA")
    img.putalpha(alfa)
    return img.crop(img.getbbox())


def piscando(img, olhos):
    """Fecha os olhos: cobre cada olho com a cor da pele logo acima e desenha a linha da pálpebra."""
    out = img.copy()
    d = ImageDraw.Draw(out)
    for x0, y0, x1, y1 in olhos:
        pele = img.getpixel(((x0 + x1) // 2, y1 + 2))[:3]
        d.ellipse((x0, y0, x1, y1), fill=pele + (255,))
        d.line((x0 + 1, (y0 + y1) // 2 + 1, x1 - 1, (y0 + y1) // 2 + 1), fill=(25, 25, 35, 255), width=1)
    return out


ALTURA_REAL = {"encolhida": 0.58}       # agachada: fica mais baixa que em pé


def encaixar(img, sobrenatural=False, nome=""):
    bb = img.getbbox()
    img = img.crop(bb)
    alvo = PES - TOPO if not sobrenatural else 1076
    alvo = int(alvo * ALTURA_REAL.get(nome.split("/")[-1], 1))
    e = alvo / img.height
    nitidez = 60 if e < 2.5 else 110                 # figuras pequenas da folha recebem mais nitidez
    img = img.resize((int(img.width * e), alvo), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, nitidez, 2))
    tela = Image.new("RGBA", (LARG, ALT), (0, 0, 0, 0))
    base = PES if not sobrenatural else 1128
    tela.alpha_composite(img, ((LARG - img.width) // 2, base - img.height))
    return tela


for nome, (folha, caixa, olhos) in PECAS.items():
    img = recortar(folha, caixa)
    sob = nome == "sobrenatural"
    (DEST / nome).parent.mkdir(parents=True, exist_ok=True)
    encaixar(img, sob, nome).save(DEST / f"{nome}.png", optimize=True)
    if olhos:
        encaixar(piscando(img, olhos), sob, nome).save(DEST / f"{nome}_piscando.png", optimize=True)
    print("ok", nome)
