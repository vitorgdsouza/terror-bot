"""Mesa do gerente: o Vitor aprova o que a equipe de agentes entrega.

Os pontos de aprovação são dois:
    roteiro  O Roteirista propõe. Com o OK do Vitor, o render começa sozinho.
    video    O Revisor confere e o Publicador propõe. Com o OK do Vitor, o vídeo entra na fila.

    data/aprovacoes.json = {"proximo": N, "itens": [{id, tipo, agente, titulo, arquivo, run_id, resumo,
                            titulo_youtube, legenda, tipo_video, status, motivo, criado, decidido}]}
    status: pendente | aprovado | renderizando | renderizado | revisado | refazer | na_fila | substituido

Uso:
    python -m src.aprovacao propor     (env: TIPO, AGENTE, ARQUIVO, RUN_ID, RESUMO)
    python -m src.aprovacao decidir    (env: ID, DECISAO=aprovar|refazer, MOTIVO)
    python -m src.aprovacao renderizado  (env: ROTEIRO_ARQ, RUN_ID)  chamado pelo refazer-video
    python -m src.aprovacao pendentes  manda no Telegram o que espera decisão
"""
import json
import os
import sys
import time

import requests

from .util import RAIZ, log

ARQ = RAIZ / "data" / "aprovacoes.json"
ICONE = {"Analista": "📊", "Roteirista": "✍️", "Diretor de Arte": "🎨", "Revisor": "🔍", "Publicador": "📣"}


def carregar() -> dict:
    try:
        return json.loads(ARQ.read_text(encoding="utf-8"))
    except Exception:
        return {"proximo": 1, "itens": []}


def salvar(d: dict) -> None:
    ARQ.parent.mkdir(parents=True, exist_ok=True)
    ARQ.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def _agora() -> str:
    return time.strftime("%Y-%m-%d %H:%M")


def _achar(d: dict, id_: int) -> dict | None:
    return next((it for it in d["itens"] if it["id"] == id_), None)


def _disparar_render(arquivo: str) -> bool:
    """Dispara o refazer-video.yml (o GITHUB_TOKEN pode disparar workflow_dispatch)."""
    tok, repo = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
    if not tok or not repo:
        log("Sem GITHUB_TOKEN: o render precisa ser disparado à mão")
        return False
    r = requests.post(f"https://api.github.com/repos/{repo}/actions/workflows/refazer-video.yml/dispatches",
                      headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json"},
                      json={"ref": "main", "inputs": {"roteiro": arquivo}}, timeout=30)
    log(f"Disparo do render de {arquivo}: {r.status_code} {r.text[:200]}")
    return r.status_code < 300


def propor() -> None:
    from . import telegram
    e = os.environ
    tipo, agente = e["TIPO"], e.get("AGENTE", "Roteirista")
    arquivo, run_id = e.get("ARQUIVO", ""), e.get("RUN_ID", "")
    rot = {}
    if arquivo and (RAIZ / arquivo).exists():
        rot = json.loads((RAIZ / arquivo).read_text(encoding="utf-8"))
    d = carregar()
    for it in d["itens"]:                      # a proposta nova substitui a anterior do mesmo roteiro e etapa
        if it["arquivo"] == arquivo and it["tipo"] == tipo and it["status"] in ("pendente", "refazer"):
            it["status"], it["decidido"] = "substituido", _agora()
    id_ = d["proximo"]
    d["proximo"] += 1
    it = {"id": id_, "tipo": tipo, "agente": agente, "titulo": rot.get("titulo", arquivo), "arquivo": arquivo,
          "run_id": run_id, "resumo": e.get("RESUMO", ""), "titulo_youtube": rot.get("titulo_youtube", ""),
          "legenda": rot.get("legenda_post", ""), "tipo_video": rot.get("tipo", "historia"),
          "status": "pendente", "motivo": "", "criado": _agora(), "decidido": ""}
    d["itens"].append(it)
    salvar(d)
    if tipo == "roteiro":
        falas = "\n".join(f"{n + 1}. {c.get('narracao', '')}" for n, c in enumerate(rot.get("cenas", [])))
        texto = (f"{ICONE.get(agente, '🤖')} [{agente}] ROTEIRO #{id_} para aprovar\n"
                 f"\"{it['titulo']}\" ({it['tipo_video']})\n\n{it['resumo']}\n\nNarração:\n{falas}\n\n"
                 f"YouTube: {it['titulo_youtube']}\n\nAprove para eu renderizar, ou mande /refazer {id_} e o que mudar.")
    else:
        texto = (f"{ICONE.get(agente, '🤖')} [{agente}] VÍDEO #{id_} para aprovar\n"
                 f"\"{it['titulo']}\" ({it['tipo_video']}). O vídeo é o último que chegou com esse título.\n\n"
                 f"{it['resumo']}\n\nYouTube: {it['titulo_youtube']}\nTikTok (legenda): {it['legenda']}\n\n"
                 f"Aprove para entrar na fila, ou mande /refazer {id_} e o que mudar.")
    telegram.enviar_mensagem(texto, botoes=[[f"/aprovar {id_}", f"/refazer {id_}"]])
    print(id_)


