"""Recorta O ABISMO da ficha (abismo.jpg) e gera as figurinhas em assets/personagem/v2/abismo/.
Rode da raiz do repositório:  python assets/personagem/v2/fonte/montar_abismo.py"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd

AQUI = Path(__file__).parent
DEST = AQUI.parent / "abismo"
F = Image.open(AQUI / "abismo.jpg").convert("RGB")
TOPO, PES, LARG, ALT = 52, 1115, 1000, 1200
# nome: (caixa na ficha, altura em relação a ele em pé)
PECAS = {"frente": ((35, 95, 235, 545), 1.0), "ataque": ((25, 675, 285, 1000), 0.78),
         "observando": ((325, 770, 540, 1000), 0.56), "rosto": ((245, 88, 530, 482), None)}


def recortar(caixa):
    sub = np.asarray(F.crop(caixa)).astype(float)
    lum = sub.mean(-1)
    fb = np.median(np.concatenate([lum[0], lum[-1], lum[:, 0], lum[:, -1]]))
    m = (lum < fb - 30) | (lum > fb + 28)            # corpo preto ou rosto claro
    m = nd.binary_closing(m, iterations=1)
    lab, k = nd.label(m)
    m = lab == (1 + int(np.argmax(nd.sum(m, lab, range(1, k + 1)))))
    buracos = nd.binary_fill_holes(m) & ~m
    lb, kb = nd.label(buracos)
    if kb:                                           # tapa furos pequenos e furos cinza do rosto (o fundo é azulado)
        tam = nd.sum(buracos, lb, range(1, kb + 1))
        azul = nd.mean(sub[:, :, 2] - sub[:, :, 0], lb, range(1, kb + 1))
        m |= np.isin(lb, [i + 1 for i, (t, z) in enumerate(zip(tam, azul)) if t < 150 or z < 11])
    m = nd.binary_opening(m, iterations=1)
    borda = m & ~nd.binary_erosion(m, iterations=3)   # contorno: pinta de preto para não sobrar o cinza do fundo
    arr = np.asarray(F.crop(caixa)).copy()
    arr[borda] = (arr[borda] * 0.15).astype("uint8")
    img = Image.fromarray(arr).convert("RGBA")
    img.putalpha(Image.fromarray((nd.binary_erosion(m, iterations=1) * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.7)))
    return img.crop(img.getbbox())


DEST.mkdir(parents=True, exist_ok=True)
for nome, (caixa, rel) in PECAS.items():
    img = recortar(caixa)
    if rel is None:                                  # rosto: só aumenta, sem tela de corpo
        e = ALT / img.height
        img.resize((int(img.width * e), ALT), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2)).save(DEST / f"{nome}.png", optimize=True)
    else:
        alvo = int((PES - TOPO) * rel)
        e = alvo / img.height
        img = img.resize((int(img.width * e), alvo), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2))
        tela = Image.new("RGBA", (max(LARG, img.width + 40), ALT), (0, 0, 0, 0))
        tela.alpha_composite(img, ((tela.width - img.width) // 2, PES - img.height))
        tela.save(DEST / f"{nome}.png", optimize=True)
    print("ok", nome)
