"""Formato "ilustrado": a história vira uma sequência de planos curtos, cada um com sua ilustração.

Usado pelo roteirista (Gemini), pelo agente diretor (Claude) e pelas ferramentas de validação.
"""

CAMERAS = ["zoom_in", "zoom_out", "pan_esquerda", "pan_direita", "parada"]
EFEITOS = ["nenhum", "luz_piscando", "relampago", "chuva", "tremor"]
AMEACAS = ["vulto", "abismo", "invasor"]

REGRAS_HISTORIA = """COMO É UMA BOA HISTÓRIA DO CANAL (siga à risca):
- Situação do dia a dia, crível, no Brasil. Nas 2 primeiras frases: quem você é, onde está e por que está sozinho(a)
  (ex.: "Você está de férias. Sua família decidiu viajar por uma semana, mas você preferiu ficar em casa.").
- Âncoras concretas: dia da história ("na terceira noite"), horário exato por extenso ("por volta das duas da manhã"),
  objetos específicos (a gaveta, o prato, o copo, o armário embaixo da escada, a câmera da sala).
- O medo cresce por PISTAS pequenas e lógicas, cada uma pior que a anterior: um som, um objeto fora do lugar,
  algo molhado ou lavado, uma porta que você tinha trancado, uma notificação, uma gravação. Você tenta explicar e a explicação falha.
- Mostre pouco. A ameaça só aparece de verdade no último terço, e de forma rápida (de relance, ao fundo, numa gravação).
  Prefira ameaças plausíveis (um estranho escondido dentro de casa) ou um sobrenatural sutil.
- Uma virada perto do fim que muda o sentido das pistas (ex.: "O mesmo homem aparece nas imagens de ontem.").
- Frases curtas e naturais, como alguém contando para um amigo. Nada de clichês vazios ("um frio sobe pela espinha",
  "o silêncio era ensurdecedor", "seu coração dispara"); mostre fatos concretos que assustam sozinhos.
- Final: uma situação-limite e duas escolhas arriscadas e plausíveis: "Opção A: ...", "Opção B: ...",
  terminando com "Comente A ou B." (pode acrescentar "A decisão mais votada decide a próxima parte.").
- Sem gore, sangue ou violência explícita. Números por extenso, sem siglas nem parênteses.
- "clima": "calma" para mistério lento, solidão, algo estranho e melancólico; "suspense" para perseguição, invasão, algo te observando, ameaça crescendo. Define o tom do narrador."""

GUIA_PLANOS = """COMO A HISTÓRIA VIRA VÍDEO (formato de planos ilustrados):
- Cada plano = UMA frase narrada curta (de 4 a 14 palavras) + UMA ilustração que mostra exatamente o que essa frase diz.
  Uma frase longa vira dois ou três planos seguidos. O vídeo troca de imagem a cada 2 a 4 segundos.
- "imagem": descrição em INGLÊS, concreta e visual, do quadro: o enquadramento (wide establishing shot, medium shot,
  close-up, extreme close-up of an object, over-the-shoulder shot, first-person POV, high angle, low angle), o que aparece,
  a ação e a expressão do protagonista, a luz. Exemplo: "Close-up of a kitchen sink at night: a clean plate with crumbs
  and a wet glass of water, lit by a warm under-cabinet light". Nunca peça texto escrito na imagem.
- Varie os planos como num desenho animado: abra com um plano geral de fora da casa e aproxime aos poucos; alterne
  plano médio do protagonista, close do objeto da pista, visão em primeira pessoa (as mãos segurando o celular com a
  imagem da câmera de segurança na tela) e plano por cima do ombro. Repita o lugar em planos seguidos quando a ação continua ali.
- "lugar": nome curto do cômodo, em minúsculas e sem acento: quarto, sala, cozinha, corredor, escada, banheiro, porao,
  garagem, fora_casa, rua, celular (tela do celular em close). Use SEMPRE o mesmo nome para o mesmo lugar.
- "personagem": true se o protagonista aparece (inteiro ou só as mãos/costas); false se não aparece.
- "ameaca": null, ou "vulto" (silhueta preta de olhos brancos), "abismo" (figura preta de rosto pálido e sorriso enorme)
  ou "invasor" (pessoa de capa de chuva amarela com o rosto escondido). Só nos planos em que ela aparece.
- "camera": zoom_in (aproxima devagar, padrão), zoom_out, pan_esquerda, pan_direita ou parada.
- "efeito": nenhum (quase sempre), luz_piscando, relampago, chuva ou tremor (só no maior susto)."""

EXEMPLO_JSON = """{
  "titulo": "título curto e chamativo",
  "clima": "suspense",
  "protagonista": "homem",
  "casa": "small two-story Brazilian suburban house: beige walls, wooden stairs in the living room, grey sofa, dark wood kitchen cabinets",
  "cenas": [
    {"narracao": "Você está de férias.", "lugar": "fora_casa", "personagem": false, "ameaca": null,
     "imagem": "Wide establishing shot of the house at night from the street, one upstairs window lit with a figure sitting at a desk inside",
     "camera": "zoom_in", "efeito": "nenhum"},
    {"narracao": "Na cozinha, você encontra um prato lavado.", "lugar": "cozinha", "personagem": false, "ameaca": null,
     "imagem": "Close-up of the kitchen sink: a freshly washed plate and a wet glass, warm light from under the cabinet",
     "camera": "zoom_in", "efeito": "nenhum"}
  ],
  "resumo": "a história inteira até aqui em até 4 frases",
  "opcao_a": "a opção A do final, em uma frase",
  "opcao_b": "a opção B do final, em uma frase",
  "legenda_post": "legenda curta terminando com: E você, A ou B?",
  "hashtags": ["#terror"]
}"""


