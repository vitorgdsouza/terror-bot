# Diário do E Se Fosse Real?

## 20/11
- Canal criado no sistema: formato `voce` com paleta `ciencia`, voz Puck, fila própria.
- 5 roteiros com fontes em `roteiros/esfr/`. O piloto "buraco que atravessa a Terra" foi renderizado (48 s) e está na fila.
- Esperando o Vitor criar o canal e configurar o token e o Upload-Post.

## 20/11 (tarde)
- Segredos conferidos: o token do YouTube e o perfil do Upload-Post apontam para o E Se Fosse Real?, e a chave de voz é própria (com TTS).
- Renders com a chave nova: Terra parando (46 s, voz 95%) e Lua sumindo (32 s, voz 91%).
- Correções no motor: número com decimal (23,5) e ano sem ponto, eixo da Terra bamboleando, rótulo do planeta no alto.
- **Fila:** buraco (20/11 20h17), Terra parando (21/11 12h17), Lua (21/11 20h17). Os roteiros 04 (espaço) e 05 (pulo) estão prontos para renderizar.
- 20/11, 17h: o Vitor entregou o comando do canal ("é você que comanda, dispare quantos achar melhor"). Ritmo: até 3 por dia (12h17, 16h17, 20h17). Arte do canal entregue (perfil refeito a pedido do Vitor, que achou simples demais). Criada a tarefa de produção diária às 9h41.
- Fila: buraco, Terra parando, Lua, espaço sem traje, todo mundo pulando.
- **Para melhorar:** o quadro "multidao" ficou fraco (fileira pequena de bonecos) e houve cenas demais só de texto no vídeo do pulo. Preferir quadros com desenho e criar novos quando o assunto pedir.

## 20/11 (20h55): piloto postado à mão
- O agendamento das 20h17 não disparou. Com o OK do Vitor, rodei `fila-esfr.yml` à mão (run 44839969400): "E se você pulasse num buraco que atravessa a Terra?" saiu no YouTube (Upload-Post completed). Ficam 4 na fila.
- Criada a tarefa de reserva (12h37, 16h37, 20h37): se o agendado falhar, ela posta à mão o próximo da fila e avisa o Vitor.

## 21/11 (manhã, tarefa diária)
- **Problema: postagem travada.** O post agendado (run 44863684279, 00h57) falhou com erro 429 do Upload-Post: "monthly_limit_reached", 10 de 10 uploads do plano grátis usados (o ciclo começou em 17/11, então volta por volta de 17/12). A chave `UPLOAD_POST_API_KEY` é a mesma nos dois canais, então o terror também fica parado. A fila não perdeu nada (o vídeo só sai da fila se postar). Vitor avisado no Telegram e no celular. Opções: plano pago, ou outra conta grátis só para este canal com um segredo próprio (ex.: `UPLOAD_POST_API_KEY_ESE`, e trocar no `fila-esfr.yml`). Upload direto pela API do YouTube não resolve: projeto sem auditoria do Google deixa o vídeo travado como privado.
- **Conexões (fila-esfr testar):** YouTube conectado ao E Se Fosse Real? (1 inscrito), perfil do Upload-Post ok, chave Gemini própria com TTS.
- **Números:** só 1 vídeo no ar (o buraco), sem dados para comparar ainda.
- **Quadros novos em `src/voce.py`:** `sol` (Sol apagando, a última luz indo até a Terra, a Terra saindo pela tangente, a Terra congelando) e `mergulho` (submarino descendo com medidor de fundura, farol, peixe, setas de pressão, fonte de calor no fundo, mar em corte com o Everest dentro). Também `"antes"` no quadro numero ("QUASE 11 KM", "MAIS DE 8.000").
- **Vídeos novos na fila (fila com 6):**
  - 06 "E se o Sol se apagasse agora?" (run 44906725852, 54 s, voz 94%). A 1ª versão abria com o Sol já apagado; refeito para o Sol brilhar antes de apagar. Fontes: Live Science, IFLScience, WorldAtlas.
  - 07 "Fossa das Marianas" (run 44907278914, 49 s, voz 89%). A 1ª versão deu 82% por causa dos números longos falados ("dez mil novecentos e trinta e cinco"); troquei por "quase onze quilômetros" e "mais de oito mil metros". Fontes: Live Science (NOAA), RMG, NASA Earth Observatory, EarthDate.
- **Aprendido:** número falado longo derruba a nota do Whisper. Arredondar na fala e mostrar o mesmo na tela ("QUASE 11 KM"). A cota do Gemini TTS deu 429 várias vezes no 4º render do dia: não passar de uns 4 renders por dia.
- **Domingo (22/11): vídeo longo.** Planejar a compilação de 8 a 12 min. O motor hoje só faz Shorts verticais de até ~1 min; falta juntar vários vídeos prontos em 16:9 (ou vertical com faixas), com vinheta entre eles e uma narração de ligação.
- **Testar depois:** se o Upload-Post voltar, ver qual gancho segura mais (espaço x oceano). Próximas ideias sem repetir: buraco negro, Terra com anéis, um dia em Vênus, raio caindo em você, gravidade sumindo por 5 s.

## 21/11 (12h40): reserva da fila
- O agendamento das 12h17 não disparou (nenhuma execução `schedule` desde 00h57). Postagem à mão de "E se a Terra parasse de girar?" (run 44920276209) **falhou**: Upload-Post 429 `monthly_limit_reached` (10 de 10, reinicia por volta de 17/12). Fila intacta com 6. Não tentei de novo.

## 21/11 (13h45): post manual do Vitor
- "E se a Terra parasse de girar?" foi postado à mão pelo Vitor no YouTube por volta das 13h15, com a thumb própria e a descrição sem as hashtags do terror. Passei o vídeo para `postados`. Ficam 5 na fila.
- Corrigido em `src/postar.py` e `src/refazer.py`: o E Se Fosse Real? não recebe mais as hashtags fixas do terror (`config/serie.json`).

## 21/11 (16h40): reserva da fila
- O agendamento das 16h17 não disparou. Não postei: o Upload-Post segue no limite do mês (429, reinicia por volta de 17/12) e às 16h35 alguém rodou `acao=telegram`, que mandou "E se a Lua sumisse hoje à noite?" no Telegram para postar à mão. Postar pela automação agora só falharia ou duplicaria. Fila intacta com 5; quando o Vitor postar a Lua, passar para `postados`.

## 21/11 (20h40): reserva da fila
- O agendamento das 20h17 não disparou (a última execução `schedule` foi às 17h53, que falhou). Não postei: o envio ainda passa pelo Upload-Post, que segue no limite do mês (429, reinicia por volta de 17/12), e "E se a Lua sumisse hoje à noite?" já foi mandada no Telegram às 16h35 para postar à mão. Fila intacta com 5. Hoje saiu 1 post (Terra, 13h15).

## 22/11 (06h40): Lua postada à mão
- O Vitor postou "E se a Lua sumisse hoje à noite?" à mão no YouTube. Com a autorização dele, passei o vídeo para `postados`. Ficam 4 na fila. Às 6h37 o canal tinha 21 inscritos e 3 Shorts: Lua com 1,3 mil views, Terra com 1,1 mil e Buraco com 1,1 mil.

