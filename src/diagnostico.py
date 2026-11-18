"""Diagnóstico: por que os Shorts novos não sobem? Status de cada vídeo + de onde vieram as views."""
import json
from datetime import date, timedelta
from pathlib import Path
from .analise import _token, _get, DATA, _relatorio, _tabela, videos


def main():
    tok = _token()
    lista, canal = videos(tok)
    ids = [v["id"] for v in lista]
    out = {"canal": {"status": canal.get("status"), "stats": canal.get("statistics")}, "videos": []}
    ch = _get(f"{DATA}/channels", tok, part="status,brandingSettings", mine="true")["items"][0]
    out["canal"]["status"] = ch.get("status")
    out["canal"]["madeForKids_padrao"] = ch.get("brandingSettings", {}).get("channel", {}).get("madeForKids")
    v = _get(f"{DATA}/videos", tok, part="snippet,status,contentDetails,statistics", id=",".join(ids))["items"]
    for it in v:
        s, sn, cd = it["status"], it["snippet"], it["contentDetails"]
        out["videos"].append({"id": it["id"], "titulo": sn["title"], "publicado": sn["publishedAt"],
            "privacidade": s.get("privacyStatus"), "upload": s.get("uploadStatus"), "rejeicao": s.get("rejectionReason"),
            "falha": s.get("failureReason"), "kids": s.get("madeForKids"), "kids_declarado": s.get("selfDeclaredMadeForKids"),
            "licenca": s.get("license"), "embed": s.get("embeddable"), "duracao": cd.get("duration"),
            "restricao_regiao": cd.get("regionRestriction"), "classificacao": cd.get("contentRating"),
            "categoria": sn.get("categoryId"), "idioma": sn.get("defaultLanguage"), "idioma_audio": sn.get("defaultAudioLanguage"),
            "tags": sn.get("tags"), "descricao": sn.get("description", "")[:200], "views": it["statistics"].get("viewCount")})
    fim = date.today().isoformat(); ini = (date.today() - timedelta(days=30)).isoformat()
    for dim in ("insightTrafficSourceType", "day"):
        try:
            out[f"por_{dim}"] = _tabela(_relatorio(tok, ini, fim, "views", dimensions=f"video,{dim}" if dim != "day" else "day",
                                                    **({"filters": "video==" + ",".join(ids)} if dim != "day" else {})))
        except Exception as e:
            out[f"por_{dim}"] = str(e)
    Path("data/analise").mkdir(parents=True, exist_ok=True)
    Path("data/analise/diagnostico.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(json.dumps(out, ensure_ascii=False, indent=1)[:6000])


if __name__ == "__main__":
    main()
