"""Cola o protagonista fixo e a ameaça (figurinhas em assets/personagem) sobre o cenário gerado pela IA.

Assim o personagem fica idêntico em todas as cenas e em todos os vídeos.
Cada cena do roteiro pode ter:
    "personagem": {"pose": "frente", "posicao": "centro", "tamanho": "medio"}
    "ameaca":     {"tipo": "sombra", "posicao": "direita", "tamanho": "longe"}
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from .util import RAIZ

PASTA = RAIZ / "assets" / "personagem"
W, H = 1080, 1920

POSES = ["frente", "medo", "costas", "celular", "lanterna", "maos_celular"]
AMEACAS = ["sombra", "olhos"]
POSICOES = {"esquerda": 0.30, "centro": 0.50, "direita": 0.70}
# altura do desenho (em fração da tela) e onde ficam os pés
TAMANHOS = {"longe": (0.34, 0.80), "medio": (0.64, 0.95), "perto": (1.25, 1.45)}

_cache: dict = {}


def escolher_protagonista(cfg: dict, historico: list) -> str:
    """'homem' ou 'mulher'. No modo 'alternar', troca a cada vídeo."""
    modo = cfg.get("protagonista_modo", "alternar")
    if modo in ("homem", "mulher"):
        return modo
    ultimo = next((h.get("protagonista") for h in reversed(historico) if h.get("protagonista")), "mulher")
    return "mulher" if ultimo == "homem" else "homem"


def _sprite(nome: str, prot: str = "homem") -> Image.Image:
    pasta = PASTA / "mulher" if prot == "mulher" and nome in POSES else PASTA
    chave = (pasta, nome)
    if chave not in _cache:
        _cache[chave] = Image.open(pasta / f"{nome}.png").convert("RGBA")
    return _cache[chave]


def _tom_noturno(img: Image.Image, forca: float) -> Image.Image:
    """Escurece e azula a figurinha para combinar com a cena noturna."""
    r, g, b, a = img.split()
    r = r.point(lambda v: int(v * (1 - 0.30 * forca)))
    g = g.point(lambda v: int(v * (1 - 0.25 * forca)))
    b = b.point(lambda v: int(v * (1 - 0.08 * forca)))
    return Image.merge("RGBA", (r, g, b, a))


def _colar(fundo: Image.Image, nome: str, posicao: str, tamanho: str, noturno: float, sombra_chao: bool,
           prot: str = "homem"):
    spr = _sprite(nome, prot)
    if nome == "maos_celular":  # close em primeira pessoa: sempre embaixo, ocupando a largura
        escala = (W * 1.05) / spr.width
        img = spr.resize((int(spr.width * escala), int(spr.height * escala)), Image.LANCZOS)
        fundo.alpha_composite(_tom_noturno(img, noturno * 0.5), ((W - img.width) // 2, H - img.height + int(img.height * 0.08)))
        return
    alt_frac, pes_frac = TAMANHOS.get(tamanho, TAMANHOS["medio"])
    escala = (H * alt_frac) / spr.height
    img = spr.resize((int(spr.width * escala), int(spr.height * escala)), Image.LANCZOS)
    if posicao == "direita":  # vira para o centro da cena
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    img = _tom_noturno(img, noturno)
    cx = int(W * POSICOES.get(posicao, 0.5))
    pes_y = int(H * pes_frac)
    x = cx - img.width // 2
    y = pes_y - int(img.height * (1115 / 1200))  # os pés ficam em y=1115 no desenho original
    if sombra_chao and tamanho != "perto":
        camada = Image.new("RGBA", fundo.size, (0, 0, 0, 0))
        larg = int(img.width * 0.32)
        ImageDraw.Draw(camada).ellipse((cx - larg, pes_y - larg // 6, cx + larg, pes_y + larg // 6), fill=(0, 0, 10, 140))
        fundo.alpha_composite(camada.filter(ImageFilter.GaussianBlur(12)))
    fundo.alpha_composite(img, (x, y))


def compor(fundo_path: Path, cena: dict, destino: Path, prot: str = "homem") -> None:
    fundo = Image.open(fundo_path).convert("RGBA").resize((W, H), Image.LANCZOS)
    p, a = cena.get("personagem"), cena.get("ameaca")
    perto = isinstance(p, dict) and p.get("tamanho") == "perto"
    if isinstance(a, dict) and a.get("tipo") in AMEACAS and perto:  # ameaça atrás do personagem em close
        _colar(fundo, a["tipo"], a.get("posicao", "centro"), a.get("tamanho", "medio"), 0, False)
    if isinstance(p, dict) and p.get("pose") in POSES:
        _colar(fundo, p["pose"], p.get("posicao", "centro"), p.get("tamanho", "medio"), 0.55, True, prot)
    if isinstance(a, dict) and a.get("tipo") in AMEACAS and not perto:
        _colar(fundo, a["tipo"], a.get("posicao", "centro"), a.get("tamanho", "medio"), 0, a["tipo"] == "sombra")
    fundo.convert("RGB").save(destino, quality=92)


def normalizar(cena: dict) -> None:
    """Corrige valores inválidos que a IA possa ter escrito."""
    p = cena.get("personagem")
    if isinstance(p, dict):
        if p.get("pose") not in POSES:
            cena["personagem"] = None
        else:
            p["posicao"] = p.get("posicao") if p.get("posicao") in POSICOES else "centro"
            p["tamanho"] = p.get("tamanho") if p.get("tamanho") in TAMANHOS else "medio"
    else:
        cena["personagem"] = None
    a = cena.get("ameaca")
    if isinstance(a, dict) and a.get("tipo") in AMEACAS:
        a["posicao"] = a.get("posicao") if a.get("posicao") in POSICOES else "centro"
        a["tamanho"] = a.get("tamanho") if a.get("tamanho") in TAMANHOS else "medio"
    else:
        cena["ameaca"] = None
