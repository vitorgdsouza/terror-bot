"""Narração com a voz do dono do canal (clonada no Kaggle com o Chatterbox, ver src/voz_clone.py).

Usada no formato "real" (ou em qualquer roteiro com "voz": "minha"). Gera um áudio por cena, tira os silêncios das
pontas, encurta pausas longas, aplica o ritmo e alinha cada palavra com o Whisper para as legendas.
"""
import subprocess
from pathlib import Path

from .util import duracao, log


def narrar_roteiro_minha(roteiro: dict, cfg: dict, pasta: Path) -> list[dict]:
    from .voz import _tratar
    from .voz_clone import gerar_falas
    from .voz_gemini import _tempos_whisper, alinhar
    conf = {"exagero": 0.45, "cfg": 0.45, **(cfg["voz"].get("minha") or {})}
    pasta.mkdir(parents=True, exist_ok=True)
    cenas = [c["narracao"].strip() for c in roteiro["cenas"]]
    textos = [{"id": f"c{i:02d}", "texto": t, "exagero": conf["exagero"], "cfg": conf["cfg"]} for i, t in enumerate(cenas)]
    log(f"Narração com a sua voz (Kaggle): {len(textos)} falas")
    rel = gerar_falas(textos, pasta / "kaggle")
    arquivos = rel.get("arquivos", {})
    faltando = [t["id"] for t in textos if t["id"] not in arquivos]
    if faltando:
        raise RuntimeError(f"o Kaggle não devolveu as falas {faltando[:5]} (erros: {rel.get('erros')})")
    ritmo = float(roteiro.get("ritmo_minha") or conf.get("ritmo") or 1.0)
    resultado = []
    for i, texto in enumerate(cenas):
        bruto = Path(arquivos[f"c{i:02d}"])
        limpo = pasta / f"voz_{i:02d}.wav"
        filtro = ("silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                  "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                  "silenceremove=stop_periods=-1:stop_duration=0.5:stop_threshold=-45dB")
        if abs(ritmo - 1) > 0.01:
            filtro += f",atempo={ritmo:.3f}"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(bruto), "-af", filtro, "-ac", "1", str(limpo)],
                       check=True)
        destino = pasta / f"voz_{i:02d}.mp3"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(limpo), "-b:a", "160k", str(destino)], check=True)
        _tratar(destino, cfg["voz"].get("minha_efeito", "normalizar"))
        total = duracao(destino)
        palavras_txt = texto.split()
        tempos = alinhar(palavras_txt, _tempos_whisper(limpo), total)
        resultado.append({"arquivo": destino, "duracao": total,
                          "palavras": [{"texto": p, "inicio": a, "fim": b} for p, (a, b) in zip(palavras_txt, tempos)]})
    roteiro["_voz"] = "sua voz (clonada)"
    return resultado