## 22/11 (manhã, tarefa diária)
- **Conexões (fila-esfr testar, run 45023666708):** YouTube conectado ao E Se Fosse Real? com **22 inscritos**, perfil do Upload-Post ok (200), chave Gemini própria com TTS. O Upload-Post segue no limite do plano grátis até por volta de 17/12; os posts continuam saindo à mão pelo Vitor.
- **Números:** sem dados novos de views (a API de análise só roda dentro dos workflows). Último registro: Lua 1,3 mil, Terra 1,1 mil, Buraco 1,1 mil. Os três de "corpo do planeta/espaço" estão parelhos; ainda não dá para dizer qual gancho segura mais.
- **Quadros novos em `src/voce.py`** (testados localmente com folha de prova antes do render):
  - `buraco_negro`: disco de gás girando em perspectiva, astronauta caindo (`de`/`ate`), `congela` (visto de fora, avermelha e para na beirada), `atravessa`, `dentro` (o céu vira um círculo que encolhe), `estica` (espaguetificação) e `pequeno` (estica antes da borda).
  - `aneis`: Terra com anel de partículas, `asteroide`, `quebra`, `forma` (o anel se fecha), `cai`, `faixa` + `crateras` (faixa de 30° do equador), `sombra`, `gelo`, `some` e `ceu` (arco cruzando o céu visto do chão).
- **Vídeos novos na fila (fila com 6, meta batida):**
  - 08 "E se você caísse num buraco negro?" (run 45025276482, 55 s, voz Puck 93%). A 1ª versão (run 45024118569) teve o astronauta tapando o selo "E SE..." e o rótulo no alto; refeito com o astronauta mais perto e o rótulo embaixo do disco. Números da NASA Goddard (simulação de Schnittman, mai/2024): 4,3 milhões de massas solares, horizonte de ~25 milhões de km, ~3 h de queda até a borda, 12,8 s até a espaguetificação. Fontes também: Live Science, Big Think.
  - 09 "E se a Terra tivesse anéis como Saturno?" (run 45025849302, 58 s, voz 91%). A 1ª versão (run 45024725778, 90%) tinha o anel saindo da tela e a chance contando de 0 ("1 em 12 milhões" no meio da animação, que é outra afirmação); refeito com o anel menor e o número fixo em 25. Fontes: Monash University (set/2024), Tomkins et al. em Earth and Planetary Science Letters (2024), Space.com, EarthSky. O roteiro deixa claro que é hipótese e que tem cientista que duvida.
- **Cota de voz:** 4 renders hoje (cada um gera 3 tomadas, ou seja 12 chamadas de TTS). Um 429 no último, que passou depois de 25 s. Manter o teto de 4 renders por dia.
- **Aprendido:** no quadro `numero`, número que é razão ("1 em 25 milhões") não pode contar a partir do zero; usar `de` igual a `ate`. Rótulo no alto briga com qualquer coisa que entre pelo canto de cima à direita.

### Vídeo longo da semana (domingo, 22/11): plano
- **Ideia:** "E se... o espaço quisesse te matar?" (compilação de 8 a 10 min): buraco que atravessa a Terra, Terra parando, Lua sumindo, espaço sem traje, Sol apagando, buraco negro e Terra com anéis (7 Shorts, uns 6 min e 20 s), mais abertura, ligações curtas entre os blocos e um fechamento pedindo inscrição, para chegar a uns 8 min. A fossa e o pulo ficam para uma compilação "Terra e oceano" mais adiante.
- **O que falta no motor (não existe hoje):**
  1. Um `src/compilar.py` que baixe o `video_final.mp4` dos runs (os artefatos duram só 30 dias: o buraco, de 20/11, expira por volta de 20/12, então a compilação tem que sair antes disso ou os vídeos precisam ser guardados fora dos artefatos).
  2. Converter de vertical para 16:9 (1920x1080): o vídeo no meio, com o fundo borrado do próprio vídeo nas laterais, e sem a legenda queimada cortada.
  3. Vinheta entre blocos e narração de ligação (Puck, 1 tomada curta por bloco), usando o mesmo TTS.
  4. Capítulos na descrição (tempos de cada bloco) e uma thumb 16:9 (`src/thumb_esfr.py` já faz 16:9).
  5. Um workflow `compilar-esfr.yml`. O post sairia à mão pelo Vitor, porque o Upload-Post está no limite e o upload direto pela API deixa o vídeo privado.
- Sem isso pronto, não montei a compilação hoje. Próximo passo sugerido: escrever o `compilar.py` numa rodada sem renders de Shorts (não gasta a cota de voz, só a ligação).

### Testar depois
- Comparar o buraco negro (espaço extremo) com a fossa (oceano) quando os dois estiverem no ar.
- Ideias ainda sem uso: um dia em Vênus, gravidade sumindo por 5 s, raio caindo perto de você (cuidado para não virar tema de saúde), Terra sem oceanos.

- 22/11 16h38: o agendamento das 16h17 não disparou. Não reenviei: "E se você saísse da nave sem roupa espacial?" (1º da fila) já foi mandado no Telegram às 11h41 (run 45034173636, `acao=telegram`) e ainda espera o Vitor confirmar que postou. Upload-Post segue no limite do mês. Fila intacta com 6.

## 22/11 (19h13): print do canal mandado pelo Vitor
- **28 inscritos** (eram 22 de manhã). "E se você saísse da nave sem roupa espacial?" já está no ar, postado à mão; passei para `postados`. Ficam 5 na fila.
- **Views:** Lua 1,9 mil (a melhor até agora), Terra 1,3 mil, Buraco 1,2 mil, Espaço sem traje 1,1 mil (é o mais novo).
- **Leitura:** a Lua abriu vantagem, com a thumb refeita (Lua se desfazendo). Thumbs com objeto grande se transformando parecem puxar mais que as de personagem. Testar isso nas thumbs do buraco negro e dos anéis.

## 22/11 (19h25): pulo refeito a pedido do Vitor
- "E se todo mundo pulasse ao mesmo tempo?" refeito do zero (run 45076982939, 54 s, voz Puck 96% na 1ª tomada). Era o mais fraco da fila: só 11 cenas, várias só com texto e a multidão em uma fileira pequena.
- **Quadro `multidao` reescrito:** 7 fileiras em perspectiva, cada pessoa de uma cor, pulo em onda. Opções novas: `ondas` (som se espalhando), `celulares` + `sem_sinal`, `andando` e `transito` (estrada lotada, luzes de freio piscando). No `planeta` entraram `ponto` (ponto pulsando) e `seta`.
- **Roteiro novo (16 cenas, nenhuma só de texto):** mais de 8 bilhões de pessoas, todo mundo apertado num estadinho dos EUA, pulo de uns 50 cm, a Terra pesando mais de 10 trilhões de vezes, descida menor que um átomo, barulhão de vários segundos, rede de celular caindo, o maior engarrafamento da história e a órbita intacta. Fontes conferidas: xkcd What If? nº 8 e ONU (8 bilhões, nov/2022). Tirei HowStuffWorks e Science ABC da descrição, porque não abri essas páginas.
- Substituído na fila, no mesmo lugar (1º). Enviado no Telegram para o post das 20h17.
- **Cota de voz:** 5º render do dia, mas só precisou de 1 tomada (96%), então saiu barato.

