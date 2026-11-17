"""Coloca a nossa thumb (vertical 1080x1920) nos Shorts do YouTube pelo Upload-Post.

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

API = "https://api.upload-post.com/api"


def _auth():
    chave = os.environ.get("UPLOAD_POST_API_KEY", "").strip()
    perfil = os.environ.get("UPLOAD_POST_USER", "").strip()
    if not chave or not perfil:
        raise RuntimeError("Faltam os segredos UPLOAD_POST_API_KEY e/ou UPLOAD_POST_USER no GitHub.")
    return {"Authorization": f"Apikey {chave}"}, perfil


def _id_do_link(url: str) -> str:
    m = re.search(r"(?:shorts/|v=|youtu\.be/)([\w-]{11})", url or "")
    return m.group(1) if m else ""


def _norm(t: str) -> str:
    t = unicodedata.normalize("NFKD", (t or "").lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", "", t.replace("#shorts", "")).strip()


def historico_youtube() -> list[dict]:
    cab, perfil = _auth()
    r = requests.get(f"{API}/uploadposts/history", headers=cab, timeout=60,
                     params={"platform": "youtube", "limit": 100, "profile_username": perfil})
    r.raise_for_status()
    itens = []
    for h in r.json().get("history", []):
        if not h.get("success"):
            continue
        pid = h.get("platform_post_id")
        if isinstance(pid, list):
            pid = pid[0] if pid else ""
        vid = _id_do_link(h.get("post_url") or "") or (pid if isinstance(pid, str) and len(pid) == 11 else "")
        if vid:
            itens.append({"video_id": vid, "titulo": h.get("post_title") or "", "url": h.get("post_url") or "",
                          "quando": h.get("upload_timestamp")})
    return itens


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


def definir(video_id: str, imagem: Path) -> dict:
    cab, perfil = _auth()
    r = requests.post(f"{API}/uploadposts/youtube/thumbnail", headers=cab, timeout=120,
                      data={"user": perfil, "video_id": video_id},
                      files={"thumbnail": ("thumb.jpg", _jpg(imagem), "image/jpeg")})
    try:
        resp = r.json()
    except ValueError:
        resp = {"error": r.text[:300]}
    resp["_status"] = r.status_code
    return resp


def _explica(resp: dict) -> str:
    if resp.get("_status", 500) < 300 and resp.get("success") is not False:
        return "na fila (o vídeo ainda está processando)" if resp.get("pending") else "ok"
    if resp.get("_status") == 403:
        return "o YouTube recusou: o canal precisa ser verificado por telefone em youtube.com/verify"
    return f"erro {resp.get('_status')}: {resp.get('error') or resp.get('message') or json.dumps(resp)[:200]}"


def _gerar_thumb(roteiro: dict, pasta: Path) -> Path | None:
    from .thumb import gerar_thumbs
    if roteiro.get("formato") == "real":                 # a thumb do formato real sai de um clipe do próprio vídeo
        clip = RAIZ / "trabalho" / "video" / "clip_00.mp4"
        if not clip.exists():
            return None
    return gerar_thumbs(roteiro, pasta)[0]


def definir_depois_de_postar(resp: dict, roteiro: dict, thumb: Path | None = None) -> str:
    """Acha o id do Short na resposta do upload e coloca a thumb (o Upload-Post espera o processamento)."""
    texto = json.dumps(resp, ensure_ascii=False)
    vid = _id_do_link(texto)
    if not vid:
        time.sleep(30)
        recentes = historico_youtube()
        vid = recentes[0]["video_id"] if recentes and _norm(roteiro.get("titulo", ""))[:20] in _norm(recentes[0]["titulo"]) else ""
    if not vid:
        return "thumb no YouTube: não achei o id do vídeo"
    thumb = thumb or _gerar_thumb(roteiro, RAIZ / "trabalho" / "thumb_yt")
    if not thumb:
        return "thumb no YouTube: sem thumb para este formato"
    return f"thumb no YouTube: {_explica(definir(vid, thumb))}"


def _roteiros_conhecidos() -> dict:
    achados = {}
    for arq in list((RAIZ / "roteiros").glob("*.json")) + list((RAIZ / "data" / "historico").glob("*.json")):
        try:
            r = json.loads(arq.read_text(encoding="utf-8"))
        except Exception:
            continue
        if r.get("titulo"):
            achados.setdefault(_norm(r["titulo"]), r)
    return achados


def antigas():
    from . import telegram
    roteiros = _roteiros_conhecidos()
    linhas = []
    for item in historico_youtube():
        nome = _norm(item["titulo"])
        r = next((r for k, r in roteiros.items() if k and (k in nome or nome.startswith(k[:25]))), None)
        if not r:
            linhas.append(f"- {item['titulo'][:50]}: sem roteiro aqui, pulei")
            continue
        try:
            thumb = _gerar_thumb(r, RAIZ / "trabalho" / "thumbs_yt" / item["video_id"])
            if not thumb:
                linhas.append(f"- {r['titulo']}: formato real, a thumb depende do clipe; pulei")
                continue
            linhas.append(f"- {r['titulo']}: {_explica(definir(item['video_id'], thumb))}")
        except Exception as e:
            linhas.append(f"- {r['titulo']}: falhou ({e})")
        log(linhas[-1])
    telegram.enviar_mensagem(("Thumbs nos Shorts do YouTube:\n" + "\n".join(linhas))[:3800])


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "antigas":
        antigas()
