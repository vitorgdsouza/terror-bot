"""Ferramentas de linha de comando usadas pelo agente diretor (Claude Code).

Todas trabalham na pasta trabalho/. Exemplos:
    python -m src.ferramentas contexto        # configuração da série, protagonista da vez e histórico
    python -m src.ferramentas validar         # confere e corrige trabalho/roteiro.json
    python -m src.ferramentas imagens         # gera a ilustração de cada plano (pago; reaproveita as já feitas)
    python -m src.ferramentas imagens --refazer 3 7   # gera de novo só os planos 3 e 7
    python -m src.ferramentas previa          # um quadro de cada cena em trabalho/previa.jpg (instantâneo)
    python -m src.ferramentas previa 4        # 3 momentos da cena 4 em trabalho/previa_cena.jpg
    python -m src.ferramentas narracao        # gera a narração de todas as cenas
    python -m src.ferramentas montar          # anima e monta trabalho/video/video_final.mp4
    python -m src.ferramentas quadros         # 8 quadros do vídeo final em trabalho/quadros.jpg
    python -m src.ferramentas enviar --nota "..."   # manda para o Telegram e salva no histórico
"""
import argparse
import json
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw

from .util import RAIZ, carregar_config, carregar_historico, duracao, rodar, salvar_no_historico

TRAB = RAIZ / "trabalho"
ROTEIRO = TRAB / "roteiro.json"
VOZES = TRAB / "vozes.json"
FINAL = TRAB / "video" / "video_final.mp4"
PALAVRAS_POR_SEGUNDO = 2.3


def _roteiro() -> dict:
    if not ROTEIRO.exists():
        sys.exit("ERRO: trabalho/roteiro.json não existe. Escreva o roteiro primeiro.")
    return json.loads(ROTEIRO.read_text(encoding="utf-8"))


def _catalogo() -> str:
    from . import animacao as A
    return (f"cenario: {', '.join(A.CENARIOS)}\n"
            f"personagem.pose: {', '.join(A.POSES)} | acao: {', '.join(A.ACOES_P)}\n"
            f"ameaca.tipo: {', '.join(A.AMEACAS)} | acao: {', '.join(A.ACOES_A)}\n"
            f"posicao: {', '.join(A.POSICOES)} | tamanho: {', '.join(A.TAMANHOS)}\n"
            f"efeito: {', '.join(A.EFEITOS)} | camera: {', '.join(A.CAMERAS)}")


def _info_serie() -> dict:
    from .serie import preparar
    try:
        return preparar(os.environ.get("TEMA", ""))
    except ValueError as e:
        sys.exit(f"ERRO NO PEDIDO: {e}")


def contexto(_):
    from .personagem import escolher_protagonista
    from .serie import bloco_para_roteiro
    cfg = carregar_config()
    info = _info_serie()
    print("=== CONFIGURAÇÃO DA SÉRIE (config/serie.json) ===")
    print(json.dumps(cfg, ensure_ascii=False, indent=2))
    quem = info.get("protagonista") or escolher_protagonista(cfg, carregar_historico())
    prot = cfg.get("protagonistas", {}).get(quem, {})
    print(f"\n=== PROTAGONISTA DESTE VÍDEO: {quem} ({prot.get('descricao', '')}) ===")
    print(f'Coloque "protagonista": "{quem}" no roteiro.json e escreva os adjetivos de "você" no {prot.get("genero", "masculino")}.')
    if info["modo"] == "nova":
        print("\n=== TIPO DE VÍDEO: história nova (termina com dilema A/B) ===")
    else:
        print(bloco_para_roteiro(info))
    from .planos import EXEMPLO_JSON, GUIA_PLANOS, REGRAS_HISTORIA, modo_ilustrado
    if modo_ilustrado(cfg):
        print(f"\nVisual do protagonista (para as descrições das imagens): {prot.get('visual', '')}")
        print(f"\n=== {REGRAS_HISTORIA}\n\n=== {GUIA_PLANOS}\n\n=== EXEMPLO DE roteiro.json ===\n{EXEMPLO_JSON}")
        print(f"\nPlanos: cerca de {cfg.get('numero_de_planos', 40)} | duração alvo: {cfg['duracao_alvo_segundos']}s "
              f"(~{int(cfg['duracao_alvo_segundos'] * PALAVRAS_POR_SEGUNDO)} palavras)")
    else:
        print("\n=== VALORES ACEITOS NAS CENAS ===\n" + _catalogo())
    hist = carregar_historico()[-40:]
    print("\n=== HISTÓRIAS JÁ PUBLICADAS (não repetir) ===")
    print("\n".join(f"- {h['titulo']} ({h['tema'][:60]})" for h in hist) or "(nenhuma ainda)")


