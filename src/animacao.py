"""Motor de animação: desenha cada cena quadro a quadro (cenário + personagem + ameaça + efeitos + câmera).

Nada aqui usa IA de imagem: os cenários e personagens são desenhos fixos em assets/.
Cada cena do roteiro usa estes campos:
    "cenario":    um de CENARIOS  ("celular_cftv" = mãos segurando o celular com a câmera de segurança na tela)
    "tela":       (só no celular_cftv) qual cenário aparece na tela da câmera
    "personagem": {"pose": ..., "acao": ..., "posicao": ..., "tamanho": ...} ou null
    "ameaca":     {"tipo": "abismo"|"olhos"|"invasor", "acao": ..., "posicao": ..., "tamanho": ...} ou null
    "efeito":     um de EFEITOS
    "camera":     um de CAMERAS
"""
import json
import math
import os
import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .util import RAIZ

FPS = 24
W, H = 1080, 1920                 # vídeo final
CW, CH = 1188, 2112               # tela dos cenários (10% maior: folga para a câmera)
PASTA_CEN = RAIZ / "assets" / "cenarios"
PASTA_PER = RAIZ / "assets" / "personagem"
META = json.loads((PASTA_CEN / "cenarios.json").read_text(encoding="utf-8"))

CENARIOS = list(META) + ["celular_cftv"]
POSES = ["frente", "medo", "gritando", "encolhida", "costas", "celular", "lanterna",
         "sentado", "abrindo_porta", "agachado", "olhando_tras",
         "engatinhando", "olhando_cima", "alcancando", "com_gato", "golpeando", "silencio", "caido", "chamando", "debrucado"]
POSES_NOVAS = ["engatinhando", "olhando_cima", "alcancando", "com_gato", "golpeando", "silencio", "caido", "chamando",
               "debrucado"]
ACOES_P = ["parado", "andando", "correndo", "entrando", "saindo", "afastando", "aproximando", "tremendo", "virando"]
try:
    ESTILO_PERSONAGEM = json.loads((RAIZ / "config" / "serie.json").read_text(encoding="utf-8")).get("personagem_estilo", "boneco")
except Exception:
    ESTILO_PERSONAGEM = "boneco"
ACOES_A = ["parada", "aparecendo", "aproximando", "sumindo", "espiando", "passando", "na_janela", "encarando", "relance",
           "teto", "rastejando", "sorriso_escuro"]
AMEACAS = ["abismo", "invasor"]
CAO_ACOES = ["parado", "andando", "correndo", "brincando", "sentado", "deitado", "levantando_cabeca", "de_pe"]
GATO_ACOES = ["parado", "andando", "correndo", "sentado", "miando", "deitado", "escondido", "assustado", "olhos_escuro"]
POSICOES = {"esquerda": 0.28, "centro": 0.5, "direita": 0.72}
TAMANHOS = {"longe": 0.36, "medio": 0.62, "perto": 1.15}
EFEITOS = ["nenhum", "luz_piscando", "tv_chiando", "relampago", "chuva", "tremor"]
CAMERAS = ["zoom_in", "zoom_out", "pan_esquerda", "pan_direita", "parada"]
PES_NO_DESENHO = 1115 / 1200      # onde ficam os pés dentro da figurinha

_cache: dict = {}
FONTE_TELA = RAIZ / "assets" / "fontes" / "Poppins-Bold.ttf"

# explicação dos valores, usada no pedido ao Gemini e nas instruções do agente
GUIA_CENAS = """Cada cena é um quadro de desenho animado montado com peças fixas:
- "cenario": o lugar. sala (sofá, TV, abajur, janela) | corredor (comprido, porta escura no fundo) |
  quarto (cama, escrivaninha com monitor aceso, janela) | cozinha (armários, geladeira, janela com lua) |
  pia_detalhe (close da pia com prato e copo, janela ao lado: só personagem "perto"; o abismo "longe" aparece lá fora, pela janela) |
  porta_entrada (porta da rua por dentro com corrente e olho mágico, cabideiro com casaco) | janela (close numa janela grande, noite lá fora) |
  escada (vista de baixo, subindo para um andar escuro) | escada_cima (vista do andar de cima, descendo para um hall escuro) | banheiro (espelho, pia, box com cortina) |
  debaixo_cama (close no chão do quarto, chinelos e o escuro embaixo da cama: só personagem "perto"; o abismo "longe" aparece no escuro embaixo da cama) |
  porao (caixas, lâmpada pendurada, escada ao fundo) | garagem (carro velho, ferramentas, portão aberto para a noite) |
  armario (quarto escuro com um guarda-roupa de porta aberta e o vão preto, abajur aceso, cama) |
  corredor_velho (corredor antigo de papel de parede rasgado, arandela acesa, porta aberta para o escuro, escada ao fundo) |
  poco (poço de pedra no quintal dos fundos, tampa de madeira quebrada, corda descendo para o escuro) |
  poco_sorriso (CENA ESPECIAL, sem personagem: o fundo do poço e, no breu do túnel, só os olhos e o sorriso do Abismo,
  parados, gargalhando; o som traz a risada e miados imitados. Use uma vez, num momento de susto) |
  janela_poco (CENA ESPECIAL, sem personagem: pela janela, no quintal, o Abismo junto do poço segurando o Stu pela nuca,
  encarando quem olha; a cabeça estala, o Stu se debate) |
  tunel_abismo (CENA ESPECIAL, sem personagem: o Abismo de corpo inteiro rastejando de quatro no túnel, vindo para a
  câmera, a cabeça estalando de lado; use uma vez, perto do clímax) |
  fundo_poco (fundo do poço seco, lua lá em cima, poças, um túnel baixo aberto na parede) |
  tunel (túnel subterrâneo de terra e tijolo, raízes e vigas, escuridão no fim) |
  parede_dentro (o vão por dentro das paredes da casa, vigas e isolamento, um buraco descendo) |
  porao_duarte (o porão antigo dos Duarte, lençóis sobre caixas, fornalha, porta trancada com ferrolho por dentro) |
  camara (a câmara do Abismo debaixo da casa: paredes arranhadas, fotos de crianças, desenhos, uma coleira num prego, uma abertura escura) |
  corda_poco (dentro do poço olhando para cima: a lua na boca do poço, a corda descendo, um túnel baixo aberto no fundo) |
  telefone_casa (close no telefone de parede da cozinha com fio enrolado e um bilhete colado: só personagem "perto") |
  tunel_bifurcacao (o túnel se divide em dois: à esquerda galeria de vigas com pegadas de gato, à direita arco de tijolo com uma luzinha no fim) |
  sotao_bisavo (o sótão da bisavó: cavalete com o desenho do homem sorrindo, lamparina, pilhas de desenhos, janela redonda) |
  desenhos_parede (close numa parede de terra coberta de desenhos infantis do homem sorrindo junto da casa e do gato; no meio, um desenho novo de um menino de moletom verde: só personagem "perto") |
  esp_stu_tunel (CENA ESPECIAL, sem personagem: o Stu encolhido e tremendo num nicho do túnel, vivo, olhos arregalados) |
  esp_abismo_teto (CENA ESPECIAL, sem personagem: o Abismo pendurado de cabeça para baixo do teto do túnel, braços compridos balançando, a cabeça estala) |
  quintal_canil (quintal dos fundos à noite: casinha de cachorro vazia, corrente solta no chão, pote, varal, mata atrás da cerca) |
  garagem_viatura (garagem com uma viatura de polícia de porta aberta, rádio aceso, portão aberto para o escuro) |
  esp_pele_corredor (CENA ESPECIAL, sem personagem: O Pele no corredor, magro e alto, vestindo o couro do Rufus nas costas, um olho humano espiando; a cabeça estala) |
  farmacia_balcao (farmácia 24h vista de trás do balcão: caixa registradora, livro aberto, abajur; a porta de vidro dá para a noite) |
  farmacia_balcao_escuro (o mesmo balcão, rua lá fora mais escura: use antes de esp_cliente_porta para o susto) |
  esp_cliente_porta (CENA ESPECIAL: o mesmo balcão, e lá fora, parado na porta de vidro sob o poste, o Cliente das 3h17 olhando para dentro) |
  farmacia_corredor (corredor entre prateleiras de remédios, câmera no teto, escuro no fundo) |
  farmacia_cftv (a farmácia vista pela câmera de segurança, imagem esverdeada e curva: só o lugar) |
  farmacia_fora (a farmácia 24h vista de fora, cruz verde acesa, estrada vazia, poste) |
  farmacia_deposito (depósito dos fundos: caixas empilhadas, lâmpada pendurada, porta de saída de emergência entreaberta para o escuro) |
  terreiro_noite (terreiro de casa de roça à noite: árvore grande, banco, janela acesa, poço de balde, lua cheia, mata atrás) |
  porteira_estrada (porteira de madeira fechada numa estrada de terra, cerca de arame, vaga-lumes, uma lamparina na mata, névoa) |
  mato_trilha (trilha estreita entrando na mata fechada, galhos formando um túnel escuro) |
  esp_pisadeira (CENA ESPECIAL, sem personagem: a Pisadeira agachada no telhado, olhos arregalados, dedos compridos nas telhas, espiando a janela acesa embaixo; a cabeça estala) |
  carro_dentro (de dentro do carro, do banco do motorista: volante, celular aceso no painel, terço no retrovisor, estrada escura: só o lugar) |
  carro_banco_tras (vista do banco de trás vazio, cinto atravessado, cheirinho balançando: só o lugar; use antes do passageiro aparecer) |
  estrada_noite (pelo para-brisa: estrada na mata, névoa, placa em branco, faróis: só o lugar) |
  esp_passageiro (CENA ESPECIAL, sem personagem: pelo retrovisor, o Passageiro do Banco de Trás sentado, sorrindo, segurando um lírio; a cabeça estala) |
  rua_sem_saida (rua sem saída abandonada, casas de janelas quebradas, muro de trepadeiras, poste aceso, poças) |
  cemiterio_portao (portão de ferro fechado de um cemitério, anjos e cruzes atrás, lampião no muro, névoa no chão) |
  tv_estatica (sala escura com poltrona e uma TV de tubo chiando, cortinas, janela) |
  escola_corredor (corredor de escola à noite, armários, portas de sala, piso vermelho, escuro no fim) |
  banheiro_escola (banheiro de escola velho: pias pingando, espelho comprido, cabines, a última porta aberta para o escuro) |
  hospital_quarto (quarto de hospital à noite: cama vazia, monitor verde, soro, cortina, porta com visor) |
  onibus_vazio / onibus_vazio2 (ônibus vazio rodando de noite, alças balançando, motorista no escuro lá na frente) |
  ponto_onibus (ponto de ônibus vazio numa rua de lojas fechadas, poste aceso, chão molhado, névoa no fim da rua) |
  floresta_noite / floresta_noite2 (floresta fechada à noite, névoa no chão, olhinhos brilhando entre as árvores) |
  quarto_porta_fechada (quarto de adolescente de noite visto da cama, só personagem "perto": porta fechada com a luz do corredor por baixo e a sombra de dois pés parados; desenhos estranhos na parede, celular aceso na mesa) |
  portaria (portaria de prédio antigo à noite: parede de monitores do CFTV, mesa com garrafa térmica, rádio e abajur, porta de vidro da rua) |
  corredor_camera4 (corredor comprido de andar de prédio, portas numeradas, tapete, plafons, escuro no fim) |
  elevador_dentro (dentro do elevador velho de madeira: painel de botões, espelho embaçado, lâmpada) |
  elevador_porta (hall do andar com a porta do elevador entreaberta para o escuro e a luz vermelha acesa em cima) |
  garagem_predio / garagem_predio2 (garagem subterrânea do prédio: pilares, carros cobertos com lona, porta com saída verde) |
  esp_moradora (CENA ESPECIAL, sem personagem: A Moradora do 13º, de camisola e cabelo no rosto, parada no meio do corredor; a cabeça estala) |
  quarto_roca (quarto da casa de roça: cama de ferro com colcha de retalhos, janela de madeira aberta para a noite, lamparina) |
  cozinha_fogao / cozinha_fogao2 / cozinha_fogao3 (cozinha da roça: fogão a lenha aceso, filtro de barro, canecas, mesa com toalha, janela para a mata; 3 = janela clareada) |
  esp_assobiador (CENA ESPECIAL, sem personagem: O Assobiador, alto e escuro, espiando de trás de uma árvore na mata, olhos claros; a cabeça estala) |
  farmacia_balcao2 (outro ângulo do balcão da farmácia: caixa, abajur, livro, porta de vidro ao fundo) |
  farmacia_balcao_luz (o balcão com a lâmpada do teto acesa e o poste lá fora) |
  farmacia_corredor2 / farmacia_cftv2 / farmacia_fora2 (outras versões do corredor, da câmera e da fachada) |
  esp_cliente_balcao / esp_cliente_balcao2 (CENA ESPECIAL, sem personagem: o Cliente das 3h17 debruçado no balcão, sorriso largo, empurrando dinheiro e um rolo de esparadrapo; 2 = no meio das prateleiras) |
  esp_cliente_estoque (CENA ESPECIAL: do balcão, o Cliente parado no fim do corredor de prateleiras, na porta dos fundos) |
  olho_tiago (Pode Entrar?, traço semi-realista, sem personagem: pelo olho mágico com aro de latão, o Tiago entregador na varanda com geada, segurando a bag verde no peito, capacete no braço, cachecol laranja, lábios roxos, SEM vapor saindo da boca; rosto em foco [0.5, 0.37, 2.6], rosto e bag em [0.5, 0.55, 1.8]) |
  olho_tiago_celular (Pode Entrar?, mesmo traço, sem personagem: pelo olho mágico, o Tiago encosta o celular no vidro com o app de entrega aberto, mapa e pino, tela sem texto; metade do rosto dele atrás do celular, SEM vapor; a tela fica em ~[0.5, 0.45]) |
  inverno_rua (Pode Entrar?, traço semi-realista: rua de bairro coberta de geada cinza, casas com muro e portão, fios e postes, carro abandonado com a porta aberta no meio da rua, uma única casa ao fundo com janela acesa e fumaça na chaminé, céu baixo) |
  caderno_lurdes (Pode Entrar?, traço semi-realista, sem personagem: close de cima do caderno espiral da Dona Lurdes na mesa de madeira, anotações à mão ilegíveis, desenho do olho mágico e de uma janela embaçada, canto da folha rasgado, vela acesa e óculos ao lado, geada na janela; texto em português só por cima) |
  esp_tiago_vidro (CENA ESPECIAL, Pode Entrar?, sem personagem: o rosto do Tiago colado no olho mágico, olho de peixe, olhos calmos e parados, boca entreaberta, o vidro limpo SEM embaçar; a cabeça inclina devagar) |
  porta_inverno (Pode Entrar?, traço semi-realista: o hall por dentro, porta de madeira com corrente e olho mágico, cadeira encostada, geada entrando por baixo, casaco no gancho, latas de comida contadas na prateleira, a lareira acesa no cômodo ao lado; olho mágico em foco [0.55, 0.265, 2.4]) |
  campainha_cftv (Pode Entrar?, traço semi-realista, sem personagem: a câmera da campainha vista de cima com olho de peixe largo, a varanda com geada e
  lâmpada no teto, o Tiago parado de frente para a porta com a bag nas costas e o capacete na mão, SEM vapor; rosto em foco [0.5, 0.33, 2.6]; ideal com "estilo": "vhs") |
  esp_tiago_campainha (CENA ESPECIAL, Pode Entrar?, sem personagem: close do rosto do Tiago olhando para cima, direto na lente da campainha, lábios
  roxos entreabertos e SEM vapor, geada caindo; a cabeça treme de frio; boca em foco [0.5, 0.58, 2.2]; também serve de thumb) |
  tv_estatica2 (close na TV de tubo chiando na sala escura) | escola_corredor2 (corredor de escola com luar entrando pelas janelas) |
  banheiro_escola2 (banheiro de escola: cabines verdes, uma porta aberta, pias e espelho manchado) | hospital_quarto2 (quarto de hospital: cama, soro, monitor verde, cortina) |
  escritorio (estantes de livros, mesa de madeira com abajur aceso, poltrona de couro, janela) |
  quarto_crianca (o antigo quarto de criança da casa, onde a bisavó dormia quando menina: cama com ursinho, berço, móbile de luas e estrelas, abajur de lua, baú de brinquedos) |
  planta_andar (o andar visto de cima, como uma planta: escritório e quarto lado a lado, o guarda-roupa aberto e escuro;
  só o lugar, sem personagem: ótimo para abrir a história ou mostrar a casa em silêncio) |
  casa_fora (a casa vista da calçada à noite, uma janela acesa) | rua (rua de bairro vista do alto, poste aceso, carros) | celular_cftv (close das mãos segurando o celular; na tela, a câmera de segurança mostrando outro cenário)
- "tela": só no celular_cftv, qual cenário aparece na câmera (ex.: "sala"). O personagem e a ameaça dessa cena aparecem DENTRO da câmera.
- "personagem": o protagonista ou null. É um boneco animado de verdade (anda mexendo pernas e braços, segura objetos, muda a cara).
  pose (o que ele faz parado): frente | medo (cara de medo, mãos no peito) | gritando (apavorado) | encolhida (sentado no chão
  abraçando os joelhos, mãos na boca) | costas | celular (olhando o celular aceso na mão) | lanterna (apontando a lanterna) |
  sentado (sentado no sofá da sala ou na beira da cama do quarto; em outros cenários fica em pé) | abrindo_porta (estende a mão devagar) | agachado (agachado olhando algo
  no chão) | olhando_tras (de lado, virando o rosto para trás) | engatinhando (de quatro; com acao "andando" vai devagar:
  túnel, vão da parede, debaixo da cama) | olhando_cima (olhos arregalados para o alto: fundo do poço, topo da escada) |
  alcancando (agachado, estica o braço devagar para dentro de um buraco ou fresta) | com_gato (abraçando o Stu no colo:
  só quando ele REALMENTE achar o gato) | silencio (uma mão
  tapando a boca, olhos arregalados: segurando o grito) | caido (caiu sentado no chão, apoiado nas mãos, recuando) |
  chamando (mãos em volta da boca, chamando o gato) | golpeando (bate com um martelo: ele encosta sozinho na parede mais
  perto, esquerda ou direita, e cada golpe solta poeira, abre rachaduras e um buraco) | debrucado (debruçado na borda do poço, braço descendo para o escuro;
  no cenário poco, "alcancando" também vira isso, junto da borda).
  olhando_cima é de costas para a tela (olhando o alto do poço ou da escada).

  acao: parado | andando (anda de lado e para) | correndo | entrando (entra pelo lado e para) | saindo (sai pelo lado) |
  afastando (de costas, andando para o fundo da cena) | aproximando (de frente, andando para a câmera) | tremendo | virando
  (estava de costas e vira). Ao parar, ele fica na pose escolhida.
  "depois" (opcional): uma segunda pose que ele assume no meio da cena (ex.: pose "frente", depois "celular").
  posicao: esquerda | centro | direita. tamanho: longe | medio | perto (perto = close do rosto e do tronco).
- "ameaca": null ou o perigo. tipo: abismo (O ABISMO: silhueta humana toda preta, rosto pálido de olhos arregalados e sorriso enorme;
  parado = em pé; medio parado = agachado observando; aproximando = vem em posição de ataque; perto = close do rosto) |
  invasor (pessoa real de capa de chuva amarela, capuz com o rosto no escuro e um machado;
  use em histórias sem sobrenatural: invasão, perseguição, alguém dentro de casa).
  acao: parada | aparecendo (surge aos poucos) | aproximando (vem para perto) | sumindo |
  espiando (só a cabeça e o ombro surgem devagar pela borda da tela, a cabeça estala; use com tamanho medio e posicao
  esquerda ou direita) | passando (atravessa o fundo de relance e some; use com tamanho longe) |
  na_janela (do lado de fora, sobe devagar e aparece no vidro olhando para dentro, cabeça tombando e sorriso abrindo;
  só em sala, quarto, cozinha, janela e casa_fora) | relance (aparece por um piscar de olhos e some). tamanho "perto" = clímax: ele de corpo inteiro, grande, encarando
  com a cara bizarra (cabeça tombando, sorriso rasgando). encarando = parado, imóvel, encarando com a cara bizarra
  (ótimo "longe" no alto da escada, com o personagem embaixo paralisado de medo). teto = pendurado de cabeça para baixo
  no teto, balançando devagar (use posicao esquerda/direita, com o personagem sem perceber: o público vê, ele não).
- "objeto": null, uma pista ou uma lista com até 2: {"tipo": coleira | tigela | pelo | novelo | ratinho | pegadas |
  arranhoes | marcas_mao | arma | caixa_arma, "posicao": esquerda|centro|direita, "tamanho": medio | perto}. perto = close da pista no chão
  com a luz da lanterna (use sem personagem ou com o personagem "perto"). pegadas = trilha de patinhas de poeira indo
  para o fundo; arranhoes e marcas_mao (mãos compridas e escuras: o Abismo esteve ali) ficam na porta/janela/parede.
  Pistas da origem do Abismo: foto (foto antiga de 1987, família na frente da casa, um rosto riscado, um vulto na
  janela) | bilhete | jornal (recorte com manchete) | desenho (desenho de criança: o moço alto do sorriso). Essas
  aceitam "texto" curto (até 4 palavras), ex.: {"tipo": "bilhete", "tamanho": "perto", "texto": "NÃO DESÇA|ELE IMITA"}.
  Para um Abismo sorrateiro, prefira espiando, passando e longe parado; deixe "medio parado" e o close para o clímax.
  posicao e tamanho como no personagem; "longe" coloca a ameaça no fundo do cenário (fim do corredor, topo da escada, porta, janela).
- "gato": null ou o gato do protagonista (gato laranja de peito branco). acao: parado | andando (anda e senta) | correndo |
  sentado | miando | deitado | escondido (encolhido, olhos arregalados) | assustado (costas arqueadas, pelo eriçado) |
  olhos_escuro (no breu, só os dois olhos verdes brilhando e piscando: o Stu escondido no túnel, no poço, no vão da parede).
  posicao: esquerda | centro | direita. tamanho: longe | medio | perto (close do gato, só em cena sem o personagem).
  Fica ao lado do personagem, nunca atrás. A ação do gato acompanha o clima da frase: cenas de carinho = sentado,
  deitado ou miando; "assustado" e "escondido" só quando o perigo está perto.
- "cachorro": null ou o cão (Rufus). acao: parado | andando | correndo | brincando (vai e volta) | sentado | deitado |
  levantando_cabeca | de_pe (só o falso: em duas pernas). "falso": true = a coisa vestida com a pele dele
  (pernas compridas demais, mãos humanas, olho humano, sorriso de dentes). posicao e tamanho como no gato.
- "foco" (opcional): [x, y, zoom] = close num detalhe do cenário, aproximando devagar (ex.: a maçaneta da porta_entrada:
  [0.47, 0.49, 3.2]). Use sem personagem; com "chacoalha": true a imagem treme (a maçaneta sendo forçada).
- "efeito": nenhum | luz_piscando | tv_chiando (só na sala e no quarto, no monitor) | relampago | chuva | tremor (susto).
- "camera": zoom_in (aproxima devagar, padrão) | zoom_out | pan_esquerda | pan_direita | parada.
A animação reage sozinha à narração: palavras de medo e frases com "...", "!" ou "?" dão uma leve aproximação da câmera,
e a tensão (bordas escuras, pulsação) cresce até o fim do vídeo. Por isso, use reticências nos momentos de suspense.
Dicas: varie cenários e enquadramentos como num desenho; deixe a ameaça para a segunda metade e aumente a presença dela
até o clímax; use celular_cftv quando a história falar de câmera de segurança ou de algo visto no celular."""


