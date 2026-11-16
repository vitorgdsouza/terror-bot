"""Clipes de IA (Kaggle) em até 3 cenas de destaque de cada episódio.

O roteiro marca as cenas com "clipe_ia": "<o que se mexe, em inglês>". O fluxo é:
  1. iniciar()   - na hora da narração: desenha o quadro inicial de cada cena marcada e dispara a GPU do Kaggle
                   (não espera; o Kaggle trabalha enquanto o resto do vídeo é feito);
  2. enviar      - o agente termina o vídeo normal e, em vez de mandar, deixa o vídeo "aguardando clipes";
  3. finalizar() - (scripts/gerar.sh, depois do agente) espera os clipes, troca as cenas marcadas por eles,
                   remonta o vídeo e envia. Se o Kaggle falhar ou demorar, envia o vídeo normal mesmo.
"""
import json
import shutil
import sys
import time
from pathlib import Path

from .util import RAIZ, carregar_config, log

TRAB = RAIZ / "trabalho"
PASTA = TRAB / "clipes_ia"
ESTADO = PASTA / "estado.json"
AGUARDANDO = TRAB / "AGUARDANDO_CLIPES"
KERNEL = "terror-bot-clipes-video"       # separado do teste, para um não cancelar o outro
DATASET = "terror-bot-entrada-video"
PALAVRAS_POR_SEGUNDO = 2.5


def config(cfg: dict) -> dict:
    return {"ligado": False, "max_por_video": 3, "espera_max_min": 100, **cfg.get("clipes_ia", {})}


def marcadas(roteiro: dict, cfg: dict) -> list[int]:
    c = config(cfg)
    if not c["ligado"]:
        return []
    ids = [i for i, cena in enumerate(roteiro["cenas"]) if str(cena.get("clipe_ia") or "").strip()]
    return ids[: c["max_por_video"]]


def iniciar(roteiro: dict, cfg: dict) -> int:
    """Dispara o Kaggle para as cenas marcadas. Devolve quantas foram pedidas (0 = nada a fazer)."""
    import os
    from .animacao import quadro
    from . import kaggle_clipes as K

    shutil.rmtree(PASTA, ignore_errors=True)
    AGUARDANDO.unlink(missing_ok=True)
    ids = marcadas(roteiro, cfg)
    if not ids:
        return 0
    if not os.environ.get("KAGGLE_API_TOKEN") or not os.environ.get("KAGGLE_USERNAME"):
        log("Clipes de IA: faltam os segredos do Kaggle; o vídeo sai só com a animação normal.")
        return 0
    entrada = PASTA / "entrada"
    entrada.mkdir(parents=True)
    prot = roteiro.get("protagonista", "homem")
    pedidos = []
    for i in ids:
        cena = roteiro["cenas"][i]
        segundos = min(5.0, len(cena["narracao"].split()) / PALAVRAS_POR_SEGUNDO + 0.8)
        quadro(dict(cena), 0.35, max(segundos, 2.0), prot, 8).save(entrada / f"cena_{i:02d}.png")
        pedidos.append({"id": f"cena_{i:02d}", "imagem": f"cena_{i:02d}.png", "segundos": round(segundos, 1),
                        "prompt": str(cena["clipe_ia"]).strip()})
    (entrada / "pedidos.json").write_text(json.dumps(pedidos, ensure_ascii=False, indent=2))
    try:
        K.enviar_dataset(entrada, DATASET=DATASET)
        K.rodar_kernel(so_disparar=True, KERNEL=KERNEL, DATASET=DATASET)
    except Exception as e:
        log(f"Clipes de IA: não consegui disparar o Kaggle ({e}); o vídeo sai só com a animação normal.")
        return 0
    ESTADO.write_text(json.dumps({"inicio": time.time(), "cenas": ids}))
    log(f"Clipes de IA disparados no Kaggle para as cenas {ids} (ficam prontos em ~{15 * len(ids) + 5} min).")
    return len(ids)


def pendente() -> bool:
    return ESTADO.exists()


def finalizar() -> None:
    """Espera os clipes, remonta o vídeo com eles e envia (ou envia o normal se der errado)."""
    from . import kaggle_clipes as K
    from . import ferramentas as F
    cfg = carregar_config()
    estado = json.loads(ESTADO.read_text())
    r = F._roteiro()
    usados, motivo = 0, ""
    try:
        passou = (time.time() - estado["inicio"]) / 60
        try:
            K.rodar_kernel(so_esperar=True, espera_max_min=max(5, int(config(cfg)["espera_max_min"] - passou)),
                           KERNEL=KERNEL, DATASET=DATASET)
        except RuntimeError as e:   # caiu no meio: aproveita os clipes que ficaram prontos
            if "passou de" in str(e):
                raise
            log(f"Notebook caiu no meio ({str(e)[:120]}); usando os clipes prontos")
        rel = K.baixar(PASTA / "saida", KERNEL=KERNEL)
        ruins = {e.split(":")[0] for e in rel.get("erros", [])}
        for i in estado["cenas"]:
            arq = rel.get("arquivos", {}).get(f"cena_{i:02d}")
            if arq and f"cena_{i:02d}" not in ruins:
                r["cenas"][i]["_clipe"] = arq
                usados += 1
        if rel.get("erros"):
            motivo = "; ".join(rel["erros"])[:300]
    except Exception as e:
        motivo = str(e)[:300]
        log(f"Clipes de IA falharam: {motivo}")
    if usados:
        from .montagem import montar_video
        vozes = [{**v, "arquivo": Path(v["arquivo"])} for v in json.loads(F.VOZES.read_text(encoding="utf-8"))]
        log(f"Remontando o vídeo com {usados} clipe(s) de IA")
        montar_video(r, vozes, cfg, TRAB / "video")
    nota = (TRAB / "nota_diretor.txt").read_text(encoding="utf-8") if (TRAB / "nota_diretor.txt").exists() else ""
    extra = f"Clipes de IA usados: {usados} de {len(estado['cenas'])}." + (f" Problema: {motivo}" if motivo else "")
    AGUARDANDO.unlink(missing_ok=True)
    F.enviar_agora(r, cfg, (nota + "\n" + extra).strip())


if __name__ == "__main__":
    if "--finalizar" in sys.argv:
        finalizar()
