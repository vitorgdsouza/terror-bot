# Direção criativa: "Você Escaparia?"

Este é o documento que a direção automática diária lê antes de criar qualquer coisa. Leia também `docs/PERSONAGENS.md`, com o elenco, os antagonistas e quando estrear cada um, e `docs/PROTOCOLOS.md`, com o que funciona em protocolo e a estrutura dos nossos. O dono do canal (Vitor) supervisiona e posta o TikTok à mão. Tudo aqui foi aprendido com o gosto e as correções dele.

## 1. Calendário de postagem (YouTube, fila automática)
- **11h47:** sempre uma **isca** (12 a 20 s). Gancho e pergunta, para trazer gente nova. Puxa uma série do canal.
- **18h47:** o **vídeo principal**, alternando por dia:
  - **Dia de protocolo:** analog horror no estilo protocolo, com o alerta vermelho e pictogramas (40 a 55 s), ou o formato sombra, com silhuetas no vermelho.
  - **Dia de história:** animação narrada com personagens e cenários (55 a 70 s). Pode ser episódio de série (Guizo/Abismo, Rufus) ou uma história nova, avulsa ou começando uma série nova.
- **Para saber que dia é:** veja o `tipo` do último principal em `data/fila.json` (itens e postados). Se foi `protocolo`, hoje é `historia`, e vice-versa.
- **Padrão das iscas (correção do Vitor, 18/11):** isca curta NÃO pode ser simples. "Você Viu Ele?" foi reprovada por ser fraca e não deve ser usada nem refeita. Cada isca precisa de:
  - uma linguagem forte: fita VHS encontrada, câmera de segurança (texto_tela "CAM 02 | 03:16"), alerta de emergência, mini-protocolo ou corte para o preto;
  - uma cena especial (ilustração com a criatura) no susto;
  - uma pequena virada no fim;
  - uma pergunta que puxe comentário.

  Use as iscas para apresentar as séries novas. Modelo: `roteiros/iscas/isca_06_farmacia.json`.
- **Sempre manter pelo menos 2 iscas na fila.** Se tiver menos, faça uma isca nova no dia.
- **No máximo 2 posts por dia.** Postar demais derruba a distribuição de cada vídeo.

## 2. O que funciona (dados do canal até 17/11/2026)
- **Os maiores:** O Guizo na Escada (1.088), O Rufus Não Abana Mais o Rabo, em VHS (1.094), Protocolo Stu (965). Séries com personagem e protocolos de animal de estimação funcionam.
- **O que foi mal:** o formato "real", com banco de imagens e voz própria (281). Não usar mais sem pedido.
- **YouTube Shorts:** o que pesa é quem desliza nos primeiros 2 s, a retenção até o fim e as revisões.
  - O primeiro quadro e a primeira frase são o gancho. Abra no meio da ação ou com a imagem mais forte.
  - O final que volta para o começo faz rever.
  - Durações curtas completam mais.
- **TikTok:** os protocolos e as perguntas diretas engajam mais.
- **Relatório:** `gh workflow run youtube.yml -f acao=relatorio` grava `data/analise/ultima.json`, com retenção, quem ficou e origem. Leia antes de decidir o dia. Os dados do YouTube atrasam 2 a 3 dias.

## 3. Gosto do Vitor (respeitar sempre)
- **Voz:** Enceladus (Gemini). Estilos: suspense e calma para histórias, alerta para protocolos. A voz não pode "bugar" palavras. O sistema grava até 3 tomadas e corta no silêncio. Se a nota da tomada ficar abaixo de 90%, refaça.
- **Animação:**
  - Personagens sempre perto do que fazem. Nada de "pegar no vento", objeto voando ou personagem sentado no ar.
  - Proporções certas com o cenário.
  - Ações que **NÃO** ficaram boas e não devem ser usadas: engatinhar de frente ou de costas, o Abismo rastejando procedural, o sorriso no escuro procedural.
  - Ações aprovadas: debruçado no poço, olhando para cima de costas, golpeando (martelo na parede), e todas as básicas.
- **Momentos de impacto com a criatura:** usar **cenas especiais**, que são ilustrações prontas e animadas por regiões (`anima` no `cenarios.json`). Exemplos: `poco_sorriso`, `tunel_abismo`, `janela_poco`. Uma por vídeo, no susto.
- **Mistério:**
  - Pistas e objetos que contam a história, como o jornal **nas mãos** (`"nas_maos": true`, depois de uma cena dele procurando).
  - Close num detalhe com `"foco": [x, y, zoom]`.
