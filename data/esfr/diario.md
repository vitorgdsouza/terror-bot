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
