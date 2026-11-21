"""Publica o vídeo aprovado nas redes da config (hoje: YouTube Shorts) pelo Upload-Post (upload-post.com).

Fluxo: quando um vídeo fica pronto, ele vai para o Telegram e fica "pendente" (data/pendente.json guarda em qual
execução do GitHub ele está). Você manda /postar no Telegram; o bot baixa esse vídeo e chama este script.

Segredos no GitHub: UPLOAD_POST_API_KEY (chave da API) e UPLOAD_POST_USER (nome do perfil no Upload-Post).
    python -m src.postar          # publica o vídeo baixado em baixado/
"""
import json
import os
import sys
import time
from pathlib import Path

import requests

from .util import RAIZ, carregar_config, log

API = "https://api.upload-post.com/api"
PENDENTE = RAIZ / "data" / "pendente.json"


def marcar_pendente(titulo: str, roteiro: dict | None = None) -> None:
    """Chamado quando um vídeo é enviado ao Telegram: guarda onde ele está para o /postar (e o /enfileirar) achar."""
    run = os.environ.get("GITHUB_RUN_ID")
    if not run:
        return
    r = roteiro or {}
    arq = os.environ.get("ROTEIRO_ARQ", "")
    tipo = r.get("tipo") or ("isca" if "/iscas/" in arq else "protocolo" if r.get("formato") in ("protocolo", "sombra")
                             else "historia")
    PENDENTE.parent.mkdir(parents=True, exist_ok=True)
    PENDENTE.write_text(json.dumps({"run_id": run, "titulo": titulo, "quando": time.strftime("%Y-%m-%d %H:%M"),
                                    "postado": False, "tipo": tipo, "titulo_youtube": r.get("titulo_youtube", ""),
                                    "legenda": r.get("legenda_post", "")}, ensure_ascii=False, indent=2), encoding="utf-8")


def _cfg() -> dict:
    return {"plataformas": ["tiktok", "youtube"], "marcar_ia": True, **(carregar_config().get("postagem") or {})}


def publicar(video: Path, titulo: str, legenda: str, hashtags: list[str]) -> dict:
    chave = os.environ.get("UPLOAD_POST_API_KEY", "").strip()
    perfil = os.environ.get("UPLOAD_POST_USER", "").strip()
    if not chave or not perfil:
        raise RuntimeError("Faltam os segredos UPLOAD_POST_API_KEY e/ou UPLOAD_POST_USER no GitHub.")
    c = _cfg()
    tags_txt = " ".join(hashtags)
    yt_titulo = os.environ.get("TITULO_YOUTUBE", "").strip() or os.environ.get("_TITULO_YT_ROTEIRO", "") or titulo
    yt_titulo = (yt_titulo[:90] + " #shorts") if "#shorts" not in yt_titulo.lower() else yt_titulo[:100]
    dados = [("user", perfil), ("title", titulo), ("async_upload", "true")]
    dados += [("platform[]", p) for p in c["plataformas"]]
    # TikTok: legenda completa com hashtags; público; conteúdo com voz de IA identificado
    dados += [("tiktok_title", f"{legenda}\n\n{tags_txt}"[:2200]), ("privacy_level", "PUBLIC_TO_EVERYONE"),
              ("is_aigc", "true" if c["marcar_ia"] else "false")]
    # YouTube Shorts
    dados += [("youtube_title", yt_titulo[:100]), ("youtube_description", f"{legenda}\n\n{tags_txt}"[:4900]),
              ("privacyStatus", "public"), ("categoryId", "24"), ("selfDeclaredMadeForKids", "false"),
              ("defaultLanguage", "pt-BR"), ("defaultAudioLanguage", "pt-BR")]
    dados += [("tags[]", h.lstrip("#")) for h in hashtags[:15]]
    log(f"Enviando para {', '.join(c['plataformas'])} pelo Upload-Post...")
    with open(video, "rb") as f:
        r = requests.post(f"{API}/upload", headers={"Authorization": f"Apikey {chave}"},
                          data=dados, files={"video": (video.name, f, "video/mp4")}, timeout=600)
    try:
        resp = r.json()
    except ValueError:
        resp = {"success": False, "erro": r.text[:500]}
    if r.status_code >= 400 or resp.get("success") is False:
        raise RuntimeError(f"Upload-Post recusou ({r.status_code}): {json.dumps(resp, ensure_ascii=False)[:800]}")
    req = resp.get("request_id")
    # o envio continua em segundo plano: acompanha até terminar (até 15 min)
    for _ in range(45):
        if not req:
            break
        time.sleep(20)
        st = requests.get(f"{API}/uploadposts/status", params={"request_id": req},
                          headers={"Authorization": f"Apikey {chave}"}, timeout=60)
        try:
            resp = st.json()
        except ValueError:
            continue
        estado = str(resp.get("status", "")).lower()
        log(f"Status: {estado or json.dumps(resp)[:200]}")
        if estado in ("completed", "finished", "done", "success", "failed", "error", "partial"):
            break
    return resp