# ---------------------------------------------------------------- utilidades
def _img(caminho: Path) -> Image.Image:
    if caminho not in _cache:
        _cache[caminho] = Image.open(caminho).convert("RGBA")
    return _cache[caminho]


def _sprite(nome: str, prot: str) -> Image.Image:
    pasta = PASTA_PER / "mulher" if prot == "mulher" and nome.split("_")[0] in POSES + ["maos"] else PASTA_PER
    arq = pasta / f"{nome}.png"
    if not arq.exists():
        arq = pasta / f"{nome.split('_')[0]}.png"
    return _img(arq)


def _escalado(img: Image.Image, altura: int, espelhar: bool, noturno: float) -> Image.Image:
    chave = (id(img), altura, espelhar, round(noturno, 2))
    if chave not in _cache:
        e = altura / img.height
        out = img.resize((max(1, int(img.width * e)), max(1, altura)), Image.BILINEAR)
        if espelhar:
            out = out.transpose(Image.FLIP_LEFT_RIGHT)
        if noturno:
            r, g, b, a = out.split()
            r = r.point(lambda v: int(v * (1 - 0.28 * noturno)))
            g = g.point(lambda v: int(v * (1 - 0.22 * noturno)))
            b = b.point(lambda v: int(v * (1 - 0.06 * noturno)))
            out = Image.merge("RGBA", (r, g, b, a))
        _cache[chave] = out
    return _cache[chave]


def _com_alfa(img: Image.Image, k: float) -> Image.Image:
    if k >= 0.999:
        return img
    a = img.getchannel("A").point(lambda v: int(v * max(0.0, k)))
    out = img.copy()
    out.putalpha(a)
    return out