## 22/11 (19h55): thumb "corrompida" no celular
- O Vitor avisou que a thumb chega como arquivo corrompido no celular, e que isso se repete. Os JPGs estão íntegros (conferi gerando aqui). A causa provável é o `sendDocument` sem tipo: o Telegram guarda como `application/octet-stream` e o celular não abre.
- Corrigido em `src/telegram.py`: o arquivo vai com `image/jpeg`, e cada thumb agora também vai como foto, para tocar e salvar na galeria. Vale para os dois canais, porque o envio é o mesmo. Mandei as thumbs do pulo direto na conversa para o post de hoje.

## 22/11 (noite): pulo no ar
- O Vitor postou o pulo refeito (thumb com "AO MESMO TEMPO"), que já tinha **125 views** pouco depois de sair. Passei para `postados`. Ficam 4 na fila; a rodada de amanhã repõe até 6.
- Comparar amanhã o ritmo do pulo novo (multidão nova, 16 cenas) com os outros nas primeiras horas.

## 22/11 (noite): estratégia para monetizar
- O Vitor reforçou que é um desafio: monetizar este canal antes do terror.
- **Conta:** 10 milhões de views em Shorts em 90 dias dá uns 111 mil por dia, e hoje cada Short faz cerca de 1 a 2 mil. A outra porta são 4.000 horas em vídeos longos, mas views de Shorts não contam para essas horas. Uma compilação de 8 min com uns 4 min assistidos por view precisa de uns 60 mil views longos para fechar as horas. Esse caminho parece mais alcançável e soma com os Shorts.
- **Prioridades:** (1) motor de compilação 16:9 (`compilar.py` + workflow), antes de 20/12, quando os primeiros vídeos renderizados expiram; (2) manter 3 Shorts por dia com pelo menos 6 na fila; (3) thumbs com objeto grande se transformando e título completo; (4) acompanhar quais temas seguram mais e dobrar neles; (5) resolver o gargalo do post manual (Upload-Post no limite até por volta de 17/12).
- **Meta intermediária:** 1.000 inscritos é a outra metade da exigência. Pedir inscrição no fim dos longos, não nos Shorts.

## 22/11 (noite): visual novo e plano do longo
- **Terra realista** (`src/globo.py`): continentes de verdade a partir da máscara do Natural Earth, de domínio público (`assets/esfr/terra_mapa.png`, gerada pelo workflow `mapa-terra.yml`). Tem oceano, gelo nos polos, nuvens andando, luz de lado, cidades no lado da noite e atmosfera, com o Brasil de frente. Vale para os vídeos (todo quadro que desenha a Terra) e para as thumbs.
- **Buraco negro realista** (`src/buraco_negro.py`): sombra preta, anel de fótons, o disco cruzando a frente da sombra e a parte de trás dobrada por cima e por baixo, com o lado que vem em nossa direção mais brilhante. Não parece mais Saturno.
- **Pesquisa de vídeo longo** registrada em `docs/ESFR_LONGO.md`. O 1º longo será "E se você pousasse em cada planeta do Sistema Solar?" (cerca de 11 min, ordem em escalada, nada de cartão de texto parado).
- **Para a próxima rodada:** refazer o 08 (buraco negro) e o 09 (anéis), que estão na fila com o visual antigo. São 2 renders, e a cota de hoje já foi.

## 22/11 (21h): motor do vídeo longo
- **Planetas** no visual novo (`src/planetas.py`), aprovados pelo Vitor.
- **Motor 16:9** (`src/longo.py`) e workflow `longo-esfr.yml` (input `blocos` para testar só um trecho). Tem:
  - quadros `sistema`, `planeta`, `superficie` (o "você" astronauta, efeitos de calor, frio, pressão e poeira, termômetro contando), `descida` (dentro dos gigantes gasosos) e `escala` (tamanho real ao lado da Terra, a Terra dentro da Grande Mancha);
  - placar "Dá pra sobreviver?" (sem tempos inventados), barra de capítulos, faixa de documentário e legenda discreta;
  - narração em blocos (2 tomadas por bloco).
- **Teste:** abertura + Mercúrio (run 45085222903, 1,3 min, voz 98% e 90%), mandado no Telegram. Depois disso, troquei a geada "de bolhas" por vinheta gelada e corrigi a escala Terra x Mercúrio.
- Fatos conferidos na NASA em `docs/esfr/longo_01_fatos.md`. Ficam fora do roteiro: "Olimpo 3x Everest" e "chuva de diamantes".
- **Próximo:** roteiro dos outros blocos (Marte, Júpiter, Saturno, Urano, Netuno, Vênus, Terra) depois do retorno do Vitor sobre o teste. O render completo leva uns 20 a 30 min e uns 10 blocos de voz: fazer num dia sem renders de Shorts (a cota de hoje deu 429).

## 22/11 (21h20): trilha própria
- O Vitor não gostou dos bipes da trilha antiga ("curious ambient electronic" do Freesound). Criada a trilha sintetizada do canal (`src/trilha_esfr.py`), aprovada por ele. Agora vale para o vídeo longo e para os Shorts: todos os roteiros `esfr_*` ficaram com `"trilha": "propria"`, e a regra entrou no `docs/ESFR.md`. Os vídeos já renderizados na fila continuam com a trilha antiga; os que forem refeitos (08 e 09 amanhã) já saem com a nova.
- O Vitor pediu para deixar o 06 (Sol) e o 07 (Fossa) como estão, com a trilha antiga, por enquanto. Não refazer esses dois.

## 23/11 (00h): vídeo longo encaminhado (pedido do Vitor)
- **Roteiro completo** `roteiros/esfr/longo_01_planetas.json`: 9 capítulos (Início, Mercúrio, Marte, Júpiter, Saturno, Urano, Netuno, Vênus, Terra), 113 cenas, cerca de 1.240 palavras, uns 9 a 10 min. Tudo conferido em `docs/esfr/longo_01_fatos.md`. Todas as cenas foram testadas aqui, uma imagem por cena.
- **Thumb 16:9** gerada pelo próprio motor ("EM QUAL PLANETA VOCÊ SOBREVIVERIA?"), mandada no Telegram como foto e como arquivo. Se o vídeo passar de 50 MB, vai uma cópia comprimida para o Telegram, e o original fica no artefato.
- **Short novo pronto para renderizar:** `esfr_10_venus.json`, para Sáb 28/11 às 16h17, ligado ao longo. Quadros novos nos Shorts: `astro` (qualquer planeta no visual novo) e `pouso` (o você no chão, igual ao longo).
- **Calendário** em `docs/ESFR_LONGO.md`: render do longo na Qua 25/11 à tarde (nesse dia, no máximo 1 Short renderizado); post do longo no Sáb 28/11 às 11h; sem Short às 12h17 nesse sábado.
- **Para a rodada diária:**
  - **Seg 23/11:** refazer o 08 e o 09, que estão na fila (trocar o `run_id` deles na fila pelo novo, no mesmo lugar), e renderizar o 10 (Vênus). O 10 **NÃO entra na fila**: só anote o `run_id` dele aqui no diário. A tarefa agendada de Sáb 28/11 (10h13) põe ele no início da fila para as 16h17.
  - **Qua 25/11:** no máximo 1 render de Short. Às 14h11, a tarefa agendada "render do 1º vídeo longo" usa a cota de voz.
  - **Sáb 28/11:** sem Short às 12h17 (dia do longo).

