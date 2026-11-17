"""Coloca a nossa thumb (vertical 1080x1920) nos Shorts do YouTube pela API oficial (thumbnails.set).

O YouTube só aceita thumb personalizada de canal verificado por telefone (youtube.com/verify). No Short ela aparece
na página do canal, na busca e nas inscrições (no feed de Shorts aparece o próprio vídeo).

    python -m src.thumb_youtube antigas      # põe a thumb em todos os Shorts já postados que tiverem roteiro aqui
    definir_depois_de_postar(resp, roteiro)   # chamado pelo /postar logo depois do upload
"""
import io
import json
import os
import re
import sys
import time
import unicodedata
from pathlib import Path

import requests
from PIL import Image

from .util import RAIZ, log



def _norm(t: str) -> str:
    t = unicodedata.normalize("NFKD", (t or "").lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", t.replace("#shorts", "")).strip()


def _videos_do_canal() -> tuple[str, list[dict]]:
    """Lista os vídeos do canal pela API oficial (mesmo acesso do relatório: YT_CLIENT_ID/SECRET/REFRESH_TOKEN)."""
    from .analise import _token, videos
    tok = _token()
    lista, _ = videos(tok)
    return tok, [{"video_id": v["id"], "titulo": v["titulo"], "quando": v["publicado"]} for v in lista]


def _jpg(caminho: Path) -> bytes:
    img = Image.open(caminho).convert("RGB")
    if img.size != (1080, 1920):
        img = img.resize((1080, 1920), Image.LANCZOS)
    for q in (92, 85, 78, 70):
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=q, optimize=True)
        if buf.tell() < 1_900_000:
            break
    return buf.getvalue()


def definir(video_id: str, imagem: Path, tok: str | None = None) -> dict:
    if tok is None:
        from .analise import _token
        tok = _token()
    r = requests.post("https://www.googleapis.com/upload/youtube/v3/thumbnails/set", timeout=120,
                      params={"videoId": video_id, "uploadType": "media"},
                      headers={"Authorization": f"Bearer {tok}", "Content-Type": "image/jpeg"}, data=_jpg(imagem))
    try:
        resp = r.json()
    except ValueError:
        resp = {"error": r.text[:300]}
    resp["_status"] = r.status_code
    return resp


def _explica(resp: dict) -> str:
    if resp.get("_status", 500) < 300:
        return "ok ✅"
    erro = resp.get("error")
    msg = erro.get("message") if isinstance(erro, dict) else erro
    if resp.get("_status") == 403:
        return ("o YouTube recusou (403): para Shorts ele só libera thumb própria para alguns canais "
                f"(verificação por telefone em youtube.com/verify; o resto vem com o Programa de Parcerias). Detalhe: {msg}")
    return f"erro {resp.get('_status')}: {msg or json.dumps(resp)[:200]}"


def _gerar_thumb(roteiro: dict, pasta: Path) -> Path | None:
    from .thumb import gerar_thumbs
    if roteiro.get("formato") == "real":                 # a thumb do formato real sai de um clipe do próprio vídeo
        clip = RAIZ / "trabalho" / "video" / "clip_00.mp4"
        if not clip.exists():
            return None
    return gerar_thumbs(roteiro, pasta)[0]


def definir_depois_de_postar(resp: dict, roteiro: dict, thumb: Path | None = None) -> str:
    """Depois do upload, acha o Short no canal pelo título e coloca a thumb (espera o YouTube processar)."""
    time.sleep(90)
    tok, lista = _videos_do_canal()
    roteiro = dict(roteiro)
    roteiro["_texto"] = _norm(" ".join(str(roteiro.get(k, "")) for k in ("titulo", "legenda_post", "resumo")))
    item = next((v for v in lista if _melhor(v["titulo"], [roteiro])), None)
    if not item:
        return "thumb no YouTube: não achei o vídeo no canal"
    thumb = thumb or _gerar_thumb(roteiro, RAIZ / "trabalho" / "thumb_yt")
    if not thumb:
        return "thumb no YouTube: sem thumb para este formato"
    return f"thumb no YouTube: {_explica(definir(item['video_id'], thumb, tok))}"


def _roteiros_conhecidos() -> list[dict]:
    achados = []
    arqs = (list((RAIZ / "roteiros").glob("*.json")) + list((RAIZ / "baixado").rglob("roteiro.json"))
            + list((RAIZ / "data" / "historico").glob("*.json")))
    for arq in arqs:
        try:
            r = json.loads(arq.read_text(encoding="utf-8"))
        except Exception:
            continue
        if r.get("titulo") and r.get("cenas"):
            legenda = arq.parent / "legenda_do_post.txt"
            extra = legenda.read_text(encoding="utf-8") if legenda.exists() else ""
            r["_texto"] = _norm(" ".join(str(r.get(k, "")) for k in ("titulo", "legenda_post", "resumo", "pergunta_thumb")) + " " + extra)
            achados.append(r)
    return achados


def _melhor(titulo_yt: str, roteiros: list[dict]):
    """O título no YouTube costuma ser a legenda do post: acha o roteiro que mais contém as palavras dele."""
    palavras = [w for w in _norm(re.sub(r"#\w+", " ", titulo_yt)).split() if len(w) > 3]
    if not palavras:
        return None
    nota, melhor = max(((sum(w in r["_texto"].split() for w in palavras) / len(palavras), r) for r in roteiros),
                       key=lambda x: x[0], default=(0, None))
    return melhor if nota >= 0.6 else None


def antigas():
    from . import telegram
    roteiros = _roteiros_conhecidos()
    linhas = []
    tok, lista = _videos_do_canal()
    for item in lista:
        r = _melhor(item["titulo"], roteiros)
        if not r:
            linhas.append(f"- {item['titulo'][:50]}: sem roteiro aqui, pulei")
            continue
        try:
            thumb = _gerar_thumb(r, RAIZ / "trabalho" / "thumbs_yt" / item["video_id"])
            if not thumb:
                linhas.append(f"- {r['titulo']}: formato real, a thumb depende do clipe; pulei")
                continue
            linhas.append(f"- {r['titulo']}: {_explica(definir(item['video_id'], thumb, tok))}")
        except Exception as e:
            linhas.append(f"- {r['titulo']}: falhou ({e})")
        log(linhas[-1])
    telegram.enviar_mensagem(("Thumbs nos Shorts do YouTube:\n" + "\n".join(linhas))[:3800])


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "antigas":
        antigas()
