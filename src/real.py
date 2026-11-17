"""Formato "real": vídeos e fotos reais de banco gratuito (Pexels) com cortes rápidos e câmera em POV.

Cada cena do roteiro tem a narração e "buscas" (termos em inglês). A cena é picotada em planos de ~2,5 s
(15 a 25 trocas por minuto); cada plano usa um vídeo ou foto diferente, com:
  - movimento de câmera: aproximação lenta, deriva lateral ou "câmera na mão" (POV, tremidinha);
  - tratamento de terror: escuro, frio, dessaturado, granulado e com vinheta;
  - corte com flash rápido e, de vez em quando, um glitch de cor;
  - texto na tela ("texto_tela") e corte seco para o preto ("corte_preto") como no formato animado.
Requer o segredo PIXABAY_API_KEY (grátis em pixabay.com/api/docs) ou PEXELS_API_KEY.
"""
import json
import math
import os
import random
import subprocess
from pathlib import Path

import requests

from .util import RAIZ, log

API_VID = "https://api.pexels.com/videos/search"
API_FOTO = "https://api.pexels.com/v1/search"
CACHE = RAIZ / "trabalho" / "real_cache"
W, H, FPS = 1080, 1920, 24
PLANO = 2.5                  # segundos por plano
GRADE = ("eq=brightness=-0.07:contrast=1.18:saturation=0.5,colorbalance=bs=0.10:bm=0.05:rs=-0.04,"
         "noise=alls=16:allf=t,vignette=angle=PI/3.6")

_usados: set = set()
_cache_ids: dict = {}
_buscas: dict = {}


def _chave() -> str:
    k = os.environ.get("PEXELS_API_KEY", "").strip()
    if not k:
        raise RuntimeError("Falta o segredo PIXABAY_API_KEY (grátis em pixabay.com/api/docs).")
    return k


PROIBIDO = {"animation", "animated", "cartoon", "illustration", "render", "3d", "fantasy", "dragon", "anime",
            "green screen", "greenscreen", "chroma", "chroma key", "ai generated", "generated", "drawing", "vector",
            "cow", "cows", "cattle", "dog", "cat", "pet", "funny", "happy", "smile", "summer", "beach", "sunset",
            "wedding", "christmas", "snow", "desert", "aerial", "drone", "skyline", "abstract",
            "lingerie", "sexy", "bikini", "erotic", "sensual", "underwear", "fashion", "beauty", "model", "nude",
            "body", "wolf", "animal", "wildlife", "bird", "fire", "campfire", "flame", "toy", "ferris", "moon",
            "planet", "space", "sea", "ocean", "boat", "castle", "forest", "leaves", "tron", "neon", "futuristic"}
MIN_REL = 2                  # no catálogo de curadoria baixa para 1 (eu escolho à mão)
VAZIAS = {"a", "of", "in", "on", "at", "the", "and", "with", "dark", "night", "close", "up", "pov", "empty", "old"}


def _relevancia(busca: str, tags: str) -> int:
    """Quantas palavras importantes da busca aparecem nas etiquetas do item; -1 se tiver etiqueta proibida."""
    t = {x.strip().lower() for x in tags.split(",")}
    palavras = set(" ".join(t).split())
    if t & PROIBIDO or palavras & PROIBIDO:
        return -1
    chave = [w for w in busca.lower().split() if w not in VAZIAS]
    n = sum(1 for w in chave if w in palavras or w.rstrip("s") in palavras)
    return n if n >= min(MIN_REL, len(chave)) else 0     # busca de 2+ palavras: precisa bater pelo menos 2


def _procurar_pixabay(busca: str, chave: str) -> list[dict]:
    itens = []
    try:
        r = requests.get("https://pixabay.com/api/videos/", params={"key": chave, "q": busca, "per_page": 15,
                                                                     "safesearch": "true"}, timeout=30)
        for v in r.json().get("hits", []):
            vs = [x for x in (v.get("videos") or {}).values() if isinstance(x, dict) and x.get("url")]
            rel = _relevancia(busca, v.get("tags", ""))
            if not vs or v.get("type", "film") != "film" or rel < 1:
                continue
            f = min(vs, key=lambda x: abs((x.get("height") or 0) - 1080) + (5000 if (x.get("height") or 0) < 700 else 0))
            itens.append({"tipo": "video", "id": f"pv{v['id']}", "url": f["url"], "dur": v.get("duration", 10),
                          "credito": v.get("user", ""), "rel": rel})
    except Exception as e:  # noqa: BLE001
        log(f"Pixabay (vídeo) falhou para '{busca}': {e}")
    try:
        r = requests.get("https://pixabay.com/api/", params={"key": chave, "q": busca, "image_type": "photo",
                                                              "orientation": "vertical", "per_page": 10,
                                                              "safesearch": "true"}, timeout=30)
        for p in r.json().get("hits", []):
            rel = _relevancia(busca, p.get("tags", ""))
            if rel < 1:
                continue
            itens.append({"tipo": "foto", "id": f"pf{p['id']}", "url": p.get("largeImageURL") or p["webformatURL"],
                          "credito": p.get("user", ""), "rel": rel})
    except Exception as e:  # noqa: BLE001
        log(f"Pixabay (foto) falhou para '{busca}': {e}")
    itens.sort(key=lambda it: -it.get("rel", 0))           # o mais parecido com a busca primeiro
    log(f"Pixabay '{busca}': {len(itens)} itens relevantes")
    return itens


