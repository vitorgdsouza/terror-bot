"""Gera clipes animados por IA na GPU grátis do Kaggle (a partir de imagens do próprio vídeo).

Fluxo: monta uma pasta com pedidos.json + imagens -> envia como dataset privado -> dispara o notebook
src/clipes_kaggle.py com GPU -> espera terminar -> baixa clipes/*.mp4 e relatorio.json.

Precisa dos segredos KAGGLE_API_TOKEN e KAGGLE_USERNAME (no GitHub: Settings > Secrets > Actions).

Teste (manda os clipes e o relatório no Telegram):
    python -m src.kaggle_clipes --teste
"""
import argparse
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

from .util import RAIZ, log

DATASET = "terror-bot-entrada"
KERNEL = "terror-bot-clipes"
SCRIPT_KAGGLE = RAIZ / "src" / "clipes_kaggle.py"   # roda no Kaggle, não é importado aqui


def _usuario() -> str:
    u = os.environ.get("KAGGLE_USERNAME", "").strip()
    if not u:
        raise RuntimeError("Falta o segredo KAGGLE_USERNAME (seu nome de usuário do Kaggle).")
    return u


def _kaggle(*args, checar=True) -> str:
    r = subprocess.run(["kaggle", *args], capture_output=True, text=True)
    saida = (r.stdout + r.stderr).strip()
    if "Traceback" in saida and "ModuleNotFoundError" in saida:     # a própria ferramenta do Kaggle quebrou
        raise RuntimeError(f"A ferramenta do Kaggle não abriu: {saida[-400:]}")
    if checar and r.returncode != 0:
        raise RuntimeError(f"kaggle {' '.join(args[:2])} falhou: {saida[-800:]}")
    return saida


def enviar_dataset(pasta: Path) -> None:
    usuario = _usuario()
    (pasta / "dataset-metadata.json").write_text(json.dumps({
        "title": DATASET, "id": f"{usuario}/{DATASET}", "licenses": [{"name": "CC0-1.0"}]}))
    existe = "ready" in _kaggle("datasets", "status", f"{usuario}/{DATASET}", checar=False).lower()
    if existe:
        _kaggle("datasets", "version", "-p", str(pasta), "-m", time.strftime("%Y-%m-%d %H:%M"), "-q")
    else:
        _kaggle("datasets", "create", "-p", str(pasta), "-q")
    for _ in range(60):                               # espera o Kaggle processar os arquivos
        if "ready" in _kaggle("datasets", "status", f"{usuario}/{DATASET}", checar=False).lower():
            return
        time.sleep(10)
    raise RuntimeError("O Kaggle não terminou de processar o dataset de entrada em 10 minutos.")


def _status_kernel(usuario: str) -> str:
    """Só o estado do notebook (ex.: "running", "complete", "error"), sem o resto da frase."""
    st = _kaggle("kernels", "status", f"{usuario}/{KERNEL}", checar=False)
    if 'has status "' in st:
        st = st.split('has status "', 1)[1].split('"', 1)[0]
    return st.lower().replace("kernelworkerstatus.", "")


def rodar_kernel(espera_max_min: int = 300, so_esperar: bool = False) -> None:
    usuario = _usuario()
    pasta = RAIZ / "trabalho" / "kaggle_kernel"
    shutil.rmtree(pasta, ignore_errors=True)
    pasta.mkdir(parents=True)
    shutil.copy(SCRIPT_KAGGLE, pasta / "clipes_kaggle.py")
    (pasta / "kernel-metadata.json").write_text(json.dumps({
        "id": f"{usuario}/{KERNEL}", "title": KERNEL, "code_file": "clipes_kaggle.py",
        "language": "python", "kernel_type": "script", "is_private": True,
        "enable_gpu": True, "enable_internet": True,
        "dataset_sources": [f"{usuario}/{DATASET}"], "competition_sources": [], "kernel_sources": []}))
    if not so_esperar:
        try:
            log(_kaggle("kernels", "push", "-p", str(pasta), "--accelerator", "NvidiaTeslaT4"))
        except RuntimeError as e:                     # versão da ferramenta sem a opção: usa o pedido do metadata
            if "accelerator" not in str(e).lower():
                raise
            log(_kaggle("kernels", "push", "-p", str(pasta)))
        time.sleep(60)
    inicio = time.time()
    while time.time() - inicio < espera_max_min * 60:
        st = _status_kernel(usuario)
        if st == "complete":
            log("Kaggle terminou.")
            return
        if st in ("error", "cancelacknowledged", "cancelrequested"):
            raise RuntimeError(f"O notebook do Kaggle falhou (estado: {st}). Veja o log em kaggle.com/code.")
        log(f"Kaggle: {st} ({(time.time() - inicio) / 60:.0f} min)")
        time.sleep(60)
    raise RuntimeError(f"O Kaggle passou de {espera_max_min} minutos.")


