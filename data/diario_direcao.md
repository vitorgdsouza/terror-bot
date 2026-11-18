# Diário da direção criativa

## 2026-11-17 (montagem)
- Calendário definido pelo Vitor: 11h47 isca; 18h47 alterna protocolo / história.
- Fila inicial de iscas: Conte as Batidas, Seu Cachorro Abana o Rabo?, Qual Porta Você Abre?, Você Viu Ele? (esta refeita na manhã de 18/11).
- Números: Guizo Ep.1 1.088, Rufus Fita 01 1.094, Protocolo Stu 965, 3 Coisas (real) 281; os 6 postados no fim da tarde de 17/11 ficaram com < 10 views em 12 h (postamos demais no mesmo dia).
- Guizo Ep. 2 "O Poço do Quintal" postado 17/11 à noite (A descer pela corda / B ligar para os pais). Aguardar votos.
- 18/11 é dia de PROTOCOLO (o primeiro principal da fila nova).
- Ideias a testar: protocolo de criatura nova (não só Stu/Rufus); história avulsa nova com cara de série; iscas que fazem rever (detalhe escondido, contar algo).

## 18/11 (madrugada): diagnóstico da queda de views
- **Os 4 primeiros vídeos**, de 16/11 à noite até 17/11 de madrugada, fizeram cerca de 1.000 views cada.
- **Tudo o que saiu a partir das 11h37 de 17/11** ficou com 4 a 8 views. Isso vale tanto para os posts manuais quanto para os do Upload-Post, então a forma de postar não é a causa.
- **Status checado pela API:** todos estão públicos, processados, sem "para crianças" e sem restrição de região.
- **Provável causa:**
  - fim do "teste inicial" que o YouTube dá a canais novos, com a retenção dos primeiros decidindo o resto;
  - 9 Shorts em cerca de 25 h.
- **Plano:**
  - no máximo 2 posts por dia, já garantido pela fila;
  - histórias com 50 a 60 s;
  - gancho visual no 1º segundo;
  - ler a retenção dos vídeos de 1.000 views quando os dados chegarem (19 a 20/11) e ajustar a partir dela.
- Os uploads manuais saíram com idioma pt-PT. Vale trocar o padrão do canal para pt-BR.

## 18/11 (manhã): dia de PROTOCOLO
- **Dia:** o último principal foi o Guizo Ep. 2 (história, 17/11), então hoje é protocolo. A fila tinha 4 iscas (Farmácia 03:17 sai às 11h47; ficam 3), então não precisou de isca nova.
- **Números (relatório de hoje):** canal com 3.470 views e 16 inscritos. Os 4 primeiros seguem perto de 1.100 (Rufus Fita 01 1.097, Protocolo Stu 1.104, Guizo Ep. 1 1.104; Fatos do sono 401). Tudo o que saiu em 17/11 está com 1 a 8 views. O relatório ainda não traz retenção nem origem (atraso de 2 a 3 dias): reler em 19 ou 20/11.
- **Tendências:** analog horror segue firme no vídeo curto, com imitadores e protocolos de cotidiano. A "versão macabra de personagem de domínio público" aparece em filmes (a onda dos clássicos infantis que viraram terror), mas não achei sinal de que esteja em alta nos Shorts: continua no radar, sem teste.
- **Feito:** "Se a Campainha Tocar Duas Vezes" (`roteiros/protocolo_03_cliente.json`, rótulo PROTOCOLO 3H17), a primeira criatura nova em protocolo. É o par da isca da manhã: a isca pergunta "o que ele pede?" e o protocolo das 18h47 responde (hortelã e esparadrapo). Também estreia o Cliente das 3h17 antes da série Turno da Madrugada. O tema é o de imitador (a ligação de quem você ama), que é o mais forte do gênero. Fecha com "Quantas vezes a campainha tocou?", que puxa revisão e comentário.
- **Código novo:** os ícones sino, camera, celular e cliente; a sombra de fundo `cliente`; e a cena especial ilustrada dentro do protocolo (`cenario` numa cena, com o alerta por cima), usada no susto com `esp_cliente_balcao2`.
- **Controle de qualidade:**
  - 1ª tomada (run 44285752913): voz Enceladus no Gemini, nota de 97%, mas 66 s, acima do limite de 55. Reprovada; enxuguei o texto.
  - 2ª tomada (run 44286464253): Enceladus no Gemini, nota de 98%, 54 s. Pictogramas legíveis, a cena especial clara e com o texto no rodapé sem tapar o rosto. Cânone conferido: não aparece na câmera, só entra se convidado, hortelã e esparadrapo, imita quem você ama. Aprovado e na fila das 18h47.
- **Testar depois:**
  - comparar o par isca + protocolo do mesmo tema com os dias soltos;
  - ver nos comentários se a pergunta da campainha gera resposta;
  - se o Cliente for bem, estrear o Turno da Madrugada (Bia) no próximo dia de história.
  - Votos do Guizo Ep. 2 e da Fita 02 ainda sem resultado do Vitor, então nada de continuação.

## 18/11 (tarde): a isca das 11h47 não saiu
- O GitHub não disparou o agendamento das 11h47 (cron 14:47 UTC). Nenhuma execução da fila foi criada. É uma falha conhecida do `schedule` do GitHub, que atrasa ou pula disparos em horário de pico.
- Com o OK do Vitor, rodei a fila à mão às 12h28 (turno manhã): a Fita da Farmácia 03:17 saiu no YouTube pelo Upload-Post.
- Trava nova em `src/fila.py`: um agendamento que chegue atrasado não posta se a faixa dele já saiu no dia, nem se já houver 2 posts no dia.
- O protocolo das 18h47 continua dependendo do agendamento. Se não sair até umas 19h15, rodar `fila.yml` com `turno=tarde`.

## 18/11 (tarde): primeiro sinal de recuperação
- A "Fita da Farmácia 03:17", isca no padrão novo, tinha **192 views 4 h depois de sair**. Os vídeos do dia 17 estavam parados em 4 a 8.
- **O que ela tinha de diferente:**
  - VHS de câmera de segurança, com o relógio virando 03:17 no susto;
  - cena especial com o rosto do Cliente;
  - thumb com o rosto da criatura em close;
  - pergunta aberta na legenda;
  - personagem novo (série nova).
- **Hipóteses para testar:**
  - thumb com rosto de criatura > thumb com pictograma ou com o Lucas;
  - linguagem VHS/CFTV segura melhor o início.
- Comparar a retenção dela com a das outras quando os dados de analytics chegarem.

## 18/11 (15h23): rodada do Revisor e do Publicador
- `data/aprovacoes.json` ainda não existe: nenhuma aprovação passou pela Mesa. Não há item "renderizado", "renderizando" nem "refazer", então o Revisor e o Roteirista não tiveram o que fazer.
- Nenhum render novo depois do Protocolo 3h17 revisado (run 44345291582, concluído às 16h19 UTC).
- **Fila:** o principal das 18h47 de hoje está garantido ("Se a Campainha Tocar Duas Vezes", protocolo). Há 3 iscas na fila (Conte as Batidas, Seu Cachorro Abana o Rabo?, Qual Porta Você Abre?), acima do mínimo de 2. Nada a avisar.
- **Mesa do Gerente:** já estava certa (nada aguardando, sem decisão nova). Não mexi.
- **Nota técnica:** nesta sessão o `gh` CLI veio com token inválido. Para disparar workflows, usar as ferramentas do GitHub (MCP) em vez do `gh`.
