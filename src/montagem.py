"""Monta o vídeo final com FFmpeg: movimento de câmera, efeitos de terror, legendas e trilha."""
import math
import random
from pathlib import Path

from .util import MUSICA, RAIZ, duracao, log, rodar

FONTES = RAIZ / "assets" / "fontes"

W, H, FPS = 1080, 1920, 30
PAUSA = 0.35         # silêncio no fim de cada cena (segundos)
LIMITE_MB = 48       # o Telegram aceita vídeos de bots até 50 MB


def _filtro_movimento(mov: str, frames: int, forca: float = 1.0) -> str:
    a = 0.2 * forca  # quanto a câmera aproxima/anda
    base = f"scale={int(W * 1.5)}:{int(H * 1.5)},"
    centro = "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    zp = f":d={frames}:s={W}x{H}:fps={FPS}"
    if mov == "zoom_out":
        return base + f"zoompan=z='1+{a:.3f}-{a:.3f}*on/{frames}':{centro}{zp}"
    if mov == "pan_cima":
        return base + f"zoompan=z={1+a:.3f}:x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*(1-on/{frames})'{zp}"
    if mov == "pan_baixo":
        return base + f"zoompan=z={1+a:.3f}:x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*on/{frames}'{zp}"
    if mov == "tremor":
        return (base + f"zoompan=z='1.06+{a/2:.3f}*on/{frames}':{centro}{zp},"
                f"crop=w=iw-40:h=ih-40:x='20+{7*forca:.1f}*sin(n*2.3)+{4*forca:.1f}*sin(n*5.7)':y='20+{7*forca:.1f}*cos(n*1.9)+{4*forca:.1f}*sin(n*4.3)',"
                f"scale={W}:{H}")
    return base + f"zoompan=z='1+{a:.3f}*on/{frames}':{centro}{zp}"  # zoom_in (padrão)


EFEITOS = {
    # "terror": imagem lavada, cintilação de lâmpada, vinheta forte e granulado
    "terror": ("eq=contrast=1.12:saturation=0.7:brightness='-0.04+0.02*sin(t*11)*sin(t*2.7)':eval=frame,"
               "vignette=angle=PI/4,noise=alls=7:allf=u,format=yuv420p"),
    # "limpo": estilo desenho animado, cores preservadas, só uma vinheta suave nas bordas
    "limpo": "vignette=angle=PI/6,format=yuv420p",
}
FORCA_MOVIMENTO = {"terror": 1.0, "limpo": 0.45}