- **Lógica da história:** cada cena tem que fazer sentido para quem assiste. Exemplos: os olhos no escuro ficam DENTRO do buraco escuro, e ele vê pela janela antes de ir até o lugar.
- **Continuidade:** o episódio novo começa exatamente onde o anterior parou.
- **Voto dividido entre redes:** a história honra as duas escolhas, sem "quebrar parede" forçado.
- **Traço livre por série (autorizado pelo Vitor em 18/11):** as histórias novas (Turno da Madrugada, Câmera 4, Férias na Roça, Corrida Noturna e as que vierem) podem ter um estilo de traço próprio para os personagens, diferente do boneco do Guizo. Exemplos: proporções mais realistas, outra paleta, contorno mais grosso ou mais fino. Exigências:
  - cada protagonista e cada antagonista tem que ser único e reconhecível;
  - o estilo tem que combinar com os cenários da série;
  - a qualidade não pode cair: proporção, ação perto do objeto, expressões legíveis.
  - O Guizo mantém o traço atual, que é a marca do canal.
- **Arte própria:** inspiração em criadores é permitida, cópia de personagem, arte ou história não.

## 4. Formatos e como fazer (repo vitorgdsouza/terror-bot)
- **Roteiros:** `roteiros/*.json`. Iscas em `roteiros/iscas/`. Cada roteiro tem:
  - `titulo`
  - `titulo_youtube`: pergunta ou gancho de busca, terminando em `#shorts`
  - `legenda_post`: termina com a pergunta A/B ou a pergunta da isca
  - `hashtags`, `selo`, `pergunta_thumb`
  - `tipo`: `isca`, `protocolo` ou `historia`
- **História animada:** cenas com `cenario`, `personagem`, `gato`, `cachorro`, `ameaca`, `objeto`, `camera`, `efeito`, `som`, `foco`. Lista completa de cenários, poses e ações no topo de `src/animacao.py`.
  - Cenários do arco do Guizo: corredor_velho, poco, fundo_poco, tunel, parede_dentro, porao_duarte, camara, mais as cenas especiais.
- **Protocolo:** `"formato": "protocolo"`, cenas com `icones` (pictogramas, incluindo `gato:<acao>`, `cachorro:<acao>`, `falso:<acao>` e `pessoa:<pose>`) ou `destaque`. Também `rotulo` (ex.: "PROTOCOLO RUFUS") e `sombra` (`abismo` ou `falso`). Para criar um protocolo de outra criatura, use pictogramas existentes ou acrescente um novo em `src/protocolo.py`.
- **Sombra:** `"formato": "sombra"`. Quadros: relogio, quarto, rosto, porta, portas, abismo, destaque, com `batidas`/`x`/`texto`.
- **VHS:** `"estilo": "vhs"`, com `pixel`, `data_fita` e `hora_fita`. Serve para o found footage do Rufus e para casos de fita perdida.
- **Renderizar:** `gh workflow run refazer-video.yml --ref main -f roteiro=<arquivo>`.
  - **Um de cada vez:** em paralelo estoura a cota do Gemini e cai na voz reserva, que é proibida.
  - Leva cerca de 10 a 15 min.
  - O vídeo chega no Telegram do Vitor e vira o "pendente".
- **Revisar SEMPRE:** depois do `git pull`, abra `data/previas/<nome-do-roteiro>.jpg` (folha de quadros). Confira:
  - personagem fora do lugar ou flutuando;
  - objeto ilegível;
  - legenda tapando algo importante;
  - cena escura demais;
  - continuidade.
  
  No log, confira se a voz saiu do Gemini e a nota da tomada. Corrija e refaça, no máximo 2 vezes.
- **Pôr na fila:** acrescente em `data/fila.json` o item `{"run_id", "titulo", "titulo_youtube", "legenda", "tipo"}`, depois commit e push.
- **Falar com o Vitor:** `gh workflow run fila.yml --ref main -f acao=aviso -f texto="..."` manda mensagem no Telegram.