## 23/11 (00h30): uma semana para polir o longo (pedido do Vitor)
- O Vitor deu 1 semana para deixar o vídeo longo na melhor versão possível.
- **Polimento feito hoje no motor** (`src/longo.py`):
  - título grande de cada capítulo entrando na tela, e a faixa de documentário só depois dele;
  - o você entra andando no pouso de Mercúrio e dá pulos lentos em Marte (gravidade fraca);
  - na descida dos gigantes, o você gira enquanto cai;
  - botão "SE INSCREVE" pulsando na última cena;
  - efeitos sonoros sintetizados (whoosh na virada de capítulo, ronco grave nas descidas, vento, rumor de calor), abaixando quando a voz fala;
  - som final normalizado em -14 LUFS (o padrão do YouTube).
- **Plano da semana:** Qua 25/11, render da versão 1 (tarefa agendada). Depois, revisão e ajustes; se precisar, versão 2 até sexta. Post no Sáb 28/11 às 11h.

## 23/11 (manhã, tarefa diária)
- **Conexões (fila-esfr testar, run 45177015431):** YouTube conectado com **28 inscritos** (igual ao print de ontem à noite), perfil do Upload-Post ok (200), chave Gemini própria com TTS. O agendamento das 00h42 (run 45107584011) tentou o Sol e levou o 429 do Upload-Post (limite do mês, reinicia por volta de 17/12). Os posts seguem à mão pelo Vitor.
- **Números:** sem dados novos de views (a análise só roda dentro dos workflows). Último registro (22/11, 19h13): Lua 1,9 mil, Terra 1,3 mil, Buraco 1,2 mil, Espaço sem traje 1,1 mil; o pulo refeito tinha 125 views logo depois de sair.
- **Refeitos no visual novo (trocado o `run_id` na fila, mesmo lugar):**
  - 08 buraco negro: run 45177197156, 54,5 s, voz Puck 92%. Buraco negro realista, números batendo (4,3 milhões, 25 milhões de km, 3 h, 12,8 s).
  - 09 anéis: run 45178321957, 48,2 s, voz 91%, Terra realista. O anel encosta nas bordas da tela nas cenas de perfil, mas sem cortar texto.
- **Quadros novos em `src/voce.py`** (testados aqui com folha de prova antes do render):
  - `perfuracao`: poço em corte com torre e broca descendo, `termometro`, `calor`, `treme`, `fosseis` (plâncton brilhando), `agua`, `lama` (bolhas de hidrogênio subindo); modos `boca` (tampa enferrujada vista de cima, com `medida`), `perfil` (você ao lado do poço, em escala) e `planeta` (a marca minúscula do poço na Terra em corte).
  - `impacto`: a Terra com o asteroide chegando e o clarão (`espaco`, `impacto`); paisagem com dinossauros genéricos e você no morro, com `bola`, `plumas`, `vento`, `tsunami`, `fogo`, `escuro`, `frio`, `vazio`, `ave`. Rótulo com caixa escura para ler no céu claro.
  - `comparar` ganhou `"numeros": false` (só as barras, quando a narração não fala os valores).
- **Vídeos novos na fila (fila com 6, meta batida):**
  - 11 "E se você descesse no buraco mais fundo já cavado?" (poço superprofundo de Kola; run 45180147143, 49,6 s, voz 93%). A 1ª versão (run 45179223048) deu 84% nas 3 tomadas: tinha muito número falado ("mil novecentos e setenta", "vinte e três centímetros", "um por cento"), que o Whisper escreve em algarismos e conta como erro. Troquei por "cientistas soviéticos", "da largura de um prato" e "um centésimo do caminho". Fontes: ZME Science, IFLScience, WorldAtlas. Ficou de fora o que as fontes não batem (ano do fim, número de espécies de fóssil, fundura da água).
  - 12 "E se você visse o asteroide dos dinossauros cair?" (run 45180951431, 48,1 s, voz 94%). Já escrito com pouco número falado. Números da NSF (uns 10 km, 20 km/s, ventos de mais de 1.000 km/h, onda de 1,5 km, que virou "mais de 1 km"), do NHM de Londres (75% dos animais = "três em cada quatro", nenhum bicho de terra com mais de 25 kg, as aves como dinossauros que escaparam) e da Sky at Night. Os 70% das florestas viraram "a maior parte".
- **Cota de voz:** 5 renders hoje (08, 09, 11 duas vezes, 12), sem 429.
- **Vênus (10) NÃO foi renderizado hoje** (cota). Renderizar na **Ter 24/11**, primeiro render do dia, e anotar o `run_id` aqui (não entra na fila; a tarefa de Sáb 28/11 põe ele no início).
- **Aprendido:** o Whisper escreve número em algarismo ("1970", "23", "1%") e a nota cai uns 3 pontos por número longo falado. Regra prática: no máximo 4 ou 5 números falados por roteiro, e de preferência curtos ("doze", "cem"); o resto vira comparação em palavras ("três em cada quatro", "da largura de um prato").
- **Testar depois:** ver se temas "Terra por dentro/história da Terra" (poço, asteroide) seguram como os de espaço. Ideias ainda sem uso: um dia em Vênus (o 10 cobre), gravidade sumindo por 5 s, Terra sem oceanos (as fontes são fracas, só simulação), raio caindo perto de você (cuidado com saúde).
- **Vídeo longo:** sem mudança hoje; render da versão 1 segue na Qua 25/11 (tarefa agendada). Na quarta, no máximo 1 Short.

- 23/11 12h41: o agendamento das 12h17 não disparou (nenhuma execução `schedule` hoje depois das 00h42). Upload-Post segue no limite do mês (429, reinicia por volta de 17/12), então mandei no Telegram (run 45207611927, `acao=telegram`) "E se o Sol se apagasse agora?" para o Vitor postar à mão. Fila intacta com 6; passa para `postados` quando ele confirmar.
- 23/11 17h40: o **Vitor recusou a Fossa das Marianas pelo visual antigo** (submarino chapado e 11 cartões de número seguidos) e postou o asteroide no lugar ("esse está atual e gostei muito"). O asteroide (quadros `impacto` e `perfuracao`, com desenho rico) é o padrão. O re-render da Fossa (run 45261959117) não resolve, porque o problema está no roteiro. **Refazer o roteiro esfr_07:** no máximo 2 cartões de número; desenho de oceano em camadas (luz sumindo, bichos de cada profundidade, Everest dentro da fossa); a pressão mostrada no submarino. Só volta para a fila depois disso.
- 23/11 20h40 (reserva da fila, faixa das 20h17): o agendamento não disparou, mas "E se você caísse num buraco negro?" já tinha sido mandado no Telegram às 20h13 (run 45286792116, `acao=telegram`, manual). Não mandei de novo. Fila intacta com 3; passa para `postados` quando o Vitor confirmar.

