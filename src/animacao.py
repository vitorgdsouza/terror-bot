"""Motor de animação: desenha cada cena quadro a quadro (cenário + personagem + ameaça + efeitos + câmera).

Nada aqui usa IA de imagem: os cenários e personagens são desenhos fixos em assets/.
Cada cena do roteiro usa estes campos:
    "cenario":    um de CENARIOS  ("celular_cftv" = mãos segurando o celular com a câmera de segurança na tela)
    "tela":       (só no celular_cftv) qual cenário aparece na tela da câmera
    "personagem": {"pose": ..., "acao": ..., "posicao": ..., "tamanho": ...} ou null
    "ameaca":     {"tipo": "sombra"|"olhos", "acao": ..., "posicao": ..., "tamanho": ...} ou null
    "efeito":     um de EFEITOS
    "camera":     um de CAMERAS
"""
import json
import math
import os
import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .util import RAIZ

FPS = 24
W, H = 1080, 1920                 # vídeo final
CW, CH = 1188, 2112               # tela dos cenários (10% maior: folga para a câmera)
PASTA_CEN = RAIZ / "assets" / "cenarios"
PASTA_PER = RAIZ / "assets" / "personagem"
META = json.loads((PASTA_CEN / "cenarios.json").read_text(encoding="utf-8"))

CENARIOS = list(META) + ["celular_cftv"]
POSES = ["frente", "medo", "costas", "celular", "lanterna"]
ACOES_P = ["parado", "andando", "entrando", "saindo", "tremendo", "virando"]
ACOES_A = ["parada", "aparecendo", "aproximando", "sumindo"]
AMEACAS = ["sombra", "olhos"]
POSICOES = {"esquerda": 0.28, "centro": 0.5, "direita": 0.72}
TAMANHOS = {"longe": 0.36, "medio": 0.62, "perto": 1.15}
EFEITOS = ["nenhum", "luz_piscando", "tv_chiando", "relampago", "chuva", "tremor"]
CAMERAS = ["zoom_in", "zoom_out", "pan_esquerda", "pan_direita", "parada"]
PES_NO_DESENHO = 1115 / 1200      # onde ficam os pés dentro da figurinha

_cache: dict = {}

# explicação dos valores, usada no pedido ao Gemini e nas instruções do agente
GUIA_CENAS = """Cada cena é um quadro de desenho animado montado com peças fixas:
- "cenario": o lugar. sala (sofá, TV, abajur, janela) | corredor (comprido, porta escura no fundo) |
  quarto (cama, escrivaninha com monitor aceso, janela) | cozinha (armários, geladeira, janela com lua) |
  pia_detalhe (close da pia com prato e copo, janela ao lado: só personagem "perto"; a sombra "longe" aparece lá fora na janela) |
  porta_entrada (porta da rua por dentro com corrente e olho mágico, cabideiro com casaco) | janela (close numa janela grande, noite lá fora) |
  escada (vista de baixo, subindo para um andar escuro) | escada_cima (vista do andar de cima, descendo para um hall escuro) | banheiro (espelho, pia, cortina) | casa_fora (a casa vista da rua à noite) |
  rua (rua escura com poste) | celular_cftv (close das mãos segurando o celular; na tela, a câmera de segurança mostrando outro cenário)
- "tela": só no celular_cftv, qual cenário aparece na câmera (ex.: "sala"). O personagem e a ameaça dessa cena aparecem DENTRO da câmera.
- "personagem": o protagonista ou null. pose: frente | medo | costas | celular (mexendo no celular) | lanterna.
  acao: parado | andando | entrando (entra pelo lado) | saindo (vira e sai) | tremendo | virando (estava de costas e vira).
  posicao: esquerda | centro | direita. tamanho: longe | medio | perto (perto = close do rosto e do tronco).
- "ameaca": null ou o vulto. tipo: sombra (vulto encapuzado de olhos brancos) | olhos (só dois olhos brancos no escuro).
  acao: parada | aparecendo (surge aos poucos) | aproximando (vem para perto) | sumindo.
  posicao e tamanho como no personagem; "longe" coloca a ameaça no fundo do cenário (fim do corredor, topo da escada, porta, janela).
- "efeito": nenhum | luz_piscando | tv_chiando (só na sala e no quarto, no monitor) | relampago | chuva | tremor (susto).
- "camera": zoom_in (aproxima devagar, padrão) | zoom_out | pan_esquerda | pan_direita | parada.
Dicas: varie cenários e enquadramentos como num desenho; deixe a ameaça para a segunda metade e aumente a presença dela
até o clímax; use celular_cftv quando a história falar de câmera de segurança ou de algo visto no celular."""


