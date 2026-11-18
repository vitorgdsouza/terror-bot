"""Fila de postagem: o bot publica no YouTube o próximo vídeo da fila em horários fixos (2 por dia).

    data/fila.json = {"itens": [{"run_id", "titulo", "titulo_youtube", "legenda"}], "postados": [...]}
    python -m src.fila proximo   # escreve run_id/título do próximo no GITHUB_OUTPUT (vazio = fila vazia)
    python -m src.fila feito     # tira o primeiro da fila, guarda em "postados" e avisa no Telegram
    python -m src.fila mostrar   # manda a fila no Telegram (/fila)
    python -m src.fila enfileirar  # põe no fim da fila o último vídeo renderizado (/enfileirar)
"""
import json
import os
import sys
import time

from .util import RAIZ, log

FILA = RAIZ / "data" / "fila.json"
PENDENTE = RAIZ / "data" / "pendente.json"
HORARIOS = "11h47 e 18h47"


def carregar() -> dict:
    try:
        return json.loads(FILA.read_text(encoding="utf-8"))
    except Exception:
        return {"itens": [], "postados": []}


def salvar(f: dict) -> None:
    FILA.parent.mkdir(parents=True, exist_ok=True)
    FILA.write_text(json.dumps(f, ensure_ascii=False, indent=1), encoding="utf-8")


def _saida(chave: str, valor: str) -> None:
    arq = os.environ.get("GITHUB_OUTPUT")
    if arq:
        with open(arq, "a", encoding="utf-8") as fh:
            fh.write(f"{chave}<<FIM\n{valor}\nFIM\n")


def _lista(f: dict) -> str:
    if not f["itens"]:
        return "A fila está vazia."
    return "\n".join(f"{i + 1}. {it.get('titulo_youtube') or it['titulo']}" for i, it in enumerate(f["itens"]))


def proximo() -> None:
    f = carregar()
    it = f["itens"][0] if f["itens"] else {}
    _saida("run_id", it.get("run_id", ""))
    _saida("titulo_youtube", it.get("titulo_youtube", ""))
    _saida("legenda", it.get("legenda", ""))
    log(f"Próximo da fila: {it.get('titulo', '(vazia)')}")


def feito() -> None:
    from . import telegram
    f = carregar()
    if not f["itens"]:
        return
    it = f["itens"].pop(0)
    it["postado_em"] = time.strftime("%Y-%m-%d %H:%M")
    f["postados"].append(it)
    salvar(f)
    restam = len(f["itens"])
    aviso = (f"Na fila: {restam} vídeo(s). Próximo: {f['itens'][0].get('titulo_youtube') or f['itens'][0]['titulo']}"
             if restam else "A fila acabou: mande /enfileirar depois de gerar o próximo vídeo.")
    telegram.enviar_mensagem(aviso)


def mostrar() -> None:
    from . import telegram
    telegram.enviar_mensagem(f"Fila de postagem do YouTube ({HORARIOS}):\n{_lista(carregar())}")


def enfileirar() -> None:
    from . import telegram
    if not PENDENTE.exists():
        telegram.enviar_mensagem("Não há vídeo renderizado para pôr na fila.")
        return
    p = json.loads(PENDENTE.read_text(encoding="utf-8"))
    f = carregar()
    if any(it["run_id"] == p["run_id"] for it in f["itens"] + f["postados"]):
        telegram.enviar_mensagem(f"\"{p['titulo']}\" já está na fila (ou já foi postado).")
        return
    f["itens"].append({"run_id": p["run_id"], "titulo": p["titulo"], "titulo_youtube": p.get("titulo_youtube", ""),
                       "adicionado": time.strftime("%Y-%m-%d %H:%M")})
    salvar(f)
    telegram.enviar_mensagem(f"Na fila ✅ \"{p['titulo']}\" (posição {len(f['itens'])}).\n{_lista(f)}")


if __name__ == "__main__":
    {"proximo": proximo, "feito": feito, "mostrar": mostrar, "enfileirar": enfileirar}[sys.argv[1]]()