## 24/11 (manhã, tarefa diária)
- **Conexões (fila-esfr testar, run 45396284505):** YouTube conectado com **36 inscritos** (eram 28 ontem de manhã), perfil do Upload-Post ok (200), chave Gemini própria com TTS. O Upload-Post segue no limite do mês (posts à mão pelo Vitor). O agendamento das 23h10 de ontem (run 45310436618) falhou, como esperado com o limite. Neste ambiente o `gh` está sem login válido: os disparos e logs foram feitos pelo GitHub MCP.
- **Números:** sem views novas (a análise só roda nos workflows). Último registro segue o de 22/11. O ganho de inscritos (+8 em um dia) veio junto com o asteroide e o pulo novo no ar.
- **Vênus (10) renderizado:** run **45396326379**, 48 s, voz Puck 88% (no limite; muitos números falados). NÃO entrou na fila: a tarefa de Sáb 28/11 (10h13) põe ele no início para as 16h17. Ele tem 4 cartões de número; se o Vitor reclamar do jeito que reclamou da Fossa, refazer com o `pouso` no lugar de alguns cartões.
- **Quadros novos em `src/voce.py`** (testados aqui com folha de prova antes de cada render):
  - `apophis`: vista em escala da Terra com o anel dos satélites geoestacionários e o asteroide passando por dentro (`medida`, `mira`, `espreme`, `orbita`); modos `perto` (close fora de escala), `data` (calendário até sexta 13 de abril de 2029), `tamanho` (ao lado de uma torre de treliça), `risco` (medidor; `recorde` = escala de perigo; `valor` = texto fixo; descendo não mostra número no caminho), `ceu` (gente no morro e o pontinho andando) e `mapa` (Terra virada para o Atlântico com os lugares que veem a passagem).
  - `estrela`: Órion com as linhas se desenhando, Betelgeuse vermelha, `explode`/`brilha`/`apaga` (ombro vazio), `lua` (meia-lua para comparar); modos `tamanho` (o Sol, um pontinho, ao lado da gigante), `neutrinos`, `supernova`, `dia`, `sombra`, `longe` e `meses`.
  - `oceano`: descida pelas 5 camadas da NOAA (sol, crepúsculo, meia-noite, abismo, fossa), com cardume e raios de sol, lulas e krill, bichos que brilham, cachalote, paredes da fossa, peixe-caracol e chão com seres de uma célula; modo `zonas` (o mar em corte). Submarino novo com volume (sombra, brilho, rebites, hélice), usado também no `mergulho`.
- **Vídeos novos na fila (fila com 6, meta batida):**
  - 13 "E se um ASTEROIDE passasse mais perto que os satélites?" (Apophis, 13/04/2029; run **45398066338**, 60 s, voz 91%). Fontes abertas: Live Science (2 matérias), Space.com (set/2025), Sky at Night (abr/2026). As fontes discordam no tamanho (340 a 450 m) e na distância (30.000 a 32.000 km): o roteiro diz "mais ou menos a altura da Torre Eiffel" e "uns trinta mil quilômetros". Ficaram de fora a velocidade (nenhuma fonte dá) e as sondas (a da NASA pode ser cancelada). **Defeito pequeno:** na cena do risco zerando, o medidor mostra uns números de passagem (2,6%...) por menos de 1 s. Já corrigido no motor; **refazer o 13 na Qua 25/11 como o único Short do dia e trocar o `run_id` na fila, no mesmo lugar**.
  - 07 Fossa das Marianas **reescrita** como o Vitor pediu (run **45400197981**, 56 s, voz 96%): mar em camadas com os bichos de cada profundidade, Everest dentro da fossa, a pressão mostrada no submarino, nenhum cartão de número. Fontes: NOAA JetStream, WHOI, Royal Museums Greenwich, Live Science, NHM de Londres (peixe-caracol a 8.178 m na própria Marianas, 2017).
  - 14 "E se você visse uma ESTRELA EXPLODIR no céu?" (Betelgeuse; run **45401260191**, 53 s, voz 96%). A 1ª versão (run 45399247995, 97%) tinha a legenda em cima da caixa "DETECTOR" e do você na cena da sombra; refeito com o detector no alto. Fontes: Astronomy.com, Discover, Sky at Night (jan/2025), Scientific American. As fontes discordam no brilho (meia-lua x lua cheia) e na distância (640 a 724 anos-luz): usei "meia-lua" (Astronomy) e "mais de seiscentos anos-luz".
- **Ordem da fila:** buraco negro (no Telegram desde ontem, esperando o Vitor confirmar), anéis, buraco mais fundo, Apophis, Fossa, Betelgeuse. A Fossa fica longe do buraco mais fundo para não repetir "descer" em seguida.
- **Cota de voz:** 5 renders hoje (Vênus 3 tomadas, Apophis 3, Betelgeuse 1 + 1, Fossa 3 = 11 chamadas de TTS), sem 429.
- **Aprendido:** frases curtas e com poucos números saem com 96% a 97% na 1ª tomada (Betelgeuse, Fossa) e economizam a cota. Legenda queimada ocupa a faixa de 75% a 85% da altura: nada importante pode ficar ali (caixas, rostos, rótulos).
- **Testar depois:** ver se "evento real com data" (Apophis, sexta 13) puxa mais que os "e se" impossíveis. Ideias sem uso: gravidade sumindo por 5 s, um dia em Mercúrio, Terra sem Lua desde o começo, o maior vulcão do Sistema Solar (cuidado com o longo, que já cita o Olimpo).
- **Vídeo longo:** sem mudança. Render da versão 1 na Qua 25/11 às 14h11 (tarefa agendada); revisão às 16h20.
- 24/11 12h50: o Vitor gostou do buraco negro, mas não do boneco (a cápsula com bolinha). **Astronauta novo** em `_astro_mini` (`src/voce.py`): capacete com viseira escura, borda ciano, reflexo laranja do disco e brilho; mochila, painel no peito, braços e pernas articulados se debatendo, luvas, botas, faixa laranja e contorno escuro, desenhado em 4x. Estica inteiro na espaguetificação (o close agora fica no meio da tela, longe da legenda). Re-render: run **45429422168**, 52 s, voz Puck 91%. `run_id` trocado na fila, no mesmo lugar (1º). Mandado no Telegram para o Vitor postar.
- 24/11 13h: a pedido do Vitor, os textos do post do E Se Fosse Real? no Telegram ganharam botões de copiar (`copy_text`): título do YouTube sempre; descrição e legenda do TikTok só quando cabem em 256 caracteres. Testado com o buraco negro novo (fila-esfr `telegram`, run 45432062678).
- 24/11 13h10: o Vitor achou a thumb "bem descentralizada". Nas thumbs feitas de quadro do vídeo, a vertical agora põe o desenho no meio do espaço livre entre o texto e o selo (zoom 1,25, de ~47% para ~58% da altura). A horizontal troca o fundo borrado (que repetia o buraco negro atrás do texto) por céu limpo, com o desenho centrado no painel da direita e a emenda esfumada. Ajustável por roteiro: `thumb_zoom`, `thumb_centro`, `thumb_alvo`.
- 24/11 13h25: o Vitor achou a thumb simples. O buraco negro ganhou arte própria (`thumb_arte: "buraco_negro"`, vertical e horizontal): o buraco negro gigante com brilho forte, riscos de luz sendo sugados, o astronauta com cara de pavor (`medo` em `_astro_mini`) esticando a caminho da borda, com rastro, e a seta vermelha apontando para ele. Modelo para as próximas: personagem com emoção + seta + o objeto gigante.
- 24/11 13h35: o Vitor topa a thumb própria como padrão **se fizer efeito**. O critério está em `docs/ESFR.md` ("Thumbs (em teste)"): comparar o 08 com os de thumb simples quando ele tiver uns 3 dias no ar.
- 24/11 13h10 (16h10 UTC): thumb nova posta no YouTube no "E se você caísse num buraco negro?" (fila-esfr `thumbs`, run 45433844331, ok). As primeiras imagens mandadas na conversa chegaram corrompidas para o Vitor; reenviadas em PNG e pelo Telegram (run 45433506057).
- 24/11 13h20: post da aba Comunidade pedindo ideias de "E se...?" (imagem em `data/esfr/comunidade/2026-11-24_ideias.jpg`). Ler as respostas nos próximos dias e usar as boas na pauta, citando quem sugeriu no vídeo.
- 24/11 22h: **pedido do Vitor: vídeo sobre o Paradoxo de Fermi.** Leve, chamativo e feito para engajar. Prioridade da próxima produção. Plano combinado:
  - **Gancho:** "Tem mais estrelas no universo do que grãos de areia nas praias da Terra. Então... cadê todo mundo?"
  - **Miolo:** Fermi, 1950, no almoço: "onde está todo mundo?". A galáxia tem 13 bilhões de anos e poderia ser atravessada em poucos milhões. Depois, 3 respostas rápidas: (1) somos os primeiros; (2) o Grande Filtro, que pode estar à nossa frente; (3) floresta escura: eles estão quietos de propósito, e nós estamos gritando.
  - **Final:** "Qual você acha? 1, 2 ou 3?" para puxar comentário.
  - **Visual:** no padrão do asteroide, com quadros novos (galáxia, olhos no escuro, filtro), no máximo 1 cartão de número.
  - **Thumb:** a Terra pequena no escuro, cercada de olhos brilhando, com a frase "CADÊ / TODO MUNDO?".
  - **Quarta 25/11:** o Fermi é o único render de Short do dia. Ele tem que terminar **antes das 14h11**, porque o render do longo é prioridade e a cota de voz precisa sobrar para ele. Se não der tempo de fazer bem os quadros novos, o Fermi passa para quinta: **o longo vem primeiro**.
