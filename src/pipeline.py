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

from . import serie, telegram
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

    from .planos import modo_ilustrado
    if usar_telegram:
        telegram.enviar_mensagem(f"Roteiro pronto: \"{roteiro['titulo']}\" ({len(roteiro['cenas'])} planos). "
                                 "Gerando ilustrações, voz e animação (leva uns 10 a 15 minutos)...")
    if modo_ilustrado(cfg):
        from .ilustrador import gerar_ilustracoes
        gerar_ilustracoes(roteiro, cfg, pasta / "imagens")
        aviso = roteiro.get("_ilustracoes", {}).get("aviso")
        if aviso and usar_telegram:
            telegram.enviar_mensagem(f"Atenção: {aviso}\nO vídeo vai sair com cenários prontos no lugar das ilustrações.")

    vozes = gerar_narracao(roteiro, cfg, pasta / "audio")
    video = montar_video(roteiro, vozes, cfg, pasta / "video")

    hashtags = " ".join(dict.fromkeys(roteiro.get("hashtags", []) + cfg["hashtags_fixas"]))
    legenda = f"{roteiro['titulo']}\n\n{roteiro.get('legenda_post', '')}\n\n{hashtags}"
    (pasta / "legenda_do_post.txt").write_text(legenda, encoding="utf-8")

    if usar_telegram:
        telegram.enviar_video(video, legenda)
        texto = "\n\n".join(c["narracao"] for c in roteiro["cenas"])
        telegram.enviar_mensagem(f"Legenda para copiar e colar:\n\n{legenda}")
        telegram.enviar_mensagem(f"Roteiro completo:\n\n{texto}"[:4000])
        info = roteiro.get("_ilustracoes")
        if info:
            telegram.enviar_mensagem(f"Ilustrações geradas: {info['geradas']} (~US$ {info['custo_usd']}), falhas: {info['falhas']}")

    if usar_telegram:
        telegram.enviar_mensagem(serie.mensagem_proximo_passo(roteiro))
    salvar_no_historico(roteiro["titulo"], roteiro["tema"], roteiro.get("protagonista", ""), serie.campos_historico(roteiro))
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