# ---------------------------------------------------------------- utilidades
def _img(caminho: Path) -> Image.Image:
    if caminho not in _cache:
        _cache[caminho] = Image.open(caminho).convert("RGBA")
    return _cache[caminho]


def _sprite(nome: str, prot: str) -> Image.Image:
    pasta = PASTA_PER / "mulher" if prot == "mulher" and nome.split("_")[0] in POSES + ["maos"] else PASTA_PER
    arq = pasta / f"{nome}.png"
    if not arq.exists():
        arq = pasta / f"{nome.split('_')[0]}.png"
    return _img(arq)


def _escalado(img: Image.Image, altura: int, espelhar: bool, noturno: float) -> Image.Image:
    chave = (id(img), altura, espelhar, round(noturno, 2))
    if chave not in _cache:
        e = altura / img.height
        out = img.resize((max(1, int(img.width * e)), max(1, altura)), Image.BILINEAR)
        if espelhar:
            out = out.transpose(Image.FLIP_LEFT_RIGHT)
        if noturno:
            r, g, b, a = out.split()
            r = r.point(lambda v: int(v * (1 - 0.28 * noturno)))
            g = g.point(lambda v: int(v * (1 - 0.22 * noturno)))
            b = b.point(lambda v: int(v * (1 - 0.06 * noturno)))
            out = Image.merge("RGBA", (r, g, b, a))
        _cache[chave] = out
    return _cache[chave]


def _com_alfa(img: Image.Image, k: float) -> Image.Image:
    if k >= 0.999:
        return img
    a = img.getchannel("A").point(lambda v: int(v * max(0.0, k)))
    out = img.copy()
    out.putalpha(a)
    return out