- 25/11 06h57 (print do Vitor): **39 inscritos**. Views: Lua 2,4 mil; Sol 1,7 mil; Sem traje 1,4 mil; Terra parando 1,3 mil; Asteroide 1,2 mil; Pulo 1,2 mil; Buraco 1,2 mil; Buraco negro ("Você viraria macarrão?") 1 mil. **Todos os 8 passaram de mil.** A grade de thumbs ficou uniforme (Terra realista e frase branca e amarela).
- 25/11 07h50: **Data do Fermi combinada com o Vitor: Qui 26/11, às 20h17** (horário nobre). Ao terminar o render, coloque o Fermi na fila na posição que cai nessa faixa (hoje saem 3; amanhã às 12h17 e 16h17 saem os 2 seguintes; o Fermi é o 6º de `itens`, contando a partir de hoje de manhã). Mande a prévia ao Vitor pelo aviso do Telegram. Thumb com arte própria (`thumb_arte`): a Terra pequena no escuro, cercada de olhos brilhando, e a frase "CADÊ / TODO MUNDO?".

## 25/11 (manhã, tarefa diária)
- **Conexões (fila-esfr testar, run 45616494876):** YouTube conectado com **39 inscritos** (igual ao print das 06h57). O perfil do Upload-Post está ok (200) e a chave Gemini própria tem TTS. O agendamento de ontem às 23h52 (run 45513528539) falhou, como esperado: o Upload-Post segue no limite do mês. O `gh` continua sem login aqui, então os disparos e os logs foram feitos pelo GitHub MCP.
- **Números:** sem views novas desde o print das 06h57 (todos os 8 vídeos passaram de mil).
- **Fermi (15) pronto e na fila:** "E se você gritasse pro universo e ninguém respondesse?", título no YouTube "CADÊ todo mundo no universo? O Paradoxo de Fermi 👽 #shorts". Run **45617477276**, 60 s, voz Puck 93% (as 3 tomadas deram 91, 93 e 90). Foi o único Short do dia e terminou às 09h55, bem antes do longo (14h11). Entrou como **6º de `itens`**, que é a faixa de **Qui 26/11 às 20h17**, como combinado. O render já mandou o vídeo no Telegram.
  - **Gancho trocado:** "mais estrelas que grãos de areia" ficou de fora porque as fontes discordam. A Scientific American diz que a areia provavelmente ganha, e o Chandra diz que os dois números são parecidos. No lugar entrou "só a nossa galáxia tem uns cem bilhões de estrelas" (Britannica).
  - **Fatos e fontes:** a pergunta "Where is everybody?" num almoço em Los Alamos, em 1950 (Britannica, Smithsonian, Universe Today, Big Think). Galáxia com 13,6 bilhões de anos (Sky at Night). Ocupar a galáxia em uns 10 milhões de anos a 1% da velocidade da luz (Britannica). Centenas de bilhões de planetas (Big Think). Grande Filtro, de Robin Hanson, que pode estar à nossa frente (Britannica, Smithsonian). Floresta escura e o rádio que a Terra vaza (National Geographic, Universe Today). O físico não aparece desenhado: são 3 bonecos genéricos.
  - **Quadro novo `fermi` em `src/voce.py`** (testado aqui com folha de prova antes do render):
    - galáxia espiral girando, com os modos `conta`, `planetas`, `busca` (radar e "?") e `onda` (colônias se espalhando);
    - `almoco` (balão "CADÊ TODO MUNDO?" sendo digitado), `tempo` (régua da idade da galáxia com o fiozinho vermelho), `primeiros` (a Terra sozinha sob um foco de luz);
    - `filtro` (muralha; com `frente`, a Terra vai na direção dela), `floresta` (olhos bravos entre as árvores; com `grita`, a Terra solta ondas de rádio e os olhos a cercam) e `votar` (cartões 1, 2 e 3).
    - Há um olho novo (`_olho`): amêndoa inclinada e pupila de fenda, que pisca.
  - **Thumb própria** (`thumb_arte: "fermi"`, vertical e horizontal): a Terra pequena no escuro, soltando ondas de rádio, cercada de olhos e com a frase "CADÊ / TODO MUNDO?".
  - **Revisão da prévia:** voz Puck 93%. Os números da tela batem com a narração (100 bilhões, + de 13 bilhões, uns 10 milhões). Nenhum texto sai da tela ou tapa a legenda. O 1º quadro escuro da prévia é só a passagem de cena.
