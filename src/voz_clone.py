"""Voz do canal clonada a partir da gravação do dono (assets/voz/referencia.wav.enc, criptografada).

A gravação fica criptografada no repositório (que é público); a chave fica no segredo VOZ_CHAVE do GitHub.
A fala é gerada na GPU grátis do Kaggle com o Chatterbox Multilingual (licença MIT).

Teste (manda as amostras no Telegram):
    python -m src.voz_clone --teste
"""
import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

from . import kaggle_clipes as K
from .util import RAIZ, log

REF_CRIPTO = RAIZ / "assets" / "voz" / "referencia.wav.enc"
SCRIPT = RAIZ / "src" / "voz_kaggle.py"
KERNEL, DATASET = "terror-bot-voz", "terror-bot-voz-entrada"

AMOSTRA = ("Você está sozinho em casa. Já passa das duas da manhã... e você escuta uma gaveta se fechando lá "
           "embaixo. Ninguém deveria estar ali. Você desce devagar, degrau por degrau. Na cozinha, encontra um "
           "prato lavado e um copo ainda molhado. Opção A: chamar a polícia. Opção B: subir e se trancar no "
           "quarto. Comente A ou B.")


def decifrar(destino: Path) -> Path:
    chave = os.environ.get("VOZ_CHAVE", "").strip()
    if not chave:
        raise RuntimeError("Falta o segredo VOZ_CHAVE no GitHub (a chave que decifra a gravação da voz).")
    r = subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-in", str(REF_CRIPTO),
                        "-out", str(destino), "-pass", f"pass:{chave}"], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("Não consegui decifrar a gravação: confira se o VOZ_CHAVE foi colado exatamente igual.")
    return destino


def gerar_falas(textos: list, pasta: Path) -> dict:
    entrada = pasta / "entrada"
    shutil.rmtree(entrada, ignore_errors=True)
    entrada.mkdir(parents=True)
    decifrar(entrada / "referencia.wav")
    (entrada / "textos.json").write_text(json.dumps(textos, ensure_ascii=False, indent=2))
    log("Enviando a referência da voz para o Kaggle (dataset privado)...")
    K.enviar_dataset(entrada, DATASET)
    (entrada / "referencia.wav").unlink()             # não deixa a voz decifrada no disco
    K.rodar_kernel(espera_max_min=120, SCRIPT=SCRIPT, KERNEL=KERNEL, DATASET=DATASET)
    return K.baixar(pasta / "saida", KERNEL)


def _teste():
    from . import telegram
    pasta = RAIZ / "trabalho" / "teste_voz"
    textos = [
        {"id": "1_calma", "texto": AMOSTRA, "exagero": 0.35, "cfg": 0.5},
        {"id": "2_suspense", "texto": AMOSTRA, "exagero": 0.55, "cfg": 0.35},
        {"id": "3_dramatica", "texto": AMOSTRA, "exagero": 0.8, "cfg": 0.3},
    ]
    telegram.enviar_mensagem("Teste da voz do canal começou (sua voz clonada com Chatterbox, na GPU do Kaggle). "
                             "Leva uns 10 a 20 minutos.")
    try:
        rel = gerar_falas(textos, pasta)
    except Exception as e:
        telegram.enviar_mensagem(f"O teste da voz falhou: {e}"[:3500])
        raise
    telegram.enviar_mensagem((f"Amostras da voz prontas. GPU: {rel.get('gpu')}, tempo: {rel.get('minutos_total')} min."
                              + ("\nErros:\n" + "\n".join(rel["erros"]) if rel.get("erros") else "")
                              + "\nOuça as 3 e me diga qual estilo prefere: 1 calma, 2 suspense, 3 dramática.")[:3800])
    for aid, arq in sorted(rel.get("arquivos", {}).items()):
        mp3 = Path(arq).with_suffix(".mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", arq, "-b:a", "160k", str(mp3)], check=False)
        telegram.enviar_audio(mp3 if mp3.exists() else arq, f"Voz do canal — {aid}")
    print(json.dumps(rel, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--teste", action="store_true")
    if ap.parse_args().teste:
        _teste()
