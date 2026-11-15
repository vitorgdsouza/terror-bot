"""Narração grátis com as vozes neurais do Microsoft Edge (biblioteca edge-tts, sem chave)."""
import asyncio
from pathlib import Path

import edge_tts

from .util import duracao, log


async def _sintetizar(texto: str, cfg_voz: dict, destino: Path) -> list[dict]:
    kwargs = dict(voice=cfg_voz["nome"], rate=cfg_voz["velocidade"], pitch=cfg_voz["tom"])
    try:
        com = edge_tts.Communicate(texto, boundary="WordBoundary", **kwargs)
    except TypeError:  # versões antigas não têm o parâmetro "boundary"
        com = edge_tts.Communicate(texto, **kwargs)
    palavras = []
    with open(destino, "wb") as f:
        async for parte in com.stream():
            if parte["type"] == "audio":
                f.write(parte["data"])
            elif parte["type"] == "WordBoundary":
                palavras.append({
                    "texto": parte["text"],
                    "inicio": parte["offset"] / 10_000_000,
                    "fim": (parte["offset"] + parte["duration"]) / 10_000_000,
                })
    return palavras


def _tempos_aproximados(texto: str, total: float) -> list[dict]:
    """Plano B: distribui as palavras pelo tempo do áudio proporcionalmente ao tamanho."""
    palavras = texto.split()
    pesos = [len(p) + 2 for p in palavras]
    soma, t, saida = sum(pesos), 0.0, []
    for p, w in zip(palavras, pesos):
        d = total * w / soma
        saida.append({"texto": p, "inicio": t, "fim": t + d})
        t += d
    return saida


def gerar_narracao(roteiro: dict, cfg: dict, pasta: Path) -> list[dict]:
    """Gera um áudio por cena. Devolve [{arquivo, duracao, palavras}] para cada cena."""
    pasta.mkdir(parents=True, exist_ok=True)
    resultado = []
    for i, cena in enumerate(roteiro["cenas"]):
        destino = pasta / f"voz_{i:02d}.mp3"
        log(f"Narração {i + 1}/{len(roteiro['cenas'])}")
        for tentativa in range(3):
            try:
                palavras = asyncio.run(_sintetizar(cena["narracao"], cfg["voz"], destino))
                break
            except Exception as e:  # falha de rede ocasional
                if tentativa == 2:
                    raise
                log(f"  erro na voz ({e}), tentando de novo")
        total = duracao(destino)
        if not palavras:
            palavras = _tempos_aproximados(cena["narracao"], total)
        resultado.append({"arquivo": destino, "duracao": total, "palavras": palavras})
    return resultado
