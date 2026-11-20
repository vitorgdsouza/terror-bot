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

CANAL = os.environ.get("CANAL", "").strip()          # vazio = Você Escaparia? (terror); "esfr" = E Se Fosse Real?
FILA = RAIZ / "data" / (f"fila_{CANAL}.json" if CANAL else "fila.json")
PENDENTE = RAIZ / "data" / "pendente.json"
HORARIOS = "12h17, 16h17 e 20h17" if CANAL else "11h47 e 18h47"


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
    rot = {"isca": "isca, 11h47", "protocolo": "protocolo, 18h47", "historia": "história, 18h47"}
    return "\n".join(f"{i + 1}. [{rot.get(it.get('tipo', 'isca'), it.get('tipo'))}] {it.get('titulo_youtube') or it['titulo']}"
                     for i, it in enumerate(f["itens"]))


def _do_turno(f: dict, turno: str) -> int | None:
    """11h47 = isca; 18h47 = o vídeo principal (protocolo ou história). Faixa vazia = não posta (nunca adianta o principal)."""
    if CANAL:                                           # canais novos não têm faixa de isca: sai o próximo
        return 0 if f["itens"] else None
    quer_isca = turno == "manha"
    for i, it in enumerate(f["itens"]):
        if (it.get("tipo", "isca") == "isca") == quer_isca:
            return i
    return None


def _ja_postou(f: dict, turno: str) -> str:
    """Trava contra post duplicado: agendamento do GitHub atrasado depois de um post manual, ou mais de 2 no dia."""
    hoje = time.strftime("%Y-%m-%d")
    do_dia = [it for it in f["postados"] if str(it.get("postado_em", "")).startswith(hoje)]
    if CANAL:                                           # canal 2: até 3 por dia, com pelo menos 2 h entre um e outro
        if len(do_dia) >= 3:
            return "já saíram 3 posts hoje"
        agora = time.time()
        for it in do_dia:
            try:
                quando = time.mktime(time.strptime(str(it["postado_em"])[:16], "%Y-%m-%d %H:%M"))
            except Exception:
                continue
            if agora - quando < 2 * 3600:
                return "saiu um post há menos de 2 h"
        return ""
    if len(do_dia) >= 2:
        return "já saíram 2 posts hoje"
    quer_isca = turno == "manha"
    if any((it.get("tipo", "isca") == "isca") == quer_isca for it in do_dia):
        return f"a faixa da {'isca' if quer_isca else 'principal'} já foi postada hoje"
    return ""


def proximo() -> None:
    f = carregar()
    turno = os.environ.get("TURNO", "manha")
    motivo = _ja_postou(f, turno)
    if motivo and os.environ.get("AGENDADO") == "1":
        log(f"Pulando o agendamento: {motivo}")
        for k in ("indice", "run_id", "titulo_youtube", "legenda"):
            _saida(k, "")
        return
    i = _do_turno(f, turno)
    it = f["itens"][i] if i is not None else {}
    _saida("indice", "" if i is None else str(i))
    _saida("run_id", it.get("run_id", ""))
    _saida("titulo_youtube", it.get("titulo_youtube", ""))
    _saida("legenda", it.get("legenda", ""))
    log(f"Próximo da fila: {it.get('titulo', '(vazia)')}")


def feito() -> None:
    from . import telegram
    f = carregar()
    if not f["itens"]:
        return
    i = int(os.environ.get("INDICE") or 0)
    it = f["itens"].pop(i if i < len(f["itens"]) else 0)
    it["postado_em"] = time.strftime("%Y-%m-%d %H:%M")
    f["postados"].append(it)
    salvar(f)
    restam = len(f["itens"])
    aviso = (f"Na fila: {restam} vídeo(s). Próximo: {f['itens'][0].get('titulo_youtube') or f['itens'][0]['titulo']}"
             if restam else "A fila acabou: mande /enfileirar depois de gerar o próximo vídeo.")
    telegram.enviar_mensagem(aviso)


def aviso() -> None:
    """Manda no Telegram a mensagem da variável AVISO (a direção automática usa para falar com você)."""
    from . import telegram
    texto = os.environ.get("AVISO", "").strip()
    for k in range(0, len(texto), 3800):
        telegram.enviar_mensagem(texto[k:k + 3800])


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
                       "tipo": p.get("tipo", "historia"), "legenda": p.get("legenda", ""),
                       "adicionado": time.strftime("%Y-%m-%d %H:%M")})
    salvar(f)
    telegram.enviar_mensagem(f"Na fila ✅ \"{p['titulo']}\" (posição {len(f['itens'])}).\n{_lista(f)}")


if __name__ == "__main__":
    {"proximo": proximo, "feito": feito, "mostrar": mostrar, "enfileirar": enfileirar, "aviso": aviso}[sys.argv[1]]()