def _procurar(busca: str) -> list[dict]:
    """Resultados de vídeos e fotos para a busca (Pixabay; ou Pexels se houver chave). Guardados para não repetir."""
    if busca in _buscas:
        return _buscas[busca]
    pix = os.environ.get("PIXABAY_API_KEY", "").strip()
    if pix:
        _buscas[busca] = _procurar_pixabay(busca, pix)
        return _buscas[busca]
    h = {"Authorization": _chave()}
    itens = []
    for orient in ("portrait", "landscape"):
        try:
            r = requests.get(API_VID, headers=h, params={"query": busca, "orientation": orient, "per_page": 12,
                                                          "size": "medium"}, timeout=30)
            for v in r.json().get("videos", []):
                arqs = [f for f in v.get("video_files", []) if f.get("file_type") == "video/mp4" and f.get("height")]
                if not arqs:
                    continue
                alvo = 1920 if orient == "portrait" else 1080
                f = min(arqs, key=lambda f: abs(f["height"] - alvo) + (5000 if f["height"] < 700 else 0))
                itens.append({"tipo": "video", "id": f"v{v['id']}", "url": f["link"], "dur": v.get("duration", 10),
                              "credito": v.get("user", {}).get("name", "")})
        except Exception as e:  # noqa: BLE001
            log(f"Pexels (vídeo) falhou para '{busca}': {e}")
        if len(itens) >= 6:
            break
    try:
        r = requests.get(API_FOTO, headers=h, params={"query": busca, "orientation": "portrait", "per_page": 8}, timeout=30)
        for p in r.json().get("photos", []):
            itens.append({"tipo": "foto", "id": f"f{p['id']}", "url": p["src"].get("large2x") or p["src"]["original"],
                          "credito": p.get("photographer", "")})
    except Exception as e:  # noqa: BLE001
        log(f"Pexels (foto) falhou para '{busca}': {e}")
    _buscas[busca] = itens
    return itens


def _baixar(item: dict) -> Path:
    if item.get("local"):
        return Path(item["local"])
    CACHE.mkdir(parents=True, exist_ok=True)
    destino = CACHE / f"{item['id']}.{'mp4' if item['tipo'] == 'video' else 'jpg'}"
    if not destino.exists():
        r = requests.get(item["url"], timeout=180)
        r.raise_for_status()
        destino.write_bytes(r.content)
    return destino


