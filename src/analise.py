"""Relatório do canal pela API oficial do YouTube (Data API v3 + YouTube Analytics API).

Segredos no GitHub: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN (acesso de leitura do seu canal).
    python -m src.analise          # manda o relatório no Telegram e guarda em data/analise/<data>.json

Indicadores por Short (os que mais pesam para o algoritmo distribuir):
  ficaram    visualizações engajadas / visualizações: quem NÃO deslizou nos primeiros segundos (o "gancho")
  % assistido  média de quanto do vídeo foi visto (acima de 100% = gente revendo, ótimo sinal)
  duração média, compartilhamentos e inscritos por 1.000 views, curtidas e comentários
  retenção: quanto do público sobra em 10%, 50% e 90% do vídeo, e onde está a maior queda
  origem: de onde vieram as views (feed de Shorts, canal, busca...)
"""
import json
import os
import re
import time
from datetime import date, timedelta
from pathlib import Path

import requests

from .util import RAIZ, log

TOKEN_URL = "https://oauth2.googleapis.com/token"
DATA = "https://www.googleapis.com/youtube/v3"
ANALYTICS = "https://youtubeanalytics.googleapis.com/v2/reports"
PASTA = RAIZ / "data" / "analise"
ORIGENS = {"SHORTS": "feed de Shorts", "YT_CHANNEL": "página do canal", "YT_SEARCH": "busca", "SUBSCRIBER": "inscritos",
           "RELATED_VIDEO": "vídeos relacionados", "EXT_URL": "links de fora", "NOTIFICATION": "notificações",
           "YT_OTHER_PAGE": "outras páginas", "HASHTAGS": "hashtags", "PLAYLIST": "playlists", "NO_LINK_OTHER": "direto/outros"}


def _token() -> str:
    faltam = [k for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not os.environ.get(k, "").strip()]
    if faltam:
        raise RuntimeError("Faltam os segredos " + ", ".join(faltam) + " no GitHub (passo a passo no README da análise).")
    r = requests.post(TOKEN_URL, timeout=30, data={"client_id": os.environ["YT_CLIENT_ID"].strip(),
                                                   "client_secret": os.environ["YT_CLIENT_SECRET"].strip(),
                                                   "refresh_token": os.environ["YT_REFRESH_TOKEN"].strip(),
                                                   "grant_type": "refresh_token"})
    if r.status_code >= 400:
        raise RuntimeError(f"O Google recusou o acesso ({r.status_code}): {r.text[:300]}")
    return r.json()["access_token"]


def _get(url, tok, **params):
    r = requests.get(url, params=params, headers={"Authorization": f"Bearer {tok}"}, timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"{url.rsplit('/', 1)[-1]} {r.status_code}: {r.text[:400]}")
    return r.json()


def _segundos(iso: str) -> int:
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    return sum(int(v or 0) * k for v, k in zip(m.groups(), (3600, 60, 1))) if m else 0


