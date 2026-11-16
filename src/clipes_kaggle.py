"""Roda DENTRO do Kaggle (GPU grátis): anima imagens com um modelo aberto de imagem-para-vídeo.

Entrada: o dataset "terror-bot-entrada" com pedidos.json e as imagens.
  pedidos.json = [{"id": "casa", "imagem": "casa.png", "prompt": "...", "segundos": 5}, ...]
Saída (/kaggle/working): clipes/<id>.mp4 e relatorio.json (modelo usado, tempo de cada clipe, erros).

Tenta primeiro o Wan 2.2 TI2V-5B (melhor movimento) e, se falhar, o LTX-Video (mais leve).
"""
import json
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path

INICIO = time.time()
SAIDA = Path("/kaggle/working")
(SAIDA / "clipes").mkdir(parents=True, exist_ok=True)
relatorio = {"modelo": None, "clipes": [], "erros": [], "gpu": None}


def salvar():
    relatorio["minutos_total"] = round((time.time() - INICIO) / 60, 1)
    (SAIDA / "relatorio.json").write_text(json.dumps(relatorio, ensure_ascii=False, indent=2))


def log(msg):
    print(f"[{(time.time() - INICIO) / 60:5.1f} min] {msg}", flush=True)


subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "diffusers>=0.35", "transformers", "accelerate",
                "ftfy", "imageio", "imageio-ffmpeg", "sentencepiece"], check=False)

import torch  # noqa: E402
from PIL import Image  # noqa: E402

relatorio["gpu"] = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "sem GPU"
log(f"GPU: {relatorio['gpu']}")

entrada = next(Path("/kaggle/input").rglob("pedidos.json"))
pasta_in = entrada.parent
pedidos = json.loads(entrada.read_text())
log(f"{len(pedidos)} pedidos em {pasta_in}")

NEGATIVO = ("photorealistic, 3d render, realistic, blurry, deformed, distorted face, extra limbs, morphing, "
            "text, watermark, low quality, jitter")
ESTILO = " 2D cartoon animation, flat colors, clean outlines, consistent character design, smooth subtle motion."
W, H = 480, 832           # vertical, múltiplos de 32


def preparar(img_path):
    im = Image.open(img_path).convert("RGB")
    e = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * e + 0.5), int(im.height * e + 0.5)), Image.LANCZOS)
    x0, y0 = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x0, y0, x0 + W, y0 + H))


def com_wan():
    from diffusers import AutoencoderKLWan, WanImageToVideoPipeline
    mid = "Wan-AI/Wan2.2-TI2V-5B-Diffusers"
    dtype = torch.bfloat16
    vae = AutoencoderKLWan.from_pretrained(mid, subfolder="vae", torch_dtype=torch.float32)
    pipe = WanImageToVideoPipeline.from_pretrained(mid, vae=vae, torch_dtype=dtype)
    pipe.enable_model_cpu_offload()
    try:
        pipe.vae.enable_tiling()
    except Exception:
        pass

    def gerar(img, prompt, segundos):
        frames = min(121, int(segundos * 24) // 4 * 4 + 1)
        return pipe(image=img, prompt=prompt + ESTILO, negative_prompt=NEGATIVO, height=H, width=W,
                    num_frames=frames, guidance_scale=5.0, num_inference_steps=30).frames[0], 24
    return "Wan2.2-TI2V-5B", gerar


def com_ltx():
    from diffusers import LTXImageToVideoPipeline
    pipe = LTXImageToVideoPipeline.from_pretrained("Lightricks/LTX-Video", torch_dtype=torch.bfloat16)
    pipe.enable_model_cpu_offload()

    def gerar(img, prompt, segundos):
        frames = min(161, int(segundos * 24) // 8 * 8 + 1)
        return pipe(image=img, prompt=prompt + ESTILO, negative_prompt=NEGATIVO, height=H, width=W,
                    num_frames=frames, num_inference_steps=40, decode_timestep=0.05,
                    image_cond_noise_scale=0.025).frames[0], 24
    return "LTX-Video", gerar


from diffusers.utils import export_to_video  # noqa: E402

gerador = None
for carregar in (com_wan, com_ltx):
    try:
        log(f"Carregando {carregar.__name__}...")
        nome, gerar = carregar()
        # teste rápido para descobrir cedo se o modelo funciona nesta GPU
        gerador = (nome, gerar)
        relatorio["modelo"] = nome
        break
    except Exception as e:
        relatorio["erros"].append(f"{carregar.__name__}: {type(e).__name__}: {e}"[:600])
        log(traceback.format_exc()[-1500:])
        torch.cuda.empty_cache()
salvar()

if gerador:
    nome, gerar = gerador
    for p in pedidos:
        t0 = time.time()
        try:
            img = preparar(pasta_in / p["imagem"])
            frames, fps = gerar(img, p["prompt"], float(p.get("segundos", 5)))
            destino = SAIDA / "clipes" / f"{p['id']}.mp4"
            export_to_video(frames, str(destino), fps=fps)
            relatorio["clipes"].append({"id": p["id"], "minutos": round((time.time() - t0) / 60, 1),
                                        "quadros": len(frames)})
            log(f"Clipe {p['id']} pronto em {(time.time() - t0) / 60:.1f} min")
        except Exception as e:
            relatorio["erros"].append(f"{p['id']}: {type(e).__name__}: {e}"[:600])
            log(traceback.format_exc()[-1500:])
            torch.cuda.empty_cache()
        salvar()
salvar()
log("Fim")