## 5. Séries
- **O Guizo na Escada:** é o carro-chefe. Cânone em `config/serie.json` (`abismo_lore`) e no doc do projeto.
  - Lucas Duarte é uma criança de uns 10 anos. Os pais viajaram e ele está sozinho com o gato Stu.
  - O Abismo nasceu dos desenhos da bisavó. Isso é segredo, revelado aos poucos.
  - O Stu está vivo nos túneis do poço.
  - O Ep. 2, "O Poço do Quintal", foi postado em 17/11. A: descer pela corda; B: ligar para os pais.
  - O Ep. 3 só sai depois do resultado da votação. O Vitor informa o TikTok, e os comentários do YouTube são lidos à mão ou com o script de votos, se a permissão existir.
- **Rufus:** policial e o cão farejador. O "falso Rufus" é um homem vestindo a pele do cão. Formato VHS. Fita 01 e Fita 02 já postadas. Fita 02: A abrir a porta / B rádio da viatura.
- **Protocolo Stu e Protocolo Rufus:** podem ganhar novos protocolos, inclusive de criaturas novas.
- **Histórias novas são bem-vindas:** personagens, criaturas e lugares novos, com cara de série que pode continuar se for bem. Libere as continuações aos poucos, com base nos números.
- **Elenco pronto para estrear** (detalhes em `docs/PERSONAGENS.md`):
  - Bia, no "Turno da Madrugada", contra O Cliente das 3h17;
  - Seu Joaquim, na "Câmera 4", contra A Moradora do 13º;
  - Davi e Dona Cida, nas "Férias na Roça", contra A Pisadeira e O Assobiador;
  - Rafa, na "Corrida Noturna", contra O Passageiro do Banco de Trás.

- **No radar (ideia do Vitor, 18/11): isca "versão macabra de personagem famoso".** São curiosidades sombrias com fotos do Pixabay. Só fazer se a análise de tendências mostrar que o formato está em alta. Regras:
  - **Personagem com dono** (Bob Esponja, Disney etc.): NUNCA usar imagem, desenho, nome no título ou imitação da voz. Isso dá strike de direitos autorais e quebra a regra de arte própria. O máximo permitido é comentar uma lenda ou creepypasta conhecida sobre o desenho ("o episódio perdido que..."), em narração, com imagens genéricas (TV chiando, fita VHS, quarto escuro).
  - **Caminho livre e mais forte:** personagens de domínio público em versão macabra:
    - folclore brasileiro: Saci, Curupira, Mula sem Cabeça, Cuca da lenda (não a do Sítio da TV);
    - contos clássicos: Chapeuzinho, João e Maria, Pinóquio, Branca de Neve dos Grimm;
    - Mickey de 1928 (Steamboat Willie), só o design original.
  - **Voz:** a Enceladus muda de estilo conforme o personagem (sussurro infantil, conto de fadas, alerta). Nunca imitar o dublador de um personagem real.

## 6. Cenários novos
- **Ilustrações** (cenários e cenas especiais) são geradas pelo Vitor no app do Gemini. A API de imagem não tem cota grátis.
- **Quando precisar de uma:** mande no aviso o prompt pronto em inglês, com o estilo base. Enquanto não chega, use os cenários que existem.
- **Estilo base dos prompts:** "2D cartoon illustration, clean dark outlines, flat colors with soft shading, night time, dark navy and blue palette with one warm light source, eerie and quiet mood, eye-level camera, empty scene with NO people, NO animals, NO text, open floor area in the lower third for characters to stand, vertical 9:16".
- **Catálogo de cenários encomendados:** https://claude.ai/artifact/2jdhgLeWWzYFesAaVMRzKj tem o nome, o uso e o prompt de cada um. Quando o Vitor mandar uma imagem com esse nome, cadastre com o mesmo nome. Os que começam com `esp_` são cenas especiais (configure `anima`). Antes de pedir um cenário novo, veja se ele já está no catálogo.
- **Ao receber a imagem:** redimensione para 1188x2112 em `assets/cenarios/` e cadastre em `cenarios.json` (piso, fundo, escala, faixa, horizonte, porta e escuro quando houver). Teste a escala com um quadro de prova.

## 7. Limites
- **Sem gore.** Os bichos nunca aparecem machucados ou mortos.
- **O Lucas é criança:** o medo vem do suspense, nunca de violência contra ele.
- **Sem pessoas reais, marcas ou personagens de terceiros.**
- **Sem trend que glorifique violência real.**
- **Segredos** só no GitHub Secrets, nunca em arquivos ou mensagens.

## 8. Diário
Registre em `data/diario_direcao.md`, a cada dia: o que foi feito, o porquê, números relevantes e o que testar depois. Essa é a memória entre os dias.
