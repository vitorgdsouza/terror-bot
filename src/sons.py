"""Sons ambientes e efeitos combinados com cada cena, buscados no Freesound (API grátis, só sons CC0).

Cada cena ganha:
  - um ambiente em loop conforme o cenário (sala = relógio e silêncio de casa, casa_fora = grilos e vento...);
  - efeitos conforme o que acontece: chuva, trovão, luz piscando, TV chiando, passos, porta rangendo, o Abismo;
  - opcional, escolhido pelo roteirista: "som": {"busca": "drawer slam", "palavra": "gaveta"}
    -> o efeito toca exatamente quando o narrador fala a palavra.

Os sons baixados ficam guardados em data/sons/ (com a ficha de licença em data/sons/creditos.json),
então cada busca só vai ao Freesound uma vez. Sem a chave FREESOUND_API_KEY, nada muda no vídeo.
Teste: python -m src.sons --teste   (baixa os sons de alguns cenários e manda uma amostra no Telegram)
"""
import json
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import numpy as np
import requests

from .util import RAIZ, log

API = "https://freesound.org/apiv2/search/text/"
PASTA = RAIZ / "data" / "sons"
CREDITOS = PASTA / "creditos.json"
SR = 44100
EXCLUIR = " -music -song -voice -speech -talking -singing"

# ambiente de fundo por cenário (busca em inglês no Freesound)
AMBIENTES = {
    "sala": "quiet house room tone night clock ticking",
    "corredor": "empty house hallway ambience creaking",
    "quarto": "bedroom night ambience quiet",
    "debaixo_cama": "bedroom night ambience quiet",
    "cozinha": "kitchen night refrigerator hum",
    "pia_detalhe": "kitchen night refrigerator hum",
    "porta_entrada": "house entrance night ambience wind",
    "janela": "night window wind outside",
    "escada": "old house creaking ambience",
    "escada_cima": "old house creaking ambience",
    "banheiro": "bathroom dripping water ambience",
    "porao": "basement ambience dark drone",
    "garagem": "garage night ambience hum",
    "casa_fora": "night crickets suburban ambience",
    "rua": "night street ambience distant dog",
    "celular_cftv": "electrical hum static ambience",
}
# efeitos visuais da cena -> som (loop = toca a cena inteira; senão toca uma vez)
EFEITOS = {
    "chuva": ("rain on window", True),
    "relampago": ("thunder strike close", False),
    "luz_piscando": ("fluorescent light flicker buzz", True),
    "tv_chiando": ("tv static white noise", True),
    "tremor": ("deep cinematic boom impact", False),
}
ACOES = {
    "andando": ("footsteps wooden floor slow", False),
    "entrando": ("footsteps wooden floor slow", False),
    "saindo": ("footsteps wooden floor slow", False),
    "afastando": ("footsteps wooden floor slow", False),
    "aproximando": ("footsteps wooden floor slow", False),
    "correndo": ("running footsteps wooden floor", False),
}
POSES = {"abrindo_porta": ("door creak open slow", False)}
AMEACA = {"loop": "dark horror drone low rumble", "susto": "horror stinger hit"}

VOLUMES = {"ambiente": 0.22, "efeito": 0.5, "acao": 0.32, "ameaca": 0.28, "susto": 0.55, "roteiro": 0.6}


def _slug(texto: str) -> str:
    t = unicodedata.normalize("NFD", texto.lower())
    return re.sub(r"[^a-z0-9]+", "_", "".join(c for c in t if c.isascii())).strip("_")[:60]


def _norm(p: str) -> str:
    p = unicodedata.normalize("NFD", p.lower())
    return "".join(c for c in p if c.isalnum())


# ---------------------------------------------------------------- busca e cache
def _creditos() -> dict:
    return json.loads(CREDITOS.read_text(encoding="utf-8")) if CREDITOS.exists() else {}


