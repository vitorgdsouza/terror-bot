"""Gera as figurinhas (SVG) do protagonista e da ameaça. Canvas 1000x1200, personagem centrado em x=500."""
import sys
from pathlib import Path

VARIANTES = {
    # homem: cabelo preto curto, capa amarela
    "homem": {"pasta": "", "capa": "#e3a827", "capa_sombra": "#b8841a", "cabelo": "#1b1a22", "longo": False},
    # mulher: cabelo loiro comprido, jaqueta vermelha
    "mulher": {"pasta": "mulher", "capa": "#c9423a", "capa_sombra": "#9a2f29", "cabelo": "#f2c94c", "longo": True},
}
V = VARIANTES[sys.argv[1] if len(sys.argv) > 1 else "homem"]
OUT = Path(__file__).parent / "svg" / V["pasta"]
OUT.mkdir(parents=True, exist_ok=True)

LINHA = "#1d1b2e"
PELE = "#f2d3ad"
CABELO = V["cabelo"]
CAPA = V["capa"]
CAPA_SOMBRA = V["capa_sombra"]
LONGO = V["longo"]
CALCA = "#3b3f4c"
SAPATO = "#141418"
W, H = 1000, 1200
CX = 500


def membro(d, cor, larg):
    """Braço/perna como traço grosso com contorno."""
    return (f'<path d="{d}" fill="none" stroke="{LINHA}" stroke-width="{larg + 14}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{cor}" stroke-width="{larg}" stroke-linecap="round" stroke-linejoin="round"/>')


def mao(x, y, r=30):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{PELE}" stroke="{LINHA}" stroke-width="7"/>'


def pernas(abertas=False):
    if abertas:
        e = membro(f"M {CX-45} 780 L {CX-85} 1060", CALCA, 62)
        d = membro(f"M {CX+45} 780 L {CX+75} 1060", CALCA, 62)
        s = (f'<ellipse cx="{CX-95}" cy="1085" rx="52" ry="26" fill="{SAPATO}" stroke="{LINHA}" stroke-width="7"/>'
             f'<ellipse cx="{CX+85}" cy="1085" rx="52" ry="26" fill="{SAPATO}" stroke="{LINHA}" stroke-width="7"/>')
    else:
        e = membro(f"M {CX-45} 780 L {CX-50} 1060", CALCA, 62)
        d = membro(f"M {CX+45} 780 L {CX+50} 1060", CALCA, 62)
        s = (f'<ellipse cx="{CX-58}" cy="1085" rx="52" ry="26" fill="{SAPATO}" stroke="{LINHA}" stroke-width="7"/>'
             f'<ellipse cx="{CX+58}" cy="1085" rx="52" ry="26" fill="{SAPATO}" stroke="{LINHA}" stroke-width="7"/>')
    return e + d + s


def casaco(costas=False):
    corpo = (f'<path d="M {CX-85} 300 Q {CX} 285 {CX+85} 300 L {CX+140} 800 Q {CX} 830 {CX-140} 800 Z" '
             f'fill="{CAPA}" stroke="{LINHA}" stroke-width="8" stroke-linejoin="round"/>')
    if costas:
        detalhe = (f'<path d="M {CX-80} 305 Q {CX} 420 {CX+80} 305" fill="{CAPA_SOMBRA}" stroke="{LINHA}" stroke-width="7"/>'
                   f'<line x1="{CX}" y1="560" x2="{CX}" y2="815" stroke="{LINHA}" stroke-width="6"/>')
    else:
        detalhe = (f'<path d="M {CX-70} 300 L {CX} 380 L {CX+70} 300" fill="none" stroke="{LINHA}" stroke-width="7" stroke-linejoin="round"/>'
                   f'<line x1="{CX}" y1="380" x2="{CX}" y2="815" stroke="{LINHA}" stroke-width="6"/>'
                   + "".join(f'<circle cx="{CX+18}" cy="{y}" r="8" fill="{LINHA}"/>' for y in (450, 540, 630, 720))
                   + f'<path d="M {CX-115} 640 L {CX-45} 640" stroke="{LINHA}" stroke-width="6" stroke-linecap="round"/>'
                   + f'<path d="M {CX+45} 640 L {CX+115} 640" stroke="{LINHA}" stroke-width="6" stroke-linecap="round"/>')
    return corpo + detalhe


