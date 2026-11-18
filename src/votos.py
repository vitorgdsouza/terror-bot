"""Conta os votos A/B nos comentários do YouTube (os do TikTok o usuário informa).

    python -m src.votos <trecho do título ou id do vídeo>
"""
import json
import re
import sys

from .analise import DATA, _get, _token, videos
from .util import log


def _voto(texto: str) -> str | None:
    t = texto.strip().upper()
    a = re.search(r"(^|[^A-Z])A([^A-Z]|$)", t) or re.search(r"\bOP[CÇ][AÃ]O A\b|\bLETRA A\b", t)
    b = re.search(r"(^|[^A-Z])B([^A-Z]|$)", t) or re.search(r"\bOP[CÇ][AÃ]O B\b|\bLETRA B\b", t)
    if a and not b:
        return "A"
    if b and not a:
        return "B"
    return None


def contar(alvo: str) -> dict:
    tok = _token()
    lista, _ = videos(tok)
    v = next((v for v in lista if v["id"] == alvo), None) or next(
        (v for v in lista if alvo.lower() in v["titulo"].lower()), None)
    if not v:
        raise RuntimeError(f"Não achei o vídeo '{alvo}' no canal.")
    contagem, pagina, comentarios = {"A": 0, "B": 0}, None, []
    while True:
        r = _get(f"{DATA}/commentThreads", tok, part="snippet", videoId=v["id"], maxResults=100, textFormat="plainText",
                 **({"pageToken": pagina} if pagina else {}))
        for it in r.get("items", []):
            texto = it["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comentarios.append(texto)
            if (voto := _voto(texto)):
                contagem[voto] += 1
        pagina = r.get("nextPageToken")
        if not pagina:
            break
    return {"video": v["titulo"], "id": v["id"], "votos": contagem, "comentarios": len(comentarios),
            "amostra": comentarios[:15]}


if __name__ == "__main__":
    res = contar(" ".join(sys.argv[1:]))
    log(json.dumps(res, ensure_ascii=False, indent=1))