def decidir(id_: int, decisao: str, motivo: str = "", avisar=True) -> str:
    d = carregar()
    it = _achar(d, id_)
    if not it:
        return f"Não achei o item #{id_}."
    if it["status"] not in ("pendente", "refazer"):
        return f"O #{id_} já foi decidido ({it['status']})."
    it["decidido"], it["motivo"] = _agora(), motivo
    if decisao == "refazer":
        it["status"] = "refazer"
        msg = (f"🔁 #{id_} \"{it['titulo']}\" volta para a equipe"
               + (f": {motivo}" if motivo else ". Diga o que mudar com /refazer " + str(id_) + " <o que mudar>"))
    elif it["tipo"] == "roteiro":
        ok = _disparar_render(it["arquivo"])
        it["status"] = "renderizando" if ok else "aprovado"
        msg = (f"✅ Roteiro #{id_} aprovado. "
               + ("Renderizando agora (cerca de 15 min); o Revisor confere e te manda o vídeo para a aprovação final."
                  if ok else "A equipe renderiza na próxima rodada."))
    else:
        from .fila import carregar as fila_carregar, salvar as fila_salvar, _lista
        f = fila_carregar()
        if not any(x["run_id"] == it["run_id"] for x in f["itens"] + f["postados"]):
            f["itens"].append({"run_id": it["run_id"], "titulo": it["titulo"], "titulo_youtube": it["titulo_youtube"],
                               "legenda": it["legenda"], "tipo": it["tipo_video"], "adicionado": _agora(),
                               "aprovacao": id_})
            fila_salvar(f)
        it["status"] = "na_fila"
        msg = f"✅ Vídeo #{id_} aprovado e na fila.\n{_lista(f)}"
    salvar(d)
    if avisar:
        from . import telegram
        telegram.enviar_mensagem(msg)
    return msg


def renderizado() -> None:
    """O refazer-video terminou: liga o run_id ao roteiro aprovado, para o Revisor achar."""
    arq, run_id = os.environ.get("ROTEIRO_ARQ", ""), os.environ.get("RUN_ID", "")
    d = carregar()
    for it in reversed(d["itens"]):
        if it["arquivo"] == arq and it["tipo"] == "roteiro" and it["status"] in ("renderizando", "aprovado", "renderizado"):
            it["status"], it["run_id"] = "renderizado", run_id
            salvar(d)
            log(f"Aprovação #{it['id']} renderizada no run {run_id}")
            return


def texto_pendentes() -> str:
    d = carregar()
    p = [it for it in d["itens"] if it["status"] in ("pendente", "refazer", "renderizando", "renderizado")]
    if not p:
        return "Nada esperando decisão. 👌"
    nome = {"pendente": "espera você", "refazer": "voltou para a equipe", "renderizando": "renderizando",
            "renderizado": "com o Revisor"}
    return "Mesa do gerente:\n" + "\n".join(
        f"#{it['id']} [{it['tipo']}] {it['titulo']}: {nome[it['status']]}" for it in p)


if __name__ == "__main__":
    acao = sys.argv[1]
    if acao == "propor":
        propor()
    elif acao == "decidir":
        print(decidir(int(os.environ["ID"]), os.environ.get("DECISAO", "aprovar"), os.environ.get("MOTIVO", "")))
    elif acao == "renderizado":
        renderizado()
    elif acao == "pendentes":
        from . import telegram
        telegram.enviar_mensagem(texto_pendentes())
