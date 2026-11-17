"""Thumbs automáticas de cada episódio (vertical 1080x1920 para TikTok/Shorts e horizontal 1280x720 para o YouTube).

Usa a cena mais forte do clímax (a última com o Abismo), sempre com ele em silhueta para não entregar o rosto,
o título do episódio em duas linhas (a segunda na caixa roxa das legendas), uma pergunta-gancho e o selo "EP. N".
    from .thumb import gerar_thumbs; vertical, horizontal = gerar_thumbs(roteiro, pasta)
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from .util import RAIZ

FONTE = RAIZ / "assets" / "fontes" / "Poppins-Bold.ttf"
ROXO, VERMELHO = (124, 58, 237), (200, 30, 40)


def _cena_chave(r: dict) -> dict:
    cenas = r.get("cenas", [])
    com_abismo = [c for c in cenas if (c.get("ameaca") or {}).get("tipo") and c.get("cenario") != "celular_cftv"]
    if com_abismo:
        c = dict(com_abismo[-1])
    else:
        c = dict(next((c for c in reversed(cenas) if c.get("personagem") and c.get("cenario") != "celular_cftv"), cenas[-1]))
    c = json.loads(json.dumps(c))
    c.update(camera="parada", efeito="nenhum", _silhueta=True)
    a = c.get("ameaca")
    if a and a.get("tamanho") == "perto":            # na thumb ele fica inteiro, ao fundo
        a.update(tamanho="longe", acao="encarando")
    return c


def _linhas(titulo: str) -> tuple[str, str]:
    p = titulo.upper().split()
    if len(p) == 1:
        return "", p[0]
    melhor = min(range(1, len(p)), key=lambda i: abs(len(" ".join(p[:i])) - len(" ".join(p[i:]))))
    return " ".join(p[:melhor]), " ".join(p[melhor:])


def _fonte(texto: str, larg: float, max_px: int) -> ImageFont.FreeTypeFont:
    px = max_px
    while px > 30 and ImageFont.truetype(str(FONTE), px).getlength(texto) > larg:
        px -= 4
    return ImageFont.truetype(str(FONTE), px)


def _texto(d, x, y, txt, f, caixa=None):
    if caixa:
        w = f.getlength(txt)
        d.rounded_rectangle((x - 24, y + f.size * 0.1, x + w + 24, y + f.size * 1.2), radius=int(f.size * 0.15), fill=caixa)
    d.text((x + 5, y + 6), txt, font=f, fill=(0, 0, 0))
    d.text((x, y), txt, font=f, fill=(255, 255, 255))


def _pergunta(r: dict) -> str:
    if r.get("pergunta_thumb"):
        return r["pergunta_thumb"].strip()
    return "E você, escaparia?" if not r.get("final") else "Como tudo termina?"


def gerar_thumbs(r: dict, pasta: Path) -> tuple[Path, Path]:
    from .animacao import quadro
    pasta.mkdir(parents=True, exist_ok=True)
    prot = r.get("protagonista", "homem")
    if r.get("formato") == "real":                     # quadro do próprio vídeo (cena marcada com "thumb": true)
        import subprocess
        i = next((k for k, c in enumerate(r["cenas"]) if c.get("thumb")), len(r["cenas"]) // 2)
        clip = RAIZ / "trabalho" / "video" / f"clip_{i:02d}.mp4"
        png = pasta / "quadro.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.0", "-i", str(clip), "-frames:v", "1", str(png)], check=True)
        cena = ImageEnhance.Brightness(Image.open(png).convert("RGB")).enhance(1.15)
    elif r.get("formato") == "sombra":                 # a cena marcada com "thumb" (ou o close do Abismo)
        from .sombra import quadro as quadro_sombra
        c = next((c for c in r["cenas"] if c.get("thumb")), None) or next(c for c in reversed(r["cenas"]) if c.get("quadro") == "abismo")
        cena = quadro_sombra(dict(c, texto=None), 3.0, 3.2, 1)
    else:
        cena = ImageEnhance.Brightness(quadro(_cena_chave(r), 2.2, 4.0, prot).convert("RGB")).enhance(1.25)
    W, H = cena.size
    l1, l2 = _linhas(r.get("titulo", "Você escaparia?"))
    pergunta = _pergunta(r)
    selo = r.get("selo") or ("FINAL" if r.get("final") else f"EP. {r.get('parte') or 1}")

    # ---------------- vertical
    v = cena.convert("RGBA")
    faixa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(faixa).rectangle((0, H * 0.36, W, H * 0.6), fill=(3, 4, 12, 130))
    v.alpha_composite(faixa.filter(ImageFilter.GaussianBlur(50)))
    d = ImageDraw.Draw(v)
    y = H * 0.38
    for txt, cx in ((l1, None), (l2, ROXO)):
        if not txt:
            continue
        f = _fonte(txt, W * 0.84, 150)
        _texto(d, (W - f.getlength(txt)) / 2, y, txt, f, cx)
        y += f.size * 1.18
    f = _fonte(pergunta, W * 0.88, 52)
    _texto(d, (W - f.getlength(pergunta)) / 2, y + 20, pergunta, f)
    fs = ImageFont.truetype(str(FONTE), 46)
    d.rounded_rectangle((40, 60, 80 + fs.getlength(selo), 130), radius=14, fill=VERMELHO)
    d.text((60, 64), selo, font=fs, fill=(255, 255, 255))
    vert = pasta / "thumb_vertical.jpg"
    v.convert("RGB").save(vert, quality=92)

    # ---------------- horizontal
    hz = Image.new("RGB", (1280, 720))
    fundo = cena.resize((1280, int(1280 * H / W))).crop((0, 300, 1280, 1020)).filter(ImageFilter.GaussianBlur(30))
    hz.paste(ImageEnhance.Brightness(fundo).enhance(0.45), (0, 0))
    hz.paste(cena.resize((450, 800)).crop((0, 40, 450, 760)), (830, 0))
    sombra = Image.new("L", (1280, 720), 0)
    ImageDraw.Draw(sombra).rectangle((780, 0, 860, 720), fill=255)
    hz = Image.composite(Image.new("RGB", (1280, 720), (5, 6, 14)), hz,
                         sombra.filter(ImageFilter.GaussianBlur(25)).point(lambda p: int(p * 0.6)))
    dz = ImageDraw.Draw(hz)
    y = 170
    for txt, cx in ((l1, None), (l2, ROXO)):
        if not txt:
            continue
        f = _fonte(txt, 700, 110)
        _texto(dz, 60, y, txt, f, cx)
        y += f.size * 1.18
    f = _fonte(pergunta, 720, 40)
    _texto(dz, 62, y + 20, pergunta, f)
    fs = ImageFont.truetype(str(FONTE), 40)
    dz.rounded_rectangle((60, 80, 96 + fs.getlength(selo), 138), radius=12, fill=VERMELHO)
    dz.text((78, 84), selo, font=fs, fill=(255, 255, 255))
    hor = pasta / "thumb_horizontal.jpg"
    hz.save(hor, quality=92)
    return vert, hor


def enviar_thumbs(r: dict, pasta: Path) -> None:
    """Gera e manda as thumbs no Telegram (como arquivo, sem perder qualidade). Falha aqui não derruba o envio."""
    from . import telegram
    try:
        vert, hor = gerar_thumbs(r, pasta)
        telegram.enviar_arquivo(vert, "Thumb vertical (capa do TikTok/Shorts)")
        telegram.enviar_arquivo(hor, "Thumb horizontal (YouTube)")
    except Exception as e:  # noqa: BLE001
        print(f"Thumbs falharam: {e}", file=sys.stderr)


if __name__ == "__main__":
    r = json.loads((RAIZ / "trabalho" / "roteiro.json").read_text(encoding="utf-8"))
    print(gerar_thumbs(r, RAIZ / "trabalho" / "thumbs"))