def _sombra_chao(largura: int) -> Image.Image:
    chave = ("sombra_chao", largura)
    if chave not in _cache:
        im = Image.new("RGBA", (largura * 2, largura // 2), (0, 0, 0, 0))
        ImageDraw.Draw(im).ellipse((largura // 2, largura // 8, largura * 3 // 2, largura * 3 // 8), fill=(0, 0, 10, 130))
        _cache[chave] = im.filter(ImageFilter.GaussianBlur(10))
    return _cache[chave]


def _fonte(tam: int):
    for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, tam)
    return ImageFont.load_default()


def _suave(x: float) -> float:
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- normalização
def normalizar(cena: dict) -> None:
    """Corrige valores inválidos que a IA possa ter escrito, preenchendo padrões."""
    if cena.get("cenario") not in CENARIOS:
        cena["cenario"] = "sala"
    if cena["cenario"] == "celular_cftv" and cena.get("tela") not in META:
        cena["tela"] = "sala"
    if cena.get("efeito") not in EFEITOS:
        cena["efeito"] = "nenhum"
    if cena.get("camera") not in CAMERAS:
        antigos = {"zoom_in": "zoom_in", "zoom_out": "zoom_out", "pan_cima": "pan_esquerda", "pan_baixo": "pan_direita", "tremor": "zoom_in"}
        cena["camera"] = antigos.get(cena.get("movimento"), "zoom_in")
    p = cena.get("personagem")
    if isinstance(p, dict) and p.get("pose") in POSES + ["maos_celular"]:
        if p["pose"] == "maos_celular":  # compatibilidade com o formato antigo
            cena["cenario"], cena["personagem"] = "celular_cftv", None
        else:
            p["acao"] = p.get("acao") if p.get("acao") in ACOES_P else "parado"
            p["posicao"] = p.get("posicao") if p.get("posicao") in POSICOES else "centro"
            p["tamanho"] = p.get("tamanho") if p.get("tamanho") in TAMANHOS else "medio"
    else:
        cena["personagem"] = None
    if META.get(cena["cenario"], {}).get("detalhe") and cena["personagem"]:
        cena["personagem"]["tamanho"] = "perto"   # cenário em close: só cabe o personagem de perto
    a = cena.get("ameaca")
    if isinstance(a, dict) and a.get("tipo") in AMEACAS:
        a["acao"] = a.get("acao") if a.get("acao") in ACOES_A else "parada"
        a["posicao"] = a.get("posicao") if a.get("posicao") in POSICOES else "centro"
        a["tamanho"] = a.get("tamanho") if a.get("tamanho") in TAMANHOS else "longe"
    else:
        cena["ameaca"] = None


# ---------------------------------------------------------------- personagem
def _desenhar_personagem(quadro, p, meta, t, dur, prot, escala_tela=1.0, noturno=0.5):
    cw, ch = quadro.size
    acao, pose = p["acao"], p["pose"]
    prog = t / dur if dur else 0
    alvo_x = POSICOES[p["posicao"]]
    lado = -1 if alvo_x <= 0.5 else 1                 # de que lado ele entra/sai
    x = alvo_x
    andando = False
    if acao == "entrando":
        k = _suave(prog / 0.6)
        x = (alvo_x + lado * 0.75) * (1 - k) + alvo_x * k
        andando = k < 1
    elif acao == "saindo":
        k = _suave((prog - 0.3) / 0.7)
        x = alvo_x * (1 - k) + (alvo_x + lado * 0.8) * k
        andando = k > 0
    elif acao == "andando":
        x = alvo_x - lado * 0.18 + lado * 0.36 * prog
        andando = True

    nome = pose
    if acao == "virando" and prog < 0.45:
        nome = "costas"
    if acao == "saindo" and prog > 0.3:
        nome = "costas"
    if andando and int(t / 0.22) % 2 == 1:
        nome = f"{nome}_passo"
    elif nome != "costas" and (t % 3.1) < 0.13:
        nome = f"{nome}_piscando"
    if acao == "tremendo" and pose == "frente":
        nome = nome.replace("frente", "medo")

    tam = p["tamanho"]
    altura = int(ch * TAMANHOS[tam] * escala_tela)
    piso = meta.get("piso", 0.9)
    if tam == "longe":
        piso = (meta.get("fundo", [0.5, piso])[1] + piso) / 2
    elif tam == "perto":
        piso = 1.42
    espelhar = p["posicao"] == "direita" and pose == "lanterna"
    img = _escalado(_sprite(nome, prot), altura, espelhar, noturno)

    bob = 0
    if andando:
        bob = -abs(math.sin(t * math.pi / 0.22)) * altura * 0.012
    else:
        bob = math.sin(t * 2 * math.pi / 3.2) * altura * 0.004       # respiração
    dx = 0
    if acao == "tremendo":
        dx = math.sin(t * 47) * altura * 0.006
    cx = int(cw * x + dx)
    pes = int(ch * piso + bob)
    if tam != "perto":
        sb = _sombra_chao(int(img.width * 0.33))
        quadro.alpha_composite(sb, (cx - sb.width // 2, int(ch * piso) - sb.height // 2))
    quadro.alpha_composite(img, (cx - img.width // 2, pes - int(img.height * PES_NO_DESENHO)))


# ---------------------------------------------------------------- ameaça
def _desenhar_ameaca(quadro, a, meta, t, dur, escala_tela=1.0):
    cw, ch = quadro.size
    prog = t / dur if dur else 0
    alfa = 1.0
    if a["acao"] == "aparecendo":
        alfa = _suave(prog / 0.5)
    elif a["acao"] == "sumindo":
        alfa = 1 - _suave((prog - 0.5) / 0.5)
    tam = a["tamanho"]
    frac = TAMANHOS[tam]
    fundo = meta.get("fundo", [0.5, meta.get("piso", 0.9), 0.4])
    if tam == "longe":
        x, piso, frac = (fundo[0] if a["posicao"] == "centro" else POSICOES[a["posicao"]]), fundo[1], fundo[2]
    else:
        x, piso = POSICOES[a["posicao"]], (meta.get("piso", 0.9) if tam == "medio" else 1.3)
    if a["acao"] == "aproximando":
        k = _suave(prog)
        frac = frac * (1 + 0.9 * k)
        piso = piso + (min(1.25, piso + 0.25) - piso) * k
        x = x + (0.5 - x) * 0.5 * k

    if a["tipo"] == "olhos":
        regiao = meta.get("porta") or meta.get("janela") or meta.get("espelho")
        larg = int(cw * (0.22 if tam == "longe" else 0.4 if tam == "medio" else 0.7) * escala_tela)
        if a["acao"] == "aproximando":
            larg = int(larg * (1 + 0.8 * _suave(prog)))
        if regiao and tam == "longe":
            cx, cy = (regiao[0] + regiao[2] / 2) * cw, (regiao[1] + regiao[3] * 0.4) * ch
        else:
            cx, cy = x * cw, ch * 0.45
        base = _sprite("olhos", "homem")
        img = _escalado(base, int(larg * base.height / base.width), False, 0)
        if (t % 2.7) < 0.12:                       # piscada
            img = img.resize((img.width, max(1, img.height // 6)))
        pulso = 0.82 + 0.18 * math.sin(t * 3)
        img = _com_alfa(img, alfa * pulso)
        quadro.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))
        return

    altura = int(ch * frac * escala_tela)
    img = _escalado(_sprite("sombra", "homem"), altura, False, 0)
    balanco = math.sin(t * 1.7) * altura * 0.004
    img = _com_alfa(img, alfa)
    quadro.alpha_composite(img, (int(cw * x - img.width / 2 + balanco), int(ch * piso - img.height * 0.94)))


# ---------------------------------------------------------------- efeitos
def _ruido(w, h, seed):
    return Image.frombytes("L", (w, h), random.Random(seed).randbytes(w * h)).convert("RGBA")


def _tv(quadro, meta, t, n):
    if "tv" not in meta:
        return
    cw, ch = quadro.size
    x, y, w, h = meta["tv"]
    box = (int(x * cw), int(y * ch), int(w * cw), int(h * ch))
    ru = _ruido(box[2] // 4, box[3] // 4, n).resize((box[2], box[3]), Image.NEAREST)
    ru = Image.blend(ru, Image.new("RGBA", ru.size, (150, 190, 255, 255)), 0.35)
    quadro.alpha_composite(ru, box[:2])
    luz = Image.new("RGBA", (box[2] * 3, box[3] * 3), (0, 0, 0, 0))
    ImageDraw.Draw(luz).ellipse((0, 0, luz.width, luz.height), fill=(140, 180, 255, int(40 + 25 * math.sin(t * 17))))
    luz = luz.filter(ImageFilter.GaussianBlur(60))
    quadro.alpha_composite(luz, (box[0] - box[2], box[1] - box[3]))


def _chuva(quadro, meta, t, n):
    cw, ch = quadro.size
    reg = meta.get("janela")
    if reg:
        x0, y0, x1, y1 = reg[0] * cw, reg[1] * ch, (reg[0] + reg[2]) * cw, (reg[1] + reg[3]) * ch
    else:
        x0, y0, x1, y1 = 0, 0, cw, ch * 0.75
    camada = Image.new("RGBA", quadro.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    rnd = random.Random(n)
    for _ in range(int((x1 - x0) * (y1 - y0) / 9000) + 10):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        d.line((x, y, x - 8, y + 40), fill=(190, 210, 255, 120), width=3)
    quadro.alpha_composite(camada)


def _brilho(quadro: Image.Image, k: float, cor=(0, 0, 0)) -> Image.Image:
    return Image.blend(quadro, Image.new("RGBA", quadro.size, cor + (255,)), k)


# ---------------------------------------------------------------- cena celular_cftv
def _tela_cftv(cena, t, dur, prot, n, tam):
    """Mini cena vista pela câmera de segurança (tons de cinza esverdeados, linhas, REC)."""
    tela = cena.get("tela", "sala")
    mini = _img(PASTA_CEN / f"{tela}.png").copy()
    meta = META[tela]
    if cena.get("personagem"):
        _desenhar_personagem(mini, cena["personagem"], meta, t, dur, prot, noturno=0.3)
    if cena.get("ameaca"):
        _desenhar_ameaca(mini, cena["ameaca"], meta, t, dur)
    mini = mini.resize(tam, Image.BILINEAR).convert("L").convert("RGBA")
    mini = Image.blend(mini, Image.new("RGBA", tam, (60, 120, 80, 255)), 0.25)
    d = ImageDraw.Draw(mini)
    for y in range(0, tam[1], 6):
        d.line((0, y, tam[0], y), fill=(0, 0, 0, 60))
    f = _fonte(max(14, tam[0] // 14))
    if int(t * 2) % 2 == 0:
        d.ellipse((14, 14, 34, 34), fill=(230, 40, 40, 255))
    d.text((42, 10), "REC", font=f, fill=(240, 240, 240, 255))
    d.text((14, tam[1] - f.size - 16), f"CAM 02   03:{(17 + int(t)) % 60:02d}", font=f, fill=(240, 240, 240, 255))
    return mini


def _quadro_cftv(cena, t, dur, prot, n):
    if "fundo_cftv" not in _cache:
        _cache["fundo_cftv"] = _brilho(_img(PASTA_CEN / "sala.png").filter(ImageFilter.GaussianBlur(14)), 0.55)
    fundo = _cache["fundo_cftv"].copy()
    maos = _sprite("maos_celular", prot)
    e = (CW * 1.0) / maos.width
    mw, mh = int(maos.width * e), int(maos.height * e)
    ox, oy = (CW - mw) // 2, CH - mh + int(mh * 0.04) + int(math.sin(t * 2.2) * 6)
    # área da tela dentro do desenho das mãos (x 335..665, y 185..835 em 1000x1200)
    sx, sy, sw, sh = ox + int(335 * e), oy + int(185 * e), int(330 * e), int(650 * e)
    fundo.alpha_composite(_escalado(maos, mh, False, 0.35), (ox, oy))
    fundo.alpha_composite(_tela_cftv(cena, t, dur, prot, n, (sw, sh)), (sx, sy))
    luz = Image.new("RGBA", (sw * 2, sh), (0, 0, 0, 0))
    ImageDraw.Draw(luz).ellipse((0, 0, sw * 2, sh), fill=(170, 220, 255, 45))
    fundo.alpha_composite(luz.filter(ImageFilter.GaussianBlur(40)), (sx - sw // 2, sy - sh // 3))
    return fundo


# ---------------------------------------------------------------- quadro completo
def quadro(cena: dict, t: float, dur: float, prot: str = "homem", n: int = 0) -> Image.Image:
    """Desenha o quadro da cena no instante t (segundos). Devolve imagem RGB 1080x1920."""
    normalizar(cena)
    if cena["cenario"] == "celular_cftv":
        img = _quadro_cftv(cena, t, dur, prot, n)
        meta = {}
    else:
        meta = META[cena["cenario"]]
        img = _img(PASTA_CEN / f"{cena['cenario']}.png").copy()
        ef = cena["efeito"]
        if ef == "tv_chiando":      # TV e chuva ficam no cenário, atrás de quem estiver na frente
            _tv(img, meta, t, n)
        elif ef == "chuva":
            _chuva(img, meta, t, n)
        a, p = cena.get("ameaca"), cena.get("personagem")
        # a ameaça fica atrás do personagem, a não ser que ela esteja em close e ele não
        ameaca_atras = a and not (a["tamanho"] == "perto" and (not p or p["tamanho"] != "perto"))
        if a and ameaca_atras:
            _desenhar_ameaca(img, a, meta, t, dur)
        if p:
            _desenhar_personagem(img, p, meta, t, dur, prot)
        if a and not ameaca_atras:
            _desenhar_ameaca(img, a, meta, t, dur)

    ef = cena["efeito"]
    if ef == "luz_piscando":
        rnd = random.Random(n // 2)
        if rnd.random() < 0.18:
            img = _brilho(img, 0.55)
    elif ef == "relampago":
        for pico in (0.3, 0.38, 0.75):
            d = abs(t / dur - pico) * dur if dur else 9
            if d < 0.08:
                img = _brilho(img, 0.55 * (1 - d / 0.08), (235, 240, 255))

    # câmera
    prog = t / dur if dur else 0
    k = _suave(prog)
    cam = cena["camera"]
    z, px = 1.0, 0.5
    if cam == "zoom_in":
        z = 1 + 0.12 * k
    elif cam == "zoom_out":
        z = 1.12 - 0.12 * k
    elif cam == "pan_esquerda":
        px = 1 - k
    elif cam == "pan_direita":
        px = k
    cw, chh = W / z, H / z
    x0 = (CW - cw) * px
    y0 = (CH - chh) * 0.5
    if ef == "tremor":
        x0 += math.sin(t * 53) * 9
        y0 += math.cos(t * 41) * 9
    x0 = min(max(0, x0), CW - cw)
    y0 = min(max(0, y0), CH - chh)
    img = img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + chh)))
    if img.size != (W, H):
        img = img.resize((W, H), Image.BILINEAR)

    # transição: escurece no começo e no fim da cena
    borda = min(t, dur - t)
    if borda < 0.2:
        img = _brilho(img, 1 - max(0.0, borda) / 0.2)
    return img.convert("RGB")


def renderizar_cena(cena: dict, voz: dict, destino: Path, prot: str, pausa: float = 0.5) -> float:
    """Gera o clipe .mp4 da cena com a narração. Devolve a duração."""
    dur = voz["duracao"] + pausa
    frames = math.ceil(dur * FPS)
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
         "-r", str(FPS), "-i", "-", "-i", str(voz["arquivo"]),
         "-filter_complex", "[1:a]aresample=44100,apad[a]", "-map", "0:v", "-map", "[a]",
         "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "160k", "-ac", "2", str(destino)],
        stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for n in range(frames):
            ff.stdin.write(quadro(cena, n / FPS, dur, prot, n).tobytes())
    finally:
        ff.stdin.close()
        erro = ff.stderr.read().decode(errors="ignore")
        ff.wait()
    if ff.returncode != 0:
        raise RuntimeError(f"FFmpeg falhou ao gravar a cena: {erro[-1500:]}")
    return dur
