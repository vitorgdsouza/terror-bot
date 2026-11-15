"""Funções compartilhadas: caminhos, configuração e log."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONFIG = RAIZ / "config" / "serie.json"
HISTORICO = RAIZ / "data" / "historico.json"
SAIDA = RAIZ / "saida"
MUSICA = RAIZ / "assets" / "musica"


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def carregar_config() -> dict:
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)


def carregar_historico() -> list:
    if HISTORICO.exists():
        with open(HISTORICO, encoding="utf-8") as f:
            return json.load(f)
    return []


def salvar_no_historico(titulo: str, tema: str) -> None:
    hist = carregar_historico()
    hist.append({"data": time.strftime("%Y-%m-%d"), "titulo": titulo, "tema": tema})
    HISTORICO.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORICO, "w", encoding="utf-8") as f:
        json.dump(hist[-200:], f, ensure_ascii=False, indent=2)


def env(nome: str, obrigatorio: bool = True) -> str:
    valor = os.environ.get(nome, "").strip()
    if obrigatorio and not valor:
        sys.exit(f"ERRO: a variável {nome} não está configurada (veja o README, seção Secrets).")
    return valor


def rodar(cmd: list, cwd=None) -> None:
    """Roda um comando (ffmpeg etc.) e mostra o erro de forma legível se falhar."""
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if r.returncode != 0:
        raise RuntimeError(f"Comando falhou: {' '.join(cmd[:6])}...\n{r.stderr[-3000:]}")


def duracao(arquivo: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(arquivo)],
        capture_output=True, text=True, check=True)
    return float(r.stdout.strip())