def baixar(busca: str, loop: bool) -> Path | None:
    """Devolve o .wav normalizado da busca (do cache ou do Freesound). None se não achar ou sem chave."""
    PASTA.mkdir(parents=True, exist_ok=True)
    destino = PASTA / f"{_slug(busca)}.mp3"
    if destino.exists():
        return destino
    chave = os.environ.get("FREESOUND_API_KEY", "").strip()
    if not chave:
        return None
    duracao = "[8 TO 180]" if loop else "[0.3 TO 8]"
    params = {"query": busca + EXCLUIR, "token": chave, "page_size": 8, "sort": "rating_desc",
              "fields": "id,name,username,license,duration,previews,url,avg_rating,num_ratings",
              "filter": f'license:"Creative Commons 0" duration:{duracao}'}
    try:
        r = requests.get(API, params=params, timeout=30)
        r.raise_for_status()
        resultados = r.json().get("results", [])
        if not resultados:  # tenta de novo só com as 3 primeiras palavras
            params["query"] = " ".join(busca.split()[:3]) + EXCLUIR
            resultados = requests.get(API, params=params, timeout=30).json().get("results", [])
    except Exception as e:
        log(f"Freesound falhou para '{busca}': {e}")
        return None
    if not resultados:
        log(f"Freesound: nada encontrado para '{busca}'")
        return None
    som = max(resultados, key=lambda s: (s.get("num_ratings", 0) >= 3, s.get("avg_rating", 0)))
    try:
        audio = requests.get(som["previews"]["preview-hq-mp3"], timeout=60)
        audio.raise_for_status()
    except Exception as e:
        log(f"Freesound: download falhou ({e})")
        return None
    bruto = destino.with_suffix(".tmp.mp3")
    bruto.write_bytes(audio.content)
    # volume padronizado, sem silêncio no começo
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(bruto), "-af",
                    "silenceremove=start_periods=1:start_threshold=-45dB,loudnorm=I=-20:TP=-2",
                    "-ar", str(SR), "-ac", "2", "-b:a", "160k", str(destino)], check=True)
    bruto.unlink()
    cred = _creditos()
    cred[destino.name] = {"busca": busca, "nome": som["name"], "autor": som["username"],
                          "licenca": som["license"], "url": som["url"], "id": som["id"]}
    CREDITOS.write_text(json.dumps(cred, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Som novo: '{busca}' -> {som['name']} (de {som['username']}, CC0)")
    return destino


def _ler(arq: Path) -> np.ndarray:
    bruto = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(arq), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                           capture_output=True, check=True).stdout
    return np.frombuffer(bruto, np.float32).reshape(-1, 2).copy()


# ---------------------------------------------------------------- mixagem
class _Mesa:
    def __init__(self, total: float):
        self.buf = np.zeros((int(total * SR) + SR, 2), np.float32)
        self.cache: dict[Path, np.ndarray] = {}
        self.pos_loop: dict[Path, int] = {}   # o mesmo ambiente continua de onde parou na cena anterior

    def _som(self, arq: Path) -> np.ndarray:
        if arq not in self.cache:
            self.cache[arq] = _ler(arq)
        return self.cache[arq]

    def loop(self, arq: Path, ini: float, fim: float, vol: float, fade: float = 0.5) -> None:
        som = self._som(arq)
        if not len(som):
            return
        a, b = int(ini * SR), min(int(fim * SR), len(self.buf))
        n = b - a
        if n <= 0:
            return
        p = self.pos_loop.get(arq, 0)
        idx = (np.arange(n) + p) % len(som)
        self.pos_loop[arq] = (p + n) % len(som)
        trecho = som[idx] * vol
        f = min(int(fade * SR), n // 2)
        if f:
            rampa = np.linspace(0, 1, f, dtype=np.float32)[:, None]
            trecho[:f] *= rampa
            trecho[-f:] *= rampa[::-1]
        self.buf[a:b] += trecho

    def uma_vez(self, arq: Path, t: float, vol: float, max_dur: float = 6.0) -> None:
        som = self._som(arq)[: int(max_dur * SR)]
        a = int(max(t, 0) * SR)
        n = min(len(som), len(self.buf) - a)
        if n <= 0:
            return
        trecho = som[:n] * vol
        f = min(int(0.3 * SR), n // 3)
        if f:
            trecho[-f:] *= np.linspace(1, 0, f, dtype=np.float32)[:, None]
        self.buf[a:a + n] += trecho


def _tempo_da_palavra(cena: dict, palavra: str) -> float | None:
    alvo = _norm(palavra)
    if not alvo:
        return None
    for p in cena.get("_palavras") or []:
        if _norm(p["texto"]).startswith(alvo[: max(4, len(alvo) - 2)]):
            return p["inicio"]
    return None


def montar_trilha_sons(roteiro: dict, duracoes: list, destino: Path) -> Path | None:
    """Cria um .wav com os sons de todas as cenas, alinhado às durações das cenas. None se não houver sons."""
    total = sum(duracoes)
    mesa = _Mesa(total)
    usados, t0 = 0, 0.0
    ambiente_anterior = None
    for cena, dur in zip(roteiro["cenas"], duracoes):
        ini, fim = t0, t0 + dur
        t0 = fim
        # ambiente (o mesmo cenário seguido emenda sem cortar)
        busca_amb = AMBIENTES.get(cena.get("cenario") or cena.get("lugar") or "", "quiet house night ambience")
        arq = baixar(busca_amb, True)
        if arq:
            fade = 0.05 if busca_amb == ambiente_anterior else 0.6
            mesa.loop(arq, ini, fim, VOLUMES["ambiente"], fade)
            usados += 1
        ambiente_anterior = busca_amb
        # efeito visual da cena
        ef = EFEITOS.get(cena.get("efeito", "nenhum"))
        if ef and (arq := baixar(*ef)):
            (mesa.loop(arq, ini, fim, VOLUMES["efeito"]) if ef[1] else mesa.uma_vez(arq, ini + 0.15, VOLUMES["efeito"]))
            usados += 1
        # o que o personagem faz
        p = cena.get("personagem") or {}
        acao = ACOES.get(p.get("acao", "")) or POSES.get(p.get("pose", ""))
        if acao and (arq := baixar(*acao)):
            mesa.uma_vez(arq, ini + 0.2, VOLUMES["acao"], max_dur=min(dur, 4.0))
            usados += 1
        # a ameaça: zumbido grave enquanto aparece, e um susto quando surge
        a = cena.get("ameaca") or {}
        if a.get("tipo"):
            if arq := baixar(AMEACA["loop"], True):
                mesa.loop(arq, ini, fim, VOLUMES["ameaca"], 0.8)
            if a.get("acao") in ("aparecendo", "aproximando") and (arq := baixar(AMEACA["susto"], False)):
                mesa.uma_vez(arq, ini + 0.3, VOLUMES["susto"])
            usados += 1
        # som pedido pelo roteiro, no momento da palavra
        som = cena.get("som")
        if isinstance(som, dict) and som.get("busca") and (arq := baixar(str(som["busca"]), False)):
            t = _tempo_da_palavra(cena, str(som.get("palavra", "")))
            mesa.uma_vez(arq, ini + (t if t is not None else 0.3), VOLUMES["roteiro"])
            usados += 1
    if not usados:
        return None
    buf = mesa.buf[: int(total * SR)]
    pico = float(np.abs(buf).max() or 1)
    if pico > 0.95:
        buf = buf * (0.95 / pico)
    pcm = (buf * 32767).astype(np.int16)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    str(destino)], input=pcm.tobytes(), check=True)
    log(f"Sons das cenas: {usados} camadas")
    return destino


def _teste() -> None:
    from . import telegram
    roteiro = {"cenas": [
        {"cenario": "casa_fora", "efeito": "nenhum", "personagem": None, "ameaca": None},
        {"cenario": "sala", "efeito": "tv_chiando", "personagem": {"acao": "parado", "pose": "medo"}, "ameaca": None,
         "_palavras": [{"texto": "gaveta", "inicio": 1.5}], "som": {"busca": "drawer slam", "palavra": "gaveta"}},
        {"cenario": "corredor", "efeito": "luz_piscando", "personagem": {"acao": "andando", "pose": "costas"},
         "ameaca": {"tipo": "abismo", "acao": "aparecendo"}},
        {"cenario": "cozinha", "efeito": "relampago", "personagem": None, "ameaca": None},
    ]}
    saida = RAIZ / "trabalho" / "teste_sons.mp3"
    saida.parent.mkdir(exist_ok=True)
    if not montar_trilha_sons(roteiro, [5, 5, 5, 5], saida.with_suffix(".wav")):
        telegram.enviar_mensagem("Teste de sons: nenhum som baixado (confira o segredo FREESOUND_API_KEY).")
        sys.exit(1)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(saida.with_suffix(".wav")), "-b:a", "160k",
                    str(saida)], check=True)
    lista = "\n".join(f"- {v['busca']}: {v['nome']} ({v['autor']})" for v in _creditos().values())
    telegram.enviar_audio(saida, "Sons das cenas: fora de casa > sala com TV > corredor com o Abismo > cozinha com trovão")
    telegram.enviar_mensagem(f"Sons escolhidos (todos CC0):\n{lista}"[:3900])


if __name__ == "__main__":
    if "--teste" in sys.argv:
        _teste()