def normalizar_plano(p: dict) -> None:
    p["lugar"] = (p.get("lugar") or "casa").strip().lower().replace(" ", "_")
    p["personagem"] = bool(p.get("personagem"))
    if p.get("ameaca") not in AMEACAS:
        p["ameaca"] = None
    if p.get("camera") not in CAMERAS:
        p["camera"] = "zoom_in"
    if p.get("efeito") not in EFEITOS:
        p["efeito"] = "nenhum"
    p["imagem"] = (p.get("imagem") or "").strip() or f"Medium shot of the {p['lugar']} at night"


def modo_ilustrado(cfg: dict) -> bool:
    return cfg.get("modo_visual", "ilustrado") == "ilustrado"


def regras_gato(cfg: dict) -> str:
    """Regras do gato do protagonista (personagem fixo da série), se estiver ligado em config/serie.json."""
    g = cfg.get("gato") or {}
    if not g.get("ligado"):
        return ""
    nome, desc = g.get("nome", "o gato"), g.get("descricao", "gato laranja")
    return f"""O GATO DO PROTAGONISTA: você tem um gato, {nome} ({desc}). Ele dá à história um segundo objetivo
além de sobreviver: encontrar {nome} e deixá-lo em segurança.
- CONEXÃO: nas primeiras cenas, um detalhe de carinho que só vocês dois têm (um ritual, uma mania de {nome}), para o
  público se importar com ele antes de ele sumir. Esse detalhe volta no final.
- MISTÉRIO COM PISTAS: o sumiço de {nome} é um quebra-cabeça. Use de 3 a 5 pistas, cada uma mais inquietante e
  apontando um caminho: algo fora do lugar (tigela virada, novelo desenrolado até uma porta), uma trilha (pegadas de
  patinhas indo para um cômodo, tufo de pelo), um sinal de que algo pegou {nome} (a coleira com o guizo largada no
  chão, arranhões fundos na porta) e a prova de que não é um animal (marcas de mãos compridas demais na janela).
  Cada pista aparece na cena com o campo "objeto" (use o close "perto" na pista mais importante).
- O ABISMO É SÁDICO: ele está brincando com você. Deixa as pistas de propósito, imita o miado de {nome}, move as
  coisas de lugar enquanto você não olha. Ele se esgueira e quase nunca se mostra inteiro antes do clímax.
- CLÍMAX: as pistas levam a um lugar (o porão, o sótão pela escada, o quarto trancado). Uma imagem forte, por exemplo:
  o Abismo parado no alto da escada, encarando, enquanto você, embaixo, fica paralisado de medo, e o miado de
  {nome} vem lá de cima.
- O dilema final envolve {nome} (ex.: Opção A: subir para buscar {nome}; Opção B: fugir sem ele).
- Nunca mostre {nome} ferido ou morto: no máximo em perigo. Ele aparece nas cenas com o campo "gato" (em 3 a 6 cenas)."""


def regras_lore(cfg: dict, historico: list | None = None) -> str:
    """Cânone secreto do Abismo e do paradeiro do gato: revelado aos poucos, episódio a episódio."""
    L = cfg.get("abismo_lore") or {}
    if not L.get("ligado"):
        return ""
    usadas = []
    for h in (historico or [])[-6:]:
        usadas += [int(x) for x in (h.get("lore") or []) if str(x).isdigit()]
    verdades = "\n".join(f"  {i}. {v}{'  (já insinuada recentemente)' if i in usadas else ''}" for i, v in enumerate(L["verdades"]))
    return f"""O MISTÉRIO DA SÉRIE (cânone secreto, NUNCA conte tudo de uma vez):
Verdades sobre a origem do Abismo:
{verdades}
Paradeiro do gato (o público não sabe): {L.get("paradeiro_do_gato", "")}
Como usar:
- Em cada episódio, insinue 1 ou 2 verdades (de preferência ainda não insinuadas), sem explicar: mostre por uma pista
  ("objeto" foto, bilhete, jornal ou desenho, com "texto" curto de até 4 palavras, ex.: {{"tipo": "jornal",
  "tamanho": "perto", "texto": "Família some em 1987"}}) ou por um detalhe na narração. O público deve sair com
  perguntas e teorias, não com respostas.
- O paradeiro do gato é um enigma: deixe sinais contraditórios e inquietantes (o miado vem de dentro da parede; a
  câmera mostra o gato num cômodo onde você acabou de olhar; a coleira está quente). Nunca resolva antes do final.
- Esconda um detalhe para quem presta atenção: numa cena, o gato aparece pequeno ao fundo ("gato" com tamanho
  "longe") sem a narração mencionar.
- Preencha "lore": [números das verdades que este episódio insinua] no roteiro.json.
- A "legenda_post" termina com uma pergunta que puxa teorias nos comentários (ex.: "Onde você acha que o Stu está?"),
  além de "E você, A ou B?"."""