def validar(_):
    from .animacao import normalizar
    from .personagem import escolher_protagonista
    from .serie import ajustar_roteiro
    cfg = carregar_config()
    r = _roteiro()
    info = _info_serie()
    if not r.get("titulo") or not r.get("cenas"):
        sys.exit("ROTEIRO INVÁLIDO: faltou título ou cenas")
    from .planos import modo_ilustrado, normalizar_plano
    ilustrado = modo_ilustrado(cfg)
    for i, c in enumerate(r["cenas"]):
        if not c.get("narracao"):
            sys.exit(f"ROTEIRO INVÁLIDO: a cena {i} não tem narração")
        if ilustrado:
            if not c.get("imagem"):
                sys.exit(f"ROTEIRO INVÁLIDO: o plano {i} não tem o campo \"imagem\" (descrição em inglês)")
            normalizar_plano(c)
        else:
            normalizar(c)
    if r.get("protagonista") not in ("homem", "mulher"):
        r["protagonista"] = escolher_protagonista(cfg, carregar_historico())
    ajustar_roteiro(r, info)
    ROTEIRO.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    palavras = sum(len(c["narracao"].split()) for c in r["cenas"])
    seg = palavras / PALAVRAS_POR_SEGUNDO
    avisos = []
    if ilustrado:
        alvo_n = cfg.get("numero_de_planos", 40)
        if not alvo_n - 8 <= len(r["cenas"]) <= alvo_n + 6:
            avisos.append(f"tem {len(r['cenas'])} planos; o ideal é perto de {alvo_n}")
        longos = [i for i, c in enumerate(r["cenas"]) if len(c["narracao"].split()) > 16]
        if longos:
            avisos.append(f"planos com frase longa demais (mais de 16 palavras), divida em dois: {longos}")
        if not r.get("casa"):
            avisos.append('preencha "casa": descrição em inglês da casa da história (usada em todas as imagens)')
        com_ameaca = [i for i, c in enumerate(r["cenas"]) if c.get("ameaca")]
        if com_ameaca and com_ameaca[0] < len(r["cenas"]) * 0.5:
            avisos.append(f"a ameaça aparece cedo (plano {com_ameaca[0]}); guarde para o último terço")
    elif len(r["cenas"]) != cfg["numero_de_cenas"]:
        avisos.append(f"tem {len(r['cenas'])} cenas; a série pede {cfg['numero_de_cenas']}")
    alvo = cfg["duracao_alvo_segundos"]
    if not 0.75 * alvo <= seg <= 1.25 * alvo:
        avisos.append(f"duração estimada {seg:.0f}s está longe do alvo de {alvo}s")
    if not r.get("final"):
        if "comente a ou b" not in r["cenas"][-1]["narracao"].lower():
            avisos.append('a última cena deve terminar com "Comente A ou B."')
        if not r.get("opcao_a") or not r.get("opcao_b"):
            avisos.append('preencha "opcao_a" e "opcao_b" (uma frase cada) para permitir a continuação')
    elif "comente a ou b" in r["cenas"][-1]["narracao"].lower():
        avisos.append("esta é a parte FINAL: a última cena deve encerrar a história, sem dilema")
    if not r.get("resumo"):
        avisos.append('preencha "resumo" (a história inteira até aqui em até 4 frases)')
    from .clipes_ia import config as cfg_clipes
    com_clipe = [i for i, c in enumerate(r["cenas"]) if str(c.get("clipe_ia") or "").strip()]
    if com_clipe and cfg_clipes(cfg)["ligado"]:
        if len(com_clipe) > cfg_clipes(cfg)["max_por_video"]:
            avisos.append(f"clipe_ia em {len(com_clipe)} cenas; o máximo é {cfg_clipes(cfg)['max_por_video']} (só as primeiras serão usadas)")
        longas = [i for i in com_clipe if len(r["cenas"][i]["narracao"].split()) > 12]
        if longas:
            avisos.append(f"cenas com clipe_ia e narração longa (mais de 12 palavras): {longas}")
    elif com_clipe:
        print("(clipes de IA desligados em config/serie.json: o campo clipe_ia será ignorado)")
    usados = [c.get("lugar") or c.get("cenario") for c in r["cenas"]]
    print(f"Tipo: {'parte FINAL' if r.get('final') else 'parte ' + str(r.get('parte', 1))} da série \"{r.get('serie')}\"")
    print(f"OK: \"{r['titulo']}\" | protagonista: {r['protagonista']} | {len(r['cenas'])} cenas | {palavras} palavras | ~{seg:.0f}s")
    print(f"Lugares/cenários usados: {', '.join(dict.fromkeys(usados))}")
    print(f"Cenas com ameaça: {sum(1 for c in r['cenas'] if c.get('ameaca'))}")
    print("(valores inválidos foram trocados por padrões; confira no roteiro.json)")
    print("\n".join(f"AVISO: {a}" for a in avisos) or "Sem avisos.")


