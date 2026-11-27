"""Sobe o vídeo direto pela API do YouTube (sem Upload-Post) como PRIVADO e AGENDADO para a hora da faixa.

    python -m src.agendar_yt escopo     # mostra os escopos do token (precisa de youtube.upload ou youtube)
    python -m src.agendar_yt            # sobe baixado/**/video_final.mp4 com título, descrição, thumb e publishAt

Variáveis: TITULO_YOUTUBE, LEGENDA_POST, PUBLICAR_EM (ISO UTC, ex.: 2026-11-26T19:17:00Z; vazio = fica só privado).
Se o YouTube travar o vídeo como privado (projeto de API não verificado), o aviso diz isso: aí o Vitor só abre o Studio e publica.
"""
import json
import os
import sys
from pathlib import Path

import requests

from .util import RAIZ, log


def escopo():
    from .analise import _token
    tok = _token()
    r = requests.get("https://oauth2.googleapis.com/tokeninfo", params={"access_token": tok}, timeout=30)
    print("escopos do token:", r.json().get("scope"))


def subir_longo(run_dir: str, roteiro: str, quando: str):
    """Vídeo longo: baixado/<run>/longo/video_longo.mp4 + thumb_longo.jpg, descrição = legenda_post + capítulos."""
    from . import telegram
    from .analise import _token
    from .thumb_youtube import definir
    base = Path(run_dir)
    video = next(base.rglob("video_longo.mp4"))
    thumb = next(base.rglob("thumb_longo.jpg"), None)
    r = json.loads(Path(roteiro).read_text(encoding="utf-8"))
    cap = Path(roteiro.replace("roteiros/esfr/", "data/esfr/").replace(".json", "_capitulos.txt").replace("longo_01_planetas", "longo_01"))
    desc = r.get("legenda_post", "").strip() + ("\n\nCapítulos:\n" + cap.read_text(encoding="utf-8").strip() if cap.exists() else "")
    corpo = {"snippet": {"title": r["titulo_youtube"][:100], "description": desc[:4900], "categoryId": "28",
                         "defaultLanguage": "pt-BR", "defaultAudioLanguage": "pt-BR"},
             "status": {"privacyStatus": "private", "publishAt": quando, "selfDeclaredMadeForKids": False, "containsSyntheticMedia": True}}
    tok = _token()
    ini = requests.post("https://www.googleapis.com/upload/youtube/v3/videos", timeout=60,
                        params={"uploadType": "resumable", "part": "snippet,status", "notifySubscribers": "true"},
                        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
                                 "X-Upload-Content-Type": "video/mp4"}, data=json.dumps(corpo))
    if ini.status_code >= 400:
        sys.exit(f"falhou: {ini.status_code} {ini.text[:400]}")
    up = requests.put(ini.headers["Location"], data=video.read_bytes(), timeout=1800,
                      headers={"Authorization": f"Bearer {tok}", "Content-Type": "video/mp4"})
    v = up.json()
    if "id" not in v:
        sys.exit(f"upload falhou: {up.text[:400]}")
    vid = v["id"]
    log(f"Subiu: {vid} | status: {json.dumps(v.get('status'))}")
    st = "sem thumb"
    if thumb:
        from PIL import Image
        t2 = thumb.with_name("thumb_yt.jpg")
        Image.open(thumb).convert("RGB").save(t2, quality=85)
        st = f"thumb {definir(vid, t2, tok).get('_status')}"
    msg = (f"[E Se Fosse Real?] VÍDEO LONGO agendado: \"{r['titulo_youtube']}\"\nSai sozinho às {quando} (UTC; 11h de Brasília), "
           f"com descrição e capítulos. {st}\nhttps://studio.youtube.com/video/{vid}/edit")
    telegram.enviar_mensagem(msg)
    print(msg)