def cabelo_atras():
    """Cabelo comprido que cai atrás dos ombros (desenhado antes do corpo)."""
    if not LONGO:
        return ""
    return (f'<path d="M {CX-128} 175 Q {CX-150} 330 {CX-150} 440 Q {CX} 470 {CX+150} 440 Q {CX+150} 330 {CX+128} 175 Z" '
            f'fill="{CABELO}" stroke="{LINHA}" stroke-width="8" stroke-linejoin="round"/>')


def cabelo_costas():
    """Vista de costas: cabelo comprido por cima do casaco."""
    if not LONGO:
        return ""
    return (f'<path d="M {CX-128} 185 Q {CX-145} 330 {CX-135} 450 Q {CX} 480 {CX+135} 450 Q {CX+145} 330 {CX+128} 185 Z" '
            f'fill="{CABELO}" stroke="{LINHA}" stroke-width="8" stroke-linejoin="round"/>'
            f'<path d="M {CX-40} 330 Q {CX-45} 400 {CX-50} 445 M {CX+40} 330 Q {CX+45} 400 {CX+50} 445" '
            f'fill="none" stroke="#c9a13a" stroke-width="5" stroke-linecap="round"/>')


def cabeca(expressao="neutro", costas=False, olhar_baixo=False):
    hy = 185
    g = f'<rect x="{CX-28}" y="270" width="56" height="40" fill="{PELE}" stroke="{LINHA}" stroke-width="7"/>'
    if not LONGO:
        g += f'<circle cx="{CX-118}" cy="{hy+10}" r="22" fill="{PELE}" stroke="{LINHA}" stroke-width="7"/>'
        g += f'<circle cx="{CX+118}" cy="{hy+10}" r="22" fill="{PELE}" stroke="{LINHA}" stroke-width="7"/>'
    if costas:
        g += f'<circle cx="{CX}" cy="{hy}" r="120" fill="{CABELO}" stroke="{LINHA}" stroke-width="8"/>'
        g += f'<path d="M {CX-95} {hy+70} Q {CX} {hy+130} {CX+95} {hy+70} Q {CX} {hy+112} {CX-95} {hy+70} Z" fill="{PELE}"/>'
        return g
    g += f'<circle cx="{CX}" cy="{hy}" r="120" fill="{PELE}" stroke="{LINHA}" stroke-width="8"/>'
    if LONGO:  # franja lateral e mechas dos dois lados do rosto
        g += (f'<path d="M {CX-134} {hy+125} Q {CX-150} {hy-135} {CX} {hy-130} Q {CX+150} {hy-135} {CX+134} {hy+125} '
              f'Q {CX+112} {hy-10} {CX+70} {hy-45} Q {CX+10} {hy-25} {CX-60} {hy-70} Q {CX-112} {hy-10} {CX-134} {hy+125} Z" '
              f'fill="{CABELO}" stroke="{LINHA}" stroke-width="8" stroke-linejoin="round"/>')
    else:  # calota com franja em pontas
        g += (f'<path d="M {CX-122} {hy-5} Q {CX-125} {hy-135} {CX} {hy-128} Q {CX+125} {hy-135} {CX+122} {hy-5} '
              f'L {CX+95} {hy-55} L {CX+60} {hy-30} L {CX+30} {hy-62} L {CX-5} {hy-35} L {CX-40} {hy-65} L {CX-75} {hy-38} L {CX-100} {hy-60} Z" '
              f'fill="{CABELO}" stroke="{LINHA}" stroke-width="8" stroke-linejoin="round"/>')
    oy = hy + (40 if olhar_baixo else 20)
    if LONGO:  # cílios
        g += (f'<path d="M {CX-56} {oy-8} L {CX-66} {oy-18} M {CX+56} {oy-8} L {CX+66} {oy-18}" '
              f'stroke="{LINHA}" stroke-width="5" stroke-linecap="round"/>')
    if expressao == "medo":
        g += f'<circle cx="{CX-42}" cy="{oy}" r="14" fill="#111"/><circle cx="{CX+42}" cy="{oy}" r="14" fill="#111"/>'
        g += f'<path d="M {CX-72} {oy-26} L {CX-24} {oy-42}" stroke="{LINHA}" stroke-width="8" stroke-linecap="round"/>'
        g += f'<path d="M {CX+72} {oy-26} L {CX+24} {oy-42}" stroke="{LINHA}" stroke-width="8" stroke-linecap="round"/>'
        g += f'<ellipse cx="{CX}" cy="{oy+52}" rx="20" ry="26" fill="#3a1418" stroke="{LINHA}" stroke-width="6"/>'
        g += f'<path d="M {CX+98} {hy-30} q 12 22 0 34 q -12 -12 0 -34 Z" fill="#9fd3ff" stroke="{LINHA}" stroke-width="4"/>'
    else:
        g += f'<circle cx="{CX-42}" cy="{oy}" r="11" fill="#111"/><circle cx="{CX+42}" cy="{oy}" r="11" fill="#111"/>'
        g += f'<path d="M {CX-18} {oy+50} Q {CX} {oy+56} {CX+18} {oy+50}" fill="none" stroke="{LINHA}" stroke-width="7" stroke-linecap="round"/>'
    return g