def _sombra_chao(largura: int) -> Image.Image:
    chave = ("sombra_chao", largura)
    if chave not in _cache:
        im = Image.new("RGBA", (largura * 2, largura // 2), (0, 0, 0, 0))
        ImageDraw.Draw(im).ellipse((largura // 2, largura // 8, largura * 3 // 2, largura * 3 // 8), fill=(0, 0, 10, 130))
        _cache[chave] = im.filter(ImageFilter.GaussianBlur(10))
    return _cache[chave]


def _fonte(tam: int):
    for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, tam)
    return ImageFont.load_default()


def _suave(x: float) -> float:
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- normalização
def normalizar(cena: dict) -> None:
    """Corrige valores inválidos que a IA possa ter escrito, preenchendo padrões."""
    if cena.get("cenario") not in CENARIOS:
        cena["cenario"] = "sala"
    if cena["cenario"] == "celular_cftv" and cena.get("tela") not in META:
        cena["tela"] = "sala"
    if cena.get("efeito") not in EFEITOS:
        cena["efeito"] = "nenhum"
    if cena.get("camera") not in CAMERAS:
        antigos = {"zoom_in": "zoom_in", "zoom_out": "zoom_out", "pan_cima": "pan_esquerda", "pan_baixo": "pan_direita", "tremor": "zoom_in"}
        cena["camera"] = antigos.get(cena.get("movimento"), "zoom_in")
    p = cena.get("personagem")
    if isinstance(p, dict) and p.get("pose") in POSES + ["maos_celular"]:
        if p["pose"] == "maos_celular":  # compatibilidade com o formato antigo
            cena["cenario"], cena["personagem"] = "celular_cftv", None
        else:
            p["acao"] = p.get("acao") if p.get("acao") in ACOES_P else "parado"
            p["posicao"] = p.get("posicao") if p.get("posicao") in POSICOES else "centro"
            p["tamanho"] = p.get("tamanho") if p.get("tamanho") in TAMANHOS else "medio"
            if p.get("depois") not in POSES:
                p.pop("depois", None)
            if p["pose"] == "engatinhando":
                p.pop("vista", None)
    else:
        cena["personagem"] = None
    if META.get(cena["cenario"], {}).get("detalhe") and cena["personagem"]:
        cena["personagem"]["tamanho"] = "perto"   # cenário em close: só cabe o personagem de perto
    a = cena.get("ameaca")
    if isinstance(a, dict) and a.get("tipo") in ("sombra", "criatura", "fantasma", "olhos"):
        a["tipo"] = "abismo"                          # nomes antigos viram O Abismo
    if isinstance(a, dict) and a.get("tipo") in AMEACAS:
        a["acao"] = a.get("acao") if a.get("acao") in ACOES_A else "parada"
        a["acao"] = {"rastejando": "aproximando", "sorriso_escuro": "encarando"}.get(a["acao"], a["acao"])   # fora de uso
        a["posicao"] = a.get("posicao") if a.get("posicao") in POSICOES else "centro"
        a["tamanho"] = a.get("tamanho") if a.get("tamanho") in TAMANHOS else "longe"
        if a["acao"] == "na_janela" and not META.get(cena["cenario"], {}).get("janela"):
            a["acao"], a["tamanho"] = "espiando", "medio"     # cenário sem janela: espia pela borda
        elif a["acao"] == "na_janela":
            a["tamanho"] = "longe"
    else:
        cena["ameaca"] = None
    from .objetos import TIPOS as TIPOS_OBJ
    objs = cena.get("objeto")
    objs = objs if isinstance(objs, list) else ([objs] if isinstance(objs, dict) else [])
    objs = [o for o in objs if isinstance(o, dict) and o.get("tipo") in TIPOS_OBJ][:2]
    for o in objs:
        o["posicao"] = o.get("posicao") if o.get("posicao") in POSICOES else "centro"
        o["tamanho"] = "perto" if o.get("tamanho") == "perto" else "medio"
    cena["objeto"] = objs or None
    cao = cena.get("cachorro")
    if isinstance(cao, dict):
        cao["acao"] = cao.get("acao") if cao.get("acao") in CAO_ACOES else "parado"
        cao["posicao"] = cao.get("posicao") if cao.get("posicao") in POSICOES else "direita"
        cao["tamanho"] = cao.get("tamanho") if cao.get("tamanho") in TAMANHOS else "medio"
        cao["falso"] = bool(cao.get("falso"))
        if cao["acao"] == "de_pe":
            cao["falso"] = True
    else:
        cena["cachorro"] = None
    g = cena.get("gato")
    if isinstance(g, dict):
        g["acao"] = g.get("acao") if g.get("acao") in GATO_ACOES else "sentado"
        g["posicao"] = g.get("posicao") if g.get("posicao") in POSICOES else "direita"
        g["tamanho"] = g.get("tamanho") if g.get("tamanho") in TAMANHOS else "medio"
        if META.get(cena["cenario"], {}).get("detalhe"):
            g["tamanho"] = "perto"
        elif g["tamanho"] == "perto" and isinstance(cena.get("personagem"), dict) and cena["personagem"].get("tamanho") != "perto":
            g["tamanho"] = "medio"                    # close do gato só sozinho (senão cobre o personagem)
    else:
        cena["gato"] = None
    if META.get(cena["cenario"], {}).get("vista_de_cima"):
        cena["personagem"], cena["gato"], cena["objeto"] = None, None, None   # visto do teto: só o lugar, ninguém em pé
        if cena.get("ameaca"):
            cena["ameaca"].update(acao="passando", tamanho="longe")
    a, p = cena["ameaca"], cena["personagem"]
    alto = META.get(cena["cenario"], {}).get("fundo", [0.5, 0.6])[1] < 0.42   # fundo bem acima da cabeça (escada)
    if a and p and a["tamanho"] == "longe" and a["posicao"] == "centro" and p["posicao"] == "centro" \
            and p["tamanho"] != "longe" and not alto:
        a["_desvio"] = 0.12          # não deixa o vulto do fundo escondido atrás da cabeça do personagem


# ---------------------------------------------------------------- personagem
PASTA_V2 = PASTA_PER / "v2"
VISTAS = {"homem": ["frente", "costas", "perfil"], "mulher": ["frente", "perfil", "costas"]}


# pose pedida -> desenho usado, por personagem (quando não há desenho próprio)
APELIDOS = {"homem": {"encolhida": "gritando"}, "mulher": {"gritando": "medo"}}


def _arquivo_pose(prot: str, pose: str):
    """Caminho do desenho próprio de uma pose (medo, gritando, encolhida…) ou None."""
    if not pose or pose in ("frente", "costas", "celular", "lanterna"):
        return None
    pose = APELIDOS.get(prot, {}).get(pose, pose)
    arq = PASTA_V2 / prot / f"{pose}.png"
    return arq if arq.exists() else None


def _figura(prot: str, vista: str, piscando: bool = False, pose: str = "") -> Image.Image:
    """Figurinha dos modelos novos (assets/personagem/v2). Se existir um desenho próprio da pose
    (ex.: v2/mulher/medo.png), usa ele; senão troca pela vista mais próxima."""
    prot = prot if prot in VISTAS else "homem"
    arq = _arquivo_pose(prot, pose) if vista == "frente" else None
    if arq:
        return _img(arq)
    if vista not in VISTAS[prot]:
        vista = {"costas": "perfil", "perfil": "frente"}.get(vista, "frente")
        if vista not in VISTAS[prot]:
            vista = "frente"
    arq = PASTA_V2 / prot / f"{vista}{'_piscando' if piscando else ''}.png"
    if not arq.exists():
        arq = PASTA_V2 / prot / f"{vista}.png"
    return _img(arq)


def _luz(larg: int, alt: int, cor, alfa: int, blur: int) -> Image.Image:
    chave = ("luz", larg, alt, cor, alfa, blur)
    if chave not in _cache:
        im = Image.new("RGBA", (larg + blur * 4, alt + blur * 4), (0, 0, 0, 0))
        ImageDraw.Draw(im).ellipse((blur * 2, blur * 2, blur * 2 + larg, blur * 2 + alt), fill=cor + (alfa,))
        _cache[chave] = im.filter(ImageFilter.GaussianBlur(blur))
    return _cache[chave]


def _noite(img: Image.Image, k: float) -> Image.Image:
    """Escurece e puxa para o azul (o boneco é desenhado com cores de dia)."""
    if k <= 0:
        return img
    r, g, b, a = img.split()
    r = r.point(lambda x: int(x * (1 - 0.55 * k)))
    g = g.point(lambda x: int(x * (1 - 0.47 * k)))
    b = b.point(lambda x: int(x * (1 - 0.25 * k)))
    return Image.merge("RGBA", (r, g, b, a))


def _feixe(quadro, origem, ang, comp):
    """Feixe de luz da lanterna saindo de "origem" na direção "ang" (graus, como atan2 na imagem)."""
    comp = max(60, int(comp) // 40 * 40)
    angq = round(ang / 3) * 3
    chave = ("feixe", comp, angq)
    if chave not in _cache:
        base = Image.new("L", (comp * 2, comp * 2), 0)
        from PIL import ImageChops
        for i in range(10):
            k = i / 9
            camada = Image.new("L", base.size, 0)
            abre = math.radians(15 - 8 * k)
            alc = comp * (1 - 0.35 * k)
            ImageDraw.Draw(camada).polygon([(comp, comp), (comp + alc * math.cos(abre), comp - alc * math.sin(abre)),
                                            (comp + alc * math.cos(abre), comp + alc * math.sin(abre))], fill=13)
            base = ImageChops.add(base, camada)
        base = base.filter(ImageFilter.GaussianBlur(comp / 40)).rotate(-angq, resample=Image.BICUBIC, center=(comp, comp))
        im = Image.new("RGBA", base.size, (255, 238, 180, 0))
        im.putalpha(base)
        _cache[chave] = im
    im = _cache[chave]
    quadro.alpha_composite(im, (int(origem[0] - comp), int(origem[1] - comp)))


ESCALA_BONECO = {"longe": 0.8, "medio": 0.74, "perto": 0.95}   # o boneco tem cabeça grande: fica um pouco menor
NOITE_BONECO = 0.58


def _desenhar_boneco(quadro, p, meta, t, dur, prot, escala_tela=1.0, noturno=0.4, paralaxe=0.0, tenso=False):
    """Protagonista como boneco articulado (src/boneco.py): anda de verdade, segura objetos e muda a expressão."""
    from . import boneco as B
    cw, ch = quadro.size
    acao, pose, tam = p["acao"], p["pose"], p["tamanho"]
    esc_cen = meta.get("escala", 1.0) if tam != "perto" else 1.0       # perspectiva do cenário (ex.: casa vista de longe)
    altura = int(ch * TAMANHOS[tam] * ESCALA_BONECO.get(tam, 0.75) * escala_tela * esc_cen)
    piso = meta.get("piso", 0.9)
    fundo = meta.get("fundo", [0.5, piso, 0.4])
    if tam == "longe":
        piso = (fundo[1] + piso) / 2
    elif tam == "perto":
        piso = 1.25
    faixa = meta.get("faixa", [0.22, 0.78])
    alvo = min(max(POSICOES[p["posicao"]], faixa[0]), faixa[1]) * cw
    if (pose == "sentado" or p.get("depois") == "sentado") and tam != "perto":
        if meta.get("assento"):                       # senta EM CIMA do sofá/cama: o quadril fica na altura do assento
            ax, ay = meta["assento"]                    # ay = altura da superfície do assento (fração da tela)
            hz = meta.get("horizonte", 0.45)
            altura = int(altura * max(0.35, (ay + 0.1 - hz) / max(0.05, piso - hz)))
            pes = ay + 0.26 * altura / ch               # no boneco sentado, os pés ficam 0,26 da altura abaixo do quadril
            alvo, piso, acao = ax * cw, pes, "parado"
            p = {**p, "_no_assento": True}
        else:                                          # sem assento no cenário: fica em pé
            p = {**p, "pose": "frente"} if pose == "sentado" else {**p, "depois": None}
            pose = p["pose"]
    lado = -1 if alvo <= cw / 2 else 1
    corre = acao == "correndo"
    vel = (0.62 if corre else 0.31) * altura          # velocidade que combina com o passo (sem "deslizar")
    tipo_passo = "correndo" if corre else "andando"
    if pose == "engatinhando":                         # de quatro: vai devagar
        vel, tipo_passo = 0.12 * altura, "engatinhando"
    x, movendo, sentido, parou_em = alvo, False, 0, None
    escala, piso_mov = 1.0, piso
    if acao == "entrando":
        inicio = alvo + lado * 0.7 * cw
        T = abs(inicio - alvo) / vel
        x = inicio + (alvo - inicio) * min(1.0, t / T)
        movendo, sentido, parou_em = t < T, -lado, T
    elif acao == "saindo":
        t0 = dur * 0.3
        x = alvo + lado * max(0.0, t - t0) * vel
        movendo, sentido = t > t0, lado
    elif acao in ("andando", "correndo"):
        dist = min(0.36 * cw, vel * dur * 0.85, (faixa[1] - faixa[0]) * cw)   # não sai do chão do cenário
        T = dist / vel
        ini = min(max(alvo - lado * dist / 2, faixa[0] * cw), faixa[1] * cw)
        ini = min(max(ini, faixa[0] * cw + (dist if lado < 0 else 0)), faixa[1] * cw - (dist if lado > 0 else 0))
        x = ini + lado * min(t, T) * vel
        movendo, sentido, parou_em = t < T, lado, T
    elif acao in ("afastando", "aproximando"):
        k = _suave(t / dur) if dur else 1
        if acao == "aproximando":
            k = 1 - k
        escala = 1 - 0.45 * k                          # vai ficando menor ao se afastar
        piso_mov = piso + (fundo[1] - piso) * 0.55 * k
        x = alvo + (fundo[0] * cw - alvo) * 0.5 * k
    # medo: a expressão muda quando a ameaça surge (ou na primeira palavra forte)
    alvo_medo = {"medo": 0.75, "gritando": 1.0, "encolhida": 0.9}.get(pose, 0.35 if tenso else 0.0)
    if acao == "tremendo":
        alvo_medo = max(alvo_medo, 0.8)
    medo = alvo_medo
    muda = p.get("_muda_em")
    if pose in ("medo", "gritando") and muda is not None:
        medo = 0.15 + (alvo_medo - 0.15) * _suave((t - muda) / 0.5)
    expressao = "aterrorizado" if pose == "gritando" and medo > 0.8 else None
    parado_como = {"frente": "parado", "medo": "parado", "gritando": "parado", "encolhida": "escondido",
                   "costas": "costas", "celular": "celular", "lanterna": "lanterna", "sentado": "sentado",
                   "abrindo_porta": "abrindo_porta", "agachado": "agachado", "olhando_tras": "olhando_tras",
                   **{k: k for k in POSES_NOVAS}}.get(pose, "parado")
    espelhar_parado = x > cw / 2
    if pose == "golpeando":                            # vira para a parede mais perto (a borda da tela)
        espelhar_parado = x < cw / 2
    if acao in ("afastando", "aproximando"):
        pose_b = B.animar(acao, t, dur, medo, expressao)
    elif movendo:
        pose_b = B.animar(tipo_passo, t, dur, medo, expressao, espelhar=sentido < 0)
    elif parou_em is not None and t - parou_em < 0.4:   # acabou de parar: passa suavemente para a pose da cena
        pose_b = B.misturar(B.animar(tipo_passo, t, dur, medo, expressao, espelhar=sentido < 0),
                            B.animar(parado_como, t, dur, medo, expressao, espelhar=espelhar_parado), (t - parou_em) / 0.4)
    elif acao == "virando":
        pose_b = B.pose_cena("virando", t, dur, medo, espelhar_parado, expressao)
    else:
        depois = p.get("depois")
        pose_b = B.pose_cena(parado_como, t, dur, medo, espelhar_parado, expressao,
                             depois={"frente": "parado", "medo": "parado"}.get(depois, depois) if depois else None,
                             troca_em=p.get("troca_em", dur * 0.5) if depois else None)
    if p.get("_no_assento") and pose_b.get("sentado"):    # no sofá/cama: sem cadeira, mãos no colo
        pose_b = {**pose_b, "cadeira": False, "ombro_e": 6, "cotovelo_e": 58, "ombro_d": 4, "cotovelo_d": 62, "tronco": 2}
    if pose in ("alcancando", "debrucado") and meta.get("debrucar") and not movendo:
        bx, bpiso, bfrac = meta["debrucar"]           # junto da borda do poço, debruçado para dentro
        pose_b = B.animar("debrucado", t, dur, medo, expressao, espelhar=bx > 0.5)
        x, chao_fix, altura = bx * cw, bpiso, int(ch * bfrac)
        escala, piso_mov = 1.0, bpiso
    if pose == "golpeando" and not movendo:          # encosta na parede: o martelo bate nela, não no ar
        alcance = 0.07 * cw + altura * escala * 0.36
        x = alcance if x < cw / 2 else cw - alcance
    vista_pedida = p.get("vista") or ("costas" if pose == "olhando_cima" else None)
    de_quatro_frente = pose == "engatinhando" and vista_pedida in ("frente", "costas")
    if vista_pedida in ("frente", "costas") and pose in POSES_NOVAS:
        if de_quatro_frente:                           # de quatro visto de frente/de costas: braços abertos até o chão
            passo = math.sin(t * 2 * math.pi / 1.3)
            pose_b = {**pose_b, "vista": vista_pedida, "y": 0.0, "tronco": 0.0, "quadril_e": 0, "quadril_d": 0,
                      "joelho_e": 0, "joelho_d": 0, "ombro_e": 44 + 8 * passo, "cotovelo_e": 4,
                      "ombro_d": 44 - 8 * passo, "cotovelo_d": 4, "cab_inc": 8}
        else:
            pose_b = {**pose_b, "vista": vista_pedida}
    img, info = B.desenhar(pose_b, max(40, int(altura * escala)), prot)
    if de_quatro_frente:                               # esconde as pernas atrás do tronco e apoia as mãos no chão
        alt_b = max(40, int(altura * escala))
        px, py = info["pes"]
        ImageDraw.Draw(img).rectangle((px - alt_b * 0.075, py - alt_b * 0.38, px + alt_b * 0.075, img.height), fill=(0, 0, 0, 0))
        img = img.crop((0, 0, img.width, int(py - alt_b * 0.3)))
        info = {**info, "pes": (px, py - alt_b * 0.34 - abs(math.sin(t * 4.8)) * alt_b * 0.01)}
    img = _noite(img, NOITE_BONECO if noturno >= 0.35 else noturno)
    pes_x, pes_y = info["pes"]
    cx = x + paralaxe * cw
    chao = ch * piso_mov
    if tam != "perto" and not p.get("_no_assento"):    # sentado no sofá/cama: sem sombra no chão
        sb = _sombra_chao(int(img.width * 0.32))
        quadro.alpha_composite(sb, (int(cx - sb.width / 2), int(chao - sb.height / 2)))
    ox, oy = int(cx - pes_x), int(chao - pes_y)
    quadro.alpha_composite(img, (ox, oy))
    if "tela" in info:                                  # luz azulada do celular no rosto
        rx, ry = info["rosto"]
        luz = _luz(int(altura * escala * 0.22), int(altura * escala * 0.26), (140, 190, 255), 34, max(6, int(altura * 0.03)))
        quadro.alpha_composite(luz, (int(ox + rx - luz.width / 2), int(oy + ry - luz.height / 2)))
    if "lanterna" in info:
        (bx, by), ang = info["lanterna"]
        _feixe(quadro, (ox + bx, oy + by), ang, altura * escala * 0.95)
    if pose == "golpeando" and not movendo:
        _rachaduras(quadro, cx + (-1 if espelhar_parado else 1) * altura * escala * 0.36, chao - altura * escala * 0.66,
                    altura * escala, t)


def _rachaduras(quadro, ix, iy, alt, t):
    """Onde o martelo bate: rachaduras que crescem a cada golpe, um buraco escuro abrindo e poeira no impacto."""
    golpes = max(0, int((t - 0.24) / 0.8) + 1) if t >= 0.24 else 0
    if not golpes:
        return
    d = ImageDraw.Draw(quadro)
    rnd = random.Random(7)
    larg = max(2, int(alt * 0.012))
    for g in range(min(golpes, 6)):
        for _ in range(3):
            ang = rnd.uniform(0, 2 * math.pi)
            comp = alt * rnd.uniform(0.05, 0.11) * (1 + g * 0.25)
            pts, px, py = [(ix, iy)], ix, iy
            for _ in range(3):
                ang += rnd.uniform(-0.6, 0.6)
                px, py = px + math.cos(ang) * comp / 3, py + math.sin(ang) * comp / 3
                pts.append((px, py))
            d.line(pts, fill=(18, 14, 12, 255), width=larg)
    if golpes >= 3:                                    # a parede cede: um buraco escuro abrindo
        r = alt * min(0.09, 0.025 * (golpes - 2))
        d.ellipse((ix - r * 1.1, iy - r, ix + r * 1.1, iy + r), fill=(6, 5, 5, 255))
    fase = (t - 0.24) % 0.8
    if fase < 0.18:                                    # poeira no momento do golpe
        k = fase / 0.18
        for j in range(9):
            a = rnd.uniform(0, 2 * math.pi)
            dist = alt * 0.08 * k * rnd.uniform(0.5, 1.2)
            r = alt * 0.008 * (1 - k * 0.5)
            px, py = ix + math.cos(a) * dist, iy + math.sin(a) * dist + k * alt * 0.03
            d.ellipse((px - r, py - r, px + r, py + r), fill=(170, 160, 145, int(220 * (1 - k))))


def _desenhar_cachorro(quadro, c, meta, t, dur, paralaxe=0.0, desvio=0.0):
    """Rufus (ou o falso Rufus): cão grande, de perfil, que corre, senta, deita e, no falso, fica de pé."""
    from . import cachorro as C
    cw, ch = quadro.size
    tam, acao = c["tamanho"], c["acao"]
    esc_cen = meta.get("escala", 1.0) if tam != "perto" else 1.0
    base = {"longe": 0.13, "medio": 0.24, "perto": 0.36}[tam] * (2.3 if acao == "de_pe" else 1.0)
    if acao == "de_pe" and tam == "longe":
        base = 0.42
    altura = int(ch * base * esc_cen)
    piso = meta.get("piso", 0.9)
    fundo = meta.get("fundo", [0.5, piso, 0.4])
    if tam == "longe":
        piso = (fundo[1] + piso) / 2
    else:
        piso -= 0.03 if tam == "medio" else 0
    if tam == "perto":
        piso = 0.98
    faixa = meta.get("faixa", [0.22, 0.78])
    alvo = (min(max(POSICOES[c["posicao"]], faixa[0]), faixa[1]) + desvio) * cw
    lado = -1 if alvo <= cw / 2 else 1
    x, sentido = alvo, (1 if alvo < cw / 2 else -1)
    if acao in ("andando", "correndo", "brincando"):
        vel = (1.4 if acao != "andando" else 0.5) * altura * (0.6 if c["falso"] else 1)
        dist = min(0.5 * cw, vel * dur * 0.9)
        T = dist / vel
        ida = (t % (2 * T)) if acao == "brincando" else min(t, T)
        if acao == "brincando" and ida > T:             # vai e volta pelo quintal
            x = alvo + lado * dist / 2 - lado * (ida - T) * vel
            sentido = -lado
        else:
            x = alvo - lado * dist / 2 + lado * ida * vel
            sentido = lado
    if tam == "perto":                                  # close: virado para a direita, com a cabeça no meio da tela
        sentido = 1
        x = cw * (0.3 if acao in ("deitado", "levantando_cabeca") else 0.4)
        if acao in ("deitado", "levantando_cabeca"):
            piso = 0.86
    pose = C.animar(acao, t, dur, espelhar=sentido < 0, falso=c["falso"])
    img, info = C.desenhar(pose, max(30, altura), falso=c["falso"])
    img = _noite(img, NOITE_BONECO)
    cx, chao = x + paralaxe * cw, ch * piso
    if tam != "perto":
        sb = _sombra_chao(int(img.width * 0.5))
        quadro.alpha_composite(sb, (int(cx - sb.width / 2), int(chao - sb.height / 2)))
    quadro.alpha_composite(img, (int(cx - info["pes"][0]), int(chao - info["pes"][1])))


def _desenhar_gato(quadro, g, meta, t, dur, escala_tela=1.0, noturno=0.4, paralaxe=0.0, desvio=0.0):
    """O gato do protagonista (src/gato.py): anda, senta, mia, se esconde e se assusta."""
    from . import gato as G
    cw, ch = quadro.size
    tam, acao = g["tamanho"], g["acao"]
    esc_cen = meta.get("escala", 1.0) if tam != "perto" else 1.0
    altura = int(ch * {"longe": 0.075, "medio": 0.13, "perto": 0.42}[tam] * escala_tela * esc_cen)
    piso = meta.get("piso", 0.9)
    fundo = meta.get("fundo", [0.5, piso, 0.4])
    if tam == "longe":
        piso = (fundo[1] + piso) / 2
    else:
        piso -= 0.03 if tam == "medio" else 0           # longe da borda de baixo (a câmera corta o rodapé)
    if tam == "perto":
        piso = 0.97
        if acao in ("deitado", "escondido"):
            altura = int(altura * 1.35)
    faixa = meta.get("faixa", [0.22, 0.78])
    alvo = (min(max(POSICOES[g["posicao"]], faixa[0]), faixa[1]) + desvio) * cw
    lado = -1 if alvo <= cw / 2 else 1
    x, sentido = alvo, (1 if alvo < cw / 2 else -1)       # parado: olha para o meio da tela
    if acao in ("andando", "correndo"):
        vel = (1.6 if acao == "correndo" else 0.75) * altura
        dist = min(0.3 * cw, vel * dur * 0.8)
        T = dist / vel
        x = alvo - lado * dist / 2 + lado * min(t, T) * vel
        sentido = lado
        if t >= T:                                        # chegou: senta
            acao = "sentado"
    if acao == "olhos_escuro":                            # no breu do túnel: só dois olhos verdes, piscando
        cx, cy = x + paralaxe * cw, ch * piso - altura * 0.62
        reg = meta.get("escuro") or meta.get("porta")     # dentro do buraco escuro do cenário, onde faz sentido
        if reg:
            cx, cy = (reg[0] + reg[2] * 0.5) * cw + paralaxe * cw, (reg[1] + reg[3] * 0.55) * ch
            altura = int(reg[2] * cw * 0.55)
        r = max(3, int(altura * 0.07))
        if (t % 2.9) > 0.15:
            for lado_ in (-1, 1):
                ex = cx + lado_ * altura * 0.13
                brilho = _luz(r * 6, r * 6, (150, 255, 160), 60, 6)
                quadro.alpha_composite(brilho, (int(ex - brilho.width / 2), int(cy - brilho.height / 2)))
                ImageDraw.Draw(quadro).ellipse((ex - r, cy - r * 0.8, ex + r, cy + r * 0.8), fill=(190, 255, 170, 255))
                ImageDraw.Draw(quadro).ellipse((ex - r * 0.25, cy - r * 0.7, ex + r * 0.25, cy + r * 0.7), fill=(10, 20, 10, 255))
        return
    pose = G.animar(acao, t, dur, espelhar=sentido < 0)
    img, info = G.desenhar(pose, max(24, altura))
    img = _noite(img, NOITE_BONECO if noturno >= 0.35 else noturno)
    pes_x, pes_y = info["pes"]
    cx, chao = x + paralaxe * cw, ch * piso
    if tam == "perto":                                    # close: o rosto do gato fica no meio da tela
        cx = cw * 0.5 - (info["rosto"][0] - pes_x) + paralaxe * cw
    if tam != "perto":
        sb = _sombra_chao(int(img.width * 0.45))
        quadro.alpha_composite(sb, (int(cx - sb.width / 2), int(chao - sb.height / 2)))
    quadro.alpha_composite(img, (int(cx - pes_x), int(chao - pes_y)))


def _desenhar_personagem(quadro, p, meta, t, dur, prot, escala_tela=1.0, noturno=0.4, paralaxe=0.0, tenso=False):
    if ESTILO_PERSONAGEM == "boneco":
        return _desenhar_boneco(quadro, p, meta, t, dur, prot, escala_tela, noturno, paralaxe, tenso)
    cw, ch = quadro.size
    acao, pose = p["acao"], p["pose"]
    prog = t / dur if dur else 0
    alvo_x = POSICOES[p["posicao"]]
    lado = -1 if alvo_x <= 0.5 else 1                 # de que lado ele entra/sai
    x = alvo_x
    andando, sentido = False, 0
    if acao == "entrando":
        k = _suave(prog / 0.6)
        x = (alvo_x + lado * 0.75) * (1 - k) + alvo_x * k
        andando, sentido = k < 1, -lado
    elif acao == "saindo":
        k = _suave((prog - 0.3) / 0.7)
        x = alvo_x * (1 - k) + (alvo_x + lado * 0.8) * k
        andando, sentido = k > 0, lado
    elif acao == "andando":
        x = alvo_x - lado * 0.18 + lado * 0.36 * prog
        andando, sentido = True, lado

    vista = "costas" if pose == "costas" else "frente"
    if acao == "virando" and prog < 0.45:
        vista = "costas"
    if andando and sentido:
        vista = "perfil"
    # piscada a cada ~3,5 s, em momentos diferentes para cada cena
    fase = (t + (hash(p["pose"] + p["posicao"]) % 7) * 0.37) % 3.5
    piscando = vista != "costas" and fase < 0.12
    espelhar = vista == "perfil" and sentido > 0          # o desenho de perfil olha para a esquerda

    tam = p["tamanho"]
    altura = int(ch * TAMANHOS[tam] * escala_tela)
    piso = meta.get("piso", 0.9)
    if tam == "longe":
        piso = (meta.get("fundo", [0.5, piso])[1] + piso) / 2
    elif tam == "perto":
        piso = 1.42
    medo = pose in ("medo", "gritando", "encolhida") or acao == "tremendo"
    # expressão muda durante a cena: começa normal e, quando a ameaça aparece ou numa palavra forte, troca para a pose
    pose_arte = pose
    if pose in ("medo", "gritando") and p.get("_muda_em") is not None and t < p["_muda_em"] and prot == "mulher":
        pose_arte = "frente"      # (o desenho de terror do homem tem outra calça: ele já começa assustado)
    tem_arte = _arquivo_pose(prot, pose_arte) is not None
    img = _escalado(_figura(prot, vista, piscando, pose_arte), altura, espelhar,
                    noturno + (0.25 if medo and not tem_arte else 0))

    # vida: respiração, peso do corpo mudando de lado; mais rápida quando há perigo na cena
    periodo = 1.7 if (tenso or medo) else 3.4
    if andando:
        bob = -abs(math.sin(t * math.pi / 0.3)) * altura * 0.010
        balanco = 0.0
    else:
        bob = math.sin(t * 2 * math.pi / periodo) * altura * 0.0035
        balanco = math.sin(t * 2 * math.pi / 5.3) * altura * 0.003
    dx = balanco
    if medo:
        forca = 0.004 if acao == "tremendo" else 0.0016
        dx += (math.sin(t * 47) + 0.5 * math.sin(t * 71)) * altura * forca
    cx = int(cw * x + dx + paralaxe * cw)
    pes = int(ch * piso + bob)
    if tam != "perto":
        sb = _sombra_chao(int(img.width * 0.5))
        quadro.alpha_composite(sb, (cx - sb.width // 2, int(ch * piso) - sb.height // 2))
    topo = pes - int(img.height * PES_NO_DESENHO)
    quadro.alpha_composite(img, (cx - img.width // 2, topo))

    escala = img.height / 1200                       # medidas da figurinha (tela 1000x1200)



# ---------------------------------------------------------------- ameaça
def _abismo_animado(quadro, a, meta, t, dur, escala_tela, paralaxe, x, piso, frac, alfa):
    """O Abismo desenhado e animado a cada quadro (src/abismo_anim.py)."""
    from . import abismo_anim as AB
    cw, ch = quadro.size
    tam, acao = a["tamanho"], a["acao"]
    prog = t / dur if dur else 0
    if acao == "na_janela" and meta.get("janela"):    # do lado de fora, encostado no vidro, olhando para dentro
        jx, jy, jw, jh = meta["janela"]
        janela = (int(jx * cw), int(jy * ch), int((jx + jw) * cw), int((jy + jh) * ch))
        pose = AB.animar("bizarro", t, dur)
        pose["silhueta"] = a.get("_silhueta", False)
        alt = int(min(jh * ch * 2.1, ch * 0.75) * escala_tela)
        img, info = AB.desenhar(pose, alt)
        img = _noite(img, 0.35)
        sobe = _suave(prog / 0.5)                         # vai subindo devagar até aparecer na janela
        cx = (janela[0] + janela[2]) / 2 + (jw * cw * 0.18 if a["posicao"] == "direita" else -jw * cw * 0.18 if a["posicao"] == "esquerda" else 0)
        topo_cab = janela[1] + (janela[3] - janela[1]) * (0.75 - 0.6 * sobe)
        ox = int(cx - info["rosto"][0])
        oy = int(topo_cab - (info["rosto"][1] - alt * 0.09))
        camada = Image.new("RGBA", quadro.size, (0, 0, 0, 0))
        camada.alpha_composite(img, (ox, oy))
        mascara = Image.new("L", quadro.size, 0)
        ImageDraw.Draw(mascara).rectangle(janela, fill=int(255 * 0.85 * alfa))   # só aparece dentro do vidro
        camada.putalpha(Image.composite(camada.getchannel("A"), Image.new("L", quadro.size, 0), mascara)
                        .point(lambda v: v * 0.85))
        quadro.alpha_composite(camada)
        return
    if tam == "perto":                                 # clímax: de corpo inteiro, grande, com a cara bizarra
        pose = AB.animar("bizarro", t, dur)
        pose["silhueta"] = a.get("_silhueta", False)
        cresce = 1 + (0.12 * _suave(prog) if acao == "aproximando" else 0.03 * prog)
        altura = ch * 0.66 * cresce * escala_tela
        img, info = AB.desenhar(pose, int(altura))
        img = _com_alfa(_noite(img, 0.25), alfa)
        cx, chao = cw * (0.5 + (x - 0.5) * 0.4) + paralaxe * cw * 0.4, ch * 0.985
        ox, oy = int(cx - info["pes"][0]), int(chao - info["pes"][1])
        bb = img.getbbox() or (0, 0, img.width, img.height)
        _aura(quadro, ox + (bb[0] + bb[2]) / 2, oy + (bb[1] + bb[3]) / 2, (bb[2] - bb[0]) * 2.0, (bb[3] - bb[1]) * 1.3, alfa)
        quadro.alpha_composite(img, (ox, oy))
        return
    if acao == "teto":                                  # pendurado de cabeça para baixo no teto, balançando devagar
        pose = AB.animar("observando", t, dur)
        pose["silhueta"] = a.get("_silhueta", False)
        alt = int(ch * (0.55 if tam != "longe" else 0.3) * escala_tela)
        img, info = AB.desenhar(pose, alt)
        img = _com_alfa(_noite(img, 0.25), alfa).transpose(Image.FLIP_TOP_BOTTOM)
        img = img.rotate(math.sin(t * 0.9) * 4, resample=Image.BICUBIC, center=(img.width / 2, 0), expand=False)
        cx = cw * x + paralaxe * cw * 0.4
        topo = ch * (0.0 if tam != "longe" else 0.14) - (img.height - info["pes"][1])   # os pés grudados no teto
        bb = img.getbbox() or (0, 0, img.width, img.height)
        _aura(quadro, cx, topo + (bb[1] + bb[3]) / 2, (bb[2] - bb[0]) * 2.0, (bb[3] - bb[1]) * 1.3, alfa)
        quadro.alpha_composite(img, (int(cx - info["pes"][0]), int(topo)))
        return
    if acao == "sorriso_escuro":                        # no breu da passagem: só olhos e dentes, parados, sem rosto
        escuro = Image.new("RGBA", quadro.size, (0, 0, 0, int(120 * alfa)))
        quadro.alpha_composite(escuro)
        reg = meta.get("porta")
        if reg and tam != "perto":
            cx, cy = (reg[0] + reg[2] / 2) * cw, (reg[1] + reg[3] * 0.45) * ch
            larg = reg[2] * cw * (1.1 if tam == "medio" else 0.7)
        else:
            cx, cy = cw * x, ch * 0.45
            larg = cw * (0.3 if tam == "longe" else 0.5 if tam == "medio" else 0.8)
        cx += paralaxe * cw * 0.4
        surge = _suave(prog / 0.35)
        camada = Image.new("RGBA", quadro.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(camada)
        tranco = (int(t * 24) % 37) in (0, 1)           # de vez em quando a imagem dá um tranco, como se estalasse
        jx = (larg * 0.04 if tranco else 0)
        ro = larg * 0.11
        for lado_ in (-1, 1):                           # olhos arregalados, pupilas minúsculas, um maior que o outro
            ex, ey = cx + lado_ * larg * 0.24 + jx, cy - larg * 0.08 + (lado_ * larg * 0.02)
            r = ro * (1.15 if lado_ > 0 else 0.92)
            d.ellipse((ex - r, ey - r, ex + r, ey + r), fill=(236, 232, 222, 255))
            d.ellipse((ex - r * 0.16, ey - r * 0.16, ex + r * 0.16, ey + r * 0.16), fill=(8, 8, 8, 255))
        gargalha = 0.55 + 0.45 * abs(math.sin(t * 7.5)) if 0.35 < prog < 0.85 else 0.35   # a boca treme gargalhando
        gy, gw, gh = cy + larg * 0.22, larg * 0.62, larg * 0.16 * gargalha
        d.chord((cx - gw + jx, gy - gh, cx + gw + jx, gy + gh * 1.6), 0, 180, fill=(236, 232, 222, 255))
        d.chord((cx - gw * 0.86 + jx, gy - gh * 0.3, cx + gw * 0.86 + jx, gy + gh * 1.25), 0, 180, fill=(30, 6, 8, 255))
        for k in range(1, 26):                           # dentes demais
            tx = cx - gw + jx + k * (2 * gw / 26)
            d.line((tx, gy, tx, gy + gh * 1.5 * math.sin(math.pi * k / 26)), fill=(150, 140, 130, 255), width=max(2, int(larg * 0.008)))
        d.line((cx - gw + jx, gy, cx + gw + jx, gy), fill=(150, 140, 130, 255), width=max(2, int(larg * 0.008)))
        brilho = _luz(int(larg * 1.8), int(larg * 1.2), (200, 210, 255), int(28 * surge * alfa), 30)
        quadro.alpha_composite(brilho, (int(cx - brilho.width / 2), int(cy - brilho.height / 2)))
        quadro.alpha_composite(_com_alfa(camada, alfa * surge * (0.8 if tranco else 1.0)))
        return
    if acao == "rastejando":                            # de quatro, de frente, vem do fundo devagar, cada vez mais perto
        fundo = meta.get("fundo", [0.5, meta.get("piso", 0.9), 0.3])
        k = _suave(prog)
        pose = AB.animar("parado", t, dur)
        passo = math.sin(t * 3.4)
        pose.update(vista="frente", ombro_e=42 + 12 * passo, cotovelo_e=-14, ombro_d=42 - 12 * passo, cotovelo_d=-14,
                    cab_inc=pose.get("cab_inc", 0) * 1.4 + 14, dedos=1.0)
        pose["silhueta"] = a.get("_silhueta", False)
        alt = int(ch * (fundo[2] * 1.3 + (0.62 - fundo[2] * 1.3) * k) * escala_tela)
        chao = ch * (fundo[1] + (min(meta.get("piso", 0.9), 0.98) - fundo[1]) * k)
        img, info = AB.desenhar(pose, alt)
        px, py = info["pes"]                              # esconde as pernas (ficam atrás do tronco, de quatro)
        quadril = int(py - alt * 0.46)
        ImageDraw.Draw(img).rectangle((px - alt * 0.11, quadril, px + alt * 0.11, img.height), fill=(0, 0, 0, 0))
        img = img.crop((0, 0, img.width, int(py - alt * 0.27)))
        img = _com_alfa(_noite(img, 0.25), alfa)
        cx = cw * (fundo[0] + (x - fundo[0]) * k) + paralaxe * cw * 0.4
        ox = int(cx - px)
        oy = int(chao - (py - alt * 0.33) + abs(passo) * alt * 0.015)   # as mãos apoiadas no chão
        bb = img.getbbox() or (0, 0, img.width, img.height)
        _aura(quadro, ox + (bb[0] + bb[2]) / 2, oy + (bb[1] + bb[3]) / 2, (bb[2] - bb[0]) * 2.0, (bb[3] - bb[1]) * 1.4, alfa)
        quadro.alpha_composite(img, (ox, oy))
        return
    espelhar = x > 0.5                                  # agachado ou atacando: virado para o meio da cena
    if acao == "passando":                              # atravessa o fundo de relance
        movimento = "andando"
    elif acao == "encarando":                           # parado, imóvel, encarando com a cara bizarra
        movimento = "bizarro"
    elif acao == "espiando":                            # só a cabeça e o ombro aparecem pela borda, a cabeça estala
        movimento = "parado"
    elif acao == "aproximando":
        movimento = "ataque" if tam == "medio" else "andando"
    elif tam == "medio" and acao == "parada":
        movimento = "observando"
    else:
        movimento = "parado"
    if tam == "longe":
        altura = ch * frac * 1.2
    else:
        altura = ch * (0.46 if movimento != "observando" else 0.54)
        piso = min(meta.get("piso", 0.9), 0.97)
    if acao == "aproximando":
        altura *= 1 + 0.3 * _suave(prog)
        x = x + (0.5 - x) * 0.35 * _suave(prog)
    if acao == "aparecendo" and alfa < 0.95 and int(t * 24) % 5 == 0:
        alfa = min(1.0, alfa * 2.2)                     # pisca entre aparecer e sumir antes de ficar
    if acao == "passando":
        espelhar = a.get("_sentido", 1) < 0
    silhueta = a.get("_silhueta", False)
    pose = AB.animar(movimento, t, dur, espelhar=(espelhar and movimento != "parado" and movimento != "andando")
                     or (acao == "passando" and espelhar))
    pose["silhueta"] = silhueta
    img, info = AB.desenhar(pose, int(altura * escala_tela))
    img = _com_alfa(_noite(img, 0.25), alfa)
    cx = cw * x + paralaxe * cw * 0.4
    chao = ch * piso
    ox, oy = int(cx - info["pes"][0]), int(chao - info["pes"][1])
    bb = img.getbbox() or (0, 0, img.width, img.height)
    _aura(quadro, ox + (bb[0] + bb[2]) / 2, oy + (bb[1] + bb[3]) / 2, (bb[2] - bb[0]) * 2.0, (bb[3] - bb[1]) * 1.4,
          alfa * (0.85 + 0.15 * math.sin(t * 1.1)))
    sb = _sombra_chao(int((bb[2] - bb[0]) * 0.6))
    quadro.alpha_composite(_com_alfa(sb, alfa), (int(cx - sb.width / 2), int(chao - sb.height / 2)))
    quadro.alpha_composite(img, (ox, oy))


def _desenhar_ameaca(quadro, a, meta, t, dur, escala_tela=1.0, paralaxe=0.0):
    cw, ch = quadro.size
    prog = t / dur if dur else 0
    alfa = 1.0
    if a["acao"] == "aparecendo":
        alfa = _suave(prog / 0.5)
    elif a["acao"] == "sumindo":
        alfa = 1 - _suave((prog - 0.5) / 0.5)
    tam = a["tamanho"]
    frac = TAMANHOS[tam]
    fundo = meta.get("fundo", [0.5, meta.get("piso", 0.9), 0.4])
    if tam == "longe":
        x, piso, frac = (fundo[0] if a["posicao"] == "centro" else POSICOES[a["posicao"]]), fundo[1], fundo[2]
        x += a.get("_desvio", 0)
        if fundo[1] < 0.42 and a["acao"] != "passando":
            x = fundo[0]                               # no alto da escada: sempre no meio do patamar
    else:
        x, piso = POSICOES[a["posicao"]], (meta.get("piso", 0.9) if tam == "medio" else 1.3)
    if a["acao"] == "aproximando":
        k = _suave(prog)
        frac = frac * (1 + 0.9 * k)
        piso = piso + (min(1.25, piso + 0.25) - piso) * k
        x = x + (0.5 - x) * 0.5 * k
    elif a["acao"] == "passando":
        # cruza o fundo de um lado ao outro no meio da cena e some: só um relance
        k = (prog - 0.1) / 0.8                           # atravessa devagar, quase a cena inteira
        sentido = -1 if a["posicao"] == "direita" else 1
        a["_sentido"] = sentido
        x = (0.05 + 0.9 * k) if sentido > 0 else (0.95 - 0.9 * k)
        alfa = 0.0 if k < 0 or k > 1 else min(1.0, k / 0.15, (1 - k) / 0.15) * 0.9
    elif a["acao"] == "relance":                         # aparece num piscar (uns 2 quadros) e some
        alfa = 0.95 if 0.44 <= prog <= 0.47 else 0.0
    elif a["acao"] == "espiando":
        # surge devagar pela borda da tela (ou do batente), espia e recua um pouco no fim
        lado = -1 if a["posicao"] == "esquerda" else 1
        k = _suave(prog / 0.45) - 0.35 * _suave((prog - 0.8) / 0.2)
        borda = 0.0 if lado < 0 else 1.0
        x = borda + lado * (0.12 - 0.22 * k) if tam != "longe" else x
        alfa = 0.95

    if a["tipo"] == "olhos":
        regiao = meta.get("porta") or meta.get("janela") or meta.get("espelho")
        larg = int(cw * (0.22 if tam == "longe" else 0.4 if tam == "medio" else 0.7) * escala_tela)
        if a["acao"] == "aproximando":
            larg = int(larg * (1 + 0.8 * _suave(prog)))
        if regiao and tam == "longe":
            cx, cy = (regiao[0] + regiao[2] / 2) * cw, (regiao[1] + regiao[3] * 0.4) * ch
        else:
            cx, cy = x * cw, ch * 0.45
        cx += paralaxe * cw * 0.4
        base = _sprite("olhos", "homem")
        img = _escalado(base, int(larg * base.height / base.width), False, 0)
        if (t % 2.7) < 0.12:                       # piscada
            img = img.resize((img.width, max(1, img.height // 6)))
        pulso = 0.82 + 0.18 * math.sin(t * 3)
        brilho = _luz(int(img.width * 0.55), int(img.height * 0.9), (170, 150, 255), int(35 * pulso * alfa), 14)
        quadro.alpha_composite(brilho, (int(cx - brilho.width / 2), int(cy - brilho.height / 2)))
        img = _com_alfa(img, alfa * pulso)
        quadro.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))
        return

    if a["tipo"] == "invasor":
        # pessoa de capa amarela e capuz, com machado: fica no chão, respira, anda quando se aproxima
        if tam == "longe":
            altura = int(ch * frac * 1.05 * escala_tela)
        else:
            altura = int(ch * {"medio": 0.62, "perto": 1.05}[tam] * escala_tela)
            if a["acao"] == "aproximando":
                altura = int(altura * (1 + 0.5 * _suave(prog)))
            piso = meta.get("piso", 0.9) if tam == "medio" else 1.38
        img = _escalado(_img(PASTA_V2 / "invasor.png"), altura, x > 0.5, 0.65)
        andando = a["acao"] == "aproximando"
        bob = (-abs(math.sin(t * math.pi / 0.42)) * 0.008 if andando else math.sin(t * 2 * math.pi / 4.1) * 0.003) * altura
        img = _com_alfa(img, alfa)
        cx = int(cw * x + paralaxe * cw * 0.4)
        pes = int(ch * piso + bob)
        if tam != "perto":
            sb = _sombra_chao(int(img.width * 0.45))
            quadro.alpha_composite(_com_alfa(sb, alfa), (cx - sb.width // 2, int(ch * piso) - sb.height // 2))
        quadro.alpha_composite(img, (cx - img.width // 2, pes - int(img.height * PES_NO_DESENHO)))
        return

    if ESTILO_PERSONAGEM == "boneco":
        return _abismo_animado(quadro, a, meta, t, dur, escala_tela, paralaxe, x, piso, frac, alfa)

    # O ABISMO: silhueta preta com rosto pálido e sorriso enorme. Fica no chão, quase parado; é o silêncio que assusta.
    if tam == "perto":
        # close do rosto: aproxima devagar e dá pequenos "saltos" de imagem, como se a câmera falhasse
        base = _img(PASTA_V2 / "abismo" / "rosto.png")
        cresce = 1 + (0.18 * _suave(prog) if a["acao"] == "aproximando" else 0.06 * prog)
        altura = int(ch * 0.62 * cresce * escala_tela)
        img = _escalado(base, altura, False, 0.35)
        salto = (int(t * 24) % 31) in (0, 1)
        dx = (9 if salto else 0) + math.sin(t * 1.3) * altura * 0.004
        img = _com_alfa(img, alfa * (0.75 if salto else 1.0))
        _aura(quadro, cw * x + dx, ch * 0.46, img.width * 1.9, img.height * 1.5, alfa)
        quadro.alpha_composite(img, (int(cw * x - img.width / 2 + dx), int(ch * 0.46 - img.height / 2)))
        return
    if a["acao"] == "aproximando":
        pose = "ataque"
    elif tam == "medio" and a["acao"] == "parada":
        pose = "observando"
    else:
        pose = "frente"
    if tam == "longe":
        altura = int(ch * frac * 1.05 * escala_tela)
    else:
        altura = int(ch * 0.62 * escala_tela * (1 + 0.45 * _suave(prog) if a["acao"] == "aproximando" else 1))
        piso = min(meta.get("piso", 0.9), 0.97)
    espelhar = pose != "frente" and x > 0.5             # agachado/atacando: virado para o meio da cena
    img = _escalado(_img(PASTA_V2 / "abismo" / f"{pose}.png"), altura, espelhar, 0.1)
    andando = a["acao"] == "aproximando"
    bob = (-abs(math.sin(t * math.pi / 0.5)) * 0.007 if andando else math.sin(t * 2 * math.pi / 5.0) * 0.002) * altura
    # ao surgir: pisca entre aparecer e sumir algumas vezes antes de ficar
    if a["acao"] == "aparecendo" and alfa < 0.95 and int(t * 24) % 5 == 0:
        alfa = min(1.0, alfa * 2.2)
    img = _com_alfa(img, alfa)
    cx = int(cw * x + paralaxe * cw * 0.4)
    pes = int(ch * piso + bob)
    topo = pes - int(img.height * PES_NO_DESENHO)
    bb = img.getbbox() or (0, 0, img.width, img.height)
    corpo_h = bb[3] - bb[1]
    pulso_aura = 0.85 + 0.15 * math.sin(t * 1.1)
    _aura(quadro, cx, topo + (bb[1] + bb[3]) / 2, (bb[2] - bb[0]) * 2.4, corpo_h * 1.5, alfa * pulso_aura)
    sb = _sombra_chao(int(img.width * 0.4))
    quadro.alpha_composite(_com_alfa(sb, alfa), (cx - sb.width // 2, int(ch * piso) - sb.height // 2))
    quadro.alpha_composite(img, (cx - img.width // 2, topo))


def _mascara_oval(w, h, borda=0.18):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).ellipse((w * borda / 2, h * borda / 2, w * (1 - borda / 2), h * (1 - borda / 2)), fill=255)
    return m.filter(ImageFilter.GaussianBlur(max(2, int(min(w, h) * borda / 3))))


def _animar_especial(img, an, t, dur):
    """Cenas especiais desenhadas prontas: a boca gargalha no escuro / a cabeça estala enquanto ele rasteja."""
    cw, ch = img.size
    prog = t / dur if dur else 0
    if an["tipo"] == "gargalhada":
        x, y, w, h = an["boca"]
        caixa = (int(x * cw), int((y - h * 0.3) * ch), int((x + w) * cw), int((y + h * 1.4) * ch))
        bw, bh = caixa[2] - caixa[0], caixa[3] - caixa[1]
        rindo = 0.3 < prog < 0.9
        abre = (0.1 + 0.16 * abs(math.sin(t * 9.0))) if rindo else 0.03 * abs(math.sin(t * 1.3))
        meio = int(bh * 0.45)                          # a mandíbula: a metade de baixo desce e volta, como numa gargalhada
        queixo = img.crop((caixa[0], caixa[1] + meio, caixa[2], caixa[3]))
        novo = queixo.resize((bw, int(queixo.height * (1 + abre))), Image.BICUBIC)
        img.paste(novo, (caixa[0], caixa[1] + meio), _mascara_oval(novo.width, novo.height, 0.35))
    elif an["tipo"] == "partes":                       # várias partes: cabeça que estala, gato que balança...
        for parte in an["partes"]:
            x, y, w, h = parte["regiao"]
            caixa = (int(x * cw), int(y * ch), int((x + w) * cw), int((y + h) * ch))
            if parte["modo"] == "estalo":
                rnd = random.Random(int(t * 1.5))
                if (t * 1.5) % 1.0 >= 0.12:              # só no estalo (2 ou 3 quadros): parece a imagem "pular"
                    continue
                ang = rnd.choice((-1, 1)) * 8
            elif parte["modo"] == "tremor":              # tremendo de medo (o Stu encolhido no túnel)
                ang = math.sin(t * 23.0) * 0.9 + math.sin(t * 2.1) * 0.6
            else:                                        # balanço de algo pendurado (o Stu se debatendo)
                ang = math.sin(t * 2.6) * 3.2 + math.sin(t * 7.1) * 0.8
            peca = img.crop(caixa)
            piv = (parte["pivo"][0] * cw - caixa[0], parte["pivo"][1] * ch - caixa[1])
            img.paste(peca.rotate(ang, resample=Image.BICUBIC, center=piv), caixa[:2], _mascara_oval(peca.width, peca.height, 0.28))
    elif an["tipo"] == "rastejando":
        x, y, w, h = an["cabeca"]
        caixa = (int(x * cw), int(y * ch), int((x + w) * cw), int((y + h) * ch))
        rnd = random.Random(int(t * 1.7))
        estalo = (t * 1.7) % 1.0 < 0.12                # de tempos em tempos a cabeça estala para o lado
        if not estalo:
            return
        ang = rnd.choice((-1, 1)) * 9
        cab = img.crop(caixa)
        piv = (an["pescoco"][0] * cw - caixa[0], an["pescoco"][1] * ch - caixa[1])
        girada = cab.rotate(ang, resample=Image.BICUBIC, center=piv, fillcolor=None)
        img.paste(girada, caixa[:2], _mascara_oval(cab.width, cab.height, 0.3))


# ---------------------------------------------------------------- efeitos
def _ruido(w, h, seed):
    return Image.frombytes("L", (w, h), random.Random(seed).randbytes(w * h)).convert("RGBA")


def _tv(quadro, meta, t, n):
    if "tv" not in meta:
        return
    cw, ch = quadro.size
    x, y, w, h = meta["tv"]
    box = (int(x * cw), int(y * ch), int(w * cw), int(h * ch))
    ru = _ruido(box[2] // 4, box[3] // 4, n).resize((box[2], box[3]), Image.NEAREST)
    ru = Image.blend(ru, Image.new("RGBA", ru.size, (150, 190, 255, 255)), 0.35)
    quadro.alpha_composite(ru, box[:2])
    luz = Image.new("RGBA", (box[2] * 3, box[3] * 3), (0, 0, 0, 0))
    ImageDraw.Draw(luz).ellipse((0, 0, luz.width, luz.height), fill=(140, 180, 255, int(40 + 25 * math.sin(t * 17))))
    luz = luz.filter(ImageFilter.GaussianBlur(60))
    quadro.alpha_composite(luz, (box[0] - box[2], box[1] - box[3]))


def _chuva(quadro, meta, t, n):
    cw, ch = quadro.size
    reg = meta.get("janela")
    if reg:
        x0, y0, x1, y1 = reg[0] * cw, reg[1] * ch, (reg[0] + reg[2]) * cw, (reg[1] + reg[3]) * ch
    else:
        x0, y0, x1, y1 = 0, 0, cw, ch * 0.75
    camada = Image.new("RGBA", quadro.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    rnd = random.Random(n)
    for _ in range(int((x1 - x0) * (y1 - y0) / 9000) + 10):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        d.line((x, y, x - 8, y + 40), fill=(190, 210, 255, 120), width=3)
    quadro.alpha_composite(camada)


def _brilho(quadro: Image.Image, k: float, cor=(0, 0, 0)) -> Image.Image:
    return Image.blend(quadro, Image.new("RGBA", quadro.size, cor + (255,)), k)


# ---------------------------------------------------------------- cena celular_cftv
def _tela_cftv(cena, t, dur, prot, n, tam):
    """Mini cena vista pela câmera de segurança (tons de cinza esverdeados, linhas, REC)."""
    tela = cena.get("tela", "sala")
    mini = _img(PASTA_CEN / f"{tela}.png").copy()
    meta = META[tela]
    if cena.get("personagem"):
        _desenhar_personagem(mini, cena["personagem"], meta, t, dur, prot, noturno=0.3)
    if cena.get("ameaca"):
        _desenhar_ameaca(mini, cena["ameaca"], meta, t, dur)
    mini = mini.resize(tam, Image.BILINEAR).convert("L").convert("RGBA")
    mini = Image.blend(mini, Image.new("RGBA", tam, (60, 120, 80, 255)), 0.25)
    d = ImageDraw.Draw(mini)
    for y in range(0, tam[1], 6):
        d.line((0, y, tam[0], y), fill=(0, 0, 0, 60))
    f = _fonte(max(14, tam[0] // 14))
    if int(t * 2) % 2 == 0:
        d.ellipse((14, 14, 34, 34), fill=(230, 40, 40, 255))
    d.text((42, 10), "REC", font=f, fill=(240, 240, 240, 255))
    d.text((14, tam[1] - f.size - 16), f"CAM 02   03:{(17 + int(t)) % 60:02d}", font=f, fill=(240, 240, 240, 255))
    return mini


def _quadro_cftv(cena, t, dur, prot, n):
    if "fundo_cftv" not in _cache:
        _cache["fundo_cftv"] = _brilho(_img(PASTA_CEN / "sala.png").filter(ImageFilter.GaussianBlur(14)), 0.55)
    fundo = _cache["fundo_cftv"].copy()
    maos = _sprite("maos_celular", prot)
    e = (CW * 1.0) / maos.width
    mw, mh = int(maos.width * e), int(maos.height * e)
    ox, oy = (CW - mw) // 2, CH - mh + int(mh * 0.04) + int(math.sin(t * 2.2) * 6)
    # área da tela dentro do desenho das mãos (x 335..665, y 185..835 em 1000x1200)
    sx, sy, sw, sh = ox + int(335 * e), oy + int(185 * e), int(330 * e), int(650 * e)
    fundo.alpha_composite(_escalado(maos, mh, False, 0.35), (ox, oy))
    fundo.alpha_composite(_tela_cftv(cena, t, dur, prot, n, (sw, sh)), (sx, sy))
    luz = Image.new("RGBA", (sw * 2, sh), (0, 0, 0, 0))
    ImageDraw.Draw(luz).ellipse((0, 0, sw * 2, sh), fill=(170, 220, 255, 45))
    fundo.alpha_composite(luz.filter(ImageFilter.GaussianBlur(40)), (sx - sw // 2, sy - sh // 3))
    return fundo


ESCURIDAO = 0.30      # quanto os cenários escurecem (0 = original, 0.5 = bem escuro)


def _cenario_escuro(nome: str) -> Image.Image:
    """Cenário escurecido e puxado para o azul-noite; luzes fortes (abajur, poste, TV) quase não perdem brilho."""
    chave = ("cen_escuro", nome)
    if chave not in _cache:
        import numpy as np
        a = np.asarray(_img(PASTA_CEN / f"{nome}.png")).astype(float)
        rgb = a[:, :, :3]
        lum = rgb.mean(axis=2, keepdims=True) / 255
        k = 1 - ESCURIDAO * (1 - lum ** 2)            # partes escuras escurecem mais que as luzes
        rgb = rgb * k * np.array([0.92, 0.95, 1.04])
        _cache[chave] = Image.fromarray(np.dstack([rgb.clip(0, 255), a[:, :, 3:]]).astype("uint8"))
    return _cache[chave]


def _aura(quadro, cx, cy, larg, alt, forca):
    """Mancha de escuridão em volta de uma ameaça, como se ela engolisse a luz."""
    if forca <= 0.01:
        return
    lq, aq = max(40, int(larg) // 40 * 40), max(40, int(alt) // 40 * 40)      # tamanhos arredondados: reaproveita
    chave = ("aura", lq, aq)
    if chave not in _cache:
        pw, ph = lq // 4 + 40, aq // 4 + 40                                  # desenha pequeno e amplia (rápido)
        m = Image.new("L", (pw, ph), 0)
        ImageDraw.Draw(m).ellipse((20, 20, pw - 20, ph - 20), fill=215)
        m = m.filter(ImageFilter.GaussianBlur(max(4, lq // 4 // 6))).resize((pw * 4, ph * 4), Image.BILINEAR)
        im = Image.new("RGBA", m.size, (0, 0, 4, 0))
        im.putalpha(m)
        _cache[chave] = im
    m = _com_alfa(_cache[chave], min(1.0, forca))
    quadro.alpha_composite(m, (int(cx - m.width / 2), int(cy - m.height / 2)))


# ---------------------------------------------------------------- ritmo da narração
PALAVRAS_FORTES = {
    "porta", "atrás", "atras", "sombra", "vulto", "olhos", "olhando", "alguém", "alguem", "ninguém", "ninguem",
    "passos", "grito", "gritou", "silêncio", "silencio", "apagou", "apagaram", "escuro", "escuridão", "sozinho",
    "sozinha", "sangue", "voz", "nome", "parou", "batida", "batidas", "bateu", "rangeu", "respiração", "sussurro",
    "sussurrou", "embaixo", "debaixo", "dentro", "janela", "espelho", "corre", "corra", "fuja", "agora", "nunca",
    "morto", "morta", "sorriu", "sorriso", "abriu", "trancada", "trancado", "câmera", "camera", "mexeu", "vindo",
}


def _acentos(cena: dict) -> list:
    """Momentos (segundos) das palavras de impacto da narração desta cena: palavras de medo e
    palavras seguidas de reticências, exclamação ou interrogação. Mínimo de 1,6 s entre um e outro."""
    if "_acentos" in cena:
        return cena["_acentos"]
    palavras = cena.get("_palavras") or []
    fichas = (cena.get("narracao") or "").split()
    usar_pont = len(fichas) == len(palavras)
    tempos = []
    for i, w in enumerate(palavras):
        limpa = w["texto"].lower().strip(".,;:!?…\"'()")
        forte = limpa in PALAVRAS_FORTES
        if usar_pont and any(fichas[i].endswith(p) for p in ("...", "…", "!", "?")):
            forte = True
        if forte and (not tempos or w["inicio"] - tempos[-1] >= 1.6):
            tempos.append(w["inicio"])
    cena["_acentos"] = tempos
    return tempos


def _envelope(t: float, tempos: list) -> float:
    """0..1: sobe rápido no início da palavra forte e some devagar em ~1 s."""
    v = 0.0
    for ta in tempos:
        d = t - ta
        if -0.3 < d < 2.2:
            v = max(v, _suave((d + 0.3) / 0.3) if d < 0 else math.exp(-d * 1.6))
    return v


def _batimento(t: float, bpm: float) -> float:
    """Pulso duplo de coração (tum-tum), 0..1."""
    f = (t * bpm / 60) % 1
    return math.exp(-((f - 0.05) / 0.04) ** 2) + 0.6 * math.exp(-((f - 0.22) / 0.04) ** 2)


def _vinheta(k: float) -> Image.Image:
    """Máscara de bordas escuras (quantizada para reaproveitar)."""
    k = round(min(0.95, max(0.0, k)) * 20) / 20
    chave = ("vinheta", k)
    if chave not in _cache:
        if "vinheta_base" not in _cache:
            m = Image.new("L", (W // 4, H // 4), 0)
            ImageDraw.Draw(m).ellipse((-W // 10, -H // 14, W // 4 + W // 10, H // 4 + H // 14), fill=255)
            _cache["vinheta_base"] = m.filter(ImageFilter.GaussianBlur(70)).resize((W, H), Image.BILINEAR)
        _cache[chave] = _cache["vinheta_base"].point(lambda v: int((255 - v) * k))
    return _cache[chave]


def _poeira(img: Image.Image, t: float, semente: int, quantidade: int = 22):
    """Partículas de poeira flutuando devagar na luz (bem discretas)."""
    rnd = random.Random(semente)
    d = ImageDraw.Draw(img, "RGBA")
    cw, ch = img.size
    for _ in range(quantidade):
        x0, y0 = rnd.uniform(0, cw), rnd.uniform(0, ch)
        vx, vy = rnd.uniform(-9, 9), rnd.uniform(-16, -4)
        fase, r = rnd.uniform(0, 6.28), rnd.uniform(1.4, 3.2)
        x = (x0 + vx * t + math.sin(t * 0.8 + fase) * 14) % cw
        y = (y0 + vy * t) % ch
        a = int(10 + 24 * (0.5 + 0.5 * math.sin(t * 1.1 + fase)))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(200, 210, 240, a))


# ---------------------------------------------------------------- quadro completo
ESCURIDAO_ILUSTRADO = 0.12     # as ilustrações já vêm noturnas: só um toque a mais de sombra


def _ilustracao(caminho: str) -> Image.Image:
    """Ilustração do plano ajustada à tela 1188x2112 (corta as sobras) e levemente escurecida."""
    chave = ("ilustr", caminho)
    if chave not in _cache:
        import numpy as np
        im = Image.open(caminho).convert("RGB")
        e = max(CW / im.width, CH / im.height)
        im = im.resize((math.ceil(im.width * e), math.ceil(im.height * e)), Image.LANCZOS)
        x0, y0 = (im.width - CW) // 2, (im.height - CH) // 2
        im = im.crop((x0, y0, x0 + CW, y0 + CH))
        a = np.asarray(im).astype(float)
        lum = a.mean(axis=2, keepdims=True) / 255
        a = a * (1 - ESCURIDAO_ILUSTRADO * (1 - lum ** 2))
        for velho in [c for c in _cache if isinstance(c, tuple) and c[0] == "ilustr"]:
            del _cache[velho]                       # guarda só a ilustração atual (os planos vêm em sequência)
        _cache[chave] = Image.fromarray(a.clip(0, 255).astype("uint8")).convert("RGBA")
    return _cache[chave]


def _quadro_ilustrado(cena: dict, t: float, dur: float, n: int) -> Image.Image:
    """Plano ilustrado: a imagem com câmera lenta, poeira, efeitos de luz, reação às palavras fortes e vinheta."""
    prog = t / dur if dur else 0
    k = _suave(prog)
    cam, ef = cena.get("camera", "zoom_in"), cena.get("efeito", "nenhum")
    tensao = float(cena.get("_progresso", 0.5))
    acento = _envelope(t, _acentos(cena))
    img = _ilustracao(cena["_img"]).copy()
    if ef == "chuva":
        _chuva(img, {}, t, n)
    _poeira(img, t, hash(cena.get("lugar", "")) % 1000, 14)
    if ef == "luz_piscando" and random.Random(n // 2).random() < 0.18:
        img = _brilho(img, 0.55)
    elif ef == "relampago":
        for pico in (0.3, 0.38, 0.75):
            d = abs(prog - pico) * dur if dur else 9
            if d < 0.08:
                img = _brilho(img, 0.55 * (1 - d / 0.08), (235, 240, 255))
    z, px, py = 1.0, 0.5, 0.5
    if cam == "zoom_in":
        z = 1 + 0.09 * k
    elif cam == "zoom_out":
        z = 1.09 - 0.09 * k
    elif cam == "pan_esquerda":
        z, px = 1.04, 0.8 - 0.6 * k
    elif cam == "pan_direita":
        z, px = 1.04, 0.2 + 0.6 * k
    z *= 1 + 0.012 * acento
    if cena.get("ameaca") and tensao > 0.5:
        z *= 1 + 0.0015 * _batimento(t, 62 + 24 * tensao)
    cw, chh = W / z, H / z
    x0, y0 = (CW - cw) * px, (CH - chh) * py
    if ef == "tremor":
        k_tr = math.exp(-t * 1.5)
        x0 += math.sin(t * 23) * 3.5 * k_tr
        y0 += math.cos(t * 19) * 3.5 * k_tr
    x0, y0 = min(max(0, x0), CW - cw), min(max(0, y0), CH - chh)
    img = img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + chh))).resize((W, H), Image.BILINEAR).convert("RGB")
    vin = 0.34 + 0.22 * tensao + 0.12 * acento + 0.03 * math.sin(t * 0.9) + (0.06 if cena.get("ameaca") else 0)
    img = Image.composite(Image.new("RGB", (W, H), (2, 3, 10)), img, _vinheta(vin))
    # cortes secos dentro do mesmo lugar; um piscar curto de escuro quando muda de lugar
    fd = 0.14
    if cena.get("_fade_in", False) and t < fd:
        img = Image.blend(img, Image.new("RGB", (W, H)), 1 - t / fd)
    if cena.get("_fade_out", False) and dur - t < fd:
        img = Image.blend(img, Image.new("RGB", (W, H)), 1 - max(0.0, dur - t) / fd)
    return img


def quadro(cena: dict, t: float, dur: float, prot: str = "homem", n: int = 0) -> Image.Image:
    """Desenha o quadro da cena no instante t (segundos). Devolve imagem RGB 1080x1920."""
    if cena.get("_img"):
        return _quadro_ilustrado(cena, t, dur, n)
    if cena.get("corte_preto") and t >= cena.get("_fim_voz", dur):   # corte seco para o preto (susto no silêncio)
        return Image.new("RGB", (W, H), (0, 0, 0))
    img = _quadro_base(cena, t, dur, prot, n)
    plano = _plano_atual(cena, t, dur)
    if plano:                                          # cena longa: corta para outro plano (rosto, criatura, detalhe)
        fx, fy, fz, t0, t1 = plano
        z = fz * (1 + 0.06 * _suave((t - t0) / max(0.1, t1 - t0)))
        cw_, ch_ = img.width / z, img.height / z
        x0 = min(max(0.0, fx * img.width - cw_ / 2), img.width - cw_)
        y0 = min(max(0.0, fy * img.height - ch_ / 2), img.height - ch_)
        img = img.resize(img.size, Image.LANCZOS, box=(x0, y0, x0 + cw_, y0 + ch_))
    if cena.get("foco"):                               # close num detalhe do cenário (ex.: a maçaneta), aproximando devagar
        fx, fy, fz = cena["foco"]
        z = fz * (1 + 0.08 * _suave(t / dur if dur else 0))
        cw_, ch_ = img.width / z, img.height / z
        x0 = min(max(0.0, fx * img.width - cw_ / 2), img.width - cw_)
        y0 = min(max(0.0, fy * img.height - ch_ / 2), img.height - ch_)
        if cena.get("efeito") == "tremor" or cena.get("chacoalha"):
            x0 += math.sin(t * 31) * cw_ * 0.006
        img = img.resize(img.size, Image.LANCZOS, box=(x0, y0, x0 + cw_, y0 + ch_))
    if cena.get("texto_tela"):
        _texto_tela(img, str(cena["texto_tela"]), t)
    if cena.get("_vhs"):
        from .vhs import aplicar
        img = aplicar(img, cena, t, dur, n)
    if cena.get("_alerta"):                            # cena especial dentro de um protocolo: a transmissão por cima
        from .protocolo import sobrepor_alerta
        img = sobrepor_alerta(img, cena, t, n)
    return img


PLANO_SEG = 2.6          # duração alvo de cada plano: imagem parada por muito tempo mata a retenção (lição do Pode Entrar? Ep. 1)


def _centro(r):
    return (r[0] + r[2] / 2, r[1] + r[3] / 2)


def _plano_atual(cena: dict, t: float, dur: float):
    """Cenas longas viram vários planos de ~2,6 s, como numa montagem de verdade.

    O primeiro plano é o geral. Os outros alternam o personagem (rosto e tronco), a criatura das cenas
    especiais e os pontos de interesse do cenário (porta, escuro, janela, TV). Use "plano_unico": true
    para manter uma imagem só, por exemplo quando a tensão vem justamente de não cortar."""
    if cena.get("foco") or cena.get("plano_unico") or cena.get("_img") or dur < PLANO_SEG * 1.35:
        return None
    meta = META.get(cena.get("cenario"), {})
    if not meta or cena.get("cenario") == "celular_cftv":
        return None
    pts = []
    an = meta.get("anima") or {}
    for parte in an.get("partes", []):
        cx, cy = _centro(parte["regiao"])
        pts.append((cx, cy + 0.04, 1.55))
    if an.get("regiao"):
        cx, cy = _centro(an["regiao"])
        pts.append((cx, cy, 1.5))
    p = cena.get("personagem")
    if p and p.get("tamanho") != "perto" and not meta.get("detalhe"):
        esc = meta.get("escala", 1.0) * (0.55 if p.get("tamanho") == "longe" else 1.0)
        pts.append((POSICOES.get(p.get("posicao"), 0.5), meta.get("piso", 0.95) - 0.24 * esc, 1.5))
    a = cena.get("ameaca")
    if a and a.get("tamanho") != "perto":
        pts.append((POSICOES.get(a.get("posicao"), 0.5), meta.get("piso", 0.95) - 0.3, 1.45))
    for chave in ("escuro", "porta", "janela", "tv", "espelho"):
        if meta.get(chave):
            cx, cy = _centro(meta[chave])
            pts.append((cx, cy, 1.4))
    if not pts:
        pts = [(0.5, 0.42, 1.25), (0.5, 0.62, 1.25)]
    uniq = []
    for q in pts:                                      # tira pontos quase iguais
        if all(abs(q[0] - u[0]) + abs(q[1] - u[1]) > 0.12 for u in uniq):
            uniq.append(q)
    n = max(2, round(dur / PLANO_SEG))
    lado = dur / n
    i = min(int(t / lado), n - 1)
    if i == 0:
        return None                                    # o primeiro plano é o geral
    fx, fy, fz = uniq[(i - 1 + cena.get("_indice", 0)) % len(uniq)]
    if i % 3 == 0 and n > 3:                           # de vez em quando volta ao geral, para o olho respirar
        return None
    return (fx, fy, fz, i * lado, (i + 1) * lado)


def _texto_tela(img: Image.Image, texto: str, t: float) -> None:
    """Texto grande no topo da tela (fora da área das legendas). Uma linha nova com "|"; "v" no fim desenha uma seta."""
    from PIL import ImageFont
    seta = texto.rstrip().endswith(" v")
    linhas = [l.strip() for l in (texto[:-2] if seta else texto).upper().split("|") if l.strip()]
    alfa = min(1.0, t / 0.35)
    camada = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    y = H * 0.11
    for i, ln in enumerate(linhas):
        px = 92
        while px > 40 and ImageFont.truetype(str(FONTE_TELA), px).getlength(ln) > W * 0.86:
            px -= 4
        f = ImageFont.truetype(str(FONTE_TELA), px)
        w = f.getlength(ln)
        x = (W - w) / 2
        roxo = i == len(linhas) - 1 and len(linhas) > 1
        d.rounded_rectangle((x - 26, y + px * 0.08, x + w + 26, y + px * 1.22), radius=18,
                            fill=(124, 58, 237, int(235 * alfa)) if roxo else (6, 8, 18, int(170 * alfa)))
        d.text((x + 4, y + 5), ln, font=f, fill=(0, 0, 0, int(255 * alfa)))
        d.text((x, y), ln, font=f, fill=(255, 255, 255, int(255 * alfa)))
        y += px * 1.3
    if seta:
        b = 0.5 + 0.5 * math.sin(t * 6)
        cx, ty = W / 2, y + 10 + 12 * b
        d.polygon([(cx - 34, ty), (cx + 34, ty), (cx, ty + 44)], fill=(255, 255, 255, int(255 * alfa)))
    img.paste(camada, (0, 0), camada)


def _quadro_base(cena: dict, t: float, dur: float, prot: str = "homem", n: int = 0) -> Image.Image:
    normalizar(cena)
    if cena.get("ameaca"):
        cena["ameaca"]["_silhueta"] = cena.get("_silhueta", False)
    prog = t / dur if dur else 0
    k = _suave(prog)
    cam = cena["camera"]
    tensao = float(cena.get("_progresso", 0.5))          # 0 no começo do vídeo, 1 no final
    acento = _envelope(t, _acentos(cena))
    # paralaxe: quem está na frente anda um pouco mais que o cenário quando a câmera desliza
    paralaxe = {"pan_esquerda": 0.035 * (k - 0.5), "pan_direita": -0.035 * (k - 0.5)}.get(cam, 0.0)
    if cena["cenario"] == "celular_cftv":
        img = _quadro_cftv(cena, t, dur, prot, n)
        meta = {}
    else:
        meta = META[cena["cenario"]]
        img = _cenario_escuro(cena["cenario"]).copy()
        if meta.get("anima"):                          # cena especial (ilustração pronta): a criatura se mexe
            _animar_especial(img, meta["anima"], t, dur)
        ef = cena["efeito"]
        if ef == "tv_chiando":      # TV e chuva ficam no cenário, atrás de quem estiver na frente
            _tv(img, meta, t, n)
        elif ef == "chuva":
            _chuva(img, meta, t, n)
        if cena.get("objeto"):                         # pistas no chão e nas paredes, atrás de quem estiver em cena
            from .objetos import desenhar as desenhar_objeto
            for o in cena["objeto"]:
                desenhar_objeto(img, o, meta, t, dur, _noite)
        a, p = cena.get("ameaca"), cena.get("personagem")
        if p and "_muda_em" not in p:     # quando a expressão muda (medo/grito): ameaça surgindo ou 1ª palavra forte
            ac = _acentos(cena)
            p["_muda_em"] = dur * 0.25 if (a and a["acao"] == "aparecendo") else (ac[0] if ac else None)
        # a ameaça fica atrás do personagem, a não ser que ela esteja em close e ele não
        ameaca_atras = a and not (a["tamanho"] == "perto" and (not p or p["tamanho"] != "perto"))
        if a and ameaca_atras:
            _desenhar_ameaca(img, a, meta, t, dur, paralaxe=paralaxe)
        g = cena.get("gato")
        desvio = 0.0
        if g and p and g["posicao"] == p["posicao"] and p["tamanho"] != "perto":
            desvio = 0.16 if POSICOES[g["posicao"]] <= 0.5 else -0.16    # não fica escondido atrás do personagem
        cao = cena.get("cachorro")
        if cao and (cao["tamanho"] == "longe" or not p):
            _desenhar_cachorro(img, cao, meta, t, dur, paralaxe=paralaxe)
        if g and g["tamanho"] == "longe":
            _desenhar_gato(img, g, meta, t, dur, paralaxe=paralaxe, desvio=desvio)
        if p:
            _desenhar_personagem(img, p, meta, t, dur, prot, paralaxe=paralaxe, tenso=bool(a))
        if cao and cao["tamanho"] != "longe" and p:
            dv = 0.0
            if cao["posicao"] == p["posicao"] and p["tamanho"] != "perto":
                dv = 0.2 if POSICOES[cao["posicao"]] <= 0.5 else -0.2
            _desenhar_cachorro(img, cao, meta, t, dur, paralaxe=paralaxe, desvio=dv)
        if g and g["tamanho"] != "longe":
            _desenhar_gato(img, g, meta, t, dur, paralaxe=paralaxe * (1.6 if g["tamanho"] == "perto" else 1.0), desvio=desvio)
        if a and not ameaca_atras:
            _desenhar_ameaca(img, a, meta, t, dur, paralaxe=paralaxe * 1.6)
        _poeira(img, t, hash(cena["cenario"]) % 1000)

    ef = cena["efeito"]
    if ef == "luz_piscando":
        rnd = random.Random(n // 2)
        if rnd.random() < 0.18:
            img = _brilho(img, 0.55)
    elif ef == "relampago":
        for pico in (0.3, 0.38, 0.75):
            d = abs(t / dur - pico) * dur if dur else 9
            if d < 0.08:
                img = _brilho(img, 0.55 * (1 - d / 0.08), (235, 240, 255))

    # câmera
    z, px = 1.0, 0.5
    if cam == "zoom_in":
        z = 1 + 0.12 * k
    elif cam == "zoom_out":
        z = 1.12 - 0.12 * k
    elif cam == "pan_esquerda":
        px = 1 - k
    elif cam == "pan_direita":
        px = k
    # palavra forte = leve aproximação; perigo ou reta final = pulsação de coração bem sutil
    z *= 1 + 0.014 * acento
    if cena.get("ameaca") or tensao > 0.65:
        z *= 1 + 0.0018 * _batimento(t, 62 + 24 * tensao)
    cw, chh = W / z, H / z
    x0 = (CW - cw) * px
    y0 = (CH - chh) * 0.5
    if ef == "tremor":
        k_tr = math.exp(-t * 1.5)              # sacode só no começo do susto e acalma
        x0 += math.sin(t * 23) * 3.5 * k_tr
        y0 += math.cos(t * 19) * 3.5 * k_tr
    x0 = min(max(0, x0), CW - cw)
    y0 = min(max(0, y0), CH - chh)
    img = img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + chh)))
    if img.size != (W, H):
        img = img.resize((W, H), Image.BILINEAR)

    # bordas escurecem conforme a história fica mais tensa e em cada palavra forte
    img = img.convert("RGB")
    vin = 0.42 + 0.30 * tensao + 0.15 * acento + 0.04 * math.sin(t * 0.9)
    if cena.get("ameaca"):
        vin += 0.08                                 # com perigo em cena, o quadro fecha mais
    img = Image.composite(Image.new("RGB", (W, H), (2, 3, 10)), img, _vinheta(vin))

    # transição: escurece no começo e no fim da cena
    borda = min(t, dur - t)
    if borda < 0.2:
        img = Image.blend(img, Image.new("RGB", (W, H), (0, 0, 0)), 1 - max(0.0, borda) / 0.2)
    return img


def marcar_revelacao(roteiro: dict) -> None:
    """O Abismo é só uma silhueta escura até o clímax. O rosto aparece a partir da primeira cena da reta final
    (último terço) em que ele encara, avança ou aparece de perto; antes disso, todas as aparições são silhueta."""
    cenas = roteiro.get("cenas", [])
    n = len(cenas)
    revela = n
    for i, c in enumerate(cenas):
        a = c.get("ameaca") or {}
        if i >= n * 0.65 and a.get("tipo") == "abismo" and (a.get("acao") in ("encarando", "aproximando") or a.get("tamanho") == "perto"):
            revela = i
            break
    if roteiro.get("parte", 1) not in (1, None, "") and not roteiro.get("silhueta_sempre"):
        revela = 0                                     # nas partes seguintes o público já viu o rosto dele
    for i, c in enumerate(cenas):
        c["_silhueta"] = i < revela


def renderizar_cena(cena: dict, voz: dict, destino: Path, prot: str, pausa: float = 0.5) -> float:
    """Gera o clipe .mp4 da cena com a narração. Devolve a duração."""
    dur = voz["duracao"] + pausa
    cena.setdefault("_palavras", voz.get("palavras") or [])
    cena["_fim_voz"] = voz["duracao"]
    frames = math.ceil(dur * FPS)
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
         "-r", str(FPS), "-i", "-", "-i", str(voz["arquivo"]),
         "-filter_complex", "[1:a]aresample=44100,apad[a]", "-map", "0:v", "-map", "[a]",
         "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "160k", "-ac", "2", str(destino)],
        stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for n in range(frames):
            ff.stdin.write(quadro(cena, n / FPS, dur, prot, n).tobytes())
    finally:
        ff.stdin.close()
        erro = ff.stderr.read().decode(errors="ignore")
        ff.wait()
    if ff.returncode != 0:
        raise RuntimeError(f"FFmpeg falhou ao gravar a cena: {erro[-1500:]}")
    return dur


def renderizar_clipe(cena: dict, voz: dict, destino: Path, pausa: float = 0.5) -> float:
    """Usa um clipe de IA (Kaggle) no lugar da animação da cena: ajusta tamanho, ritmo e duração à narração."""
    dur = voz["duracao"] + pausa
    clipe = Path(cena["_clipe"])
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(clipe)],
                       capture_output=True, text=True)
    dur_clipe = float(r.stdout.strip() or 4.0)
    lento = min(max(dur / dur_clipe, 1.0), 1.5)          # desacelera até 1,5x; o resto segura o último quadro
    filtro = (f"[0:v]setpts={lento:.3f}*PTS,scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,"
              f"crop={W}:{H},fps={FPS},tpad=stop_mode=clone:stop_duration={dur:.3f},trim=duration={dur:.3f},"
              f"fade=t=in:d=0.2,fade=t=out:st={max(dur - 0.2, 0):.3f}:d=0.2,format=yuv420p[v];"
              "[1:a]aresample=44100,apad[a]")
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(clipe), "-i", str(voz["arquivo"]),
                        "-filter_complex", filtro, "-map", "[v]", "-map", "[a]", "-t", f"{dur:.3f}", "-r", str(FPS),
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
                        "-ac", "2", str(destino)], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-800:])
    return dur