- **Fila:** 6 vídeos (meta batida): anéis, buraco mais fundo, Apophis, Fossa, Betelgeuse, Fermi.
- **Cota de voz:** 1 render hoje (3 tomadas). O resto fica para o longo das 14h11.
- **Apophis (13):** o re-render ficou para **Qui 26/11** (hoje a cota é do longo). Ele mostra por menos de 1 s números de passagem no medidor de risco, e o motor já está corrigido. Trocar o `run_id` na fila, no mesmo lugar, se o 13 ainda não tiver saído.
- **Testar depois:** ver se o tema "aliens/Fermi" (pedido do Vitor e com pergunta de votação no final) puxa mais comentários que os outros. Se puxar, repetir o final "1, 2 ou 3?" em temas com várias respostas possíveis, sempre com roteiro diferente. Ideias sem uso: a gravidade sumindo por 5 s, a Terra sem a Lua desde o começo, um dia em Mercúrio.
- **Vídeo longo:** sem mudança. Render da versão 1 hoje às 14h11 (tarefa agendada) e post no Sáb 28/11 às 11h.
- 25/11 12h07 (reserva da fila, faixa das 12h17): nenhum post hoje e o Upload-Post segue no limite do mês (429, reinicia por volta de 17/12). Mandei no Telegram (run 45641281284, `acao=telegram`) "E se a Terra tivesse anéis como Saturno?" para o Vitor postar à mão. Fila intacta com 6; passa para `postados` na próxima faixa.
- 25/11 13h26: o Vitor postou "anéis". A fila foi reordenada para o Apophis sair só depois do re-render de quinta de manhã. Ordem: hoje 16h17 buraco mais fundo e 20h17 Fossa; qui 12h17 Betelgeuse, 16h17 Apophis (re-render ANTES das 12h de quinta, trocando o run_id) e 20h17 Fermi.

## 25/11 (tarde): render do 1º longo, não ficou pronto
- **Run 45662288412** (14h12 às 15h14): o vídeo inteiro foi montado, mas o job morreu no último passo com `NameError: thumb` (a função `thumb` estava definida depois do `if __name__ == "__main__"`). Sem artefato, sem prévia e sem Telegram: o vídeo se perdeu.
  - **Duração:** 7,8 min (abaixo dos 8 min da regra).
  - **Voz por bloco (Whisper, melhor tomada):** Início 98%, Mercúrio **87%**, Marte **87%**, Júpiter 94%, Saturno 91%, Urano **85%**, Netuno 90%, Vênus 88% (a 2ª tomada caiu no 429), Terra 92%. Três blocos abaixo de 88%.
  - **Capítulos dessa versão:** 0:00 Início, 0:33 Mercúrio, 1:40 Marte, 2:49 Júpiter, 3:51 Saturno, 4:40 Urano, 5:29 Netuno, 6:10 Vênus, 7:12 Terra. Vão mudar no próximo render, porque o roteiro cresceu.
- **Correção (commit cd16029):**
  - `src/longo.py`: o `__main__` foi para o fim do arquivo, e uma falha na thumb não derruba mais o envio do vídeo. Cada bloco pode ter `"tomadas"` própria. Thumb testada aqui: ok.
  - Roteiro: +7 falas curtas (cerca de +30 s), só com fatos do `longo_01_fatos.md` ou frases sem número. Exemplos: a exosfera de Mercúrio, Venera, o dia e o ano de Vênus, 1989 na mancha de Netuno, "vinte e um anos no escuro". Saíram duas falas com dado fora do arquivo de fatos (tornados magnéticos de Mercúrio e Fobos). Mercúrio, Marte, Urano e Vênus passam a ter 3 tomadas.
  - **Atenção:** o roteiro ainda tem números que não estão no arquivo de fatos, como 687 dias, 84 anos, 21% de oxigênio, gravidade de Júpiter, metano em Netuno e "50 km" em Vênus. Conferir e incluir as fontes no arquivo antes do post.
- **Run 45675455221** (re-render, 15h28): morreu no 1º bloco com **429 "You exceeded your current quota"** (cota diária do TTS esgotada: Fermi de manhã + cerca de 17 chamadas do 1º render). Não insisti.
- **Conclusão:** o longo gasta cerca de 20 chamadas de voz, a cota inteira de um dia. Ele precisa de um dia **sem nenhum Short renderizado**. Proposta: render na **Sex 27/11 de manhã**, porque na quinta a cota vai para o Apophis. O post de sábado às 11h continua possível.
- 25/11 16h05 (reserva da fila, faixa das 16h17): 1 post hoje (anéis), o último há mais de 2 h, e o Upload-Post segue no limite do mês (429, reinicia por volta de 17/12). Mandei no Telegram (run 45681585774, `acao=telegram`, 16h05) "E se você descesse no buraco mais fundo já cavado?" para o Vitor postar à mão. Fila intacta com 5; passa para `postados` na próxima faixa.

## 25/11 (16h40): revisão da v1 do longo e plano até sábado
- **O NameError da thumb foi culpa minha**: eu acrescentei a função `thumb` no fim do arquivo, depois do `__main__`. A rodada da tarde já tinha corrigido.
- **Agora**, um ensaio completo aqui (as 9 partes, narração falsa e Telegram desligado) roda do começo ao fim: vídeo, capítulos, prévia, thumb e `vozes.json`. Não deve mais morrer no último passo.
- **Proteção da cota:**
  - A narração de cada bloco agora vira artefato (`narracao-longo`), mesmo se o job falhar.
  - O `longo-esfr.yml` tem o input `reusar_narracao=<run>`, que reaproveita a voz dos blocos cujo texto não mudou. Assim, refazer o visual não gasta cota.
  - O vídeo também é guardado mesmo com falha. Teste local do reaproveitamento: ok.
- **Voz dos blocos fracos** (Mercúrio 87%, Marte 87%, Urano 85%): os números falados mais longos ficaram mais simples, e a tela continua mostrando o valor exato:
  - "quase seis meses" (176 dias);
  - "mais de cento e cinquenta graus negativos" (-153);
  - "quase dois anos da Terra" (687 dias);
  - "praticamente deitado" (97,8°);
  - "passa de duzentos e vinte graus negativos" (-224);
  - "uns oito meses e uns sete meses e meio" (243 e 225 dias).
- **Visual:**
  - Planeta em várias cenas seguidas agora alterna o enquadramento sozinho (`_variar`).
  - Eixo de rotação tracejado em Urano (deitado) e em Marte (25°).
- **Fatos:** os números que faltavam (687 dias, 84 anos, 21% de oxigênio, gravidade de Júpiter, metano, 50 km em Vênus etc.) foram anotados com a fonte em `docs/esfr/longo_01_fatos.md`.
- **Plano da cota até sábado:**
  - **Qui 26/11:** só o re-render do Apophis (3 chamadas). **NADA do longo.**
  - **Sex 27/11:** o longo inteiro às **08h11** (tarefa agendada). A rodada diária de sexta (09h41) **não renderiza Short nenhum antes de o longo terminar**. Se a fila precisar, renderiza depois, só se sobrar cota.
  - Se a v2 precisar de ajuste só visual, re-renderizar com `reusar_narracao=<run da sexta>`, sem gastar voz.
