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
    import os
    arq = os.environ.get("ROTEIRO_ARQ", "").strip()          # roteiro pronto do repositório (ex.: roteiros/x.json)
    achados = [RAIZ / arq] if arq else sorted((RAIZ / "baixado").rglob("roteiro.json"))
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
    telegram.enviar_mensagem(f"Montando \"{r['titulo']}\"...")
    vozes = gerar_narracao(r, cfg, TRAB / "audio")
    final = montar_video(r, vozes, cfg, TRAB / "video")
    legenda = next((p.read_text(encoding="utf-8") for p in (RAIZ / "baixado").rglob("legenda_do_post.txt")), None)
    if not legenda:
        tags = " ".join(dict.fromkeys(r.get("hashtags", []) + cfg.get("hashtags_fixas", [])))
        legenda = f"{r['titulo']}\n\n{r.get('legenda_post', '')}\n\n{tags}"
    import time
    telegram.enviar_video(final, f"{r['titulo']} ({'versão ajustada ' if not arq else ''}{time.strftime('%H:%M', time.localtime(time.time() - 3 * 3600))})")
    telegram.enviar_mensagem(f"Legenda para copiar e colar:\n\n{legenda}")
    from .thumb import enviar_thumbs
    enviar_thumbs(r, TRAB / "thumbs")
    from .postar import marcar_pendente
    marcar_pendente(r["titulo"])
    telegram.enviar_mensagem("Gostou? Mande /postar para publicar esta versão no YouTube Shorts.")


if __name__ == "__main__":
    main()