def baixar(destino: Path) -> dict:
    usuario = _usuario()
    shutil.rmtree(destino, ignore_errors=True)
    destino.mkdir(parents=True)
    _kaggle("kernels", "output", f"{usuario}/{KERNEL}", "-p", str(destino))
    rel = next(destino.rglob("relatorio.json"), None)
    relatorio = json.loads(rel.read_text()) if rel else {"erros": ["relatorio.json não veio"]}
    relatorio["arquivos"] = {p.stem: str(p) for p in destino.rglob("*.mp4")}
    return relatorio


def gerar_clipes(pedidos: list, imagens: dict, pasta: Path, so_esperar: bool = False) -> dict:
    """pedidos: [{"id", "prompt", "segundos"}], imagens: {id: caminho}. Devolve o relatório com os .mp4."""
    if so_esperar:                                   # o notebook já está rodando: só espera e baixa
        rodar_kernel(so_esperar=True)
        return baixar(pasta / "saida")
    entrada = pasta / "entrada"
    shutil.rmtree(entrada, ignore_errors=True)
    entrada.mkdir(parents=True)
    lista = []
    for p in pedidos:
        nome = f"{p['id']}.png"
        shutil.copy(imagens[p["id"]], entrada / nome)
        lista.append({**p, "imagem": nome})
    (entrada / "pedidos.json").write_text(json.dumps(lista, ensure_ascii=False, indent=2))
    log("Enviando imagens para o Kaggle...")
    enviar_dataset(entrada)
    log("Disparando a GPU do Kaggle...")
    rodar_kernel()
    return baixar(pasta / "saida")


def _teste(so_esperar: bool = False):
    """Renderiza 3 quadros do próprio vídeo, anima no Kaggle e manda tudo no Telegram."""
    from . import telegram
    from .animacao import quadro
    pasta = RAIZ / "trabalho" / "teste_kaggle"
    pasta.mkdir(parents=True, exist_ok=True)
    P = lambda pose, acao="parado", pos="centro", tam="medio": {"pose": pose, "acao": acao, "posicao": pos, "tamanho": tam}
    cenas = {
        "casa": ({"cenario": "casa_fora", "personagem": None, "ameaca": None, "efeito": "nenhum", "camera": "parada"},
                 "slow cinematic camera push in toward the house at night, the warm lit window flickers softly, "
                 "leaves and bushes sway gently in the wind, static house"),
        "corredor": ({"cenario": "corredor", "personagem": P("costas"),
                      "ameaca": {"tipo": "abismo", "acao": "parada", "posicao": "centro", "tamanho": "longe"},
                      "efeito": "nenhum", "camera": "parada"},
                     "a boy in a green hoodie stands still seen from behind in a dark hallway, at the far end a tall "
                     "black figure slowly tilts its head, wall lamps flicker, very subtle motion, static camera"),
        "sala": ({"cenario": "sala", "personagem": P("medo", "parado", "esquerda"), "ameaca": None,
                  "efeito": "nenhum", "camera": "parada"},
                 "a scared cartoon boy breathes nervously and looks around the dark living room, the tv screen "
                 "flickers with static, subtle natural motion, static camera"),
    }
    imagens, pedidos = {}, []
    for i, (cid, (cena, prompt)) in enumerate(cenas.items()):
        img = quadro(cena, 1.0, 4.0, "homem", 24)
        caminho = pasta / f"{cid}.png"
        img.save(caminho)
        imagens[cid] = caminho
        pedidos.append({"id": cid, "prompt": prompt, "segundos": 4})
    if not so_esperar:
        telegram.enviar_mensagem("Teste do Kaggle começou: 3 clipes de 4 s com IA aberta (Wan 2.2) na GPU grátis. "
                                 "Pode levar de 30 a 90 minutos.")
    else:
        telegram.enviar_mensagem("Teste do Kaggle: esperando o notebook que já está rodando terminar...")
    try:
        rel = gerar_clipes(pedidos, imagens, pasta, so_esperar)
    except Exception as e:
        telegram.enviar_mensagem(f"O teste do Kaggle falhou: {e}"[:3500])
        raise
    resumo = (f"Teste do Kaggle terminou.\nModelo: {rel.get('modelo')}\nGPU: {rel.get('gpu')}\n"
              f"Tempo total: {rel.get('minutos_total')} min\n"
              + "\n".join(f"- {c['id']}: {c['minutos']} min" for c in rel.get("clipes", []))
              + ("\nErros:\n" + "\n".join(rel["erros"]) if rel.get("erros") else ""))
    telegram.enviar_mensagem(resumo[:3800])
    for cid, arq in rel.get("arquivos", {}).items():
        try:
            telegram.enviar_video(Path(arq), f"Clipe IA (Kaggle): {cid}")
        except Exception as e:
            telegram.enviar_mensagem(f"Não consegui enviar o clipe {cid}: {e}")
    print(json.dumps(rel, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--teste", action="store_true")
    ap.add_argument("--so-esperar", action="store_true", help="não reenvia; espera o notebook que já está rodando")
    a = ap.parse_args()
    if a.teste:
        _teste(a.so_esperar)