- 25/11 20h05 (reserva da fila, faixa das 20h17): "buraco mais fundo" (Telegram 16h05) passou para `postados` como postado. 2 posts hoje, o último há mais de 2 h, e o Upload-Post segue no limite do mês (429, reinicia por volta de 17/12). Mandei no Telegram (run 45718551793, `acao=telegram`, 20h05) "E se você descesse até o fundo da Fossa das Marianas?" para o Vitor postar à mão. Fila com 4; passa para `postados` na próxima faixa.
- 25/11 20h57: o print do Vitor mostra que só os 'anéis' estão no ar hoje: o buraco mais fundo (mandado às 16h05) e a Fossa (20h05) ainda não foram postados. O buraco mais fundo voltou para a fila. A pedido do Vitor, que quer um vídeo diferente para furar a bolha, o **Fermi sai agora (21h)**. Ordem nova: qui 12h17 buraco mais fundo, 16h17 Fossa, 20h17 Betelgeuse; sex Apophis.
- 26/11 07h10: **o Fermi rendeu pouco** (palavra do Vitor, cerca de 10 h depois do post das 21h). Leitura:
  - **Gancho abstrato:** "gritasse pro universo" não ameaça nada concreto no mundo de quem assiste. Os campeões ameaçam algo concreto e agora: a Lua (2,4 mil), o Sol (1,7 mil), o traje (1,4 mil).
  - **Conceito pesado:** 3 hipóteses em 60 s. A Lua, o melhor do canal, tem 91 palavras e uns 40 s.
  - **Regra nova:** 35 a 45 s (no máximo cerca de 100 palavras), um objeto concreto em perigo já na 1ª frase e uma ideia só por vídeo.
  - **Próximo teste do tema "aliens"** (concreto e em segunda pessoa): "E se um sinal alienígena chegasse hoje?" ou "E se os aliens já estivessem vendo a Terra?". Não repostar nem apagar o Fermi; esperar 72 h, porque Shorts às vezes ganham uma 2ª onda.

## 26/11 (manhã, tarefa diária)
- **Conexões (fila-esfr testar, run 45822384970):** YouTube conectado com **43 inscritos** (eram 39 ontem), Upload-Post ok (200, segue no limite do mês até ~17/12), chave Gemini própria com TTS. O `gh` voltou a funcionar neste ambiente.
- **Números:** sem views novas (a análise só roda nos workflows). Último print segue o de 25/11 (todos os 8 primeiros passaram de mil).
- **Fila:** o Fermi (postado ontem às 21h) passou para `postados`.
- **Render do longo (1,2,5) às 09h29 (run 45820084741)**, disparado pelo Vitor, terminou ok. Os Shorts de hoje esperaram ele acabar.
- **Vídeos novos, já na regra do Fermi** (objeto concreto em perigo na 1ª frase, uma ideia, ~40 s, poucos números falados):
  - 16 "E se o SOL desligasse a internet do mundo?" (tempestade solar de 1859; run **45824177115**, 41,8 s, voz Puck **99% na 1ª tomada**). Fontes: Space.com/The Conversation (David Wallace, abr/2022), IFLScience (dez/2020), EarthSky (mai/2024). Só 1 número falado ("quinhentos anos", Space.com). O ano 1859 virou "na época do telégrafo". Ficaram de fora: a hora de viagem da nuvem e o "quase acertou em 2012" (nenhuma fonte aberta dava o número).
  - 17 "E se o gelo da ANTÁRTIDA derretesse inteiro?" (run **45824764161**, 40,9 s, voz 97% na 2ª tomada; a 1ª deu 93%, e houve dois 429 de minuto, que passaram sozinhos). Fontes: NSIDC (Quick Facts: 58 m, quase 4,9 km no ponto mais grosso, área de EUA + México; Why Ice Sheets Matter: uns 400 lagos sob o gelo), NASA Sea Level (58 m; rocha abaixo do nível do mar na Antártida Ocidental), AntarcticGlaciers.org, PolarTREC/NSF ("milhares de anos"). O gancho "prédio de vinte andares" é a conta 58 m ≈ 20 andares de 3 m. As fontes discordam (58 x 60 m): usei 58 (NSIDC Quick Facts e NASA).
- **Apophis (13) re-renderizado:** run **45825799729**, 51,9 s, voz 96%. O medidor descendo agora mostra "•••" no lugar dos números de passagem. `run_id` trocado na fila, no mesmo lugar.
- **Quadros novos em `src/voce.py`** (testados com folha de prova antes):
  - `solar`: o Sol no alto soltando a nuvem até a Terra com o escudo magnético (`choque` espreme as linhas e acende auroras nos polos); `telegrafo` (chave batendo, fita de papel, `faiscas`, `fogo`, `choque` no operador, `sem_bateria`); `aurora` (cortinas verde e rosa, casas antigas, `jornal`); `cidade` (janelas apagando em onda, `transformador` com faíscas e fumaça, `sem_internet`); `gps` (celular com o ponto pulando e o círculo de erro).
  - `gelo`: litoral com o mar subindo e régua em metros (prédio de 20 andares com você no teto); `mapa` (Antártida de cima, `derrete`, `solta`); `corte` (gelo sobre a rocha, `medida`, `abaixo`, `lagos`).
- **Fila com 6 (meta batida):** buraco mais fundo, Fossa, Betelgeuse, Apophis, tempestade solar, Antártida. O Vênus (10, run 45396326379) segue fora, para a tarefa de sábado.
- **Cota de voz hoje:** 3 renders de Short (4 chamadas de TTS + 2 tentativas com 429 de minuto) depois do teste do longo do Vitor. Nada mais hoje, para a cota de amanhã ficar livre para o longo das 08h11.
- **Duração:** a tarefa diária pede 45 a 60 s, mas a lição do Fermi (`docs/ESFR.md`) pede 35 a 45 s. Os dois novos ficaram em ~41 s, seguindo a lição, que é mais nova e veio dos números.
- **Testar depois:** comparar os dois novos (gancho concreto, ~41 s) com o Fermi (abstrato, 60 s) e com a Lua (91 palavras). Se segurarem melhor, ~40 s vira o padrão. Ideias sem uso: sinal alienígena chegando hoje (o próximo do tema aliens, concreto), a Terra sem a Lua desde o começo, um dia em Mercúrio. A "gravidade sumindo por 5 s" foi descartada por enquanto: as fontes abertas são fracas, falam muito do corpo (saúde) e um texto até diz que a água "viraria hidrogênio".
- **Vídeo longo:** hoje é quinta (o planejamento semanal é no domingo). Render completo amanhã às 08h11, como combinado.

- 26/11 12h06 (reserva da fila, faixa das 12h17): nenhum post hoje, o último foi o Fermi (25/11 21h). Upload-Post segue no limite do mês (429, reinicia por volta de 17/12). Mandei no Telegram (run 45845511997, `acao=telegram`, 12h06) "E se você descesse no buraco mais fundo já cavado?" para o Vitor postar à mão. Fila com 6; passa para `postados` na próxima faixa.
- 26/11 12h57: **TESTE de agendamento direto no YouTube** (`acao=agendar`): a Fossa subiu privada e agendada para hoje às 16h17 (id 62h4CPs7r3M, thumb ok). **A reserva das 16h03 NÃO deve mandar nada hoje: a faixa das 16h17 é da Fossa agendada.** A das 20h03 segue o normal (Betelgeuse).
- 26/11 16h25: **o agendamento direto no YouTube FUNCIONOU.** A Fossa (62h4CPs7r3M) ficou pública sozinha às 16h17. Daqui em diante a reserva AGENDA cada faixa (`acao=agendar`). Cota: 1.600 unidades da API por envio (10 mil por dia no projeto, compartilhado com o terror), até 6 envios por dia somando os canais.
- 26/11 20h05 (reserva, faixa das 20h17): Betelgeuse ("E se você visse uma estrela explodir no céu?") AGENDADO direto no YouTube (run 45908690714, id _x7yN5gaVZo, thumb ok), sai às 20h17. 3 posts hoje (meta batida). Fila com 3.
