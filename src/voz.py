"""Narração grátis com as vozes neurais do Microsoft Edge (biblioteca edge-tts, sem chave)."""
import asyncio
from pathlib import Path

import edge_tts

from .util import duracao, log, rodar

# tratamento "narrador sombrio": voz um pouco mais grave (sem mudar a velocidade), graves encorpados,
# presença na fala, compressão de locutor, eco curto de sala e volume padronizado
EFEITOS_VOZ = {
    "narrador_sombrio": ("aresample=44100,asetrate=44100*0.95,aresample=44100,atempo=1.0526316,"
                         "equalizer=f=110:t=q:w=1.2:g=5,equalizer=f=3500:t=q:w=1.5:g=2,"
                         "acompressor=threshold=-20dB:ratio=3:attack=10:release=200,"
                         "aecho=0.8:0.5:45|90:0.18|0.10,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100"),
    "nenhum": "",
}


def _tratar(arquivo: Path, efeito: str) -> None:
    filtro = EFEITOS_VOZ.get(efeito, "")
    if not filtro:
        return
    tmp = arquivo.with_suffix(".tmp.mp3")
    rodar(["ffmpeg", "-y", "-i", str(arquivo), "-af", filtro, "-ac", "1", "-b:a", "128k", str(tmp)])
    tmp.replace(arquivo)


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
        _tratar(destino, cfg["voz"].get("efeito", "nenhum"))
        total = duracao(destino)
        if not palavras:
            palavras = _tempos_aproximados(cena["narracao"], total)
        resultado.append({"arquivo": destino, "duracao": total, "palavras": palavras})
    return resultado
