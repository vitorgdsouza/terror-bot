"""Ferramentas de linha de comando usadas pelo agente diretor (Claude Code).

Todas trabalham na pasta trabalho/. Exemplos:
    python -m src.ferramentas contexto              # mostra a configuração da série e o histórico
    python -m src.ferramentas validar               # confere trabalho/roteiro.json
    python -m src.ferramentas imagens               # gera as imagens que ainda faltam
    python -m src.ferramentas folha                 # junta todas as cenas em trabalho/folha.jpg
    python -m src.ferramentas imagem 3 --tentativa 1  # refaz o cenário da cena 3 com outra semente
    python -m src.ferramentas recompor 3            # reaplica personagem/ameaça da cena 3 (sem gerar cenário)
    python -m src.ferramentas narracao              # gera a narração de todas as cenas
    python -m src.ferramentas montar                # monta trabalho/video/video_final.mp4
    python -m src.ferramentas quadros               # quadros do vídeo final em trabalho/quadros.jpg
    python -m src.ferramentas enviar --nota "..."   # manda para o Telegram e salva no histórico
"""
import argparse
import json
import sys
import time
from pathlib import Path

from .util import RAIZ, carregar_config, carregar_historico, duracao, log, rodar, salvar_no_historico

TRAB = RAIZ / "trabalho"
ROTEIRO = TRAB / "roteiro.json"
IMGS = TRAB / "imagens"
VOZES = TRAB / "vozes.json"
FINAL = TRAB / "video" / "video_final.mp4"
ULTIMO_PEDIDO = TRAB / ".ultimo_pedido_imagem"
PALAVRAS_POR_SEGUNDO = 2.3


def _roteiro() -> dict:
    if not ROTEIRO.exists():
        sys.exit("ERRO: trabalho/roteiro.json não existe. Escreva o roteiro primeiro.")
    return json.loads(ROTEIRO.read_text(encoding="utf-8"))


def contexto(_):
    cfg = carregar_config()
    print("=== CONFIGURAÇÃO DA SÉRIE (config/serie.json) ===")
    print(json.dumps(cfg, ensure_ascii=False, indent=2))
    from .personagem import escolher_protagonista
    quem = escolher_protagonista(cfg, carregar_historico())
    info = cfg.get("protagonistas", {}).get(quem, {})
    print(f"\n=== PROTAGONISTA DESTE VÍDEO: {quem} ({info.get('descricao', '')}) ===")
    print(f'Coloque "protagonista": "{quem}" no roteiro.json e escreva os adjetivos de "você" no {info.get("genero", "masculino")}.')
    hist = carregar_historico()[-40:]
    print("\n=== HISTÓRIAS JÁ PUBLICADAS (não repetir) ===")
    print("\n".join(f"- {h['titulo']} ({h['tema'][:60]})" for h in hist) or "(nenhuma ainda)")


def validar(_):
    from .roteiro import MOVIMENTOS, _validar
    cfg = carregar_config()
    r = _roteiro()
    try:
        _validar(r, cfg)
    except (ValueError, KeyError) as e:
        sys.exit(f"ROTEIRO INVÁLIDO: {e}")
    if r.get("protagonista") not in ("homem", "mulher"):
        from .personagem import escolher_protagonista
        r["protagonista"] = escolher_protagonista(cfg, carregar_historico())
    ROTEIRO.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    palavras = sum(len(c["narracao"].split()) for c in r["cenas"])
    seg = palavras / PALAVRAS_POR_SEGUNDO
    avisos = []
    if len(r["cenas"]) != cfg["numero_de_cenas"]:
        avisos.append(f"tem {len(r['cenas'])} cenas; a série pede {cfg['numero_de_cenas']}")
    alvo = cfg["duracao_alvo_segundos"]
    if not 0.75 * alvo <= seg <= 1.25 * alvo:
        avisos.append(f"duração estimada {seg:.0f}s está longe do alvo de {alvo}s")
    if cfg.get("formato") == "segunda_pessoa_com_escolha" and "comente a ou b" not in r["cenas"][-1]["narracao"].lower():
        avisos.append('a última cena deve terminar com "Comente A ou B."')
    from .personagem import AMEACAS, POSES, POSICOES, TAMANHOS
    sem_prot = sum(1 for c in r["cenas"] if not c.get("personagem"))
    print(f"OK: \"{r['titulo']}\" | protagonista: {r['protagonista']} | {len(r['cenas'])} cenas | {palavras} palavras | ~{seg:.0f}s narrados")
    print(f"Cenas sem o protagonista: {sem_prot} | com ameaça: {sum(1 for c in r['cenas'] if c.get('ameaca'))}")
    print(f"Valores válidos -> pose: {', '.join(POSES)} | ameaça: {', '.join(AMEACAS)} | posicao: {', '.join(POSICOES)} "
          f"| tamanho: {', '.join(TAMANHOS)} | movimento: {', '.join(MOVIMENTOS)}")
    print("\n".join(f"AVISO: {a}" for a in avisos) or "Sem avisos.")