def _jornal(texto: str) -> Path:
    """Recorte de jornal antigo, em português, feito aqui (no lugar de jornal real de banco de imagens)."""
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    CACHE.mkdir(parents=True, exist_ok=True)
    import hashlib
    destino = CACHE / f"jornal_{hashlib.md5(texto.encode()).hexdigest()[:10]}.jpg"
    if destino.exists():
        return destino
    titulo, _, sub = texto.partition("|")
    fonte = next((p for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
                              str(RAIZ / "assets" / "fontes" / "Poppins-Bold.ttf")) if Path(p).exists()))
    pw, ph = 900, 1250
    papel = np.full((ph, pw, 3), (214, 204, 178), np.float32)
    papel += np.random.default_rng(3).normal(0, 9, (ph, pw, 1))
    yy, xx = np.mgrid[0:ph, 0:pw]
    papel *= (1 - 0.28 * (((xx - pw / 2) / pw) ** 2 + ((yy - ph / 2) / ph) ** 2))[..., None] * 1.1
    img = Image.fromarray(papel.clip(0, 255).astype("uint8"))
    d = ImageDraw.Draw(img)
    d.text((40, 30), "O NOTURNO", font=ImageFont.truetype(fonte, 44), fill=(40, 36, 32))
    d.line((40, 92, pw - 40, 92), fill=(40, 36, 32), width=4)
    d.text((40, 100), "Edição de 26 de maio de 1988", font=ImageFont.truetype(fonte, 22), fill=(60, 54, 48))
    px, y = 86, 150
    palavras, linha, linhas = titulo.upper().split(), "", []
    f = ImageFont.truetype(fonte, px)
    for w in palavras:
        if f.getlength((linha + " " + w).strip()) > pw - 80:
            linhas.append(linha)
            linha = w
        else:
            linha = (linha + " " + w).strip()
    linhas.append(linha)
    for ln in linhas:
        d.text((40, y), ln, font=f, fill=(20, 18, 16))
        y += int(px * 1.15)
    if sub:
        ps = 34
        while ps > 18 and ImageFont.truetype(fonte, ps).getlength(sub) > pw - 80:
            ps -= 2
        d.text((40, y + 6), sub, font=ImageFont.truetype(fonte, ps), fill=(50, 46, 40))
        y += 60
    y += 20
    d.rectangle((40, y, 480, y + 330), fill=(70, 66, 60))                         # "foto" da matéria
    d.polygon([(80, y + 200), (260, y + 70), (440, y + 200)], fill=(42, 40, 36))
    d.rectangle((110, y + 200, 410, y + 330), fill=(52, 50, 46))
    for k in range(int((ph - y - 40) / 26)):                                      # colunas de texto
        yy_ = y + 10 + k * 26
        for x0, x1 in ((510, pw - 40),) if yy_ < y + 340 else ((40, pw // 2 - 15), (pw // 2 + 15, pw - 40)):
            d.line((x0, yy_, x1 - (k * 37 % 60), yy_), fill=(120, 112, 98), width=7)
    img = img.filter(ImageFilter.GaussianBlur(0.8)).rotate(-4, expand=True, fillcolor=(8, 8, 10))
    fundo = Image.new("RGB", (1080, 1920), (8, 8, 10))
    img.thumbnail((1000, 1500))
    fundo.paste(img, ((1080 - img.width) // 2, (1920 - img.height) // 2))
    fundo.save(destino, quality=92)
    return destino


def _por_id(ident: str) -> dict | None:
    """Item específico do Pixabay pelo id da curadoria (pv123 = vídeo, pf123 = foto, jornal:Manchete|subtítulo)."""
    if ident.startswith("jornal:"):
        return {"tipo": "foto", "id": ident, "local": str(_jornal(ident[7:])), "credito": ""}
    chave = os.environ.get("PIXABAY_API_KEY", "").strip()
    video = ident.startswith("pv")
    url = "https://pixabay.com/api/videos/" if video else "https://pixabay.com/api/"
    try:
        hits = requests.get(url, params={"key": chave, "id": ident[2:]}, timeout=30).json().get("hits", [])
    except Exception:  # noqa: BLE001
        return None
    if not hits:
        return None
    h = hits[0]
    if video:
        vs = [x for x in (h.get("videos") or {}).values() if isinstance(x, dict) and x.get("url")]
        f = min(vs, key=lambda x: abs((x.get("height") or 0) - 1080))
        return {"tipo": "video", "id": ident, "url": f["url"], "credito": h.get("user", "")}
    return {"tipo": "foto", "id": ident, "url": h.get("largeImageURL") or h["webformatURL"], "credito": h.get("user", "")}


def _escolher(buscas: list[str], i: int, prefere_video: bool, ids: list | None = None) -> dict | None:
    """Um item ainda não usado no vídeo: primeiro os ids escolhidos na curadoria, depois as buscas da cena."""
    if ids:                                              # curadoria: só os escolhidos (repete se faltar)
        livres = [x for x in ids if x not in _usados] or ids
        ident = livres[i % len(livres)] if not [x for x in ids if x not in _usados] else livres[0]
        _usados.add(ident)
        if ident not in _cache_ids:
            _cache_ids[ident] = _por_id(ident)
        return _cache_ids[ident]
    for k in range(len(buscas)):
        itens = _procurar(buscas[(i + k) % len(buscas)])
        livres = [it for it in itens if it["id"] not in _usados]
        if prefere_video:
            livres.sort(key=lambda it: it["tipo"] != "video")
        if livres:
            it = livres[0]
            _usados.add(it["id"])
            return it
    return None


def _serve(arq: Path, item: dict) -> bool:
    """Descarta imagem estourada/branca e fundo verde (chroma key): olha 3 quadros."""
    import numpy as np
    from PIL import Image
    tempos = [0.5, 0.5 * max(1.0, _duracao(arq)), max(0.5, _duracao(arq) - 0.5)] if item["tipo"] == "video" else [0]
    medias = []
    for t in tempos:
        png = arq.with_suffix(".teste.png")
        cmd = ["ffmpeg", "-y", "-loglevel", "error"] + (["-ss", f"{t:.2f}"] if item["tipo"] == "video" else []) + \
              ["-i", str(arq), "-frames:v", "1", "-vf", "scale=96:-1", str(png)]
        if subprocess.run(cmd, capture_output=True).returncode != 0 or not png.exists():
            return False
        a = np.asarray(Image.open(png).convert("RGB")).astype(float)
        png.unlink()
        if a.mean() > 150:
            return False
        medias.append(a.mean())
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        if ((g > r * 1.4) & (g > b * 1.4) & (g > 90)).mean() > 0.25:
            return False
    item["brilho"] = sum(medias) / max(1, len(medias))
    return True


def _duracao(arq: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(arq)],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def _plano(item: dict | None, arq: Path | None, d: float, mov: str, glitch: bool, destino: Path, semente: int) -> None:
    """Renderiza um plano de d segundos (1080x1920, sem áudio)."""
    rnd = random.Random(semente)
    D = max(d, 0.1)
    # movimento: o quadro é ampliado e recortado com a posição variando no tempo
    if mov == "pov":
        z = "1.14"
        cx = f"(iw-{W})/2+10*sin(t*1.9)+6*sin(t*4.7)"
        cy = f"(ih-{H})/2+8*sin(t*1.5+1)+5*sin(t*5.3)"
    elif mov == "deriva":
        z = "1.16"
        s = rnd.choice([-1, 1])
        cx = f"(iw-{W})/2+{s}*(iw-{W})*0.45*(t/{D:.3f}-0.5)"
        cy = f"(ih-{H})/2"
    else:                                               # aproxima devagar (ou afasta)
        a = rnd.choice([0.08, 0.12, -0.08])
        z = f"(1.04+{max(a, 0):.2f}*t/{D:.3f}+{max(-a, 0):.2f}*(1-t/{D:.3f}))"
        cx, cy = f"(iw-{W})/2", f"(ih-{H})/2"
    escala = (f"scale=w='ceil({W}*{z}*max(1\\,{H}/{W}*iw/ih)/2)*2':h=-2:eval=frame,"
              f"scale=w='max(iw\\,{W})':h='max(ih\\,{H})':force_original_aspect_ratio=increase:eval=frame,"
              f"crop={W}:{H}:x='{cx}':y='{cy}'")
    claro = ""
    if item and item.get("brilho", 99) < 45:            # imagem escura demais: levanta as sombras antes do tratamento
        g = 1.6 if item["brilho"] < 25 else 1.35
        claro = f"eq=gamma={g}:brightness=0.03,"
    filtro = f"{escala},{claro}{GRADE},fps={FPS},fade=t=in:st=0:d=0.12:color=white@0.5"
    if glitch:
        filtro += ",rgbashift=rh=10:bh=-10:enable='lt(t\\,0.18)'"
    filtro += ",format=yuv420p"
    if arq is None:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"color=c=0x05060c:s={W}x{H}:d={D:.3f}:r={FPS}",
               "-vf", f"noise=alls=20:allf=t,format=yuv420p"]
    elif item["tipo"] == "foto":
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", f"{D:.3f}", "-i", str(arq), "-vf", filtro]
    else:
        total = _duracao(arq)
        ini = rnd.uniform(0, max(0.0, total - D - 0.2)) if total > D + 0.4 else 0.0
        lento = "setpts=1.35*PTS," if total < D * 1.3 + ini else ""        # vídeo curto: câmera lenta
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{ini:.2f}", "-i", str(arq), "-an",
               "-vf", lento + filtro + f",tpad=stop_mode=clone:stop_duration={D:.3f}"]
    cmd += ["-t", f"{D:.3f}", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", str(destino)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-600:])


def renderizar_cena_real(cena: dict, voz: dict, destino: Path, pausa: float, indice: int) -> float:
    dur = voz["duracao"] + pausa
    fim_voz = voz["duracao"] if cena.get("corte_preto") else dur
    n = max(1, round(fim_voz / PLANO))
    buscas = cena.get("buscas") or ["dark empty room night"]
    pasta = destino.parent / f"planos_{indice:02d}"
    pasta.mkdir(parents=True, exist_ok=True)
    partes = []
    movs = cena.get("movimentos") or ["pov", "aproxima", "deriva"]
    for i in range(n):
        d = fim_voz / n
        item, arq = None, None
        for _ in range(6):                               # até achar um que sirva (não claro demais nem fundo verde)
            item = _escolher(buscas, i, prefere_video=i % 3 != 2, ids=cena.get("ids"))
            if not item:
                break
            try:
                arq = _baixar(item)
            except Exception as e:  # noqa: BLE001
                log(f"  download falhou ({e})")
                item, arq = None, None
                continue
            if _serve(arq, item):
                break
            log(f"  descartado (claro demais ou fundo verde): {item['id']}")
            item, arq = None, None
        p = pasta / f"p{i:02d}.mp4"
        _plano(item, arq, d, movs[(indice + i) % len(movs)], glitch=(indice + i) % 4 == 3, destino=p,
               semente=indice * 100 + i)
        partes.append(p)
        if item:
            _creditos(item)
    if fim_voz < dur:                                       # corte seco para o preto
        p = pasta / "preto.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                        f"color=c=black:s={W}x{H}:d={dur - fim_voz:.3f}:r={FPS}", "-c:v", "libx264", "-preset",
                        "veryfast", "-pix_fmt", "yuv420p", str(p)], check=True)
        partes.append(p)
    lista = pasta / "lista.txt"
    lista.write_text("".join(f"file '{p.name}'\n" for p in partes))
    video = pasta / "video.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lista), "-c", "copy",
                    str(video)], check=True)
    # texto na tela por cima + voz
    entradas = ["-i", str(video), "-i", str(voz["arquivo"])]
    filtro = "[1:a]aresample=44100,apad[a]"
    mapa_v = "0:v"
    if cena.get("texto_tela"):
        from PIL import Image
        from .animacao import _texto_tela
        png = pasta / "texto.png"
        camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        _texto_tela(camada, str(cena["texto_tela"]), 1.0)
        camada.save(png)
        entradas += ["-loop", "1", "-i", str(png)]
        filtro = f"[2:v]format=rgba,fade=t=in:d=0.3:alpha=1[t];[0:v][t]overlay=0:0:shortest=1[v];" + filtro
        mapa_v = "[v]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *entradas, "-filter_complex", filtro,
                    "-map", mapa_v, "-map", "[a]", "-t", f"{dur:.3f}", "-r", str(FPS), "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-ac", "2",
                    str(destino)], check=True)
    return dur


