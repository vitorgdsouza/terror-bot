"""Remonta um episódio já feito com as melhorias atuais da animação, sem mudar a história.

Usa o roteiro.json de uma execução anterior (artefato baixado em baixado/), gera a narração de novo,
anima, monta e manda no Telegram como "versão ajustada". Não mexe no histórico da série.
    python -m src.refazer
"""
import json
import shutil
import sys
from pathlib import Path

from .util import RAIZ, carregar_config, log

TRAB = RAIZ / "trabalho"


def main():
    from . import telegram
    from .montagem import montar_video
    from .voz import gerar_narracao
    achados = sorted((RAIZ / "baixado").rglob("roteiro.json"))
    if not achados:
        telegram.enviar_mensagem("Não achei o roteiro desse episódio no GitHub para refazer.")
        sys.exit(1)
    shutil.rmtree(TRAB, ignore_errors=True)
    TRAB.mkdir(parents=True)
    r = json.loads(achados[0].read_text(encoding="utf-8"))
    for c in r["cenas"]:                                  # limpa marcas internas da montagem anterior
        for k in [k for k in c if k.startswith("_")]:
            c.pop(k)
        for chave in ("personagem", "ameaca", "gato"):
            if isinstance(c.get(chave), dict):
                for k in [k for k in c[chave] if k.startswith("_")]:
                    c[chave].pop(k)
    (TRAB / "roteiro.json").write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    cfg = carregar_config()
    log(f"Refazendo: {r['titulo']} ({len(r['cenas'])} cenas)")
    telegram.enviar_mensagem(f"Refazendo \"{r['titulo']}\" com os ajustes (Abismo em silhueta até a escada, coleira menor)...")
    vozes = gerar_narracao(r, cfg, TRAB / "audio")
    final = montar_video(r, vozes, cfg, TRAB / "video")
    legenda = next((p.read_text(encoding="utf-8") for p in (RAIZ / "baixado").rglob("legenda_do_post.txt")), r["titulo"])
    import time
    telegram.enviar_video(final, f"{r['titulo']} (versão ajustada {time.strftime('%H:%M', time.localtime(time.time() - 3 * 3600))})")
    telegram.enviar_mensagem(f"Legenda para copiar e colar:\n\n{legenda}")


if __name__ == "__main__":
    main()
