"""Remonta um episódio já feito com as melhorias atuais da animação, sem mudar a história.

Usa o roteiro.json de uma execução anterior (artefato baixado em baixado/), gera a narração de novo,
anima, monta e manda no Telegram como "versão ajustada". Não mexe no histórico da série.
    python -m src.refazer
"""
import json
import os
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
    if r.get("formato") == "real" and not (os.environ.get("PIXABAY_API_KEY") or os.environ.get("PEXELS_API_KEY")):
        telegram.enviar_mensagem("Para o formato real falta o segredo PIXABAY_API_KEY no GitHub (grátis em pixabay.com/api/docs).")
        sys.exit(1)
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
    # folha de contato (um quadro a cada 1,5 s) para revisão: fica no repositório em data/previas/
    import subprocess
    previas = RAIZ / "data" / "previas"
    previas.mkdir(parents=True, exist_ok=True)
    from .util import duracao
    passo = 0.5 if duracao(final) < 30 else 1.5          # vídeo curto: mais quadros por segundo na folha
    nome = Path(os.environ.get("ROTEIRO_ARQ", "")).stem or "ultima_folha"
    for destino in {previas / "ultima_folha.jpg", previas / f"{nome}.jpg"}:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(final), "-vf", f"fps=1/{passo},scale=150:-1,tile=8x7",
                        "-frames:v", "1", "-q:v", "4", str(destino)])
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
