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

## 18/11 (noite): série nova "Pode Entrar?" (Roteirista, conversa com o Vitor)
- O Vitor pediu uma série de episódios em que o público decide se deixa um visitante entrar em casa, inspirada só na mecânica de No, I'm Not a Human. Ficou combinado: mundo próprio, sem o cânone do Cliente e sem nada do jogo (história, criaturas, sinais, arte).
- Premissa aprovada pelo Vitor: o Inverno Errado (geada cinza há 19 dias), os Ocos e o caderno da Dona Lurdes. Detalhes em DIRECAO §5 e PERSONAGENS.
- Gosto novo do Vitor: POV vai até a porta e o zoom no olho mágico passa a mostrar só quem está lá fora; todo episódio abre com um contexto rápido do universo.
- Ep. 1 "O Entregador" escrito em `roteiros/pode_entrar_01.json` (11 cenas, ~148 palavras, mira 55 a 60 s). NÃO foi proposto ainda: depende de 5 cenários novos.
- **Pedido ao Diretor de Arte:** criar o traço da série e os prompts de `olho_tiago`, `inverno_rua`, `caderno_lurdes`, `esp_tiago_vidro` e `olho_tiago_celular` (descrições em PERSONAGENS), e conferir o ponto do olho mágico em `porta_entrada` (usei foco [0.3, 0.38, 3.5]). Assim que as imagens forem cadastradas, o Roteirista propõe o Ep. 1.

## 18/11 (noite): traço e arte do "Pode Entrar?" (Diretor de Arte)
- **Traço da série:** pintura digital semi-realista, limpa e nítida, paleta fria de geada (cinza, azul-ardósia, prata) com o âmbar da lareira como única cor quente; visitantes vistos pelo olho mágico (círculo com leve olho de peixe, preto em volta). Sem granulado, ruído, glitch ou rosto deformado, para ficar longe do visual do No, I'm Not a Human. O medo vem do "certo demais", não de monstro. Bloco de estilo e marca visual do Tiago (cachecol laranja, jaqueta verde-petróleo com faixas prateadas, argola na orelha esquerda) em `docs/PERSONAGENS.md`.
- **Prompts entregues ao Vitor pela conversa (sem aviso no Telegram, a pedido do Roteirista):** `olho_tiago`, `inverno_rua`, `caderno_lurdes`, `esp_tiago_vidro` e `olho_tiago_celular`, mais o opcional `porta_inverno`. Todos no catálogo de cenários, seção "Pode Entrar?". Gerar o `olho_tiago` primeiro e usá-lo como referência nos outros com o Tiago.
- **Aprovação do traço:** o `olho_tiago`, com quadro de prova, é o quadro de teste. O traço só estreia depois de o Vitor aprovar.
- **Olho mágico do `porta_entrada`:** fica em (0,329; 0,346) da imagem. O motor corta 1188→1080 e soma o zoom da câmera, então no quadro ele cai em x≈0,30 e y≈0,32. O foco da cena 5 foi de [0.3, 0.38, 3.5] para [0.3, 0.32, 3.5]. Com 0.38 o olho mágico ficava no terço de cima do quadro e subia durante a cena; com 0.32 fica no centro (conferido com quadros de prova no início, meio e fim). O zoom 3.5 mantém a moldura da porta visível; 5.0 vira um ponto num fundo liso.
- **Atenção:** o `porta_entrada` está no traço cartoon do Guizo. Para a série ficar coerente, sugeri o `porta_inverno` (porta por dentro com lareira, no traço novo). Se o Vitor gerar, troca-se o cenário da cena 5 e recalcula-se o foco.
- **`anima` sugerida para `esp_tiago_vidro`:** `partes` com o rosto em `balanco` e o pivô no queixo (a cabeça inclina devagar). O motor não tem piscar de olhos; as regiões exatas são medidas quando a imagem chegar.
- **Ao receber cada imagem:** medir a posição do rosto e da bag no `olho_tiago` e ajustar os focos das cenas 7 ([0.5, 0.62, 1.8]) e 8 ([0.5, 0.42, 2.4]).
- **18/11 (noite, depois):** os prompts do Ep. 1 não estavam salvos no catálogo. Reescrevi os 6 (`olho_tiago`, `inverno_rua`, `caderno_lurdes`, `esp_tiago_vidro`, `olho_tiago_celular` e o opcional `porta_inverno`) e gravei na seção "Pode Entrar?" do catálogo de cenários. Mandados ao Vitor pela conversa. No `olho_tiago` ele segura a bag no peito (cena 7) e não sai vapor da boca.
- **`olho_tiago` recebido (18/11, noite):** veio em 3:4 (896x1200), então em vez de corte de cobertura completei com preto em cima e embaixo até 1188x2112 (o fundo já é preto, e o aro do olho mágico fica inteiro). O Gemini desenhou uma nuvem de vapor saindo da boca, o que quebraria a pista do episódio; apaguei com um remendo do fundo ao lado. Cadastrado em `cenarios.json` e no guia do `src/animacao.py`. Focos ajustados no roteiro: cena 7 [0.5, 0.55, 1.8] (rosto e bag) e cena 8 [0.5, 0.37, 2.6] (rosto e lábios). Quadro de teste do traço enviado ao Vitor; o traço só estreia com a aprovação dele.
