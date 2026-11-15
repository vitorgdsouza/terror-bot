"""Gera as imagens das cenas com a API gratuita do Pollinations (sem cadastro)."""
import hashlib
import os
import time
from pathlib import Path
from urllib.parse import quote

import requests

from .util import log, rodar

URL = "https://image.pollinations.ai/prompt/{prompt}"
LARGURA, ALTURA = 768, 1344  # vertical 9:16; o FFmpeg amplia para 1080x1920
ESPERA_ENTRE_IMAGENS = 16  # o plano anônimo aceita cerca de 1 pedido a cada 15 s


def semente_do_video(titulo: str) -> int:
    return int(hashlib.md5(titulo.encode()).hexdigest()[:8], 16) % 1_000_000


def montar_prompt(cena: dict, roteiro: dict, cfg: dict) -> str:
    visuais = {p["nome"]: p["visual"] for p in roteiro.get("personagens", [])}
    descricoes = [f"{nome}: {visuais[nome]}" for nome in cena.get("personagens_na_cena", []) if nome in visuais]
    # o estilo vai PRIMEIRO: os geradores dão mais peso ao começo do pedido
    partes = [cfg["estilo_visual"], "Scene: " + cena["imagem"]]
    if descricoes:
        partes.append("Characters: " + "; ".join(descricoes))
    partes.append("flat vector cartoon, adult characters only")
    return ". ".join(partes)


def placeholder(destino: Path) -> None:
    """Se a API falhar de vez, cria um fundo escuro com neblina para o vídeo não quebrar."""
    rodar(["ffmpeg", "-y", "-f", "lavfi", "-i",
           f"color=c=0x0b0d12:s={LARGURA}x{ALTURA}:d=1", "-vf",
           "noise=alls=30:allf=t,vignette=PI/3", "-frames:v", "1", str(destino)])


def gerar_imagem(prompt: str, destino: Path, semente: int, tentativas: int = 4) -> bool:
    """Pede UMA imagem ao Pollinations. Devolve True se conseguiu."""
    token = os.environ.get("POLLINATIONS_TOKEN", "").strip()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    params = {"width": LARGURA, "height": ALTURA, "seed": semente,
              "model": os.environ.get("POLLINATIONS_MODEL", "flux"), "nologo": "true"}
    destino.parent.mkdir(parents=True, exist_ok=True)
    for tentativa in range(tentativas):
        try:
            r = requests.get(URL.format(prompt=quote(prompt[:1500])), params=params,
                             headers=headers, timeout=240)
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("image"):
                destino.write_bytes(r.content)
                return True
            log(f"  resposta {r.status_code}: {r.text[:150]}")
        except requests.RequestException as e:
            log(f"  erro de rede: {e}")
        time.sleep(ESPERA_ENTRE_IMAGENS * (tentativa + 1))
    return False


def gerar_imagens(roteiro: dict, cfg: dict, pasta: Path) -> list[Path]:
    pasta.mkdir(parents=True, exist_ok=True)
    caminhos, falhas = [], 0
    base = semente_do_video(roteiro["titulo"])
    for i, cena in enumerate(roteiro["cenas"]):
        destino = pasta / f"cena_{i:02d}.jpg"
        log(f"Imagem {i + 1}/{len(roteiro['cenas'])}")
        if not gerar_imagem(montar_prompt(cena, roteiro, cfg), destino, base + i):
            falhas += 1
            log("  usando fundo escuro no lugar desta imagem")
            placeholder(destino)
        caminhos.append(destino)
        if i < len(roteiro["cenas"]) - 1:
            time.sleep(ESPERA_ENTRE_IMAGENS)
    if falhas == len(roteiro["cenas"]):
        raise RuntimeError("Nenhuma imagem foi gerada: o Pollinations parece fora do ar.")
    return caminhos