def videos(tok) -> list[dict]:
    canal = _get(f"{DATA}/channels", tok, part="contentDetails,statistics,snippet", mine="true")["items"][0]
    uploads = canal["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, pagina = [], None
    while True:
        p = _get(f"{DATA}/playlistItems", tok, part="contentDetails", playlistId=uploads, maxResults=50,
                 **({"pageToken": pagina} if pagina else {}))
        ids += [i["contentDetails"]["videoId"] for i in p["items"]]
        pagina = p.get("nextPageToken")
        if not pagina:
            break
    out = []
    for k in range(0, len(ids), 50):
        v = _get(f"{DATA}/videos", tok, part="snippet,statistics,contentDetails", id=",".join(ids[k:k + 50]))
        for it in v["items"]:
            out.append({"id": it["id"], "titulo": it["snippet"]["title"], "publicado": it["snippet"]["publishedAt"][:10],
                        "duracao": _segundos(it["contentDetails"]["duration"]),
                        "views_publicas": int(it["statistics"].get("viewCount", 0))})
    return out, canal


def _relatorio(tok, inicio, fim, metricas, **extra):
    return _get(ANALYTICS, tok, ids="channel==MINE", startDate=inicio, endDate=fim, metrics=metricas, **extra)


def _tabela(resp) -> list[dict]:
    nomes = [c["name"] for c in resp.get("columnHeaders", [])]
    return [dict(zip(nomes, linha)) for linha in resp.get("rows", []) or []]


def coletar() -> dict:
    tok = _token()
    lista, canal = videos(tok)
    inicio, fim = "2026-01-01", date.today().isoformat()
    por_id = {v["id"]: v for v in lista}
    filtro = "video==" + ",".join(por_id)
    base = "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,likes,comments,shares,subscribersGained"
    try:
        linhas = _tabela(_relatorio(tok, inicio, fim, base + ",engagedViews", dimensions="video", filters=filtro,
                                    sort="-views", maxResults=200))
    except RuntimeError as e:                                   # se a métrica engajada não vier junto, tenta sem ela
        log(f"engagedViews não veio por vídeo ({e}); seguindo sem")
        linhas = _tabela(_relatorio(tok, inicio, fim, base, dimensions="video", filters=filtro, sort="-views", maxResults=200))
    for l in linhas:
        por_id.get(l["video"], {}).update({k: v for k, v in l.items() if k != "video"})
    for v in lista:
        if not v.get("views"):
            continue
        try:                                                    # curva de retenção
            ret = _tabela(_relatorio(tok, inicio, fim, "audienceWatchRatio,relativeRetentionPerformance",
                                     dimensions="elapsedVideoTimeRatio", filters=f"video=={v['id']}"))
            v["retencao"] = [(round(r["elapsedVideoTimeRatio"], 2), round(r["audienceWatchRatio"], 3),
                              round(r.get("relativeRetentionPerformance") or 0, 2)) for r in ret]
        except RuntimeError as e:
            log(f"retenção de {v['titulo']}: {e}")
        try:                                                    # de onde vieram as views
            org = _tabela(_relatorio(tok, inicio, fim, "views", dimensions="insightTrafficSourceType",
                                     filters=f"video=={v['id']}", sort="-views"))
            v["origem"] = {o["insightTrafficSourceType"]: o["views"] for o in org}
        except RuntimeError as e:
            log(f"origem de {v['titulo']}: {e}")
        time.sleep(0.3)
    return {"data": fim, "canal": {"nome": canal["snippet"]["title"], **canal["statistics"]}, "videos": lista}


def _ponto(ret, x):
    if not ret:
        return None
    return min(ret, key=lambda r: abs(r[0] - x))[1]


def _maior_queda(ret, dur):
    if not ret or len(ret) < 3:
        return None
    quedas = [(ret[i][1] - ret[i + 1][1], ret[i + 1][0]) for i in range(1, len(ret) - 1)]   # ignora o 1º ponto (início)
    q, x = max(quedas)
    return round(x * dur), q


def resumir(dados: dict) -> str:
    vs = [v for v in dados["videos"] if v.get("views")]
    if not vs:
        return "Ainda não há dados de Analytics (o YouTube atrasa de 48 a 72 horas)."
    linhas = [f"📊 {dados['canal']['nome']}: {dados['canal'].get('subscriberCount', '?')} inscritos, "
              f"{dados['canal'].get('viewCount', '?')} views no total\n(dados do YouTube têm 2 a 3 dias de atraso)\n"]
    for v in sorted(vs, key=lambda v: -v["views"]):
        views = v["views"]
        fic = f"{100 * v['engagedViews'] / views:.0f}%" if v.get("engagedViews") else "?"
        mil = 1000 / views
        ret = v.get("retencao") or []
        queda = _maior_queda(ret, v["duracao"])
        origem = v.get("origem") or {}
        top = max(origem, key=origem.get) if origem else None
        linhas.append(
            f"▶ {v['titulo'][:48]} ({v['duracao']}s, {v['publicado'][5:]})\n"
            f"   {views} views · ficaram {fic} · assistido {v.get('averageViewPercentage', 0):.0f}% "
            f"({v.get('averageViewDuration', 0)}s)\n"
            f"   ❤ {v.get('likes', 0)} · 💬 {v.get('comments', 0)} · ↗ {v.get('shares', 0)} "
            f"({v.get('shares', 0) * mil:.1f}/mil) · +{v.get('subscribersGained', 0)} inscritos\n"
            + (f"   retenção: 10% → {_ponto(ret, 0.1):.0%} · metade → {_ponto(ret, 0.5):.0%} · fim → {_ponto(ret, 0.95):.0%}"
               + (f" · maior queda ~{queda[0]}s" if queda else "") + "\n" if ret else "")
            + (f"   origem: {ORIGENS.get(top, top)} ({100 * origem[top] / max(1, sum(origem.values())):.0f}%)\n" if top else ""))
    return "\n".join(linhas)


def main():
    from . import telegram
    try:
        dados = coletar()
    except Exception as e:
        telegram.enviar_mensagem(f"Relatório do YouTube falhou: {e}"[:3800])
        raise
    PASTA.mkdir(parents=True, exist_ok=True)
    (PASTA / f"{dados['data']}.json").write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    (PASTA / "ultima.json").write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    texto = resumir(dados)
    for k in range(0, len(texto), 3800):
        telegram.enviar_mensagem(texto[k:k + 3800])


if __name__ == "__main__":
    main()
