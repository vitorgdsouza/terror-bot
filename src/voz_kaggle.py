"""Roda DENTRO do Kaggle (GPU grátis): fala textos com a voz do dono do canal (clonagem com Chatterbox Multilingual).

Chatterbox Multilingual (Resemble AI) é aberto e tem licença MIT (permite uso comercial). Cada áudio gerado leva
uma marca d'água inaudível da Resemble que identifica o áudio como sintético.

Entrada: dataset "terror-bot-voz-entrada" com referencia.wav (a voz do dono) e textos.json:
  [{"id": "amostra_calma", "texto": "...", "exagero": 0.4, "cfg": 0.5}, ...]
Saída (/kaggle/working): audios/<id>.wav e relatorio.json.
"""
import json
import subprocess
import sys
import time
import traceback
import urllib.request
from pathlib import Path

INICIO = time.time()
SAIDA = Path("/kaggle/working")
(SAIDA / "audios").mkdir(parents=True, exist_ok=True)
relatorio = {"modelo": "Chatterbox Multilingual", "audios": [], "erros": [], "gpu": None}


def salvar():
    relatorio["minutos_total"] = round((time.time() - INICIO) / 60, 1)
    (SAIDA / "relatorio.json").write_text(json.dumps(relatorio, ensure_ascii=False, indent=2))


def log(msg):
    print(f"[{(time.time() - INICIO) / 60:5.1f} min] {msg}", flush=True)


try:
    urllib.request.urlopen("https://huggingface.co", timeout=15)
    internet = True
except Exception:
    internet = False
gpu = subprocess.run(["nvidia-smi"], capture_output=True).returncode == 0
if not (internet and gpu):
    relatorio["erros"].append("Rodou sem GPU ou sem internet (verifique o telefone no Kaggle).")
    salvar()
    sys.exit(0)

# O pacote chatterbox-tts trava versões antigas (numpy<1.26 etc.) que não existem para o Python do Kaggle.
# Então: instala o chatterbox sem dependências e, uma a uma, só o que ele usa (mantendo o PyTorch do Kaggle).
def pip(*pacotes):
    r = subprocess.run([sys.executable, "-m", "pip", "install", "-q", *pacotes], capture_output=True, text=True)
    if r.returncode != 0:
        relatorio.setdefault("pip_falhas", []).append(f"{' '.join(pacotes)}: {(r.stdout + r.stderr)[-300:]}")
    return r.returncode == 0


pip("--no-deps", "chatterbox-tts")
for pacote in ("transformers==4.46.3", "diffusers==0.29.0", "resemble-perth", "conformer==0.3.2", "s3tokenizer",
               "librosa", "safetensors", "pyloudnorm", "omegaconf", "pykakasi", "spacy-pkuseg"):
    pip(pacote)
v = subprocess.run([sys.executable, "-c", "import torch, transformers; print(torch.__version__, transformers.__version__)"],
                   capture_output=True, text=True)
relatorio["versoes"] = (v.stdout + v.stderr).strip()[-300:]

import torch  # noqa: E402
import torchaudio  # noqa: E402

relatorio["gpu"] = torch.cuda.get_device_name(0)
entrada = next(Path("/kaggle/input").rglob("textos.json"))
textos = json.loads(entrada.read_text())
ref = str(entrada.parent / "referencia.wav")

try:
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    modelo = ChatterboxMultilingualTTS.from_pretrained(device="cuda")
    log("Modelo carregado")
except Exception as e:
    relatorio["erros"].append(f"carregar modelo: {type(e).__name__}: {e}"[:800])
    relatorio["detalhe"] = traceback.format_exc()[-1500:]
    log(traceback.format_exc()[-2000:])
    salvar()
    sys.exit(0)

for t in textos:
    t0 = time.time()
    try:
        wav = modelo.generate(t["texto"], language_id="pt", audio_prompt_path=ref,
                              exaggeration=float(t.get("exagero", 0.5)), cfg_weight=float(t.get("cfg", 0.5)),
                              temperature=float(t.get("temperatura", 0.8)))
        destino = SAIDA / "audios" / f"{t['id']}.wav"
        torchaudio.save(str(destino), wav.cpu(), modelo.sr)
        relatorio["audios"].append({"id": t["id"], "segundos_gerados": round(wav.shape[-1] / modelo.sr, 1),
                                    "segundos_gastos": round(time.time() - t0, 1)})
        log(f"{t['id']} pronto")
    except Exception as e:
        relatorio["erros"].append(f"{t['id']}: {type(e).__name__}: {e}"[:800])
        log(traceback.format_exc()[-2000:])
    salvar()
salvar()
log("Fim")