def _renderizar_cena(img: Path, voz: dict, mov: str, destino: Path, estilo: str = "terror") -> float:
    dur = voz["duracao"] + PAUSA
    frames = math.ceil(dur * FPS)
    fade_out = max(dur - 0.35, 0)
    vf = (f"{_filtro_movimento(mov, frames, FORCA_MOVIMENTO.get(estilo, 1.0))},{EFEITOS.get(estilo, EFEITOS['terror'])},"
          f"fade=t=in:st=0:d=0.25,fade=t=out:st={fade_out:.2f}:d=0.35")
    rodar(["ffmpeg", "-y", "-i", str(img), "-i", str(voz["arquivo"]),
           "-filter_complex", f"[0:v]{vf}[v];[1:a]aresample=44100,apad[a]",
           "-map", "[v]", "-map", "[a]", "-t", f"{dur:.3f}", "-r", str(FPS),
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-c:a", "aac", "-b:a", "160k", "-ac", "2", str(destino)])
    return dur


def _tempo_ass(s: float) -> str:
    h, r = divmod(max(s, 0), 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def _cor_ass(hexcor: str) -> str:
    h = hexcor.lstrip("#")
    return f"&H00{h[4:6]}{h[2:4]}{h[0:2]}".upper()


def _limpar(texto: str) -> str:
    return texto.replace("{", "(").replace("}", ")").replace("\\", "").upper()


def _fichas_alinhadas(narracao: str, palavras: list) -> list:
    """Texto original de cada palavra (com pontuação), quando dá para alinhar com as palavras da voz."""
    fichas = narracao.split()
    return fichas if len(fichas) == len(palavras) else [p["texto"] for p in palavras]


def _legendas_frase(roteiro: dict, vozes: list, duracoes: list, cfg: dict, destino: Path) -> None:
    """Estilo do vídeo de referência: a frase vai se formando no terço de baixo da tela (até 2 linhas),
    a palavra falada fica numa caixa roxa e as palavras de impacto aparecem um pouco maiores."""
    from .animacao import PALAVRAS_FORTES
    leg = cfg["legenda"]
    tam = leg.get("tamanho", 64)
    roxo = _cor_ass(leg.get("cor_destaque", "#7B2FE0"))
    margem = int(H * (1 - leg.get("posicao_y", 0.72)))
    n_max = max(2, int(leg.get("palavras_por_bloco", 6)))
    fonte = leg.get("fonte", "Poppins")
    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Fala,{fonte},{tam},&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,3,3,2,110,110,{margem},1
Style: Caixa,{fonte},{tam},&H00FFFFFF,&H00FFFFFF,{roxo},&H00000000,-1,0,0,0,100,100,0,0,3,10,0,2,110,110,{margem},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    linhas, deslocamento = [], 0.0
    for voz, dur, cena in zip(vozes, duracoes, roteiro["cenas"]):
        palavras = voz["palavras"]
        fichas = _fichas_alinhadas(cena.get("narracao", ""), palavras)
        # blocos de até n_max palavras, quebrando depois de pontuação
        blocos, atual = [], []
        for j, p in enumerate(palavras):
            atual.append(j)
            if len(atual) >= n_max or fichas[j].rstrip("\"'”").endswith((".", "!", "?", "…", ",", ":")):
                blocos.append(atual)
                atual = []
        if atual:
            blocos.append(atual)
        for b, bloco in enumerate(blocos):
            prox = palavras[blocos[b + 1][0]]["inicio"] if b + 1 < len(blocos) else min(dur, palavras[bloco[-1]]["fim"] + 0.5)
            textos = []
            for j in bloco:
                txt = _limpar(fichas[j]).rstrip(".,;:…").lstrip("\"'“") or _limpar(fichas[j])
                forte = (fichas[j].lower().strip(".,;:!?…\"'") in PALAVRAS_FORTES) or fichas[j].endswith(("!", "...", "…"))
                textos.append(f"{{\\fscx122\\fscy122}}{txt}{{\\fscx100\\fscy100}}" if forte else txt)
            for k, j in enumerate(bloco):
                ini = deslocamento + palavras[j]["inicio"]
                fim = deslocamento + (palavras[bloco[k + 1]]["inicio"] if k + 1 < len(bloco) else prox)
                if fim <= ini:
                    continue
                visiveis = textos[:k + 1]               # a frase vai se formando palavra por palavra
                caixa = " ".join(("{\\alpha&HFF&}" + x + "{\\alpha&HFF&}") if q != k else ("{\\alpha&H00&}" + x + "{\\alpha&HFF&}")
                                 for q, x in enumerate(visiveis))
                linhas.append(f"Dialogue: 0,{_tempo_ass(ini)},{_tempo_ass(fim)},Caixa,,0,0,0,,{caixa}")
                linhas.append(f"Dialogue: 1,{_tempo_ass(ini)},{_tempo_ass(fim)},Fala,,0,0,0,,{' '.join(visiveis)}")
        deslocamento += dur
    destino.write_text(cab + "\n".join(linhas) + "\n", encoding="utf-8")


def _escrever_legendas(roteiro: dict, vozes: list, duracoes: list, cfg: dict, destino: Path) -> None:
    if roteiro.get("formato") == "protocolo" or roteiro.get("estilo") == "vhs":   # o texto já está no quadro
        destino.write_text(f"[Script Info]\nScriptType: v4.00+\nPlayResX: {W}\nPlayResY: {H}\n\n[V4+ Styles]\n"
                           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
                           "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, "
                           "Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
                           "Style: Default,Arial,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,1,0,2,10,10,10,1\n\n"
                           "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n",
                           encoding="utf-8")
        return
    if cfg["legenda"].get("estilo") == "frase":
        return _legendas_frase(roteiro, vozes, duracoes, cfg, destino)
    leg = cfg["legenda"]
    tam = leg["tamanho"]
    roxo = _cor_ass(leg.get("cor_destaque", "#7B2FE0"))
    karaoke = leg.get("estilo", "karaoke") == "karaoke"
    margem = 620 if karaoke else 560
    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Fala,{leg['fonte']},{tam},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,{4 if karaoke else 6},{2 if karaoke else 3},2,90,90,{margem},1
Style: Caixa,{leg['fonte']},{tam},&H00FFFFFF,&H00FFFFFF,{roxo},&H00000000,-1,0,0,0,100,100,0,0,3,9,0,2,90,90,{margem},1
Style: Titulo,{leg['fonte']},70,&H003C3CE6,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,2,0,1,6,3,8,80,80,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    linhas = []
    if leg.get("mostrar_titulo", True):
        linhas.append(f"Dialogue: 2,{_tempo_ass(0)},{_tempo_ass(3.0)},Titulo,,0,0,0,,"
                      f"{{\\fad(300,400)}}{_limpar(roteiro['titulo'])}")
    deslocamento, n = 0.0, max(1, int(leg["palavras_por_bloco"]))
    for voz, dur in zip(vozes, duracoes):
        palavras = voz["palavras"]
        for j in range(0, len(palavras), n):
            bloco = palavras[j:j + n]
            prox = palavras[j + n]["inicio"] if j + n < len(palavras) else bloco[-1]["fim"] + 0.3
            fim_bloco = deslocamento + max(prox, bloco[-1]["fim"])
            textos = [_limpar(p["texto"]) for p in bloco]
            if not karaoke:
                linhas.append(f"Dialogue: 0,{_tempo_ass(deslocamento + bloco[0]['inicio'])},{_tempo_ass(fim_bloco)},"
                              f"Fala,,0,0,0,,{' '.join(textos)}")
                continue
            # karaokê: o bloco inteiro em branco e a palavra falada em cima de uma caixa colorida
            for k, p in enumerate(bloco):
                ini = deslocamento + p["inicio"]
                fim = deslocamento + bloco[k + 1]["inicio"] if k + 1 < len(bloco) else fim_bloco
                antes = " ".join(textos[:k]) + " " if k else ""
                depois = " " + " ".join(textos[k + 1:]) if k + 1 < len(textos) else ""
                # só a palavra falada fica visível nesta camada (os espaços também ficam ocultos)
                caixa = f"{{\\alpha&HFF&}}{antes}{{\\alpha&H00&}}{textos[k]}{{\\alpha&HFF&}}{depois}"
                linhas.append(f"Dialogue: 0,{_tempo_ass(ini)},{_tempo_ass(fim)},Caixa,,0,0,0,,{caixa}")
                linhas.append(f"Dialogue: 1,{_tempo_ass(ini)},{_tempo_ass(fim)},Fala,,0,0,0,,{' '.join(textos)}")
        deslocamento += dur
    destino.write_text(cab + "\n".join(linhas) + "\n", encoding="utf-8")


def _trilha(total: float, cfg: dict, roteiro: dict | None = None) -> list:
    """Devolve (entradas extras do ffmpeg, filtro da trilha). Se o roteiro pedir "trilha" (busca no Freesound),
    usa esse ambiente sombrio do começo ao fim; senão uma música de assets/musica; senão um drone gerado."""
    busca = (roteiro or {}).get("trilha")
    if busca:
        try:
            from .sons import baixar
            arq = baixar(str(busca), True)
        except Exception as e:  # noqa: BLE001
            arq = None
            log(f"Trilha '{busca}' falhou ({e})")
        if arq:
            vol = float((roteiro or {}).get("trilha_volume", 0.55))
            log(f"Trilha sombria: {busca}")
            return (["-stream_loop", "-1", "-i", str(arq)],
                    f"[1:a]aformat=channel_layouts=stereo,volume={vol},afade=t=in:d=2,"
                    f"afade=t=out:st={max(total - 2.5, 0):.2f}:d=2.5[bg]")
    musicas = sorted(list(MUSICA.glob("*.mp3")) + list(MUSICA.glob("*.m4a")) + list(MUSICA.glob("*.wav")))
    if musicas:
        escolhida = random.choice(musicas)
        log(f"Trilha: {escolhida.name}")
        vol = cfg["musica"]["volume_musica"]
        return (["-stream_loop", "-1", "-i", str(escolhida)],
                f"[1:a]volume={vol},afade=t=out:st={max(total - 2, 0):.2f}:d=2[bg]")
    log("Trilha: ambiente gerado automaticamente")
    vol = cfg["musica"]["volume_ambiente_gerado"]
    drone = (f"aevalsrc='0.25*sin(2*PI*55*t)*(0.6+0.4*sin(2*PI*0.07*t))"
             f"+0.12*sin(2*PI*82.4*t)*(0.5+0.5*sin(2*PI*0.05*t))':s=44100:d={total:.2f}")
    vento = f"anoisesrc=color=brown:amplitude=0.35:d={total:.2f}:r=44100,lowpass=f=350"
    filtro = (f"{drone}[d];{vento}[n];[d][n]amix=inputs=2:normalize=0,"
              f"volume={vol},afade=t=in:d=1.5,afade=t=out:st={max(total - 2, 0):.2f}:d=2,aformat=channel_layouts=stereo[bg]")
    return [], filtro


def montar_video(roteiro: dict, vozes: list, cfg: dict, pasta: Path) -> Path:
    """Anima cada cena (src/animacao.py), junta tudo e coloca legendas e trilha."""
    from .animacao import marcar_revelacao, renderizar_cena, renderizar_clipe
    pasta.mkdir(parents=True, exist_ok=True)
    marcar_revelacao(roteiro)
    if roteiro.get("estilo") == "vhs":                    # fita VHS pixelada: relógio da fita corre pelo vídeo
        t0 = 0.0
        for c, v in zip(roteiro["cenas"], vozes):
            c.update(_vhs=True, _t0=t0, _pixel=roteiro.get("pixel", 6), _data=roteiro.get("data_fita", "NOV 16 1997"),
                     _hora=tuple(roteiro.get("hora_fita", (3, 12, 40))))
            t0 += v["duracao"] + PAUSA
    prot = roteiro.get("protagonista", "homem")
    cenas, duracoes = [], []
    lista_cenas = roteiro["cenas"]
    for i, (voz, cena) in enumerate(zip(vozes, lista_cenas)):
        log(f"Animando cena {i + 1}/{len(vozes)} ({cena.get('lugar') or cena.get('cenario')})")
        destino = pasta / f"clip_{i:02d}.mp4"
        cena["_progresso"] = i / max(1, len(vozes) - 1)   # usado para aumentar a tensão ao longo do vídeo
        cena["_palavras"] = voz.get("palavras") or []
        pausa = PAUSA + float(cena.get("pausa_extra") or 0)
        if cena.get("_img"):
            # planos ilustrados: ritmo de vídeo curto (pausa mínima no mesmo lugar, um respiro ao trocar de lugar)
            ultimo = i == len(vozes) - 1
            muda = ultimo or lista_cenas[i + 1].get("lugar") != cena.get("lugar")
            pausa = 1.6 if ultimo else (0.38 if muda else 0.1)
            cena["_fade_in"] = i == 0 or lista_cenas[i - 1].get("lugar") != cena.get("lugar")
            cena["_fade_out"] = muda
        if cena.get("_clipe") and Path(cena["_clipe"]).exists():
            try:
                duracoes.append(renderizar_clipe(cena, voz, destino, pausa))
                cenas.append(destino)
                continue
            except Exception as e:  # clipe com problema: usa a animação normal nesta cena
                log(f"  clipe de IA da cena {i} falhou na montagem ({e}); usando a animação normal")
        if roteiro.get("formato") == "protocolo":
            from .protocolo import renderizar_cena_protocolo
            duracoes.append(renderizar_cena_protocolo(cena, voz, destino, pausa, i))
            cenas.append(destino)
            continue
        if roteiro.get("formato") == "real":
            from .real import renderizar_cena_real
            duracoes.append(renderizar_cena_real(cena, voz, destino, pausa, i))
            cenas.append(destino)
            continue
        duracoes.append(renderizar_cena(cena, voz, destino, prot, pausa))
        cenas.append(destino)

    lista = pasta / "lista.txt"
    lista.write_text("".join(f"file '{c.name}'\n" for c in cenas), encoding="utf-8")
    juntos = pasta / "juntos.mp4"
    rodar(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lista), "-c", "copy", str(juntos)])

    total = duracao(juntos)
    _escrever_legendas(roteiro, vozes, duracoes, cfg, pasta / "legendas.ass")
    extras, filtro_bg = _trilha(total, cfg, roteiro)
    final = pasta / "video_final.mp4"
    # sons ambientes e efeitos de cada cena (Freesound); abaixam sozinhos quando o narrador fala
    sons = None
    try:
        from .sons import montar_trilha_sons
        sons = montar_trilha_sons(roteiro, duracoes, pasta / "sons.wav")
    except Exception as e:
        log(f"Sons das cenas falharam ({e}); seguindo sem eles")
    if sons:
        idx = 1 + (1 if extras else 0)
        extras = [*extras, "-i", sons.name]
        mistura = (f"[0:a]asplit=3[voz][chave][chave2];[{idx}:a]aformat=channel_layouts=stereo[sfx];"
                   "[sfx][chave]sidechaincompress=threshold=0.04:ratio=3:attack=30:release=400[sfxd];"
                   "[bg][chave2]sidechaincompress=threshold=0.05:ratio=2.5:attack=40:release=600[bgd];"
                   "[voz][bgd][sfxd]amix=inputs=3:duration=first:normalize=0[a]")
    else:
        mistura = ("[0:a]asplit=2[voz][chave];[bg][chave]sidechaincompress=threshold=0.05:ratio=2.5:attack=40:"
                   "release=600[bgd];[voz][bgd]amix=inputs=2:duration=first:normalize=0[a]")

    def codificar(crf: int) -> None:
        rodar(["ffmpeg", "-y", "-i", "juntos.mp4", *extras,
               "-filter_complex",
               f"[0:v]ass=legendas.ass:fontsdir={FONTES}[v];{filtro_bg};{mistura}",
               "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", final.name],
              cwd=pasta)

    log("Juntando cenas, legendas e trilha")
    codificar(23)
    if final.stat().st_size > LIMITE_MB * 1024 * 1024:
        log("Vídeo grande demais para o Telegram, comprimindo mais")
        codificar(29)
    log(f"Vídeo pronto: {total:.0f}s, {final.stat().st_size / 1e6:.1f} MB")
    return final
