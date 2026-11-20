"""Narração com as vozes do Gemini (TTS do Google), ex.: "Enceladus". Usa a mesma GEMINI_API_KEY do roteiro.

O estilo da leitura é controlado por uma instrução em texto antes da fala (calma, suspense, dramática).
Teste: python -m src.voz_gemini --teste [--voz Enceladus]  -> manda 3 amostras no Telegram.
"""
import base64
import shutil
import subprocess
import sys
import time
from pathlib import Path

import requests

from .util import env, log

URL = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
MODELOS = ["gemini-2.5-flash-preview-tts", "gemini-2.5-pro-preview-tts", "gemini-2.5-pro-tts", "gemini-2.5-flash-tts"]

ESTILOS = {
    "alerta": ("Leia em português do Brasil como um comunicado de emergência gravado: voz baixa, fria, monótona e "
               "controlada, sem emoção, pausas curtas e regulares entre as frases, como uma instrução de segurança"),
    "calma": ("Leia em português do Brasil, como narrador de uma história de terror: voz grave, calma, "
              "baixa e próxima, ritmo tranquilo, com pequenas pausas nas reticências"),
    "suspense": ("Leia em português do Brasil, como narrador de uma história de terror: voz grave e tensa, "
                 "quase sussurrada nos momentos de medo, criando suspense, ritmo pausado"),
    "curioso": ("Leia em português do Brasil como um apresentador jovem de vídeos de ciência e curiosidades: "
                "voz animada, curiosa e clara, ritmo rápido e envolvente, com ênfase nas palavras e números surpreendentes, "
                "pausas curtas só nas reticências"),
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


# ---------------------------------------------------------------- narração do episódio inteiro
def _norm(p: str) -> str:
    import unicodedata
    p = unicodedata.normalize("NFD", p.lower())
    return "".join(c for c in p if c.isalnum())


def _tempos_whisper(wav: Path) -> list[dict]:
    """Palavras reconhecidas com início/fim (faster-whisper, CPU). Vazio se não estiver instalado."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        log("faster-whisper não instalado: tempos das palavras serão estimados")
        return []
    import numpy as np
    try:
        # decodifica com o FFmpeg (o leitor interno do faster-whisper quebra com algumas versões do PyAV)
        bruto = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(wav), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                               capture_output=True, check=True).stdout
        audio = np.frombuffer(bruto, np.int16).astype(np.float32) / 32768.0
        modelo = WhisperModel("small", device="cpu", compute_type="int8")
        segs, _ = modelo.transcribe(audio, language="pt", word_timestamps=True, beam_size=1, vad_filter=False)
        segs = list(segs)
    except Exception as e:
        log(f"Whisper falhou ({e}): tempos das palavras serão estimados")
        return []
    return [{"t": w.word.strip(), "i": w.start, "f": w.end} for s in segs for w in (s.words or []) if w.word.strip()]


def _nota_fala(palavras: list[str], reconhecidas: list[dict]) -> float:
    """Quanto do roteiro o Whisper reconheceu na fala (1.0 = tudo)."""
    import difflib
    if not reconhecidas:
        return 0.0
    a = [_norm(p) for p in palavras]
    b = [_norm(r["t"]) for r in reconhecidas]
    casadas = sum(bl.size for bl in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks())
    return casadas / max(1, len(a))


def _silencios(arquivo) -> list[tuple[float, float]]:
    """Trechos de silêncio do áudio (para cortar as cenas sem comer palavra)."""
    r = subprocess.run(["ffmpeg", "-i", str(arquivo), "-af", "silencedetect=noise=-42dB:d=0.12", "-f", "null", "-"],
                       capture_output=True, text=True)
    ini, out = None, []
    for linha in r.stderr.splitlines():
        if "silence_start:" in linha:
            ini = float(linha.split("silence_start:")[1].split()[0])
        elif "silence_end:" in linha and ini is not None:
            out.append((ini, float(linha.split("silence_end:")[1].split()[0])))
            ini = None
    return out


def alinhar(palavras: list[str], reconhecidas: list[dict], total: float) -> list[tuple[float, float]]:
    """Dá início/fim a cada palavra do roteiro, casando com o que o Whisper ouviu; o resto é interpolado."""
    import difflib
    n = len(palavras)
    tempos: list[tuple[float, float] | None] = [None] * n
    if reconhecidas:
        a = [_norm(p) for p in palavras]
        b = [_norm(r["t"]) for r in reconhecidas]
        for bloco in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
            for k in range(bloco.size):
                r = reconhecidas[bloco.b + k]
                tempos[bloco.a + k] = (r["i"], max(r["f"], r["i"] + 0.05))
    # interpola os buracos proporcionalmente ao tamanho das palavras
    i = 0
    while i < n:
        if tempos[i] is not None:
            i += 1
            continue
        j = i
        while j < n and tempos[j] is None:
            j += 1
        ini = tempos[i - 1][1] if i > 0 else 0.0
        fim = tempos[j][0] if j < n else total
        pesos = [len(palavras[k]) + 2 for k in range(i, j)]
        t, soma = ini, sum(pesos)
        for k, w in zip(range(i, j), pesos):
            d = max(fim - ini, 0.0) * w / soma
            tempos[k] = (t, t + min(d, 0.09 * w + 0.1))  # não estica a palavra por cima de uma pausa
            t += d
        i = j
    return tempos  # type: ignore[return-value]


def escolher_estilo(roteiro: dict, cfg_voz: dict) -> str:
    estilos = cfg_voz.get("estilos") or ["calma", "suspense"]
    clima = str(roteiro.get("clima", "")).strip().lower()
    if clima in ESTILOS and (roteiro.get("formato") == "protocolo" or clima == "curioso"):
        return clima
    return clima if clima in estilos else cfg_voz.get("estilo_padrao", estilos[-1])


def narrar_roteiro(roteiro: dict, cfg: dict, pasta: Path) -> list[dict]:
    """Narra o episódio num pedido só (economiza a cota grátis), alinha as palavras e corta por cena."""
    from .voz import _tratar
    from .util import duracao
    cfg_voz = cfg["voz"]
    voz = roteiro.get("voz") or cfg_voz.get("gemini_voz", "Enceladus")   # cada canal pode ter a sua voz
    import os
    if roteiro.get("canal") == "esfr" and os.environ.get("GEMINI_API_KEY_ESE", "").strip():
        os.environ["GEMINI_API_KEY"] = os.environ["GEMINI_API_KEY_ESE"]     # cota de voz separada do canal de terror
    estilo = escolher_estilo(roteiro, cfg_voz)
    roteiro["_voz"] = f"{voz} ({estilo})"
    pasta.mkdir(parents=True, exist_ok=True)
    cenas = [c["narracao"].strip() for c in roteiro["cenas"]]
    completo = pasta / "narracao_completa.wav"
    log(f"Narração com a voz {voz}, estilo {estilo} (clima do episódio)")
    ritmo = float(roteiro.get("ritmo") or cfg_voz.get("gemini_ritmo") or 1.0)   # 1.2 = 20% mais rápido
    palavras, dono = [], []
    for i, texto in enumerate(cenas):
        for p in texto.split():
            palavras.append(p)
            dono.append(i)
    # até 3 tomadas: fica com a que o Whisper entende melhor (fala embolada ou palavra comida = nota baixa)
    melhor = None
    for tomada in range(3):
        bruto = pasta / f"narracao_bruta_{tomada}.wav"
        candidato = pasta / f"narracao_{tomada}.wav"
        try:
            sintetizar(" ".join(cenas), bruto, voz, estilo)
        except Exception as e:
            if melhor is None:
                raise
            log(f"Tomada {tomada + 1} falhou ({e}); fico com a melhor até aqui")
            break
        # o Gemini às vezes deixa silêncios enormes entre frases: encurta qualquer pausa para no máximo ~0,6 s
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(bruto), "-af",
                        "silenceremove=start_periods=1:start_threshold=-50dB:stop_periods=-1:stop_duration=0.55:"
                        "stop_threshold=-50dB" + (f",atempo={ritmo:.3f}" if abs(ritmo - 1) > 0.01 else ""),
                        str(candidato)], check=True)
        ouvidas = _tempos_whisper(candidato)
        nota = _nota_fala(palavras, ouvidas)
        log(f"Tomada {tomada + 1}: {duracao(candidato):.1f}s, o Whisper entendeu {nota:.0%} do texto")
        if melhor is None or nota > melhor[0]:
            melhor = (nota, candidato, ouvidas)
        if nota >= 0.96:
            break
    nota, escolhido, ouvidas = melhor
    shutil.copy(escolhido, completo)
    total = duracao(completo)
    tempos = alinhar(palavras, ouvidas, total)
    log(f"Alinhamento: {len(tempos)} palavras, áudio de {total:.1f}s (tomada com {nota:.0%})")
    silencios = _silencios(completo)

    # corte entre cenas: no meio do silêncio entre a última palavra de uma e a primeira da próxima
    primeiras = [dono.index(i) for i in range(len(cenas))]
    cortes = [0.0]
    for i in range(1, len(cenas)):
        fim_ant, ini_prox = tempos[primeiras[i] - 1][1], tempos[primeiras[i]][0]
        alvo = (fim_ant + ini_prox) / 2
        # o corte cai sempre num silêncio de verdade perto dali (nunca no meio de uma palavra)
        perto = [(abs((a + b) / 2 - alvo), (a + b) / 2) for a, b in silencios if abs((a + b) / 2 - alvo) < 0.9]
        if perto:
            alvo = min(perto)[1]
        cortes.append(max(cortes[-1] + 0.2, alvo))
    cortes.append(total)

    resultado = []
    for i in range(len(cenas)):
        destino = pasta / f"voz_{i:02d}.mp3"
        ini, fim = cortes[i], cortes[i + 1]
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(completo), "-ss", f"{ini:.3f}", "-to", f"{fim:.3f}",
                        "-ac", "1", "-b:a", "160k", str(destino)], check=True)
        _tratar(destino, cfg_voz.get("gemini_efeito", "normalizar"))
        pals = [{"texto": palavras[k], "inicio": max(tempos[k][0] - ini, 0.0), "fim": max(tempos[k][1] - ini, 0.01)}
                for k in range(len(palavras)) if dono[k] == i]
        resultado.append({"arquivo": destino, "duracao": duracao(destino), "palavras": pals})
    return resultado


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


def _teste_narracao(voz: str) -> None:
    """Narra um mini-roteiro de 3 cenas e mostra os tempos (confere o alinhamento das legendas)."""
    from . import telegram
    from .voz_clone import AMOSTRA
    import json as _json
    frases = AMOSTRA.split(". ")
    roteiro = {"clima": "suspense", "cenas": [{"narracao": ". ".join(frases[:3]) + "."},
                                              {"narracao": ". ".join(frases[3:5]) + "."},
                                              {"narracao": ". ".join(frases[5:])}]}
    cfg = {"voz": {"gemini_voz": voz, "estilos": ["calma", "suspense"]}}
    res = narrar_roteiro(roteiro, cfg, Path("trabalho/teste_narracao"))
    for i, r in enumerate(res):
        print(f"cena {i}: {r['duracao']:.2f}s", _json.dumps(r["palavras"][:4] + r["palavras"][-2:], ensure_ascii=False))
        telegram.enviar_audio(r["arquivo"], f"Teste de corte: cena {i + 1} ({r['duracao']:.1f}s)")


if __name__ == "__main__":
    if "--narracao" in sys.argv:
        _teste_narracao(sys.argv[sys.argv.index("--voz") + 1] if "--voz" in sys.argv else "Enceladus")
    elif "--teste" in sys.argv:
        voz = sys.argv[sys.argv.index("--voz") + 1] if "--voz" in sys.argv else "Enceladus"
        _teste(voz)