def testar() -> None:
    """Confere a chave e o perfil do Upload-Post sem postar nada (lê o histórico de uploads)."""
    from . import telegram
    chave = os.environ.get("UPLOAD_POST_API_KEY", "").strip()
    perfil = os.environ.get("UPLOAD_POST_USER", "").strip()
    if not chave or not perfil:
        msg = "Upload-Post: faltam os segredos UPLOAD_POST_API_KEY e/ou UPLOAD_POST_USER."
    else:
        r = requests.get(f"{API}/uploadposts/history", headers={"Authorization": f"Apikey {chave}"},
                         params={"limit": 10}, timeout=60)
        if r.status_code == 401 or r.status_code == 403:
            msg = f"Upload-Post: a chave foi recusada ({r.status_code}). Confira o segredo UPLOAD_POST_API_KEY."
        elif r.status_code >= 400:
            msg = f"Upload-Post: erro {r.status_code}: {r.text[:200]}"
        else:
            n = len(r.json().get("history", []))
            msg = f"Upload-Post conectado ✅ (perfil \"{perfil}\", {n} uploads recentes no histórico). O /postar está liberado."
    log(msg)
    telegram.enviar_mensagem(msg)


def _links(resp: dict) -> str:
    """Tira da resposta os links/estado de cada rede, sem depender do formato exato."""
    linhas = []
    res = resp.get("results") or resp.get("result") or {}
    if isinstance(res, list):
        res = {str(i.get("platform", i)): i for i in res if isinstance(i, dict)}
    for rede, info in (res.items() if isinstance(res, dict) else []):
        if isinstance(info, dict):
            url = info.get("url") or info.get("post_url") or info.get("video_url") or ""
            ok = info.get("success", info.get("status", ""))
            erro = info.get("error") or info.get("message") or ""
            linhas.append(f"- {rede}: {'ok' if ok in (True, 'success', 'completed') else ok} {url} {erro}".strip())
    return "\n".join(linhas) or json.dumps(resp, ensure_ascii=False)[:1500]


def main():
    from . import telegram
    base = RAIZ / "baixado"
    videos = sorted(base.rglob("video_final.mp4"), key=lambda p: p.stat().st_mtime)
    if not videos:
        telegram.enviar_mensagem("Não achei o vídeo para postar (ele fica guardado 30 dias). Gere de novo e mande /postar.")
        sys.exit(1)
    roteiros = sorted(base.rglob("roteiro.json"))
    r = json.loads(roteiros[0].read_text(encoding="utf-8")) if roteiros else {}
    titulo = r.get("titulo", "Você escaparia?")
    legenda = os.environ.get("LEGENDA_POST", "").strip() or r.get("legenda_post", "")
    if os.environ.get("TITULO_YOUTUBE", "").strip():     # veio da fila: ajuda a achar o vídeo na hora da thumb
        r["titulo_youtube"] = os.environ["TITULO_YOUTUBE"].strip()
    if r.get("titulo_youtube"):                          # título pensado para busca, definido no roteiro
        os.environ["_TITULO_YT_ROTEIRO"] = r["titulo_youtube"]
    cfg = carregar_config()
    # as hashtags fixas são do terror; o E Se Fosse Real? usa só as do próprio roteiro/legenda
    esfr = r.get("canal") == "esfr" or os.environ.get("CANAL") == "esfr"
    fixas = [] if esfr else cfg.get("hashtags_fixas", [])
    hashtags = list(dict.fromkeys((r.get("hashtags") or []) + fixas))
    try:
        resp = publicar(videos[-1], titulo, legenda, hashtags)
    except Exception as e:
        telegram.enviar_mensagem(f"A postagem de \"{titulo}\" falhou: {e}"[:3800])
        raise
    extra = ""
    if "youtube" in _cfg()["plataformas"]:
        try:
            from .thumb_youtube import definir_depois_de_postar
            extra = "\n" + definir_depois_de_postar(resp, r)
        except Exception as e:
            extra = f"\nthumb no YouTube: falhou ({e})"
    telegram.enviar_mensagem(f"Postado: \"{titulo}\"\n{_links(resp)}{extra}"[:3800])
    if PENDENTE.exists() and not os.environ.get("DA_FILA"):
        p = json.loads(PENDENTE.read_text(encoding="utf-8"))
        p["postado"] = True
        PENDENTE.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "testar":
        testar()
    else:
        main()
