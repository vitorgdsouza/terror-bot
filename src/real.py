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
    CACHE.mkdir(parents=True, exist_ok=True)
    destino = CACHE / f"{item['id']}.{'mp4' if item['tipo'] == 'video' else 'jpg'}"
    if not destino.exists():
        r = requests.get(item["url"], timeout=180)
        r.raise_for_status()
        destino.write_bytes(r.content)
    return destino


def _por_id(ident: str) -> dict | None:
    """Item específico do Pixabay pelo id da curadoria (pv123 = vídeo, pf123 = foto)."""
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
    for ident in ids or []:
        if ident not in _usados:
            it = _por_id(ident)
            _usados.add(ident)
            if it:
                return it
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
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        if ((g > r * 1.4) & (g > b * 1.4) & (g > 90)).mean() > 0.25:
            return False
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
    filtro = f"{escala},{GRADE},fps={FPS},fade=t=in:st=0:d=0.12:color=white@0.5"
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