def _rotulo(img: Image.Image, texto: str) -> Image.Image:
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 70, 44), fill=(0, 0, 0))
    d.text((10, 8), texto, fill=(255, 230, 0))
    return img


def _previa_ilustrada(r):
    if not all(c.get("_img") for c in r["cenas"]):
        sys.exit("As ilustrações ainda não existem. Rode: python -m src.ferramentas imagens")
    imgs = []
    for i, c in enumerate(r["cenas"]):
        im = Image.open(c["_img"]).convert("RGB")
        im = im.resize((216, int(im.height * 216 / im.width)))
        im = im.crop((0, 0, 216, 384))
        imgs.append(_rotulo(im, str(i)))
    cols = 8
    linhas = -(-len(imgs) // cols)
    folha = Image.new("RGB", (216 * cols, 384 * linhas))
    for i, im in enumerate(imgs):
        folha.paste(im, ((i % cols) * 216, (i // cols) * 384))
    folha.save(TRAB / "previa.jpg", quality=82)
    print("Prévia salva em trabalho/previa.jpg (o número de cada imagem é o índice do plano)")


def previa(a):
    """Quadros de prévia, sem narração (o agente avalia a composição antes de montar)."""
    from .animacao import quadro
    r = _roteiro()
    if r["cenas"] and (r["cenas"][0].get("imagem") or r["cenas"][0].get("_img")) and a.cena is None:
        return _previa_ilustrada(r)
    prot = r.get("protagonista", "homem")
    if a.cena is not None:
        cena = r["cenas"][a.cena]
        imgs = [_rotulo(quadro(dict(cena), t, 6.0, prot, int(t * 24)).resize((360, 640)), f"{a.cena}:{t:.0f}s")
                for t in (0.6, 3.0, 5.4)]
        destino = TRAB / "previa_cena.jpg"
        cols = 3
    else:
        imgs = [_rotulo(quadro(dict(c), 3.0, 6.0, prot, 72).resize((240, 427)), str(i)) for i, c in enumerate(r["cenas"])]
        destino = TRAB / "previa.jpg"
        cols = 7
    w, h = imgs[0].size
    linhas = -(-len(imgs) // cols)
    folha = Image.new("RGB", (w * min(cols, len(imgs)), h * linhas))
    for i, im in enumerate(imgs):
        folha.paste(im, ((i % cols) * w, (i // cols) * h))
    folha.save(destino, quality=85)
    print(f"Prévia salva em trabalho/{destino.name}")


def imagens(a):
    from .ilustrador import gerar_ilustracoes
    r, cfg = _roteiro(), carregar_config()
    gerar_ilustracoes(r, cfg, TRAB / "imagens", refazer=a.refazer)
    ROTEIRO.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    info = r.get("_ilustracoes", {})
    reservas = [i for i, c in enumerate(r["cenas"]) if c.get("_reserva")]
    print(f"Ilustrações prontas: {info.get('geradas', 0)} geradas neste vídeo (~US$ {info.get('custo_usd', 0)})")
    if reservas:
        print(f"AVISO: os planos {reservas} usaram imagem reserva (a geração falhou). {info.get('aviso', '')}")
    print("Veja com: python -m src.ferramentas previa")


def narracao(_):
    from .voz import gerar_narracao
    r, cfg = _roteiro(), carregar_config()
    vozes = gerar_narracao(r, cfg, TRAB / "audio")
    VOZES.write_text(json.dumps([{**v, "arquivo": str(v["arquivo"])} for v in vozes], ensure_ascii=False), encoding="utf-8")
    print(f"Narração pronta: {sum(v['duracao'] for v in vozes):.0f}s no total" + (f" | voz: {r['_voz']}" if r.get("_voz") else ""))
    from . import clipes_ia
    n = clipes_ia.iniciar(r, cfg)
    if n:
        print(f"Clipes de IA disparados no Kaggle para {n} cena(s); entram no vídeo automaticamente depois do envio.")
    for i, v in enumerate(vozes):
        print(f"  cena {i}: {v['duracao']:.1f}s")


def montar(_):
    from .montagem import montar_video
    r, cfg = _roteiro(), carregar_config()
    if not VOZES.exists():
        sys.exit("ERRO: rode 'narracao' antes de montar.")
    vozes = [{**v, "arquivo": Path(v["arquivo"])} for v in json.loads(VOZES.read_text(encoding="utf-8"))]
    video = montar_video(r, vozes, cfg, TRAB / "video")
    print(f"Vídeo: {video} ({duracao(video):.0f}s, {video.stat().st_size / 1e6:.1f} MB)")


def quadros(_):
    if not FINAL.exists():
        sys.exit("ERRO: o vídeo final ainda não existe.")
    d = duracao(FINAL)
    rodar(["ffmpeg", "-y", "-i", str(FINAL), "-vf", f"fps=8/{d:.2f},scale=270:-2,tile=4x2",
           "-frames:v", "1", "-q:v", "4", str(TRAB / "quadros.jpg")])
    print("8 quadros do vídeo final: trabalho/quadros.jpg")


def enviar(a):
    from . import clipes_ia
    r, cfg = _roteiro(), carregar_config()
    if not FINAL.exists():
        sys.exit("ERRO: o vídeo final ainda não existe.")
    if clipes_ia.pendente():
        (TRAB / "nota_diretor.txt").write_text(a.nota or "", encoding="utf-8")
        clipes_ia.AGUARDANDO.write_text("ok")
        (TRAB / "ENVIADO").write_text("ok")
        print("Vídeo pronto. Os clipes de IA ainda estão sendo feitos no Kaggle: o vídeo será remontado com eles e "
              "enviado automaticamente depois. Pode encerrar.")
        return
    enviar_agora(r, cfg, a.nota)
    print("Enviado para o Telegram e salvo no histórico.")


def enviar_agora(r: dict, cfg: dict, nota: str = "") -> None:
    from . import telegram
    hashtags = " ".join(dict.fromkeys(r.get("hashtags", []) + cfg["hashtags_fixas"]))
    legenda = f"{r['titulo']}\n\n{r.get('legenda_post', '')}\n\n{hashtags}"
    (TRAB / "legenda_do_post.txt").write_text(legenda, encoding="utf-8")
    telegram.enviar_video(FINAL, legenda)
    telegram.enviar_mensagem(f"Legenda para copiar e colar:\n\n{legenda}")
    custo = r.get("_ilustracoes", {})
    if nota or custo:
        extra = f"\nIlustrações geradas: {custo.get('geradas', 0)} (~US$ {custo.get('custo_usd', 0)})" if custo else ""
        telegram.enviar_mensagem(f"Nota do diretor (Claude):\n{nota}{extra}")
    from .serie import campos_historico, mensagem_proximo_passo
    telegram.enviar_mensagem(mensagem_proximo_passo(r))
    salvar_no_historico(r["titulo"], r.get("tema", ""), r.get("protagonista", ""), campos_historico(r))
    (TRAB / "ENVIADO").write_text("ok")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("contexto").set_defaults(f=contexto)
    sub.add_parser("validar").set_defaults(f=validar)
    s = sub.add_parser("previa")
    s.add_argument("cena", type=int, nargs="?", default=None)
    s.set_defaults(f=previa)
    s = sub.add_parser("imagens")
    s.add_argument("--refazer", type=int, nargs="*", default=[])
    s.set_defaults(f=imagens)
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