def subir():
    from . import telegram
    from .analise import _token
    base = RAIZ / "baixado"
    videos = sorted(base.rglob("video_final.mp4"), key=lambda p: p.stat().st_mtime)
    if not videos:
        sys.exit("sem vídeo em baixado/")
    roteiros = sorted(base.rglob("roteiro.json"))
    r = json.loads(roteiros[0].read_text(encoding="utf-8")) if roteiros else {}
    titulo = (os.environ.get("TITULO_YOUTUBE") or r.get("titulo_youtube") or r.get("titulo", "")).strip()[:100]
    desc = (os.environ.get("LEGENDA_POST") or r.get("legenda_post", "")).strip()[:4900]
    quando = os.environ.get("PUBLICAR_EM", "").strip()
    status = {"privacyStatus": "private", "selfDeclaredMadeForKids": False, "containsSyntheticMedia": True}
    if quando:
        status["publishAt"] = quando
    corpo = {"snippet": {"title": titulo, "description": desc, "categoryId": "28" if r.get("canal") == "esfr" else "24",
                         "defaultLanguage": "pt-BR", "defaultAudioLanguage": "pt-BR"}, "status": status}
    tok = _token()
    ini = requests.post("https://www.googleapis.com/upload/youtube/v3/videos", timeout=60,
                        params={"uploadType": "resumable", "part": "snippet,status", "notifySubscribers": "true"},
                        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
                                 "X-Upload-Content-Type": "video/mp4"}, data=json.dumps(corpo))
    if ini.status_code >= 400:
        telegram.enviar_mensagem(f"Agendar no YouTube falhou ({ini.status_code}): {ini.text[:400]}")
        sys.exit(f"falhou: {ini.status_code} {ini.text[:400]}")
    up = requests.put(ini.headers["Location"], data=videos[-1].read_bytes(), timeout=600,
                      headers={"Authorization": f"Bearer {tok}", "Content-Type": "video/mp4"})
    v = up.json()
    if up.status_code >= 400 or "id" not in v:
        telegram.enviar_mensagem(f"Upload no YouTube falhou ({up.status_code}): {up.text[:400]}")
        sys.exit(f"upload falhou: {up.text[:400]}")
    vid = v["id"]
    log(f"Subiu: {vid} | status: {json.dumps(v.get('status'))}")
    thumb = "thumb: não"
    try:
        from .thumb_youtube import _gerar_thumb, definir, _marcar
        img = _gerar_thumb(r, RAIZ / "trabalho" / "thumbs")
        if img:
            res = definir(vid, img, tok)
            thumb = "thumb: ok" if res.get("_status", 500) < 300 else f"thumb: {res.get('_status')}"
            if res.get("_status", 500) < 300:
                _marcar(vid, titulo)
    except Exception as e:
        thumb = f"thumb: falhou ({e})"
    st = v.get("status", {})
    travado = st.get("privacyStatus") == "private" and quando and not st.get("publishAt")
    hora = ""
    if st.get("publishAt"):
        from datetime import datetime, timedelta
        h = datetime.fromisoformat(st["publishAt"].replace("Z", "+00:00")) - timedelta(hours=3)
        hora = h.strftime("%d/%m às %Hh%M")
    msg = (f"{'[E Se Fosse Real?] ' if r.get('canal') == 'esfr' else ''}No YouTube, pronto: \"{titulo}\"\n"
           f"https://studio.youtube.com/video/{vid}/edit\n"
           + (f"Agendado: sai sozinho {hora}. Não precisa fazer nada no YouTube." if hora else
              "Ficou PRIVADO, sem agendamento: abra o link e toque em Publicar.")
           + (" (O YouTube não aceitou o agendamento pela API.)" if travado else "")
           + f"\n{thumb}")
    telegram.enviar_mensagem(msg[:3800])
    print(msg)
    Path(os.environ.get("GITHUB_OUTPUT", "/dev/null")).open("a").write(f"video_id={vid}\n")


def status(vid: str):
    from .analise import _token, _get, DATA
    d = _get(f"{DATA}/videos", _token(), part="status,statistics,snippet", id=vid)
    for v in d.get("items", []):
        print("STATUS", vid, json.dumps(v["status"]), json.dumps(v.get("statistics")))


if __name__ == "__main__":
    if sys.argv[1:2] == ["escopo"]:
        escopo()
    elif sys.argv[1:2] == ["longo"]:                 # longo <pasta> <roteiro> <publishAt>
        subir_longo(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1:2] == ["thumb"]:                 # thumb <video_id> <roteiro.json>
        from .thumb_youtube import _gerar_thumb, definir
        img = _gerar_thumb(json.loads(Path(sys.argv[3]).read_text(encoding="utf-8")), RAIZ / "trabalho" / "thumbs")
        print("THUMB", sys.argv[2], definir(sys.argv[2], img).get("_status"))
    elif sys.argv[1:2] == ["status"]:
        status(sys.argv[2])
    else:
        subir()
