# E Se Fosse Real?: vídeos longos

Regras do formato longo (8 a 12 min), separadas dos Shorts. Valem só para este canal. Pesquisa feita em 22/11/2026.

## O que funciona em canais parecidos
- **"What Would Dying on Every Planet Be Like? (Venus Takes 5 Seconds)"**, do canal What If: cerca de 17 milhões de views (vidIQ, nov/2026). Passa planeta por planeta, como uma simulação.
- **Ciência Todo Dia**, a referência no Brasil: os longos têm mediana de cerca de 12 min, e vários passam de 700 mil views. **10 a 12 min é o tamanho certo para o público daqui.**
- **melodysheep** ("Timelapse of the Future"): a escala acelera o tempo inteiro, e a sensação de progresso segura o vídeo.
- **Kurzgesagt**: um personagem com quem o público se identifica no centro, com movimento contínuo.

## Regras do longo (diferente dos Shorts)
1. **Nada de cartão parado com texto ou conta.** Cada número vira um objeto que se mexe: o boneco ao lado de um vulcão, a Terra dentro de uma tempestade, uma barra enchendo. A câmera nunca para.
2. **O personagem "você" é recorrente**, com um traje que vai se estragando de um planeta para o outro. As piadas são visuais (bandeira derretendo, capacete embaçando).
3. **Gancho com o resultado primeiro (0 a 5 s)**, sem logo, e a promessa até os 30 s. O placar começa vazio na tela.
4. **Open loops:** cada parte termina com um mini-gancho para a próxima ("Mercúrio parece fácil… até o Sol nascer").
5. **Escalada e placar fixo no canto** ("4 de 8"), para a pessoa ver o progresso.
6. **Reengajamento perto dos min 3 e 6**, com o maior espetáculo do vídeo nesses pontos.
7. **Escala e comparação visual** no lugar de números soltos.
8. **Capítulos** na descrição e na barra do vídeo.
9. **Final seco:** não anunciar o fim. Pergunta para o próximo vídeo e corte.
10. **A essência do canal fica:** segunda pessoa, "E se você...?", fatos com fonte, visual da paleta ciência e voz Puck.

## 1º longo: "E se você pousasse em cada planeta do Sistema Solar?"
Estrutura (cerca de 11 min). A ordem segue a escalada, não a distância ao Sol:
- **0:00 a 0:30:** gancho em Vênus ("você dura menos que esta frase"), os 8 planetas enfileirados e o placar "tempo de sobrevivência" vazio.
- **0:30 a 1:30:** Mercúrio. O pouso é fácil, mas o Sol nasce.
- **1:30 a 2:45:** Marte. A "boa notícia": dá para sobreviver de traje. Escala com o Monte Olimpo.
- **2:45 a 4:15:** Júpiter. Não tem chão: descida contínua, a câmera atravessando as camadas (reengajamento).
- **4:15 a 5:45:** Saturno. Os anéis de perto; um planeta menos denso que a água.
- **5:45 a 7:00:** Urano. Deitado de lado, estações longas, frio (reengajamento).
- **7:00 a 8:15:** Netuno. Os ventos mais rápidos, longe e escuro.
- **8:15 a 9:30:** volta a Vênus em detalhe: por que ele é o pior. Payoff do gancho.
- **9:30 a 10:30:** a Terra vista de fora. "O único lugar do placar com tempo infinito."
- **10:30 a 11:00:** pergunta para o próximo ("e se fosse nas luas?") e corte.
- **Todo número sai de fonte** (NASA e afins), conferida antes de escrever, como nos Shorts.

## O que falta no motor
- Render em **16:9 (1920x1080)**: os quadros de hoje são verticais.
- **Câmera contínua** entre as cenas (zoom e travelling), não só um corte por frase.
- **Placar e barra de capítulos fixos** na tela.
- **Narração em blocos** (um por planeta), com o mesmo TTS, e a junção com a trilha.
- **Quadros dos planetas** (Mercúrio, Vênus, Marte, Júpiter, Saturno, Urano, Netuno) no padrão novo: a Terra com os continentes de verdade (`src/globo.py`) e o buraco negro realista (`src/buraco_negro.py`) são a referência de qualidade.

Fontes da pesquisa: vidiq.com (estatísticas dos canais What If e Ciência Todo Dia), uniladtech.com (sobre o vídeo de 17 mi), wikiwand.com (Timelapse of the Future), kurzgesagt.org, kottke.org (bastidores do Kurzgesagt), memorando de produção da equipe MrBeast (alexanderjarvis.com), 1of10.com e vidiq.com/blog (retenção).

## Calendário do 1º longo (combinado com o Vitor em 22/11)
- **Qua 25/11, à tarde:** render completo (`longo-esfr.yml`, roteiro `roteiros/esfr/longo_01_planetas.json`, cerca de 9 a 10 min, trilha própria). Revisar a prévia `data/previas/longo_01_planetas.jpg` e o log (voz de cada bloco ≥ 88%). Nesse dia, a rodada de Shorts faz no máximo 1 render (cota de voz).
- **Qua 25/11, resultado:** não ficou pronto. O run 45662288412 montou 7,8 min, mas morreu no fim (bug da thumb, já corrigido), com a voz abaixo de 88% em Mercúrio (87%), Marte (87%) e Urano (85%). O roteiro ganhou cerca de 30 s e 3 tomadas nesses blocos. O re-render (run 45675455221) parou no 429 de cota diária. **O longo gasta a cota de voz de um dia inteiro: renderize num dia sem Short (proposta: Sex 27/11 de manhã).** Os capítulos saem do log do próximo render.
- **Qui 26/11, 09h30 (teste dos blocos fracos, run 45820084741):** Marte 92%; Mercúrio 87/87/87; Urano 85/87/86. As notas eram iguais nas 3 tomadas, o que indica um problema na **régua** e não na voz: o Whisper escreve "88", "38%" e "-180°C", e o roteiro escreve tudo por extenso, então cada número contava como erro. Os blocos com mais números (Mercúrio e Urano) eram os mais punidos. **Corrigido em `src/voz_gemini.py` (`_expande`): números em algarismos agora contam por extenso.** A narração desses 3 blocos ficou guardada nesse run e serve de reserva se a cota acabar na sexta (`reusar_narracao=45820084741`).
- **Sáb 28/11, 11h:** o Vitor posta o longo à mão no YouTube (Upload-Post no limite até por volta de 17/12): título, descrição com os capítulos, thumb 16:9 (`thumb_longo.jpg`, que vai no Telegram).
- **Sáb 28/11:** sem Short às 12h17. O Short "E se você pousasse em Vênus?" (`esfr_10_venus.json`) sai às 16h17, com o longo como "vídeo relacionado".
- **Depois:** um longo por semana, sempre sábado às 11h, até o Studio mostrar o horário real do público (Análises → Público → "Quando seus espectadores estão no YouTube").

### Render (27/11): VERSÃO FINAL = v2, run 46003770264
- 8,5 min; vídeo e thumb mandados no Telegram (cópia de 47 MB; o original de 107 MB fica no artefato `video-longo` desse run).
- A v1 (run 45988557168) ficou como plano B; não usar.
- Capítulos para a descrição (v2):
  0:00 Início
  0:40 Mercúrio
  1:43 Marte
  2:56 Júpiter
  4:02 Saturno
  4:57 Urano
  5:46 Netuno
  6:35 Vênus
  7:48 Terra
