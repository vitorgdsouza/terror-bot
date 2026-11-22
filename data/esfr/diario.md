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