def _respeitar_limite():
    from .imagens import ESPERA_ENTRE_IMAGENS
    if ULTIMO_PEDIDO.exists():
        falta = ESPERA_ENTRE_IMAGENS - (time.time() - float(ULTIMO_PEDIDO.read_text()))
        if falta > 0:
            time.sleep(falta)
    ULTIMO_PEDIDO.write_text(str(time.time()))


def _previa(origem: Path, destino: Path, largura: int = 360):
    rodar(["ffmpeg", "-y", "-i", str(origem), "-vf", f"scale={largura}:-2", "-q:v", "4", str(destino)])


def _gerar_cena(r: dict, cfg: dict, i: int, tentativa: int) -> bool:
    from .imagens import gerar_imagem, montar_prompt, placeholder, semente_do_video
    fundo = IMGS / f"fundo_{i:02d}.jpg"
    semente = semente_do_video(r["titulo"]) + i + 1000 * tentativa
    _respeitar_limite()
    log(f"Cena {i} (tentativa {tentativa}, semente {semente})")
    ok = gerar_imagem(montar_prompt(r["cenas"][i], r, cfg), fundo, semente)
    marca = IMGS / f"cena_{i:02d}.falhou"
    if ok:
        marca.unlink(missing_ok=True)
    else:
        placeholder(fundo)
        marca.write_text("1")
        log(f"  FALHOU: cena {i} ficou com fundo escuro provisório; tente de novo mais tarde")
    _compor_cena(r, i)
    return ok


def _compor_cena(r: dict, i: int):
    from .personagem import compor
    destino = IMGS / f"cena_{i:02d}.jpg"
    compor(IMGS / f"fundo_{i:02d}.jpg", r["cenas"][i], destino, r.get("protagonista", "homem"))
    _previa(destino, IMGS / f"previa_{i:02d}.jpg")


def recompor(a):
    """Reaplica personagem/ameaça (depois de mudar pose, posição ou tamanho no roteiro) sem gerar o cenário de novo."""
    r = _roteiro()
    alvo = range(len(r["cenas"])) if a.cena is None else [a.cena]
    for i in alvo:
        if not (IMGS / f"fundo_{i:02d}.jpg").exists():
            sys.exit(f"ERRO: a cena {i} ainda não tem cenário. Rode 'imagens' antes.")
        _compor_cena(r, i)
    print("Recomposto. Rode 'folha' para conferir.")


def imagem(a):
    r, cfg = _roteiro(), carregar_config()
    if not 0 <= a.cena < len(r["cenas"]):
        sys.exit(f"ERRO: a cena deve ir de 0 a {len(r['cenas']) - 1}")
    _gerar_cena(r, cfg, a.cena, a.tentativa)
    print(f"Prévia: trabalho/imagens/previa_{a.cena:02d}.jpg")


def imagens(_):
    r, cfg = _roteiro(), carregar_config()
    for i in range(len(r["cenas"])):
        if (IMGS / f"fundo_{i:02d}.jpg").exists() and not (IMGS / f"cena_{i:02d}.falhou").exists():
            continue
        _gerar_cena(r, cfg, i, 0)
    falhas = sorted(p.stem for p in IMGS.glob("*.falhou"))
    print("Todas as imagens geradas." if not falhas else f"Ainda com falha: {', '.join(falhas)}")


