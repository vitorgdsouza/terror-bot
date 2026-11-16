"""Narração com as vozes do Gemini (TTS do Google), ex.: "Enceladus". Usa a mesma GEMINI_API_KEY do roteiro.

O estilo da leitura é controlado por uma instrução em texto antes da fala (calma, suspense, dramática).
Teste: python -m src.voz_gemini --teste [--voz Enceladus]  -> manda 3 amostras no Telegram.
"""
import base64
import subprocess
import sys
import time
from pathlib import Path

import requests

from .util import env, log

URL = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
MODELOS = ["gemini-2.5-pro-preview-tts", "gemini-2.5-flash-preview-tts", "gemini-2.5-pro-tts", "gemini-2.5-flash-tts"]

ESTILOS = {
    "calma": ("Leia em português do Brasil, como narrador de uma história de terror: voz grave, calma, "
              "baixa e próxima, ritmo tranquilo, com pequenas pausas nas reticências"),
    "suspense": ("Leia em português do Brasil, como narrador de uma história de terror: voz grave e tensa, "
                 "quase sussurrada nos momentos de medo, criando suspense, ritmo pausado"),
    "dramatica": ("Leia em português do Brasil, como narrador de uma história de terror: voz grave, intensa e "
                  "dramática, aumentando a tensão a cada frase e enfatizando as palavras fortes"),
}


def sintetizar(texto: str, destino: Path, voz: str = "Enceladus", estilo: str = "calma") -> Path:
    """Gera um .wav (24 kHz mono) com a voz pedida. Devolve o caminho."""
    chave = env("GEMINI_API_KEY")
    instrucao = ESTILOS.get(estilo, estilo)
    corpo = {
        "contents": [{"parts": [{"text": f"{instrucao}:\n\n{texto}"}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voz}}},
        },
    }
    erros = []
    for modelo in MODELOS:
        for tentativa in range(4):
            try:
                r = requests.post(URL.format(modelo=modelo), json=corpo, timeout=300,
                                  headers={"x-goog-api-key": chave})
            except requests.RequestException as e:
                erros.append(f"{modelo}: {type(e).__name__}")
                time.sleep(10)
                continue
            if r.status_code == 200:
                try:
                    dados = r.json()["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
                except (KeyError, IndexError, ValueError):
                    erros.append(f"{modelo}: resposta sem áudio {r.text[:200]}")
                    break
                pcm = destino.with_suffix(".pcm")
                pcm.write_bytes(base64.b64decode(dados))
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", "24000", "-ac", "1",
                                "-i", str(pcm), str(destino)], check=True)
                pcm.unlink()
                log(f"Voz {voz} ({estilo}) gerada com {modelo}")
                return destino
            if r.status_code in (429, 500, 503) and tentativa < 3:
                espera = 25 * (tentativa + 1)
                log(f"Gemini TTS ocupado/limite ({r.status_code}) em {modelo}, tentando em {espera}s")
                erros.append(f"{modelo}: {r.status_code} {r.text[:200]}")
                time.sleep(espera)
                continue
            erros.append(f"{modelo}: {r.status_code} {r.text[:300]}")
            break  # modelo inexistente ou recusado: tenta o próximo
    raise RuntimeError("Gemini TTS falhou:\n" + "\n".join(erros[-6:]))


def _teste(voz: str) -> None:
    from . import telegram
    from .voz_clone import AMOSTRA

    pasta = Path("trabalho/teste_voz_gemini")
    pasta.mkdir(parents=True, exist_ok=True)
    telegram.enviar_mensagem(f"Gerando 3 amostras com a voz {voz} do Gemini...")
    falhas = []
    for i, estilo in enumerate(ESTILOS, 1):
        try:
            wav = sintetizar(AMOSTRA, pasta / f"{i}_{estilo}.wav", voz, estilo)
        except Exception as e:
            falhas.append(f"{estilo}: {e}")
            continue
        mp3 = wav.with_suffix(".mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-b:a", "128k", str(mp3)], check=True)
        telegram.enviar_audio(mp3, f"Voz {voz} — {i} {estilo}")
        time.sleep(8)  # respeita o limite por minuto do plano gratuito
    if falhas:
        telegram.enviar_mensagem(("Algumas amostras falharam:\n" + "\n".join(falhas))[:3800])
        if len(falhas) == len(ESTILOS):
            raise SystemExit(1)
    else:
        telegram.enviar_mensagem("Pronto! Ouça e diga qual estilo prefere: 1 calma, 2 suspense, 3 dramática.")


if __name__ == "__main__":
    if "--teste" in sys.argv:
        voz = sys.argv[sys.argv.index("--voz") + 1] if "--voz" in sys.argv else "Enceladus"
        _teste(voz)