def _creditos(item: dict) -> None:
    arq = RAIZ / "trabalho" / "creditos_pexels.json"
    dados = json.loads(arq.read_text()) if arq.exists() else {}
    dados[item["id"]] = item.get("credito", "")
    arq.write_text(json.dumps(dados, ensure_ascii=False, indent=1))


def catalogo(roteiro: dict, pasta: Path) -> list[Path]:
    """Folhas com as opções de cada cena (quadro + id) para escolher à mão os melhores planos."""
    from PIL import Image, ImageDraw
    pasta.mkdir(parents=True, exist_ok=True)
    folhas = []
    for i, cena in enumerate(roteiro["cenas"]):
        itens = []
        for b in cena.get("buscas") or []:
            itens += [it for it in _procurar(b) if it["id"] not in {x["id"] for x in itens}]
        miniaturas = []
        for it in itens[:20]:
            try:
                arq = _baixar(it)
                png = arq.with_suffix(".mini.png")
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + (["-ss", "1"] if it["tipo"] == "video" else []) +
                               ["-i", str(arq), "-frames:v", "1", "-vf", "scale=240:-1", str(png)], check=True)
                im = Image.open(png).convert("RGB")
                im.thumbnail((240, 240))
                c = Image.new("RGB", (240, 262), (0, 0, 0))
                c.paste(im, ((240 - im.width) // 2, (240 - im.height) // 2))
                ImageDraw.Draw(c).text((4, 244), it["id"], fill=(255, 255, 0))
                miniaturas.append(c)
            except Exception:  # noqa: BLE001
                continue
        if not miniaturas:
            continue
        folha = Image.new("RGB", (240 * 4, 262 * math.ceil(len(miniaturas) / 4) + 30), (20, 20, 30))
        ImageDraw.Draw(folha).text((6, 6), f"cena {i}: {cena['narracao'][:110]}", fill=(255, 255, 255))
        for k, m in enumerate(miniaturas):
            folha.paste(m, ((k % 4) * 240, 30 + (k // 4) * 262))
        destino = pasta / f"cena_{i:02d}.jpg"
        folha.save(destino, quality=70)
        folhas.append(destino)
    return folhas


if __name__ == "__main__":
    import sys
    MIN_REL = 1
    r = json.loads((RAIZ / sys.argv[1]).read_text(encoding="utf-8"))
    print(catalogo(r, RAIZ / "data" / "previas" / "catalogo"))