def folha(_):
    """Junta as prévias numa grade numerada (para avaliar todas de uma vez)."""
    r = _roteiro()
    n = len(r["cenas"])
    entradas, filtros = [], []
    for i in range(n):
        p = IMGS / f"previa_{i:02d}.jpg"
        if not p.exists():
            sys.exit(f"ERRO: falta a imagem da cena {i}. Rode 'imagens' antes.")
        entradas += ["-i", str(p)]
        filtros.append(f"[{i}:v]scale=240:420,drawtext=text='{i}':x=10:y=10:fontsize=36:"
                       f"fontcolor=yellow:box=1:boxcolor=black@0.7[c{i}]")
    colunas = 7 if n > 7 else n
    linhas = -(-n // colunas)
    layout = "|".join(f"{(i % colunas) * 240}_{(i // colunas) * 420}" for i in range(n))
    filtros.append("".join(f"[c{i}]" for i in range(n)) +
                   f"xstack=inputs={n}:layout={layout}:fill=black[out]" if n > 1 else "[c0]null[out]")
    rodar(["ffmpeg", "-y", *entradas, "-filter_complex", ";".join(filtros),
           "-map", "[out]", "-frames:v", "1", "-q:v", "4", str(TRAB / "folha.jpg")])
    print(f"Folha com {n} cenas ({colunas}x{linhas}): trabalho/folha.jpg")


def narracao(_):
    from .voz import gerar_narracao
    r, cfg = _roteiro(), carregar_config()
    vozes = gerar_narracao(r, cfg, TRAB / "audio")
    VOZES.write_text(json.dumps([{**v, "arquivo": str(v["arquivo"])} for v in vozes],
                                ensure_ascii=False), encoding="utf-8")
    total = sum(v["duracao"] for v in vozes)
    print(f"Narração pronta: {total:.0f}s no total")
    for i, v in enumerate(vozes):
        print(f"  cena {i}: {v['duracao']:.1f}s")


def montar(_):
    from .montagem import montar_video
    r, cfg = _roteiro(), carregar_config()
    if not VOZES.exists():
        sys.exit("ERRO: rode 'narracao' antes de montar.")
    vozes = [{**v, "arquivo": Path(v["arquivo"])} for v in json.loads(VOZES.read_text(encoding="utf-8"))]
    imgs = [IMGS / f"cena_{i:02d}.jpg" for i in range(len(r["cenas"]))]
    falt = [str(p.name) for p in imgs if not p.exists()]
    if falt:
        sys.exit(f"ERRO: faltam imagens: {', '.join(falt)}")
    video = montar_video(r, imgs, vozes, cfg, TRAB / "video")
    print(f"Vídeo: {video} ({duracao(video):.0f}s, {video.stat().st_size / 1e6:.1f} MB)")


def quadros(_):
    if not FINAL.exists():
        sys.exit("ERRO: o vídeo final ainda não existe.")
    d = duracao(FINAL)
    rodar(["ffmpeg", "-y", "-i", str(FINAL), "-vf", f"fps=8/{d:.2f},scale=270:-2,tile=4x2",
           "-frames:v", "1", "-q:v", "4", str(TRAB / "quadros.jpg")])
    print("8 quadros do vídeo final: trabalho/quadros.jpg")


def enviar(a):
    from . import telegram
    r, cfg = _roteiro(), carregar_config()
    if not FINAL.exists():
        sys.exit("ERRO: o vídeo final ainda não existe.")
    hashtags = " ".join(dict.fromkeys(r.get("hashtags", []) + cfg["hashtags_fixas"]))
    legenda = f"{r['titulo']}\n\n{r.get('legenda_post', '')}\n\n{hashtags}"
    (TRAB / "legenda_do_post.txt").write_text(legenda, encoding="utf-8")
    telegram.enviar_video(FINAL, legenda)
    telegram.enviar_mensagem(f"Legenda para copiar e colar:\n\n{legenda}")
    if a.nota:
        telegram.enviar_mensagem(f"Nota do diretor (Claude):\n{a.nota}")
    salvar_no_historico(r["titulo"], r.get("tema", ""), r.get("protagonista", ""))
    (TRAB / "ENVIADO").write_text("ok")
    print("Enviado para o Telegram e salvo no histórico.")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("contexto").set_defaults(f=contexto)
    sub.add_parser("validar").set_defaults(f=validar)
    s = sub.add_parser("imagem")
    s.add_argument("cena", type=int)
    s.add_argument("--tentativa", type=int, default=1, help="mude o número para obter outra semente")
    s.set_defaults(f=imagem)
    sub.add_parser("imagens").set_defaults(f=imagens)
    s = sub.add_parser("recompor")
    s.add_argument("cena", type=int, nargs="?", default=None)
    s.set_defaults(f=recompor)
    sub.add_parser("folha").set_defaults(f=folha)
    sub.add_parser("narracao").set_defaults(f=narracao)
    sub.add_parser("montar").set_defaults(f=montar)
    sub.add_parser("quadros").set_defaults(f=quadros)
    s = sub.add_parser("enviar")
    s.add_argument("--nota", default="")
    s.set_defaults(f=enviar)
    a = p.parse_args()
    TRAB.mkdir(exist_ok=True)
    a.f(a)


if __name__ == "__main__":
    main()