def svg(corpo, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<defs>{defs}</defs>{corpo}</svg>')


def salvar(nome, conteudo):
    (OUT / f"{nome}.svg").write_text(conteudo, encoding="utf-8")


# 1. frente
braco_e = membro(f"M {CX-95} 330 Q {CX-150} 500 {CX-160} 680", CAPA, 58)
braco_d = membro(f"M {CX+95} 330 Q {CX+150} 500 {CX+160} 680", CAPA, 58)
salvar("frente", svg(cabelo_atras() + pernas() + braco_e + braco_d + casaco() + mao(CX-160, 700) + mao(CX+160, 700) + cabeca()))

# 2. medo (mãos junto ao peito)
be = membro(f"M {CX-95} 330 Q {CX-175} 470 {CX-50} 470", CAPA, 58)
bd = membro(f"M {CX+95} 330 Q {CX+175} 470 {CX+50} 470", CAPA, 58)
salvar("medo", svg(cabelo_atras() + pernas() + casaco() + be + bd + mao(CX-35, 470) + mao(CX+35, 470) + cabeca("medo")))

# 3. costas (andando)
be = membro(f"M {CX-95} 330 Q {CX-150} 500 {CX-150} 670", CAPA, 58)
bd = membro(f"M {CX+95} 330 Q {CX+150} 500 {CX+170} 660", CAPA, 58)
salvar("costas", svg(pernas(abertas=True) + be + bd + casaco(costas=True) + mao(CX-150, 690) + mao(CX+172, 680) + cabeca(costas=True) + cabelo_costas()))

# 4. celular (olhando para baixo, rosto iluminado)
defs = ('<radialGradient id="luz" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#bfe6ff" stop-opacity="0.55"/>'
        '<stop offset="100%" stop-color="#bfe6ff" stop-opacity="0"/></radialGradient>')
be = membro(f"M {CX-95} 330 Q {CX-170} 500 {CX-45} 520", CAPA, 58)
bd = membro(f"M {CX+95} 330 Q {CX+170} 500 {CX+45} 520", CAPA, 58)
fone = (f'<rect x="{CX-38}" y="455" width="76" height="120" rx="12" fill="#101018" stroke="{LINHA}" stroke-width="7"/>'
        f'<rect x="{CX-29}" y="466" width="58" height="98" rx="6" fill="#9fd8ff"/>')
brilho = f'<ellipse cx="{CX}" cy="330" rx="230" ry="260" fill="url(#luz)"/>'
salvar("celular", svg(cabelo_atras() + pernas() + casaco() + be + bd + fone + mao(CX-42, 530) + mao(CX+42, 530)
                      + cabeca(olhar_baixo=True) + brilho, defs))

# 5. lanterna (braço direito estendido com feixe de luz)
defs = ('<linearGradient id="feixe" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#fff4b8" stop-opacity="0.75"/>'
        '<stop offset="100%" stop-color="#fff4b8" stop-opacity="0"/></linearGradient>')
be = membro(f"M {CX-95} 330 Q {CX-150} 500 {CX-160} 680", CAPA, 58)
bd = membro(f"M {CX+95} 330 Q {CX+170} 420 {CX+255} 470", CAPA, 58)
feixe = f'<polygon points="{CX+320},455 {W},300 {W},640 {CX+320},485" fill="url(#feixe)"/>'
lanterna = (f'<rect x="{CX+265}" y="452" width="62" height="34" rx="6" fill="#2b2f3a" stroke="{LINHA}" stroke-width="6"/>'
            f'<rect x="{CX+318}" y="446" width="14" height="46" rx="4" fill="#fff4b8" stroke="{LINHA}" stroke-width="5"/>')
salvar("lanterna", svg(feixe + cabelo_atras() + pernas() + be + casaco() + bd + mao(CX-160, 700) + lanterna + mao(CX+265, 470)
                       + cabeca("medo"), defs))

# 6. mãos segurando o celular (visão em primeira pessoa, close)
defs = ('<radialGradient id="tela" cx="50%" cy="40%" r="70%"><stop offset="0%" stop-color="#cdeeff"/>'
        '<stop offset="100%" stop-color="#5b8fc4"/></radialGradient>')
fone = (f'<rect x="{CX-190}" y="130" width="380" height="760" rx="48" fill="#121218" stroke="{LINHA}" stroke-width="10"/>'
        f'<rect x="{CX-165}" y="185" width="330" height="650" rx="20" fill="url(#tela)"/>'
        f'<rect x="{CX-40}" y="150" width="80" height="16" rx="8" fill="#2a2a33"/>')
mao_e = (membro(f"M {CX-420} 1200 Q {CX-330} 900 {CX-215} 760", PELE, 150)
         + membro(f"M {CX-205} 560 Q {CX-170} 590 {CX-150} 640", PELE, 46))
mao_d = (membro(f"M {CX+420} 1200 Q {CX+330} 900 {CX+215} 760", PELE, 150)
         + membro(f"M {CX+205} 600 Q {CX+170} 630 {CX+150} 680", PELE, 46))
mangas = (membro(f"M {CX-500} 1250 L {CX-400} 1110", CAPA, 190) + membro(f"M {CX+500} 1250 L {CX+400} 1110", CAPA, 190))
salvar("maos_celular", svg(fone + mao_e + mao_d + mangas, defs))

if V["pasta"]:
    print("ok")
    sys.exit()

# 7. sombra: vulto encapuzado com olhos brancos
defs = ('<radialGradient id="brilho" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>'
        '<stop offset="100%" stop-color="#ffffff" stop-opacity="0"/></radialGradient>')
vulto = (f'<path d="M {CX} 60 Q {CX+175} 70 {CX+180} 300 Q {CX+260} 520 {CX+290} 1130 L {CX-290} 1130 '
         f'Q {CX-260} 520 {CX-180} 300 Q {CX-175} 70 {CX} 60 Z" fill="#06060b" stroke="#1a1a2a" stroke-width="6"/>'
         f'<ellipse cx="{CX}" cy="250" rx="120" ry="140" fill="#000003"/>')
olhos = (f'<ellipse cx="{CX-48}" cy="240" rx="40" ry="30" fill="url(#brilho)"/><ellipse cx="{CX+48}" cy="240" rx="40" ry="30" fill="url(#brilho)"/>'
         f'<ellipse cx="{CX-48}" cy="240" rx="17" ry="26" fill="#ffffff"/><ellipse cx="{CX+48}" cy="240" rx="17" ry="26" fill="#ffffff"/>')
salvar("sombra", svg(vulto + olhos, defs))

# 8. olhos no escuro
olhos = (f'<ellipse cx="{CX-70}" cy="600" rx="70" ry="55" fill="url(#brilho)"/><ellipse cx="{CX+70}" cy="600" rx="70" ry="55" fill="url(#brilho)"/>'
         f'<ellipse cx="{CX-70}" cy="600" rx="26" ry="40" fill="#ffffff"/><ellipse cx="{CX+70}" cy="600" rx="26" ry="40" fill="#ffffff"/>')
salvar("olhos", svg(olhos, defs))
print("ok")
