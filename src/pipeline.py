"""Pipeline completo: roteiro -> imagens -> narração -> montagem -> Telegram.

Uso:
    python -m src.pipeline                      # tema padrão da série
    python -m src.pipeline --tema "Corpo Seco"  # tema escolhido
    python -m src.pipeline --sem-telegram       # só gera o vídeo na pasta saida/
"""
import argparse
import json
import re
import sys
import time
import traceback

from . import telegram
from .imagens import gerar_imagens
from .montagem import montar_video
from .roteiro import gerar_roteiro
from .util import SAIDA, carregar_config, log, salvar_no_historico
from .voz import gerar_narracao


def _pasta_do_video(titulo: str):
    slug = re.sub(r"[^a-z0-9]+", "-", titulo.lower())[:40].strip("-") or "video"
    return SAIDA / f"{time.strftime('%Y%m%d-%H%M')}-{slug}"


def executar(tema: str | None = None, usar_telegram: bool = True):
    cfg = carregar_config()
    roteiro = gerar_roteiro(cfg, tema)
    pasta = _pasta_do_video(roteiro["titulo"])
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / "roteiro.json").write_text(json.dumps(roteiro, ensure_ascii=False, indent=2), encoding="utf-8")

    if usar_telegram:
        telegram.enviar_mensagem(f"Roteiro pronto: \"{roteiro['titulo']}\". Gerando imagens, voz e vídeo (leva uns 5 a 10 minutos)...")

    imagens = gerar_imagens(roteiro, cfg, pasta / "imagens")
    vozes = gerar_narracao(roteiro, cfg, pasta / "audio")
    video = montar_video(roteiro, imagens, vozes, cfg, pasta / "video")

    hashtags = " ".join(dict.fromkeys(roteiro.get("hashtags", []) + cfg["hashtags_fixas"]))
    legenda = f"{roteiro['titulo']}\n\n{roteiro.get('legenda_post', '')}\n\n{hashtags}"
    (pasta / "legenda_do_post.txt").write_text(legenda, encoding="utf-8")

    if usar_telegram:
        telegram.enviar_video(video, legenda)
        texto = "\n\n".join(c["narracao"] for c in roteiro["cenas"])
        telegram.enviar_mensagem(f"Legenda para copiar e colar:\n\n{legenda}")
        telegram.enviar_mensagem(f"Roteiro completo:\n\n{texto}")

    salvar_no_historico(roteiro["titulo"], roteiro["tema"])
    log(f"Concluído: {video}")
    return video


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tema", default="")
    p.add_argument("--sem-telegram", action="store_true")
    a = p.parse_args()
    try:
        executar(a.tema.strip() or None, usar_telegram=not a.sem_telegram)
    except Exception as e:
        traceback.print_exc()
        if not a.sem_telegram:
            try:
                telegram.enviar_mensagem(f"Deu erro ao gerar o vídeo:\n{str(e)[:1500]}\n\nVeja os detalhes na aba Actions do GitHub.")
            except Exception:
                pass
        sys.exit(1)


if __name__ == "__main__":
    main()
