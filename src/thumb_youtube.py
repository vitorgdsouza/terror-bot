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



FEITAS = RAIZ / "data" / "thumbs_feitas.json"      # vídeos que já receberam a nossa thumb (não reenviar)


def _feitas() -> dict:
    try:
        return json.loads(FEITAS.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _marcar(video_id: str, titulo: str) -> None:
    f = _feitas()
    f[video_id] = {"titulo": titulo, "quando": time.strftime("%Y-%m-%d %H:%M")}
    FEITAS.parent.mkdir(parents=True, exist_ok=True)
    FEITAS.write_text(json.dumps(f, ensure_ascii=False, indent=1), encoding="utf-8")


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
    if resp.get("_status") == 429:
        return "o YouTube limitou o envio de thumbs por hoje; o bot tenta de novo sozinho"
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
    resp = definir(item["video_id"], thumb, tok)
    if resp.get("_status", 500) < 300:
        _marcar(item["video_id"], roteiro.get("titulo", ""))
    return f"thumb no YouTube: {_explica(resp)}"


def _roteiros_conhecidos() -> list[dict]:
    achados = []
    arqs = (list((RAIZ / "roteiros").rglob("*.json")) + list((RAIZ / "baixado").rglob("roteiro.json"))
            + list((RAIZ / "data" / "historico").glob("*.json")))
    for arq in arqs:
        try:
            r = json.loads(arq.read_text(encoding="utf-8"))
        except Exception:
            continue
        if r.get("canal", "") != os.environ.get("CANAL", "").strip():   # cada canal só enxerga os seus roteiros
            continue
        if r.get("titulo") and r.get("cenas"):
            legenda = arq.parent / "legenda_do_post.txt"
            extra = legenda.read_text(encoding="utf-8") if legenda.exists() else ""
            r["_texto"] = _norm(" ".join(str(r.get(k, "")) for k in ("titulo", "titulo_youtube", "legenda_post", "resumo", "pergunta_thumb")) + " " + extra)
            achados.append(r)
    return achados


def _melhor(titulo_yt: str, roteiros: list[dict]):
    """O título no YouTube costuma ser a legenda do post: acha o roteiro que mais contém as palavras dele."""
    alvo = _norm(re.sub(r"#\w+", " ", titulo_yt))
    exato = next((r for r in roteiros if r.get("titulo_youtube") and _norm(re.sub(r"#\w+", " ", r["titulo_youtube"])) == alvo), None)
    if exato:                                         # o título postado é o do roteiro: sem dúvida
        return exato
    palavras = [w for w in alvo.split() if len(w) > 3]
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
    feitas = _feitas()
    if not feitas:                                    # as 10 primeiras foram enviadas antes deste controle existir
        feitas = {v["video_id"]: {} for v in lista if v["quando"] <= "2026-11-17" and "protocolo rufus" not in _norm(v["titulo"])}
        for vid in feitas:
            _marcar(vid, "")
    trocar = _norm(os.environ.get("TROCAR", ""))
    if trocar:                                        # troca a thumb de um vídeo que já tem (pedido do Vitor)
        lista = [v for v in lista if trocar in _norm(v["titulo"])]
    else:
        lista = [v for v in lista if v["video_id"] not in feitas]
    if not lista:
        log("Todos os Shorts já têm thumb.")
        return
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
            resp = definir(item["video_id"], thumb, tok)
            if resp.get("_status", 500) < 300:
                _marcar(item["video_id"], r["titulo"])
            linhas.append(f"- {r['titulo']}: {_explica(resp)}")
            if resp.get("_status") == 429:            # limite diário do YouTube: tenta o resto na próxima rodada
                linhas.append("(limite de thumbs do YouTube; tento de novo em algumas horas)")
                break
        except Exception as e:
            linhas.append(f"- {r['titulo']}: falhou ({e})")
    for l in linhas:
        log(l)
    if any("ok" in l or "recusou" in l for l in linhas) or os.environ.get("GITHUB_EVENT_NAME") != "schedule":
        telegram.enviar_mensagem(("Thumbs nos Shorts do YouTube:\n" + "\n".join(linhas))[:3800])


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "antigas":
        antigas()
