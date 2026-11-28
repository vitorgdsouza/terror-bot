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
- **`olho_tiago_celular` recebido (18/11, noite):** veio em 9:16 (768x1376); fiz corte de cobertura para 1188x2112. O Gemini pôs vapor de novo ao lado do rosto; apaguei. Cadastrado em `cenarios.json` e no guia. Prova da cena 10 ok: a tela do celular fica grande e legível no centro, com barras vazias onde cabe um `texto_tela` (sugestão ao Roteirista: "PEDIDO #… · há 19 dias"). Faltam `inverno_rua`, `caderno_lurdes`, `esp_tiago_vidro` (e o opcional `porta_inverno`).
- **`inverno_rua` recebido (18/11, noite):** veio em 3:4; corte de cobertura para 1188x2112, deslocado um pouco à direita para manter o carro e a casa da chaminé. A janela acesa com fumaça ao fundo ficou boa: é a única casa "viva" da rua. Prova das cenas 2 (pan) e 3 (zoom na casa) ok. Faltam `caderno_lurdes` e `esp_tiago_vidro` (e o opcional `porta_inverno`).
- **`caderno_lurdes` recebido (18/11, noite):** o Gemini escreveu palavras legíveis em INGLÊS ("door in peephole", "Fogged window"), o que não combina com o caderno de uma senhora brasileira e quebraria a regra de texto só por cima. Cobri as duas linhas com rabiscos clonados de linhas ilegíveis da mesma página (alinhados às pautas e com a luz corrigida). Corte 9:16 puxado para a direita para manter a vela. Prova da cena 4 ok. Falta só `esp_tiago_vidro` (e o opcional `porta_inverno`).
- **`esp_tiago_vidro` recebido (18/11, noite):** sem vapor e com o vidro limpo, como pedido. Completado com preto até 1188x2112 (aro inteiro). `anima`: `partes` com o rosto em `balanco` e o pivô no queixo, então a cabeça inclina devagar sem rasgar a imagem (prova em 4 instantes ok). **As 5 artes obrigatórias do Ep. 1 estão cadastradas.** Recado ao Roteirista: o Ep. 1 "O Entregador" já pode ser proposto ao Vitor; sugestão de `texto_tela` na cena 10 sobre as barras vazias do app ("PEDIDO · há 19 dias"). O `porta_inverno` (opcional) não chegou, então a cena 5 segue no `porta_entrada` cartoon. O traço da série ainda espera a aprovação do Vitor no quadro de teste do `olho_tiago`.
- **`porta_inverno` recebido (18/11, noite):** a porta por dentro no traço da série, com as latas de comida contadas na prateleira (bom detalhe da premissa). Corte 9:16 puxado para a esquerda para manter a lareira, que é a única luz quente. Cena 5 trocada de `porta_entrada` para `porta_inverno`, com foco [0.55, 0.265, 2.4]: mostra a porta, a corrente e a cadeira e aproxima do olho mágico (com 3.5 vira só madeira lisa). **Todas as artes do Ep. 1 estão prontas.**

## 18/11 (noite): regra base do "Pode Entrar?" (Roteirista)
- Regra do Vitor: Oco + só você na casa → você morre pelo Primeiro (líder dos Ocos, humanoide distorcido). Oco + 2 humanos (fora você) → o Oco leva um humano. O protagonista testa quem está dentro para expulsar o Oco. Registrado em DIRECAO §5 e PERSONAGENS.
- Sinal físico novo proposto: a geada não derrete nos Ocos. Ainda não entra no Ep. 1 (que já está equilibrado em 2 sinais de cada lado); estreia numa página nova do caderno.
- Ep. 1: a fala do caderno agora avisa "se um entrar... o Primeiro vem buscar você" (aumenta o peso do voto). 153 palavras: o Revisor confere se passa de 60 s.
- Decisão do Vitor: o Ep. 1 mantém o voto SIM/NÃO, mas o Tiago é humano em qualquer caso (segredo da equipe, explicações em PERSONAGENS). Ep. 1 enviado para aprovação.

## 18/11 (noite): plano do Ep. 2 do "Pode Entrar?" (Roteirista, rascunho, não proposto)
- Duas versões prontas para quando o Vitor informar o voto. A visitante nova é a mesma nas duas (economiza arte): **Lia, 34, técnica de enfermagem**, com uma maleta de remédios; a sua tosse começou ontem.
  - Sinal de humano: o bafo dela embaça o vidro. Sinal de Oco: a geada nos cílios não derrete (sinal novo, página 2 do caderno). Mais um: ela sabe o seu nome.
- **Versão SIM:** abre no Tiago dentro de casa, perto da lareira, dividindo a comida. Ele acha o caderno sozinho ("como ele sabia onde estava?"). Página 2 revela a geada. Batida: Lia. Voto: abre para a Lia?
- **Versão NÃO:** abre com as batidas parando. De manhã não amanhece; pelo olho mágico, a varanda vazia e a bag do Tiago encostada na porta. Batida: Lia, usando o cachecol laranja do Tiago. Voto: abre?
- Arte a encomendar depois do OK do Vitor: `sala_lareira_tiago`, `caderno_lurdes2`, `olho_bag`, `olho_lia`, `olho_lia_cachecol`, `esp_lia_cilios`.

## 18/11 (noite): o protocolo das 18h47 também não saiu sozinho
- O agendamento das 18h47 (cron 21:47 UTC) não disparou de novo. É a segunda falha do `schedule` do GitHub no dia.
- Com o OK do Vitor, o Publicador rodou `fila.yml` com `turno=tarde` às 19h15 (run 44409859984). "Se a Campainha Tocar Duas Vezes" saiu no YouTube pelo Upload-Post (status completed, 22:19 UTC).
- Fila agora: 3 iscas e **nenhum principal**. É preciso aprovar um principal (história) para 19/11.
- Sugestão: o `schedule` do GitHub falhou nas duas faixas de hoje. Vale ter um disparo de reserva (por exemplo, uma tarefa agendada que confere e roda a fila uns 20 min depois de cada faixa).

## 18/11 (noite): erro meu na fila (Roteirista)
- Rodei `fila.yml` à mão (turno tarde) para soltar o protocolo, sem conferir que o Publicador já tinha postado às 22h19 UTC. Como a fila não tinha mais principal, ela postou a isca "Conte as Batidas" às 22h27 UTC. O Vitor apagou o vídeo.
- Corrigido: "Conte as Batidas" voltou para o topo da fila. O Ep. 1 do Pode Entrar? entrou na fila (aprovado pelo Vitor) para 19/11 às 18h47. `pendente.json` marcado como resolvido para o /postar antigo não publicar o Ep. 1 antes da hora.
- **Lição:** antes de rodar a fila à mão, `git pull` e conferir `postados`. Ponto fraco: a trava de `src/fila.py` só vale para o agendamento; a execução manual passa por cima dela e, sem principal, cai numa isca.
- O Vitor vai postar o protocolo à mão no TikTok. Plano de 19/11: uma isca no padrão da Fita da Farmácia às 11h47 e o Ep. 1 às 18h47.

## 19/11 (madrugada): isca da campainha (Roteirista)
- Print do Vitor às 23h52: protocolo da campainha 597 views em ~4 h, Farmácia 961, Poço do Quintal (thumb do Lucas) 18. Reforça: thumb com rosto de criatura ou pictograma + pergunta.
- O Vitor tirou "Conte as Batidas" da fila (removida).
- Isca nova "Câmera da Campainha 01:58" (`roteiros/iscas/isca_07_campainha.json`), no padrão da Farmácia: VHS da campainha, o Tiago 2 min parado antes de bater, sem vapor na boca a -9 °C. Pergunta: "O que tem de errado nele?". Decisão do Vitor: sai DEPOIS do Ep. 1 (que vai em 19/11 18h47) para puxar o público até ele, então mira 20/11 11h47.
- Pedido de arte: `campainha_cftv` e `esp_tiago_campainha`. Propor para aprovação quando as imagens estiverem cadastradas.

## 19/11: arte da isca "Câmera da Campainha 01:58" (Diretor de Arte)
- **O pedido:** prompts de `campainha_cftv` e `esp_tiago_campainha` para `roteiros/iscas/isca_07_campainha.json`, que vai ao ar em 20/11 como trailer do Pode Entrar? Ep. 1. Os dois estão no catálogo de cenários, na subseção da isca dentro de "Pode Entrar?", e foram entregues ao Vitor pela conversa, sem Telegram.
- **Traço:** o mesmo da série, com o `olho_tiago` anexado como referência. A imagem sai limpa: o VHS (`pixel` 6), o carimbo e o `texto_tela` entram por cima, no vídeo. O `campainha_cftv` deixa livre o quinto de cima para o `texto_tela` e põe o Tiago um pouco abaixo do centro, longe da legenda.
- **`anima` sugerida para `esp_tiago_campainha`:** `partes` com o rosto em `tremor` e o pivô no pescoço. É um tremor de frio humano, coerente com o segredo da equipe. Não usar `estalo`, para ele não parecer monstro. As regiões são medidas quando a imagem chegar.
- **Ordem de geração:** `olho_tiago` → `campainha_cftv` → `esp_tiago_campainha`. Se o `olho_tiago` não chegar antes, o `campainha_cftv` vira a referência do rosto.

## 19/11: regras do Vitor para o Pode Entrar? (Roteirista)
- Oco + você + 1 humano: o Oco espera (seria óbvio). Só mata com mais de 2 humanos hóspedes. A organização (O Censo, nome provisório) leva um hóspede aleatório para testes, para a casa não lotar. Registrado em DIRECAO §5.

## 19/11: imagens da isca "Câmera da Campainha 01:58" cadastradas (Diretor de Arte)
- **Formato:** `campainha_cftv` e `esp_tiago_campainha` chegaram em 896x1200 (3:4). O corte de cobertura para 1188x2112 tira cerca de 12% de cada lado. Nada importante se perdeu: o Tiago, a porta, o guarda-corpo e o rosto inteiro ficaram no quadro.
- **Cadastro:** as duas estão em `cenarios.json` e no guia de `src/animacao.py`. A `anima` do `esp_tiago_campainha` é `partes` com `tremor` na cabeça (região [0.18, 0.17, 0.62, 0.4], pivô no pescoço [0.48, 0.56]): um tremor de frio humano.
- **Quadro de prova** (VHS com `pixel` 6, as 4 cenas da isca):
  - o "CAM PORTA -9°C" cai no teto da varanda sem tapar nada;
  - a legenda da fita, a 70% da altura, pega só os pés e o capacete na câmera de cima, e só o cachecol no close;
  - a boca roxa fica legível logo acima da legenda, no "Repara na boca dele";
  - o REC, a data e a hora ficam livres.
  - Não precisou mexer em foco nem no texto da isca.
- **Focos de referência para usos futuros:** rosto no `campainha_cftv` = [0.5, 0.33, 2.6]; boca no `esp_tiago_campainha` = [0.5, 0.58, 2.2].
- **Continuidade das argolas:** o `olho_tiago` já mostra argolinhas nas DUAS orelhas, então o close bate com ele. O que estava errado era a ficha, que dizia só na esquerda. `docs/PERSONAGENS.md` foi corrigido.

## 19/11: Ep. 2 do Pode Entrar? em rascunho (Roteirista)
- O Vitor decidiu: a Lia é Oca (segredo em PERSONAGENS). A isca da campainha sai DEPOIS do Ep. 1 (20/11 11h47), para levar público ao episódio.
- Rascunhos: `roteiros/pode_entrar_02_sim.json` e `roteiros/pode_entrar_02_nao.json` (A Enfermeira). Só propor depois do resultado do voto.
- Arte em comum às duas versões: `caderno_lurdes2`, `olho_lia`, `esp_lia_cilios`. Só da versão SIM: `sala_lareira_tiago`. Só da NÃO: `olho_bag`, `olho_lia_cachecol`.
- Pendente com o Vitor: o que acontece num "game over" (proposta: recomeçar com outro sobrevivente numa casa nova, com o caderno).

## 19/11: prompts do Pode Entrar? Ep. 2 "A Enfermeira" (Diretor de Arte)
- **Seis prompts no catálogo** (subseção "Ep. 2, A Enfermeira (Lia)"):
  - para as duas versões: `olho_lia`, `esp_lia_cilios` e `caderno_lurdes2`;
  - só SIM: `sala_lareira_tiago`;
  - só NÃO: `olho_bag` e `olho_lia_cachecol`.
  - Entregues pela conversa, sem Telegram.
- **Visual da Lia** (marca em `docs/PERSONAGENS.md`):
  - cores próprias: gorro bordô, sobretudo cinza-chumbo e pijama hospitalar azul-claro, para não brigar com o verde-petróleo e o laranja do Tiago;
  - pinta embaixo do olho esquerdo e maleta branca com cartelas;
  - a boca sempre coberta (máscara; no NÃO, o cachecol do Tiago), assim a imagem não entrega o vapor;
  - o sinal físico: geada intacta e cristalina nos cílios.
- **`anima` sugerida para `esp_lia_cilios`:** `tremor` só na metade de baixo (máscara, queixo e ombros) e a faixa dos olhos parada: o rosto finge frio, os olhos não.
- **SIM:** no `sala_lareira_tiago`, a geada do cabelo dele começa a derreter, com uma gota caindo, que é o sinal de humano da cena 5. A composição segue os focos do roteiro: caderno em [0.5, 0.55], cabelo em [0.5, 0.35]. Confiro quando a imagem chegar.
- **Ordem de geração:** `olho_lia` → `esp_lia_cilios` → `caderno_lurdes2` e, depois do voto, `sala_lareira_tiago` (SIM) ou `olho_bag` + `olho_lia_cachecol` (NÃO).
- **Referências para anexar:** o `olho_tiago` para a moldura e o traço, o `olho_lia` para o rosto dela e o `caderno_lurdes` para o caderno.
- Correção do Vitor: Oco sozinho com você não mata. Você só morre se o Primeiro vier à porta e sentir que você está sozinho em casa (derruba a porta). Game over = requel com outro sobrevivente no mesmo universo. Em aberto: o Oco dentro de casa conta como "companhia" para o Primeiro?
- Fechado com o Vitor: Oco não conta como companhia. O Primeiro chega em noites aleatórias; se encontrar só você e um Oco, derruba a porta. Ep. 2 NÃO ganhou a fala "quem passa a noite sozinho... o Primeiro sente".

## 19/11 (00h50): agenda nova do Vitor (Roteirista)
- Rufus descansa por enquanto (já tem 2 eps e protocolo). "Seu Cachorro Abana o Rabo?" saiu da fila.
- Agenda: 19/11 11h47 Fita da Farmácia 02 (`roteiros/iscas/isca_08_farmacia2.json`, só com artes que já existem: a mãe liga pedindo para abrir a porta dos fundos, o Cliente no fim do corredor); 19/11 18h47 Pode Entrar? Ep. 1; 20/11 11h47 Câmera da Campainha.

## 19/11 (01h40): Fita da Farmácia 02 reprovada pelo Revisor (Publicador)
- Render da aprovação nº 3 (run 44456653956): voz Enceladus em 91%, sem palavras bugadas, mas o vídeo tem ~32 s (o alvo da isca é de 12 a 20 s).
- Lógica/cânone: a fala diz "a câmera não mostra ele" e a tela mostra o Cliente com o REC por cima; ele aparece DENTRO do estoque (só entra se convidado); falta telefone no balcão; hortelã e esparadrapo não aparecem.
- O Publicador já trocou o título ("A mãe dela ligou às 3h17... 📼 #shorts") e a legenda (a pergunta logo antes das hashtags).
- Para o Roteirista: cortar a narração para 25 a 30 palavras, abrir com o telefone, resolver a cena do susto (ele do lado de fora, ou a cena sem o REC). Depois disso, o render volta a pedir a aprovação do Vitor.
- Render da Câmera da Campainha (nº 2) rodando (run 44459126756).

## 19/11 (07h25): rodada da manhã da equipe
- **Analista:** pauta em `data/pauta/2026-11-19.md` (relatório run 44505343743). Canal com 3.809 views (+339) e 22 inscritos (+6). O Protocolo Stu (54 s) segura mais: 61,7% assistido. Histórias de 99 a 100 s ficam em 28 a 35%. Farmácia 01 com 1.104 views e o protocolo da campainha com 819 em menos de 12 h. Os 5 posts de 17/11 à tarde/noite ficaram entre 13 e 23 views, o que confirma o máximo de 2 por dia.
- **18h47 de hoje:** coberto pelo Ep. 1 "O Entregador" (já na fila). Nenhum principal novo escrito.
- **Iscas:** só 1 na fila ("Qual Porta", sai às 11h47). As 2 que faltam vêm da Câmera da Campainha (render pronto, espera o Revisor) e da Fita da Farmácia 02.
- **Roteirista:** Fita da Farmácia 02 refeita seguindo a reprovação do Revisor: 29 palavras (~23 s), abre com o telefone, o Cliente fica do lado de fora do vidro (`esp_cliente_porta`) e a virada é o "boa noite, mãe" (o convite, pelo cânone). Sem hortelã/esparadrapo e sem arte nova. Proposta como **nº 4**. Ressalva para o Revisor: o REC da fita aparece também na cena do Cliente (que "não aparece na câmera"); a cena não tem texto "CAM", como na Fita 01.
- **Diretor de Arte:** não precisou, nenhuma imagem nova.
- **Mesa do Gerente:** nº 4 em "Aguardando"; histórico com os nº 1, 2 e 3. A frase "Nada esperando agora" acima da tabela não foi mexida (a rodada só muda as tabelas): vale atualizar à mão ou liberar a mudança.
- **Pendências:** o protocolo de 20/11 18h47 ainda não tem roteiro (o Analista sugere "Protocolo Geada", do Pode Entrar?, 45 a 55 s). Os itens nº 1, 2 e 3 seguem com status "renderizando" em `aprovacoes.json`, embora os renders tenham terminado.
- **Ferramenta:** o gh CLI estava sem token nesta sessão; os workflows foram disparados pelo conector do GitHub.

## 19/11 (14h): Protocolo Geada para 20/11 18h47 (Roteirista)
- **Pedido do Vitor:** protocolo do universo Pode Entrar?: como saber se quem bate é humano ou Oco; se der ruim, o Primeiro te mata. `roteiros/protocolo_04_geada.json`, rótulo PROTOCOLO GEADA, `sombra: primeiro`. 116 palavras em 18 cenas (o Protocolo Stu tem 116 palavras e 54 s): mira 50 a 55 s. Revisor, confira a duração.
- **Estrutura:** gancho com ameaça ("Se baterem na sua porta durante a geada... pode não ser gente. Você está sozinho.") → 3 sinais físicos do cânone: vapor na boca, o olho mágico que embaça (contar até cinco), a geada que vira gota no humano e nunca derrete no Oco → regra estranha "não deixe ele perceber que você está olhando" → virada: "Oco não conta como companhia. Se ficarem só você e ele... o Primeiro sente." → `porta_inverno` (a porta com a cadeira escorada, vista de dentro) com tremor e corte para o preto: "Ele não bate. Ele derruba a porta." → alerta com a porta derrubada e a pergunta "Qual sinal você testa primeiro? Vapor, vidro... ou geada?". Sem gore e sem arte nova.
- **Segredo da Lia protegido:** o protocolo não usa "não sentem frio"/tremor (ela treme), não fala de cílios nem de "saber o seu nome", e não diz que comportamento se finge. Também não dá a explicação do Tiago (prender a respiração).
- **Pictogramas novos em `src/protocolo.py`** (testados com quadro de prova): `vapor`, `olho_magico`, `vidro_embacado`, `geada`, `oco` (contorno de pessoa vazio por dentro), `primeiro` e `porta_derrubada`, mais a sombra de fundo `primeiro`. Thumb: o pictograma do Primeiro, com "É gente ou é Oco?".
- **Para o Diretor de Arte:** o pictograma do Primeiro é só uma silhueta provisória (alto, curvado, cabeça tombada, um braço com cotovelo a mais). Quando o design oficial for encomendado, dá para alinhar o ícone a ele.
- Proposto para aprovação; o render só começa quando o Vitor aprovar.

## 19/11 (11h20): rodada do Revisor e do Publicador
- **Câmera da Campainha (nº 2): aprovada pelo Revisor depois de 2 refações.**
  - Render das 04h44 (run 44459126756) reprovado: 28 s (alvo da isca até 25 s) e uma só tomada com 78% (a cota do Gemini deu 429). A fala "às duas em ponto" brigava com o relógio da fita, que mostrava 01:58.
  - Refação 1 (run 44538486327): narração de 32 para 23 palavras ("Uma e cinquenta e oito. Nove graus negativos. / Dois minutos parado ali. Sem bater. / Repara na boca dele. / Então ele bateu. Você abriria?"). Saiu com 18 s e 100%, mas sem som de batida: o Freesound não acha "heavy knocking on wooden door", e o "vento" era o som de um carro passando.
  - Refação 2 (run 44539327937): buscas trocadas para "door knock", "wind howling" e "horror stinger hit". Ficou com Enceladus/Gemini, 100% na 2ª tomada, 19 s, batida na porta com som e a legenda abaixo da boca no close.
  - **Publicador:** legenda termina na pergunta, com "(história de ficção)" e #podeentrar. Mandado ao Vitor como **nº 5** (vídeo), para sair 20/11 às 11h47.
- **Fita da Farmácia 02 (nº 4):** o Vitor aprovou às 11h02, no lugar da Qual Porta, que ele tirou da fila. O render (run 44539513525) ficou **sem a voz Enceladus**: a cota diária do Gemini TTS acabou, a voz reserva entrou e também falhou ("No audio"). **Reprovado.** Renderizar de novo depois que a cota voltar (~05h). O Vitor foi avisado para não postar o vídeo que chegou no Telegram.
  - Causa provável: 3 renders entre 10h56 e 11h17 (as 2 refações da Campainha mais a Fita 02, esta começando em paralelo com a 2ª refação). Lição: com cota curta, refação de detalhe (som) espera a rodada seguinte.
- **Fila:** só "O Entregador" (hoje 18h47). **A faixa das 11h47 de hoje fica vazia.** Iscas aprovadas na fila: 0 (o mínimo é 2). A Campainha (nº 5) e a Fita 02 cobrem 20/11 e 21/11 se forem aprovadas.
- **Protocolo Geada (nº 6):** o Roteirista o propôs às 11h16 para 20/11 18h47. Se for aprovado hoje, o render cai sem voz; o aviso pediu para aprovar depois das ~05h.
- **Correções de sistema:**
  - `aprovacoes.json`: nº 1 → na_fila (run 44400389600), nº 2 com o run, nº 3 → "substituido" (status novo, some de /pendentes).
  - `refazer-video.yml`: o "renderizado" nunca gravava porque o render começa antes de a Mesa salvar o "renderizando". Agora o workflow traz só o `data/aprovacoes.json` do main antes de marcar. A 1ª versão (git pull com autostash) deixou marcas de conflito no `pendente.json` no render da Fita 02. Isso foi consertado e trocado por um checkout só desse arquivo.
- **Mesa do Gerente:** "Aguardando" com os nº 6 e 5. O histórico ganhou o nº 4 e a saída da Qual Porta.
- **Ferramenta:** o gh CLI seguiu sem token, então tudo foi feito pelo conector do GitHub. Nesta rodada não usei subagentes: segui os arquivos do Revisor, do Publicador e do Roteirista um de cada vez. Não havia nada com status "refazer".

## 19/11 (12h31): Fita da Farmácia 02 postada (Publicador)
- O Roteirista refez a Fita 02 (29 palavras, o Cliente do lado de fora do vidro, a virada "boa noite é convite"). Render 44542181080: Enceladus 93%, 19 s, revisado e aprovado pelo Revisor.
- O Vitor aprovou na conversa com o Publicador ("passe a correção e depois publique"). Aprovação nº 7 → fila → postada à mão no turno da manhã (run 44555530468, Upload-Post completed).
- Hoje: 1 post. Às 18h47 sai O Entregador (Pode Entrar? Ep. 1). Fila de iscas vazia depois disso; a Câmera da Campainha (nº 5) espera o Vitor para 20/11 11h47.

## 19/11 (15h55): rodada do Revisor e do Publicador
- **Nada novo para revisar.** Os dois itens com status "renderizado" já tinham sido tratados: a Câmera da Campainha (nº 2) foi revisada e está com o Vitor como vídeo nº 5; a Fita da Farmácia 02 (nº 4) foi aprovada (nº 7) e postada às 12h33. Nenhum render rodando nem item "renderizando" (último render: 44542181080, às 11h17).
- **Correção:** `aprovacoes.json` nº 2 → "revisado" (status novo, some de /pendentes) e nº 4 → "na_fila", para não aparecerem como "com o Revisor".
- **Roteirista:** nada com status "refazer".
- **Fila:** o principal das 18h47 de hoje está coberto ("O Entregador", Pode Entrar? Ep. 1). Iscas aprovadas na fila: 0. Esperam o Vitor: nº 5 (Campainha, 20/11 11h47) e nº 6 (roteiro do Protocolo Geada, 20/11 18h47; aprovar depois de ~05h por causa da cota do Gemini).
- **Mesa do Gerente:** "Aguardando" segue com nº 6 e nº 5; o histórico ganhou o nº 7.
- **Aviso no Telegram:** não mandado; não há decisão nova (nº 5 e nº 6 já foram avisados).

## 19/11 (19h23): O Entregador postado à mão (Publicador)
- O agendamento das 18h47 falhou de novo (3ª vez em 2 dias). Rodei `fila.yml` turno=tarde (run 44626363969): Upload-Post completed, vídeo lAaMldaxFs4. A thumb entrou logo depois do post (marcada em `thumbs_feitas.json`).
- Lembrete: no feed de Shorts o YouTube mostra o próprio vídeo, não a thumb; ela aparece na página do canal, na busca e nas inscrições.
- Fila vazia. Para 20/11: a Câmera da Campainha (nº 5) e o Protocolo Geada (nº 6) esperam o Vitor.

## 20/11 (07h25): rodada da manhã da equipe
- **Analista:** pauta em `data/pauta/2026-11-20.md` (relatório run 44719126452). Canal com 6.374 views (+2.565) e 24 inscritos (+2). Protocolo Stu segue no topo da retenção (60,9% assistido, 43% no fim); histórias de 100 s ficam em 31 a 36%. Views públicas: Farmácia 01 1.254, protocolo da campainha 1.042 (o que mais cresceu), Fita 02 654 em ~16 h, **Pode Entrar? Ep. 1 só 117 em ~9 h** (87 s, estático: confirma a lição do "vídeo com vida"). Pesquisa web: CFTV/VHS/found footage seguem fortes; "personagem famoso macabro" sem sinal de alta.
- **18h47 de hoje (protocolo):** coberto pelo nº 6 Protocolo Geada, ainda pendente com o Vitor. Só sai hoje se for aprovado até ~14h (render + Revisor + aprovação do vídeo). Não há protocolo reserva; não escrevi outro para não duplicar.
- **Iscas:** fila com 0 aprovadas. O nº 5 (Câmera da Campainha) cobre só hoje 11h47, se aprovado. Roteirista escreveu 2 novas no padrão novo (só artes que já existem, sem pedido ao Diretor de Arte):
  - **nº 8 "Dashcam 04:02"** (`roteiros/iscas/isca_10_dashcam.json`, estreia da Corrida Noturna): 32 palavras, ~20 s, susto `esp_passageiro`, virada: o cinto de trás continua afivelado no portão do cemitério. Pergunta: "Você olharia no retrovisor?".
  - **nº 9 "CAM 04 | 03:13"** (`roteiros/iscas/isca_09_camera4.json`, estreia da Câmera 4): 33 palavras, ~21 s, susto `esp_moradora`, virada: o elevador para no 13º num prédio de 12 andares e ela passa para a câmera da portaria.
  - Sugestão: postar a Dashcam antes da CAM 04, porque o piloto "Grupo do Prédio" (formato voce, renderizado às 04h25, em `pendente.json`) também é de prédio.
- **Ressalvas para o Revisor/Vitor:**
  - CAM 04: o 1º quadro (`elevador_porta`) saiu escuro na prova; e a fala "Apareceu na câmera um" fecha num plano da portaria sem ela visível. Conferir se o susto final lê bem ou se precisa de um sinal dela no monitor.
  - Dashcam: a ficha diz que o Passageiro "não aparece no retrovisor", mas a única arte (`esp_passageiro`) é ele pelo retrovisor. O roteiro trata como Rafa quebrando a regra ("Ele olhou."). Se o Vitor quiser o cânone estrito, falta uma `esp_` dele direto no banco de trás.
  - `planta_andar` é a planta da casa do Guizo; não serve para prédio.
- **Refazer:** nada com status "refazer" em `aprovacoes.json`.
- **Mesa do Gerente:** "Aguardando" com nº 9, 8, 6 e 5 (o texto do nº 6 agora diz que a cota já voltou). Histórico sem decisões novas desde o nº 7 (19/11).
- **Ferramenta:** gh CLI segue sem token; workflows pelo conector do GitHub. Analista e Roteirista rodaram como subagentes.

## 20/11 (10h55): rodada do Revisor e do Publicador
- **Revisor:** nada para revisar. Nenhum item com status "renderizado" ou "renderizando" em `aprovacoes.json`, e nenhum render de `refazer-video.yml` rodando (os últimos foram os pilotos do formato voce, às 04h08–04h25, que estão em `pendente.json` e não passam pela Mesa).
- **Publicador:** nenhum vídeo novo para mandar. Continua com o Vitor o nº 5 (Câmera da Campainha, vídeo final): se não for aprovado até ~11h40, a faixa das 11h47 de hoje fica vazia e ela passa para a próxima faixa de isca.
- **Fila:** 0 itens. O principal das 18h47 de hoje é o nº 6 (roteiro do Protocolo Geada), ainda esperando o Vitor (aprovar até ~14h). Como há item esperando aprovação, não mandei aviso novo. Iscas aprovadas na fila: 0 (o mínimo é 2); os nº 8 (Dashcam) e nº 9 (CAM 04) esperam o Vitor.
- **Roteirista:** nada com status "refazer".
- **Mesa do Gerente:** sem mudança. "Aguardando" já tem só os nº 9, 8, 6 e 5; nenhuma decisão nova do Vitor para o histórico.
- **Aviso no Telegram:** não mandado (nada novo desde a rodada da manhã).
- **Ferramenta:** gh CLI segue com token inválido; consultas pelo conector do GitHub. Sem subagentes nesta rodada (não havia trabalho para eles).

## 20/11 (15h55): rodada do Revisor e do Publicador
- **Revisor:** nada para revisar. Nenhum item "renderizado" ou "renderizando" em `aprovacoes.json`. O único render de `refazer-video.yml` rodando agora (44796429840) é do E Se Fosse Real? (`esfr_02`), que não é da equipe do terror.
- **Publicador:** nenhum vídeo novo para mandar. Desde a rodada das 10h55 o Vitor aprovou (11h17) a CAM 04 (nº 9, fila 21/11 11h47), a Dashcam (nº 8, fila 22/11 11h47) e os pilotos do formato Você ("Pode Entrar? versão Você" postado às 14h38; "Grupo do Prédio (Parte 1)" na fila).
- **Fila:** o principal das 18h47 de hoje está coberto pelo Grupo do Prédio (história). Iscas na fila: 2 (mínimo atendido). Hoje: 2 posts no máximo (Pode Entrar? Você + Grupo do Prédio).
- **Esperam o Vitor:** nº 5 (vídeo final da Câmera da Campainha; a faixa de 20/11 11h47 passou, próxima livre 23/11 11h47) e nº 6 (roteiro do Protocolo Geada; o 18h47 de hoje ficou com o Grupo do Prédio, então vai para o próximo dia de protocolo).
- **Roteirista:** nada com status "refazer".
- **Mesa do Gerente:** "Aguardando" ficou só com nº 6 e nº 5 (textos de data atualizados); o histórico ganhou nº 8, nº 9 e os pilotos do formato Você.
- **Aviso no Telegram:** não mandado (nada novo para decidir; nº 5 e nº 6 já foram avisados).
- **Ferramenta:** gh CLI segue com token inválido; consultas pelo conector do GitHub. Sem subagentes (não havia trabalho para eles).

## 21/11 (07h25): rodada da manhã da equipe
- **Analista:** pauta em `data/pauta/2026-11-21.md` (relatório run 44894280257). Canal com 7.475 views (+1.101) e 29 inscritos (+5). A Fita da Farmácia 01 virou a melhor retenção do canal (68,8% assistido, 38% no fim); a Fita 02 foi de 654 para 1.117 views. Os 3 vídeos de bicho somam 3.324 views e 17 dos 29 inscritos. Pode Entrar? (versão Você): 368 views em ~20 h, 3x o ritmo do Ep. 1.
- **Furo de 20/11 18h47:** o Grupo do Prédio Pt 1 não saiu. O agendamento (run 44824933560) pulou porque `_ja_postou` viu o "Pode Entrar? (versão Você)" (tipo historia, postado à mão às 14h38 UTC) e considerou a faixa do principal já usada. Ele é o único principal na fila e sai hoje 18h47 sozinho; com isso são duas histórias seguidas. Fila não mexida. A testar: a trava podia olhar a faixa pelo horário do post, não pelo tipo.
- **Mapa:** 21/11 CAM 04 + Grupo Pt 1 (fila); 22/11 Dashcam (fila) + Geada nº 10 (espera); 23/11 Campainha nº 5 + Grupo Pt 2 nº 11 (esperam); 24/11 vazio.
- **Roteirista** (pauta pediu 24/11; skills protocolo-analog-horror e video-making carregadas; só arte que já existe):
  - **nº 12 "Fita do Terreiro 02:51"** (`roteiros/iscas/isca_11_terreiro.json`): isca VHS da Férias na Roça, 7 cenas, 37 palavras, ~23 s, susto `esp_pisadeira` (estreia), o cachorro Tição foge para dentro e fica bem. Faixa 24/11 11h47.
  - **nº 13 "Protocolo Pisadeira"** (`roteiros/protocolo_05_pisadeira.json`): "Se o Seu Gato Encarar o Teto", 15 cenas, 94 palavras, ~43 s, 4 regras + "a parte mais importante", corte seco em `esp_pisadeira`. Faixa 24/11 18h47.
- **Ressalvas para o Revisor/Vitor:** o cachorro usa o desenho do Rufus (`de_pe` vira o falso Rufus, então usei `levantando_cabeca`/`correndo`); sem `sombra`, o motor desenha o Abismo apagado no fundo do protocolo (pode confundir a criatura); `gato:olhos_escuro` sai como gato em pé; tesoura vai como `destaque`. Diretor de Arte não acionado (o roteiro roda com o banco atual); se o Vitor quiser, uma silhueta da Pisadeira resolveria o fundo.
- **Refazer:** nada com status "refazer".
- **Mesa do Gerente:** "Aguardando" com nº 13, 12, 11, 10 e 5 (o nº 6 saiu, substituído pelo nº 10); histórico ganhou o nº 6.
- **Aprendizado (Analista):** protocolo de 40 a 45 s, no máximo 5 regras, corte seco depois da última; isca até 25 s para caber no TikTok.
- **Ferramenta:** gh CLI segue com token inválido; workflows pelo conector do GitHub. Analista e Roteirista rodaram como subagentes.

## 21/11 (10h55): rodada do Revisor e do Publicador
- **Revisor:** nada para revisar. Nenhum item "renderizado" ou "renderizando" em `aprovacoes.json`. Os renders de `refazer-video.yml` de hoje (44905839296 a 44907278914) são todos do E Se Fosse Real? e já terminaram; nenhum do terror rodando.
- **Publicador:** nenhum vídeo novo para mandar. Fila: CAM 04 (isca, hoje 11h47), Grupo do Prédio Pt 1 (principal, hoje 18h47) e Dashcam (isca, 22/11 11h47). O principal das 18h47 de hoje está coberto.
- **Esperam o Vitor:** nº 13 e 12 (roteiros Pisadeira, 24/11), nº 11 (Grupo Pt 2), nº 10 (Protocolo Geada, 22/11 18h47) e nº 5 (Campainha, 23/11 11h47). Sem decisão nova desde a rodada das 07h25.
- **Roteirista:** nada com status "refazer".
- **Mesa do Gerente:** sem mudança (o "Aguardando" já tem só nº 13, 12, 11, 10 e 5; histórico sem decisão nova).
- **Aviso no Telegram:** não mandado (nada novo para decidir).
- **Ferramenta:** gh CLI funcionou nesta rodada para leitura (`gh run list`). Sem subagentes (não havia trabalho para eles).

## 21/11 (12h10): reserva da fila (Publicador)
- **Furo de 21/11 11h47:** o agendamento do fila.yml não disparou. Postagem à mão da CAM 04 (run 44917640341) **falhou**: Upload-Post recusou (429, `monthly_limit_reached`, 10 de 10 usados; o ciclo começou em 17/11 e reinicia por volta de 17/12). A conta é a mesma dos dois canais.
- Fila intacta (CAM 04 segue em primeiro). Não tentei de novo. Nada sai no 18h47 de hoje (Grupo do Prédio Pt 1) até o Vitor decidir: plano pago do Upload-Post ou conta separada para o E Se Fosse Real?.

## 21/11 (13h40): post manual do Vitor
- Com o Upload-Post no limite, o Vitor postou à mão no YouTube o **Protocolo Geada** (run 44816462692, aprovações nº 10), por volta das 13h35. Às 13h39 já tinha 178 visualizações. Registrado em `postados` em `data/fila.json`. Os itens da fila não mudaram: CAM 04, Grupo do Prédio Pt 1 e Dashcam continuam esperando.

## 21/11 (15h55): rodada do Revisor e do Publicador
- **Revisor:** nada para revisar. Nenhum item "renderizado", "renderizando" ou "refazer" em `aprovacoes.json`. Os últimos renders de `refazer-video.yml` (44905839296 a 44907278914) são do E Se Fosse Real? e já terminaram.
- **Publicador:** nenhum vídeo novo para mandar. O principal de hoje já saiu: o Vitor postou o Protocolo Geada à mão (~13h35). Marquei o nº 10 como `na_fila` em `aprovacoes.json` (com o motivo), para ele sair do /pendentes.
- **Fila:** CAM 04, Grupo do Prédio Pt 1 e Dashcam seguem parados porque o Upload-Post está no limite do mês (10/10, volta ~17/12). Hoje: 1 post (Geada); a isca das 11h47 não saiu. Esse problema já está com o Vitor (registro das 12h10), então não mandei aviso novo.
- **Esperam o Vitor:** nº 13 e 12 (roteiros Pisadeira, 24/11), nº 11 (Grupo Pt 2) e nº 5 (Campainha).
- **Mesa do Gerente:** saiu o nº 10 do "Aguardando"; o histórico ganhou "21/11 #10 Protocolo Geada, postado à mão pelo Vitor".
- **Aviso no Telegram:** não mandado (nada novo para decidir).
- **Ferramenta:** gh CLI funcionou para leitura (`gh run list`), apesar de `gh auth status` dizer token inválido. Sem subagentes (não havia trabalho).

## 22/11 (07h25): rodada da manhã da equipe
- **Analista:** pauta em `data/pauta/2026-11-22.md`. Números iguais aos de ontem (o `ultima.json` ainda é o relatório de 21/11: 7.475 views, 29 inscritos); o commit 693be22 de hoje foi só a rodada de thumbs. Próximo relatório automático: 23/11.
- **Grupo do Prédio Pt 1 parece postado:** a rodada de thumbs de hoje achou um Short novo (`_9eTAbgUSrs`) e pôs nele a thumb do "Grupo do Prédio". Provavelmente o Vitor postou à mão na noite de 21/11. `data/fila.json` ainda tem o Pt 1 em `itens`; não mexi (falta o Vitor confirmar que está público, aí o Publicador passa para `postados`).
- **Hoje (22/11) vira dia de protocolo** (último principal: Pt 1, história). Não há protocolo aprovado na fila; o candidato é o nº 13 (Pisadeira, roteiro). Se não ficar pronto até ~17h, a reserva é o Pt 2 (nº 11, vídeo pronto, continuação direta).
- **Mapa:** 22/11 CAM 04 + Pisadeira nº 13 (espera); 23/11 Dashcam + Pt 2 nº 11 (espera); 24/11 Campainha nº 5 (espera) + protocolo novo nº 14; 25/11 Terreiro nº 12 + vazio (história).
- **Roteirista** (skills protocolo-analog-horror e video-making carregadas; só arte que já existe): **nº 14 "Protocolo Assobiador"** (`roteiros/protocolo_06_assobiador.json`), "Se o Seu Gato Eriçar Pra Janela e Alguém Assobiar", 15 cenas, 93 palavras, ~43 s, 4 regras, gato eriçado na cena 1, corte seco em `esp_assobiador` (estreia), fecho "quantos assobios você ouviu?". O gato termina calmo. Iscas novas: 0 (fila com 2).
- **Ressalvas para o Revisor/Vitor (nº 14):** sem `sombra` própria o motor desenha o Abismo apagado no fundo (mesma ressalva da Pisadeira; uma silhueta `assobiador` em `src/protocolo.py` resolveria); `pessoa:encolhida` não existe, usei `pessoa:silencio`; conferir se os 3 assobios dos sons se ouvem e não parecem apito, e a duração (40 a 45 s).
- **Diretor de Arte:** não acionado (nenhuma imagem faltando).
- **Refazer:** nada com status "refazer". Nenhuma decisão nova do Vitor em `aprovacoes.json` desde 21/11 13h35, então o histórico da Mesa não mudou; o "Aguardando" ganhou o nº 14.
- **Ferramenta:** gh CLI com token inválido; workflows pelo conector do GitHub. Analista e Roteirista rodaram como subagentes.

## 22/11 (10h55): rodada do Revisor e do Publicador
- **Revisor:** nada para revisar. Nenhum item "renderizado" ou "renderizando" em `aprovacoes.json`. Os renders de `refazer-video.yml` de hoje (45024118569 a 45025849302) são todos do E Se Fosse Real? e já terminaram; nenhum do terror rodando.
- **Publicador:** nenhum vídeo novo para mandar. Fila sem mudança: Grupo do Prédio Pt 1 (provavelmente já postado à mão, falta o Vitor confirmar), CAM 04 e Dashcam, todos parados pelo limite do Upload-Post (10/10, volta ~17/12; já com o Vitor desde 21/11 12h10).
- **Principal de hoje (22/11 18h47, dia de protocolo):** não há vídeo aprovado na fila, mas há coisa esperando o Vitor (nº 11 Grupo Pt 2, vídeo pronto, reserva; nº 13 Pisadeira, roteiro), então não mandei aviso.
- **Esperam o Vitor:** nº 14, 13 e 12 (roteiros), nº 11 (Grupo Pt 2) e nº 5 (Campainha). Nenhuma decisão nova desde 21/11 13h35.
- **Roteirista:** nada com status "refazer".
- **Mesa do Gerente:** sem mudança (o "Aguardando" já tem só nº 14, 13, 12, 11 e 5; histórico sem decisão nova).
- **Aviso no Telegram:** não mandado (nada novo para decidir).
- **Ferramenta:** gh CLI funcionou para leitura (`gh run list`, `gh run view`) apesar de `gh auth status` dizer token inválido. Sem subagentes (não havia trabalho).

## 22/11 (15h55): rodada do Revisor e do Publicador
- **Revisor:** nada para revisar. Nenhum item "renderizado" ou "renderizando" em `aprovacoes.json`. Nenhum render novo de `refazer-video.yml` desde 13h07 UTC (os de hoje são todos do E Se Fosse Real? e terminaram).
- **Publicador:** nenhum vídeo novo para mandar. Às 14h41 UTC rodou um `fila.yml` manual em modo Telegram (run 45034176843) com a CAM 04 (próxima da fila) para post à mão; a fila não mudou. Grupo do Prédio Pt 1, CAM 04 e Dashcam seguem parados pelo limite do Upload-Post (já com o Vitor desde 21/11 12h10).
- **Principal de hoje (22/11 18h47):** sem vídeo aprovado na fila, mas há coisa esperando o Vitor (nº 11 Grupo Pt 2, vídeo pronto; nº 13 e 14, roteiros de protocolo), então não mandei aviso.
- **Esperam o Vitor:** nº 14, 13 e 12 (roteiros), nº 11 (Grupo Pt 2) e nº 5 (Campainha). Nenhuma decisão nova desde 21/11 13h35.
- **Roteirista:** nada com status "refazer".
- **Mesa do Gerente:** sem mudança.
- **Aviso no Telegram:** não mandado (nada novo para decidir).
- **Ferramenta:** gh CLI funcionou para leitura apesar de `gh auth status` dizer token inválido. Sem subagentes (não havia trabalho).

## 22/11 (19h08): reserva da fila, turno tarde
- **Agendado das 18h47:** `fila.yml` (run 45068642443, 20:49 UTC) falhou no upload do Grupo do Prédio Pt 1: Upload-Post 429 `monthly_limit_reached` (10/10, período começou em 17/11).
- **Reserva:** não postei à mão. O mesmo limite bloquearia o upload; não insisti. Fila intacta (Grupo Pt 1, CAM 04, Dashcam). Nenhum post hoje.
- **Aviso:** Vitor avisado por notificação.

## 22/11 (noite): requel em bunker (Roteirista, conversa com o Vitor)
- Referência do Vitor: "Sobrevivendo 1 Ano Trancado num Bunker | FILME COMPLETO" (@leonofimdomundo, 66 mil em 3 dias): boneco fixo + fundos ilustrados, sobrevivência dia a dia, Shorts que viram um filme longo. Nada do personagem, nome ou história deles.
- O Vitor escolheu: requel do Pode Entrar? com o protagonista trancado num bunker.
- Rascunho (não proposto): série "O Bunker do Vô", `roteiros/bunker_01.json` (Dia 1: A Escotilha, 18 cenas, 112 palavras). Nando se tranca no bunker que o avô fez para o bug do milênio no Dia 1 da geada; o vizinho Seu Jair bate às 3h, descalço e sem tremer. Segue a regra do vídeo com vida (até 8 palavras por cena, cenário no máximo 3 vezes).
- Depende do OK do Vitor e de arte nova (boneco do Nando, 8 cenários e 1 cena especial, contador de dias/latas na tela).

## 23/11 (07h25): rodada da manhã da equipe
- **Analista** (subagente): pauta em `data/pauta/2026-11-23.md`, com relatório novo (run 45155830250). Canal com 8.220 views (+745 desde 21/11) e 35 inscritos (+6). % assistido cai com a duração: fitas de 20 a 27 s ficam em 69 a 76%, protocolos de 54 s em 50 a 61%, histórias de 73 a 100 s em 31 a 36%. Feed de Shorts = 92 a 96% do tráfego.
- **Descobertas no relatório:**
  - **CAM 04 já foi postada** (`atlITzZFEtU`, 22/11): 1.131 views em ~1 dia, a largada mais rápida do canal.
  - **Grupo do Prédio Pt 1** (`_9eTAbgUSrs`, 21/11, 73 s) tem só 4 views; o Geada, no mesmo período, fez 1.386. Precisa o Vitor conferir se está público.
  - `data/fila.json` ainda tem CAM 04 e Pt 1 em `itens` (não mexi; é do Publicador, com confirmação do Vitor). Com isso só a Dashcam é isca aprovada de verdade.
- **Hoje 23/11 = protocolo** (último principal postado: Pt 1, história). Sem protocolo aprovado; candidatos nº 14 Assobiador (preferido, tem gato) e nº 13 Pisadeira, com o Vitor.
- **Mapa:** 23/11 Dashcam + nº 14/13; 24/11 nº 5 Campainha + nº 11 Pt 2 (só se o Pt 1 estiver público); 25/11 nº 12 Terreiro + o protocolo que sobrar; 26/11 vazio → coberto pelos roteiros de hoje.
- **Roteirista** (subagente; skills video-making e protocolo-analog-horror carregadas; só arte que já existe):
  - **nº 15 "Câmera 4, Ep. 1: O 13º Andar"** (`roteiros/camera4_01.json`), história para 26/11 18h47: 16 cenas, 89 palavras, ~50 s, VHS/CFTV em 12 cenas, susto `esp_moradora`, voto A escada / B elevador. Começa onde a CAM 04 parou.
  - **nº 16 "Fita da Farmácia 03"** (`roteiros/iscas/isca_12_farmacia3.json`), isca para 26/11 11h47: 6 cenas, 32 palavras, ~22 s, susto `esp_cliente_estoque` (estreia), virada: a câmera mostra o corredor vazio.
- **Ressalvas para o Revisor/Vitor:** o boneco `adulto` tem cara de criança, então o Seu Joaquim só aparece de costas e pequeno (cena 15); não há arte de interfone (close no painel de latão da portaria); `elevador_porta` e `farmacia_corredor2` saem escuros na prova; o 8º andar reaproveita o desenho do `corredor_camera4`. Se a história passar de 55 s: `"ritmo": 1.05` ou cortar a cena 4.
- **Diretor de Arte:** não acionado (os roteiros rodam com o banco atual). Para o futuro: boneco próprio do Seu Joaquim (idoso, cabelo branco, uniforme) e arte do interfone.
- **Refazer:** nada com status "refazer". Nenhuma decisão nova do Vitor em `aprovacoes.json` desde 21/11.
- **Mesa do Gerente:** "Aguardando" ganhou nº 16 e 15, e as faixas dos nº 5, 11, 12, 13 e 14 foram atualizadas pelo mapa novo; histórico ganhou "22/11 #9 CAM 04 postada à mão".
- **Aprendizado (Analista):** cada meio minuto a mais custa ~15 pontos de % assistido. História até 50 s, isca até 25 s; se não couber, vira 2 episódios.
- **Ferramenta:** gh CLI funcionou para disparar workflows nesta rodada (apesar de `gh auth status` dizer token inválido).

## 23/11 (13h55 UTC): rodada do Revisor e do Publicador
- **Revisor:** nada para revisar. Nenhum item "renderizado" ou "renderizando" em `aprovacoes.json`. Os renders de hoje em `refazer-video.yml` são todos do E Se Fosse Real? (último 13:08 UTC, terminado).
- **Publicador:** nenhum vídeo novo para mandar. Fila sem mudança (Grupo Pt 1, CAM 04, Dashcam; CAM 04 e Pt 1 já postados segundo o Analista, aguardando o Vitor confirmar a limpeza).
- **Principal de hoje (23/11 18h47, protocolo):** sem protocolo aprovado na fila, mas nº 13 Pisadeira e nº 14 Assobiador esperam o Vitor, então não mandei aviso.
- **Esperam o Vitor:** nº 16, 15, 14, 13, 12 (roteiros), nº 11 (Grupo Pt 2) e nº 5 (Campainha). Nenhuma decisão nova desde 21/11 13h35.
- **Roteirista:** nada com status "refazer".
- **Mesa do Gerente:** sem mudança (já estava em dia desde a rodada das 07h25).
- **Aviso no Telegram:** não mandado (nada novo para decidir).
- **Ferramenta:** gh CLI funcionou para leitura apesar de `gh auth status` dizer token inválido. Sem subagentes (não havia trabalho).

## 23/11 (15h10 UTC): reserva da fila, turno manhã
- **Agendamento das 11h47 não disparou** (nenhuma execução `schedule` do fila.yml hoje de manhã; as duas últimas agendadas, 22/11 20h49 e 23/11 01h58 UTC, falharam).
- **Não postei à mão:** a primeira isca em `itens` é a CAM 04, que já saiu em 22/11 (`atlITzZFEtU`). Disparar o fila.yml postaria a CAM 04 de novo. A Dashcam só sai depois que a CAM 04 e o Pt 1 forem tirados de `itens` (limpeza que espera o Vitor).
- Aviso mandado ao Vitor por notificação.

## 23/11 (18h55 UTC): rodada do Revisor e do Publicador
- **Revisor:** nada para revisar. Nenhum item "renderizado" ou "renderizando" em `aprovacoes.json`. Nenhum render do terror em `refazer-video.yml` hoje (os de hoje são do E Se Fosse Real?, todos terminados).
- **Publicador:** nenhum vídeo novo para mandar. Fila já limpa (commit 6f8a0a9): só a Dashcam em `itens`. Às 15h47 UTC rodou um `fila.yml` manual (run 45209246875); a fila não mudou.
- **Principal de hoje (23/11 18h47, protocolo):** sem protocolo aprovado na fila, mas nº 14 Assobiador e nº 13 Pisadeira esperam o Vitor, então não mandei aviso.
- **Esperam o Vitor:** nº 16, 15, 14, 13, 12 (roteiros), nº 11 (Grupo Pt 2) e nº 5 (Campainha). Nenhuma decisão nova desde 21/11 13h35.
- **Roteirista:** nada com status "refazer".
- **Mesa do Gerente:** sem mudança (nada novo pendente nem decidido desde a rodada das 07h25).
- **Aviso no Telegram:** não mandado (nada novo para decidir).
- **Ferramenta:** gh CLI funcionou para leitura apesar de `gh auth status` dizer token inválido. Sem subagentes (não havia trabalho).

## 23/11 (22h10 UTC): reserva da fila, turno tarde
- **Agendamento das 18h47 não disparou** (nenhuma execução `schedule` do fila.yml hoje).
- **Não postei à mão:** o Grupo do Prédio (Parte 2) já está no YouTube (`iseuGKOPE5M`, thumb às 21h38 UTC), postado pelo Vitor depois do envio pelo Telegram (run 45261575576).
- **Atenção:** o Pt 2 continua em `itens` do `data/fila.json`. O próximo fila.yml da tarde postaria de novo. A limpeza espera o Vitor. A Dashcam 04:02 (isca) também segue em `itens` e não aparece no YouTube.

## 24/11 (07h25): rodada da manhã da equipe
- **Analista** (subagente): pauta em `data/pauta/2026-11-24.md`, com o relatório de hoje (já gravado pela rodada automática; não rodei o youtube.yml de novo). Canal com 9.619 views (+1.399 desde 23/11) e 36 inscritos (+1). Retenção nova só do Protocolo Geada (58 s): 48,9% assistido, 100% / 44% / 23%, 8 inscritos (2º do canal, atrás do Guizo). CAM 04 em 1.114 views, ainda sem retenção.
- **Fila desatualizada de novo:** os dois itens em `itens` de `data/fila.json` já estão no YouTube: **Dashcam 04:02** (`vp0on5WliLU`, 23/11, 188 views no 1º dia; o render saiu com 35 s) e **Grupo do Prédio Pt 2** (`iseuGKOPE5M`, 23/11, 28 views). A fila aprovada de verdade está vazia. Risco de o `fila.yml` repostar. Não mexi (é do Publicador, com o Vitor). O Pt 1 segue com 5 views (conferir se está público); a pauta não pede Pt 3.
- **Hoje 24/11 = protocolo** (último principal: Pt 2, história). Sem protocolo aprovado; candidatos nº 14 Assobiador (preferido, tem gato) e nº 13 Pisadeira, com o Vitor. Aprovar até ~15h.
- **Mapa:** 24/11 Campainha nº 5 + nº 14/13; 25/11 Terreiro nº 12 + Câmera 4 Ep. 1 nº 15 (adiantado de 26/11); 26/11 Farmácia 03 nº 16 + o protocolo que sobrar; 27/11 vazio → coberto pelos roteiros de hoje.
- **Roteirista** (subagente; skill video-making carregada; só arte que já existe):
  - **nº 17 "Turno da Madrugada, Ep. 1: Duas Vezes"** (`roteiros/turno_01.json`), história para 27/11 18h47: 15 cenas, 71 palavras, ~45 a 49 s (`ritmo` 1.08), VHS com 5 cenas de CFTV, susto `esp_cliente_balcao2`. Continua da Fita 03 e honra as duas escolhas (tranca os fundos e depois foge pela frente). Voto A voltar pela irmã / B ligar para casa.
  - **nº 18 "CAM 02 | GARAGEM | 03:13"** (`roteiros/iscas/isca_13_garagem.json`), isca para 27/11 11h47: 6 cenas, 27 palavras, ~20 a 23 s, susto `esp_moradora`, 19/11/1998, noite anterior ao Ep. 1 (não toca no voto). Virada: planta antiga com 13 andares. Pergunta "Quem morava no treze?".
- **Ressalvas para o Revisor/Vitor:** a Bia não aparece (o boneco "mulher" destoa), como nas Fitas; `telefone_casa` é uma cozinha, close no telefone para esconder o fogão; a planta de 1979 com 13 andares é cânone novo (precisa do OK do Vitor); CAM 09 criada para o subsolo; se a isca passar de 25 s, cortar a cena 2; se a história passar de 50 s, ritmo 1.1 ou cortar a cena 3.
- **Diretor de Arte:** não acionado (nenhuma imagem faltando).
- **Refazer:** nada com status "refazer".
- **Mesa do Gerente:** "Aguardando" ganhou nº 18 e 17, saiu o nº 11 (decidido) e as faixas dos nº 13, 14 e 15 foram atualizadas pelo mapa novo; histórico ganhou "23/11 #11 Grupo Pt 2 aprovado e postado à mão" e "23/11 #8 Dashcam postada à mão".
- **Aprendizado (Analista):** o que conta é a duração do render, não a do roteiro. A Dashcam (32 palavras) deu 35 s e largou 6 vezes pior que a CAM 04 (33 palavras, 26 s). Conte pausas e sons; isca acima de 25 s no render é cortada antes de ir ao Vitor.
- **Ferramenta:** gh CLI funcionou para disparar workflows apesar de `gh auth status` dizer token inválido. Repo usado em /home/claude/terror-bot (clone já existente). Analista e Roteirista rodaram como subagentes.

## 24/11 (13h55 UTC): rodada do Revisor e do Publicador
- **Revisor:** nada para revisar. Nenhum item "renderizado" ou "renderizando" em `aprovacoes.json`. Os renders de hoje em `refazer-video.yml` são todos do E Se Fosse Real? (último 13:13 UTC, terminado).
- **Publicador:** nenhum vídeo novo para mandar.
- **Principal de hoje (24/11 18h47, protocolo):** sem protocolo aprovado, mas nº 14 Assobiador e nº 13 Pisadeira esperam o Vitor. A isca das 11h47 (nº 5 Campainha) também espera.
- **Fila com risco de repost:** Dashcam 04:02 e Grupo do Prédio Pt 2 já estão no YouTube, mas seguem em `itens` de `data/fila.json`. A trava do `fila.py` só conta posts do dia, não confere o YouTube, então o agendamento das 11h47/18h47 pode repostar. Não mexi na fila (espera o OK do Vitor).
- **Esperam o Vitor:** nº 18, 17, 16, 15, 14, 13, 12 (roteiros) e nº 5 (Campainha). Nenhuma decisão nova desde 23/11 20h38 (nº 11).
- **Roteirista:** nada com status "refazer".
- **Mesa do Gerente:** sem mudança (já em dia desde a rodada das 07h25).
- **Aviso no Telegram:** mandado (run 45408419989), pedindo o OK para mover Dashcam e Pt 2 para `postados`.
- **Ferramenta:** clone novo em /home/claude/terror-bot-git. gh CLI funcionou apesar de `gh auth status` dizer token inválido. Sem subagentes (não havia trabalho).

## 24/11 manhã (reserva da fila, 12h09)
- O agendado das 11h47 não disparou. Rodei fila.yml à mão (turno manha, run 45422379091) para a isca "Dashcam 04:02": falhou. Upload-Post recusou (429, monthly_limit_reached): 10 de 10 envios do plano grátis usados, contagem desde 17/11. Nada saiu e o item continua na fila. Não tentei de novo. **Erro meu:** não li o diário antes; a Dashcam já está no YouTube (vp0on5WliLU, 23/11), então eu teria repostado. A falha do Upload-Post evitou o repost. Os dois itens em `itens` (Dashcam e Pt 2) já saíram: a fila aprovada real está vazia e o próximo fila.yml tentaria repostar. Precisa do Vitor: limpar a fila (mover os dois para `postados`) e decidir o Upload-Post (plano pago ou postar direto pela API do YouTube).

## 24/11 (13h, conversa com o Vitor)
- **nº 5 Câmera da Campainha 01:58** aprovada e postada à mão pelo Vitor. Registrada em `aprovacoes.json` e em `postados` de `data/fila.json`.
- Dashcam e Grupo Pt 2 seguem em `itens` (já no ar); a limpeza ainda espera o OK do Vitor.
- Com o OK do Vitor, Dashcam 04:02 (`vp0on5WliLU`) e Grupo do Prédio Pt 2 (`iseuGKOPE5M`) saíram de `itens` e foram para `postados`. A fila aprovada ficou vazia; não há mais risco de repost.

## 24/11 (19h00 UTC): rodada do Revisor e do Publicador
- **Revisor:** nada para revisar. Nenhum item "renderizado" ou "renderizando" em `aprovacoes.json`. Os renders de hoje em `refazer-video.yml` são todos do E Se Fosse Real? (último 15:46 UTC, terminado).
- **Publicador:** nenhum vídeo novo para mandar. Fila aprovada (`itens`) vazia; Campainha, Dashcam e Grupo Pt 2 já em `postados`.
- **Principal de hoje (24/11 18h47, protocolo):** sem protocolo aprovado, mas nº 14 Assobiador e nº 13 Pisadeira esperam o Vitor, então não mandei aviso. Lembrete: o Upload-Post segue no limite do mês, então mesmo aprovado o vídeo sai à mão.
- **Esperam o Vitor:** nº 18, 17, 16, 15, 14, 13, 12 (roteiros). Decisões novas desde a última rodada: nº 5 Campainha aprovada e postada à mão (~13h) e a limpeza da fila (Dashcam e Pt 2 para `postados`).
- **Roteirista:** nada com status "refazer".
- **Mesa do Gerente:** saiu o nº 5 de "Aguardando"; o Histórico ganhou "24/11 #5 Campainha aprovada e postada à mão" e "24/11 Fila: Dashcam e Pt 2 para postados".
- **Aviso no Telegram:** não mandado (nada novo para decidir).
- **Ferramenta:** clone novo em /home/claude/terror-bot-git. gh CLI funcionou apesar de `gh auth status` dizer token inválido. Sem subagentes (não havia trabalho).

## 25/11 (07h25): rodada da manhã da equipe
- **Regra nova do Vitor (25/11):** 2 posts todo dia (11h47 e 18h47). Em 24/11 só saiu 1 (sem principal), porque os roteiros esperavam aprovação e ninguém cobrou.
- **Decisões do Vitor desde a última rodada:** aprovou os roteiros nº 12 Terreiro (07h02), nº 13 Pisadeira (07h08), nº 16 Farmácia 03 (07h12) e nº 15 Câmera 4 Ep. 1 (07h19). Renders: 12 e 13 prontos e já mandados como vídeos nº 19 e nº 20; 16 renderizado (falta o Revisor); 15 renderizando (run 45593828707).
- **Analista** (subagente): pauta em `data/pauta/2026-11-25.md`, relatório novo (run 45594935642). Canal com 11.905 views (+2.286) e 39 inscritos (+3). CAM 04 com retenção: 68,0% assistido, 125% / 62% / 39%, mas só 1 inscrito (isca puxa view, protocolo traz inscrito: Geada 8). Campainha 01:58 (20 s) fez 1.194 views em menos de 1 dia, o melhor 1º dia do canal. Dashcam (35 s) em 522. Geada virou o vídeo com mais views (1.392). Grupo Pt 1 está público (4 views no Analytics), só não teve distribuição.
- **Alternância:** último principal postado foi história (Grupo Pt 2, 23/11) → hoje protocolo, 26 história, 27 protocolo, 28 história. Por isso o nº 17 Turno Ep. 1 (história) passou de 27/11 para 28/11 e o nº 14 Assobiador ocupa 27/11 18h47.
- **Mapa:** 25/11 nº 19 Terreiro + nº 20 Pisadeira (vídeos, esperam o Vitor) | 26/11 nº 16 Farmácia 03 (renderizada) + nº 15 Câmera 4 Ep. 1 (renderizando) | 27/11 nº 18 Garagem + nº 14 Assobiador (roteiros) | 28/11 11h47 **vazia**, 18h47 nº 17 Turno Ep. 1. Fila aprovada: 0 de 6 faixas.
- **Roteirista:** 0 roteiros hoje. As 6 faixas de 25 a 27/11 têm candidato e a regra é não acumular o que o Vitor não viu. Nada com status "refazer". Amanhã: isca de 28/11 11h47 (sugestão do Analista: nova noite da Câmera da Campainha, 20 s no render).
- **Riscos para o Vitor/Revisor:** Terreiro com 27 s (teto 25) e voz 89% (seção 3 pede 90%); Pisadeira com 59 s (teto 55).
- **Diretor de Arte:** não acionado (nenhuma imagem faltando).
- **Mesa do Gerente:** "Aguardando" agora tem nº 20, 19, 18, 17 e 14 com as faixas novas (saíram 12, 13, 15 e 16, já aprovados); o Histórico ganhou as 4 aprovações de hoje.
- **Aviso no Telegram:** mandado (run 45595485206) com /aprovar 19 e 20 para hoje e 18, 14 e 17 para 27 e 28/11.
- **Aprendizado (Analista):** escrever a isca para 18 s, porque o render soma 5 a 15 s (20 s → 1.194 views; 26 s → 1.114; 35 s → 522).
- **Ferramenta:** clone novo em /home/claude/terror-bot-git. gh CLI funcionou apesar de `gh auth status` dizer token inválido.

## 25/11 (10h55): rodada do Revisor e do Publicador
- **Revisor:** conferiu os 5 renders novos (nº 14, 15, 16, 17 e 18), com a folha de quadros e o log de cada um. Os nº 12 e 13 já estavam com o Vitor como vídeos nº 19 e 20 (as ressalvas de duração e voz seguem no resumo deles).
  - **nº 15 Câmera 4 Ep. 1:** passou. 55 s, Gemini 88% (a nota baixa vem de 1301, "treze zero" e Seu Joaquim; as legendas estão certas). Cenário no máximo 3x, susto esp_moradora. Ressalva: o close de costas do Seu Joaquim na escada é grande.
  - **nº 17 Turno Ep. 1:** passou. 44 s, Gemini 96%. Ressalva: abaixo do alvo de 50 s de história.
  - **nº 16 Farmácia 03:** reprovada por 26 s (teto da isca 25 s). Refeita com `ritmo` 1.1 e `pausa_extra` 0.5 no susto (run 45628901016): **23 s, Gemini 91%**, aprovada.
  - **nº 18 Garagem:** reprovada. O render saiu sem a Enceladus (429 no Gemini; a reserva Edge também falhou). A busca "slow footsteps concrete" virou "slow footsteps". O 2º render (run 45630752976) também falhou: a **cota diária do Gemini TTS acabou** ("You exceeded your current quota", flash e pro). Não mandei ao Vitor.
  - **nº 14 Assobiador:** reprovado. 51 s, Gemini 92%, mas o Freesound não achou os assobios das cenas 2 e 13, e o da cena 6 virou "Whistle and Explosion Single_Firework" (som de fogos). O final "Você contou quantos assobios ouviu?" ficaria sem sentido. As buscas viraram "human whistling" (as 3), "footsteps leaves" e "window close". **Não renderizei de novo** porque a cota do Gemini acabou. Falta 1 refação para cada um.
- **Publicador:** títulos e legendas afinados: Câmera 4 com "Ela aparece mais perto a cada câmera... escada ou elevador?" e Turno mais curto; as duas legendas agora dizem qual é o A e qual é o B. Propostos ao Vitor: **nº 21 Câmera 4 Ep. 1 (Qui 26/11 18h47)**, **nº 22 Farmácia 03 (Qui 26/11 11h47)** e **nº 23 Turno Ep. 1 (Sáb 28/11 18h47)**.
- **Erro meu (corrigido):** mandei as propostas da Câmera 4 e do Turno com 20 s de intervalo. As duas pegaram o nº 21; a do Turno não gravou (conflito no push), mas a mensagem com botões "/aprovar 21" chegou ao Vitor. Reenviei o Turno como nº 23 e avisei. **Regra:** mandar uma proposta por vez e esperar o aprovacao.yml terminar antes da próxima.
- **Fila:** `itens` vazia. Hoje 11h47 (nº 19) e 18h47 (nº 20) esperam o Vitor, então não mandei aviso de faixa vazia. Mapa: 26/11 nº 22 + nº 21; 27/11 Garagem + Assobiador (re-render pendente); 28/11 11h47 **vazia**, 18h47 nº 23.
- **Próximo passo:** a cota do Gemini volta por volta das 05h (meia-noite do Pacífico). A rodada das 07h23 de 26/11 deve renderizar **primeiro a Garagem (nº 18) e depois o Assobiador (nº 14)**, um por vez, conferir a voz no log e se os sons dos assobios são de assobio humano. Na rodada das 15h23 de hoje, a cota provavelmente ainda não voltou: não renderizar.
- **Roteirista:** nada com status "refazer".
- **Mesa do Gerente:** "Aguardando" tem agora os nº 23, 22, 21, 20 e 19 (saíram os roteiros 18, 17 e 14, já aprovados). O Histórico ganhou as aprovações dos nº 18 (07h30), 17 (07h40) e 14 (07h49).
- **Ferramenta:** clone novo em /home/claude/terror-bot-git. gh CLI funcionou apesar de `gh auth status` dizer token inválido. Sem subagentes; os papéis foram feitos em sequência.
- 25/11 13h26: **o Vitor postou o Protocolo Assobiador (nº 14) à mão**, na faixa das 11h47. NÃO re-renderizar: o nº 14 está como "postado". Mapa novo: hoje 18h47 Pisadeira (nº 20); 26/11 Farmácia 03 (nº 22) e Câmera 4 (nº 21); 27/11 Garagem (nº 18) e Turno (nº 23); 28/11 11h47 Fita do Terreiro (nº 19, que fecha o buraco).

## 25/11 (15h55): rodada do Revisor e do Publicador
- **Revisor:** o único item "renderizado" sem vídeo proposto é o nº 18 Garagem (run 45630752976). O log confirma: 429 "You exceeded your current quota" no flash e no pro, então saiu sem a Enceladus. Não renderizei de novo: a cota ainda está esgotada (o render do canal 2 às 18h28 UTC bateu no mesmo limite). Falta 1 refação; fazer na rodada das 07h23 de 26/11. Os outros "renderizado" (12, 13, 15, 16, 17) já estão com o Vitor como vídeos 19 a 23. Nada "renderizando".
- **Publicador:** nenhum vídeo novo para mandar. `itens` da fila vazia.
- **Principal de hoje (25/11 18h47):** a Pisadeira (nº 20) espera o /aprovar, então não é faixa sem candidato.
- **Faixa vazia nova:** Sex 27/11 18h47 (protocolo). O Assobiador, que ocupava a faixa, saiu hoje à mão às 11h47. Mapa: 26/11 nº 22 + nº 21 | 27/11 nº 18 Garagem (re-render) + **vazia** | 28/11 nº 19 Terreiro + nº 23 Turno. Fila aprovada: 0 de 6.
- **Roteirista:** nada com status "refazer". Pauta de 26/11: um protocolo para 27/11 18h47 (ou o Vitor põe o Turno nela e a vaga vira 28/11).
- **Mesa do Gerente:** no "Aguardando", o nº 19 passou para a faixa Sáb 28/11 11h47. O Histórico ganhou "25/11 #14 Assobiador postado à mão às 13h26".
- **Aviso no Telegram:** mandado (run 45680224105): faixa de 27/11 18h47 vazia + lembrete do /aprovar 20.
- **Ferramenta:** clone novo em /home/claude/terror-bot-git. gh CLI funcionou apesar de `gh auth status` dizer token inválido. Sem subagentes; os papéis foram feitos em sequência.

## 25/11 (18h35): reserva da fila (Publicador, turno tarde)
- Hoje saiu 1 post (Assobiador, à mão às 13h26). `itens` da fila vazia: sem principal para 18h47. Não mandei outro tipo no lugar.
- Aviso mandado (run 45705540453 + push) com /aprovar 20 (Pisadeira), 21 (Câmera 4 Ep. 1) ou 23 (Turno Ep. 1). Upload-Post segue no limite: aprovado, vai pelo Telegram.

## 26/11 (07h25): rodada da manhã da equipe
- **Analista** (subagente): pauta em `data/pauta/2026-11-26.md`, relatório novo (run 45801155470, ~13 min por causa da instalação do FFmpeg). Canal com 13.702 views (+1.797) e 45 inscritos (+6), 21 vídeos. Assobiador com 938 views em menos de 1 dia (provável fonte dos +6). Retenção nova: Dashcam (35 s) 43,0% assistido e 39% no início (CFTV fixa: 59 a 61%), 0 inscrito; Grupo Pt 2 (64 s) 30,5%. Pisadeira e Terreiro **não** estão no ar (o canal bate com `aprovacoes.json`).
- **Em 25/11 saiu só 1 post** (Assobiador, à mão, faixa 11h47); 18h47 ficou vazia (Pisadeira nº 20 sem /aprovar).
- **Alternância:** último principal = Assobiador (protocolo) → Qui 26 história, Sex 27 protocolo, Sáb 28 história.
- **Mapa:** Qui 26/11 nº 22 Farmácia 03 + nº 21 Câmera 4 Ep. 1 | Sex 27/11 nº 18 Garagem (roteiro aprovado, falta render válido) + nº 20 Pisadeira (passou de 25/11) | Sáb 28/11 nº 19 Terreiro + nº 23 Turno Ep. 1. Fila aprovada: 0 de 6. Próximas faixas vazias: Dom 29/11 (isca e protocolo), prioridade da rodada de amanhã.
- **Roteirista:** 0 roteiros hoje (as 6 faixas têm candidato; regra de não acumular o que o Vitor não viu). Nada com status "refazer". Reserva para Dom 29/11 11h47: nova noite da Câmera da Campainha (18 s no roteiro), confirmar com a retenção da 01:58.
- **Render:** não renderizei (a rodada da manhã não renderiza). **A Garagem (nº 18) precisa ser refeita pelo Revisor na rodada das 10h53**, com a cota do Gemini já renovada, conferindo a Enceladus no log.
- **Diretor de Arte:** não acionado (nenhuma imagem faltando).
- **Mesa do Gerente:** "Aguardando" com as faixas novas (nº 22 e 21 HOJE com prazo, nº 20 para Sex 27/11 18h47, nº 19 Sáb 28/11 11h47). Histórico sem linha nova: nenhuma decisão do Vitor desde o Assobiador (25/11 13h26, já registrado).
- **Aviso no Telegram:** mandado (run 45803727688) com /aprovar 22 e 21 para hoje, 20 para amanhã 18h47, 19 e 23 para sábado.
- **Aprendizado (Analista):** o primeiro segundo decide e câmera fixa ganha: o 1º quadro precisa do carimbo de lugar e horário e de algo errado à vista antes da primeira fala.
- **Ferramenta:** clone novo em /home/claude/terror-bot-git. gh CLI funcionou apesar de `gh auth status` dizer token inválido. Analista como subagente; os outros papéis feitos em sequência.

## 26/11 (10h55): rodada do Revisor e do Publicador
- **Decisões do Vitor desde a manhã:** nenhuma. Os vídeos nº 19 a 23 continuam pendentes.
- **Revisor:** o único "renderizado" sem vídeo proposto era o nº 18 Garagem. Com a cota do Gemini renovada, fiz a 2ª e última refação (run 45833867073): **voz Enceladus (gemini-2.5-flash-preview-tts), tomada 2 com 100%** (a tomada 1 tinha 52% e foi descartada), **24 s**, 6 cenas. Checklist: garagem e elevador 2x cada; susto esp_moradora no 13º; legenda sem tapar o rosto; sem personagem, então nada flutuando; sem gore. **Passou**, com ressalvas: o "elevator ding" virou "snd_elevator_power_down" (som de elevador desligando, não um ding); a planta_andar escurece no último segundo; 24 s fica perto do teto de 25 s; o 1º quadro não mostra nada errado antes da fala (aprendizado de hoje do Analista). Nada "renderizando" e nenhum render de mais de 40 min.
- **Publicador:** título trocado para "3h13: o elevador subiu sozinho até o 13º... o prédio só tem 12 📼 #shorts", que repete o gancho da CAM 04 (1.131 views); legenda mantida. Proposto como **vídeo nº 24** (run 45834926885), faixa **Sex 27/11 11h47**.
- **Fila:** `itens` vazia. As duas faixas de hoje têm candidato esperando o Vitor (nº 22 às 11h47 e nº 21 às 18h47), então o principal de hoje não está "sem nada". Mapa: Qui 26/11 nº 22 + nº 21 | Sex 27/11 nº 24 Garagem + nº 20 Pisadeira | Sáb 28/11 nº 19 Terreiro + nº 23 Turno. Faltam Dom 29/11 (isca e protocolo), para a rodada de amanhã às 07h23.
- **Roteirista:** nada com status "refazer".
- **Mesa do Gerente:** "Aguardando" ganhou o nº 24 em cima, e o prazo do nº 22 passou para ~11h30. Histórico sem linha nova (nenhuma decisão do Vitor).
- **Aviso no Telegram:** mandado, com o nº 24 novo e a lembrança do nº 22, que sai às 11h47.
- **Ferramenta:** clone novo em /home/claude/terror-bot-git. gh CLI funcionou apesar de `gh auth status` dizer que o token é inválido. Sem subagentes; os papéis foram feitos em sequência.

## 26/11 (11h35): reserva da fila (Publicador, turno manhã)
- Nenhum post hoje ainda. `itens` da fila vazia: sem isca para 11h47. Não mandei outro tipo no lugar.
- Aviso mandado (run 45840318065 + push) com /aprovar 22 (Farmácia 03, faixa de hoje), 24 (Garagem, Sex 27/11) e 19 (Terreiro, Sáb 28/11). Upload-Post segue no limite: aprovado, vai pelo Telegram.

## 26/11 (15h58): rodada do Revisor e do Publicador (tarde)
- **Decisões do Vitor desde as 10h55:** nenhuma. Os vídeos nº 19 a 24 continuam pendentes; nada com status "refazer".
- **Revisor:** todos os "renderizado" (12, 13, 15, 16, 17, 18) já têm vídeo proposto (19 a 24). Nada "renderizando" e nenhum render de mais de 40 min (último refazer-video: 45833867073, ok). Nada a refazer.
- **Publicador:** nenhum vídeo novo. `itens` da fila vazia. A faixa de hoje 11h47 passou sem isca (nº 22 sem /aprovar). O principal de hoje 18h47 tem candidato esperando (nº 21), então não é "faltando sem nada pendente". Mapa: Sex 27/11 nº 24 + nº 20 | Sáb 28/11 nº 19 + nº 23 | Dom 29/11 o nº 22 pode cobrir a isca; falta o protocolo de Dom 29/11 (rodada de amanhã 07h23).
- **Mesa do Gerente:** no "Aguardando", o nº 22 passou para "próxima isca livre: Dom 29/11 11h47". Histórico sem linha nova.
- **Aviso no Telegram:** não mandado (nada novo; os lembretes do nº 21 e do nº 22 já foram às 10h55 e 11h35).
- **Ferramenta:** clone novo em /home/claude/terror-bot-git; gh CLI funcionou. Sem subagentes; papéis em sequência.

## 26/11 (18h34): reserva da fila (Publicador, turno tarde)
- Nenhum post hoje (11h47 passou sem isca). `itens` da fila vazia: sem principal para 18h47. Não mandei outro tipo no lugar.
- Aviso mandado (run 45899024960 + push) com /aprovar 21 (Câmera 4 Ep. 1, faixa de hoje), 23 (Turno Ep. 1) ou 20 (Pisadeira). Upload-Post segue no limite: aprovado, vai pelo Telegram.
- 26/11 19h: **o Vitor aprovou o agendamento direto no YouTube para o terror.** O fila.yml roda às 11h31 e 18h31 (cron) com `agendar`: o vídeo sobe privado e sai sozinho às 11h47 e 18h47. O Publicador confere às 11h40 e 18h40. O Telegram fica só como plano B (cota da API). A aprovação do Vitor continua obrigatória para entrar na fila.

## 27/11 (07h25): rodada da manhã da equipe
- **Decisões do Vitor desde a última rodada:** em 26/11 às 19h00 aprovou o nº 20 Pisadeira, que saiu às 19h01. Também postou à mão a **Garagem (nº 24)** em 26/11, com 1.159 views em menos de 1 dia. Marquei o nº 24 como "postado" em `aprovacoes.json` para não sair duplicado. Nada com status "refazer".
- **Analista** (papel feito por mim, sem subagente): pauta em `data/pauta/2026-11-27.md`, com relatório novo. Canal com 15.014 views (+1.312), 52 inscritos (+7) e 23 vídeos. A Campainha 01:58 teve 68,7% assistido e 4 inscritos. Assobiador com 1.084 views; Pisadeira com 577 em ~12 h.
- **Alternância:** o último principal foi a Pisadeira (protocolo) → Sex 27 história, Sáb 28 protocolo, Dom 29 história.
- **Mapa:** Sex 27/11 nº 22 Fita 03 + nº 21 Câmera 4 Ep. 1 | Sáb 28/11 nº 19 Terreiro + **nº 25 Protocolo 13º Andar** | Dom 29/11 **nº 26 Fita 00** + nº 23 Turno Ep. 1. Fila aprovada: 0 de 6, mas todas as faixas têm candidato.
- **Roteirista:** 2 roteiros, para as 2 faixas sem candidato.
  - **nº 25 Protocolo 13º Andar** (`roteiros/protocolo_07_13andar.json`): 14 cenas e 92 palavras, sombra "moradora". Criei os ícones novos `elevador`, `interfone` e `moradora` em `src/protocolo.py`, testados num quadro de prova.
  - **nº 26 Fita 00** (`roteiros/iscas/isca_14_farmacia0.json`): prequel com 30 palavras e só arte que já existe.
  - Não acumulei além das 6 faixas.
- **Render:** não renderizei. Os nº 25 e 26 renderizam sozinhos quando o Vitor aprovar, um por vez. O nº 25 precisa de aprovação até Sáb ~15h.
- **Diretor de Arte:** não acionado (nenhuma imagem faltando).
- **Mesa do Gerente:** "Aguardando" refeita com a coluna "Faixa" (22, 21, 19, 25, 26, 23); a Garagem saiu. O Histórico ganhou o nº 20 (aprovado e postado) e o nº 24 (postado à mão).
- **Lembrete:** o roteiro do vídeo longo "As Fitas da Madrugada" é escrito amanhã, Sáb 28/11 (`docs/LONGO_TERROR.md`).
- **Ferramenta:** clone em /home/claude/terror-bot-git. Workflows disparados pelo GitHub MCP (actions_run_trigger), em vez do gh CLI.

## 27/11 (10h55): rodada do Revisor e do Publicador
- **Decisões do Vitor desde as 07h25:** nenhuma. Os vídeos nº 19, 21, 22 e 23 e os roteiros nº 25 e 26 continuam pendentes; nada com status "refazer".
- **Revisor:** todos os "renderizado" (12, 13, 15, 16, 17, 18) já têm vídeo proposto ou postado (19 a 24). Nada "renderizando". Último refazer-video do terror: 45833867073 (26/11, ok); nenhum render em andamento. Nada a revisar nem refazer.
- **Publicador:** nenhum vídeo novo para mandar. `itens` da fila vazia. As duas faixas de hoje têm candidato esperando o Vitor (nº 22 às 11h47, nº 21 às 18h47), então o principal de hoje não está "faltando sem nada pendente". O agendamento das 11h31 só sobe a isca se o nº 22 for aprovado antes. Mapa sem mudança: Sex 27/11 nº 22 + nº 21 | Sáb 28/11 nº 19 + nº 25 (roteiro) | Dom 29/11 nº 26 (roteiro) + nº 23.
- **Roteirista:** nada com status "refazer".
- **Mesa do Gerente:** no "Aguardando", o prazo do nº 22 passou de ~10h30 para ~11h30 (quando o agendamento roda). Histórico sem linha nova.
- **Aviso no Telegram:** não mandado (nada novo; a reserva das 11h35 lembra o nº 22 se ainda faltar).
- **Ferramenta:** clone novo em /home/claude/terror-bot-git. `gh` com token inválido; leitura das runs pelo GitHub MCP. Sem subagentes; papéis em sequência.

## 27/11 (11h45): conferência do agendamento da manhã (Publicador)
- O cron das 11h31 do fila.yml ainda não tinha rodado às 11h41 (atraso do GitHub). `itens` da fila vazia: nenhuma isca aprovada.
- Faixa das 11h47 vazia. Não mandei outro tipo. Avisei o Vitor (push + Telegram via `acao=aviso`): `/aprovar 22` (Fita 03) ou `/aprovar 19` (Terreiro).

## 27/11 (15h55): rodada do Revisor e do Publicador (tarde)
- **Decisões do Vitor desde as 10h55** (horários de Brasília; o bot grava em UTC): aprovou o nº 22 Fita 03 (12h25), o nº 21 Câmera 4 Ep. 1 (12h25), o nº 23 Turno Ep. 1 (12h27) e o nº 19 Terreiro (12h28). O /aprovar 24 (12h26) foi ignorado pela Mesa porque a Garagem já estava postada: sem duplicado. A Fita 03 foi agendada às 12h29 e saiu no YouTube às 12h39 (WI8oUod9U4E). Nada com status "refazer".
- **Revisor:** todos os "renderizado" (12, 13, 15, 16, 17, 18) já têm vídeo aprovado, na fila ou postado. Nenhum render novo desde 45833867073 (26/11) e nada "renderizando". Nada a revisar.
- **Publicador:** nenhum vídeo novo para mandar. Fila `itens`: Câmera 4 Ep. 1 (história), Turno Ep. 1 (história) e Terreiro (isca). O principal de hoje 18h47 está garantido (Câmera 4, agendamento das 18h31).
- **Atenção à ordem:** o `fila.py` pega o primeiro principal da lista. Sem mexer, o Turno sai Sáb 28/11 18h47 (2 histórias seguidas, quebrando a alternância), e o nº 25 Protocolo 13º Andar, se aprovado, entra depois e vai para Dom 29/11. Não reordenei: o Vitor decide. Mapa: Sex 27 Fita 03 (postada) + Câmera 4 | Sáb 28 Terreiro + Turno (ou nº 25) | Dom 29 nº 26 (roteiro) + nº 25 ou Turno. Seg 30/11 sem candidato (rodada de amanhã 07h23).
- **Roteirista:** nada com status "refazer".
- **Mesa do Gerente:** "Aguardando" ficou só com os roteiros nº 25 e 26 (a faixa do nº 25 explica a ordem). Histórico ganhou 5 linhas de 27/11 (19, 23, 24, 21, 22).
- **Aviso no Telegram:** mandado, com a questão da ordem e os nº 25 e 26 pendentes.
- **Ferramenta:** clone novo em /home/claude/terror-bot-git; gh CLI funcionou. Sem subagentes; papéis em sequência.

## 27/11 (18h55): conferência do agendamento da tarde (Publicador)
- O cron das 18h31 do fila.yml não tinha rodado às 18h41 (atraso do GitHub). Disparei `acao=agendar turno=tarde` (run 46071943734): a Câmera 4 Ep. 1 (nº 21) subiu como xo2vmMFveMg, agendada para 18h52 (faixa já perto, +10 min), saiu pública e a thumb foi reaplicada. Se o cron atrasado rodar depois, a trava do `fila.py` barra o 2º principal do dia.

## 28/11 (07h25): rodada da manhã da equipe
- **Decisões do Vitor desde a última rodada (27/11 18h55):** nenhuma. Os roteiros nº 25 e 26 seguem pendentes; nada com status "refazer". A Câmera 4 Ep. 1 (nº 21) saiu em 27/11 às 18h52 (xo2vmMFveMg). Histórico da Mesa sem linha nova.
- **Analista** (papel feito por mim; relatório novo, run 46135071248): pauta em `data/pauta/2026-11-28.md`. Canal com 16.978 views (+1.964), 56 inscritos (+4) e 25 vídeos. Iscas VHS/CFTV e protocolos passam de mil: Fita 03 com 1.103 em ~1 dia, Pisadeira com 1.096, Assobiador com 1.184 (49,4% assistido, 8 inscritos), Geada com 1.407 (8 inscritos). **As histórias ficam para trás:** Câmera 4 Ep. 1 com 210 em ~15 h e Grupo pt. 2 com 101. A Dashcam é a isca mais fraca (580 views, 0 inscrito), então a Corrida Noturna descansa.
- **Mapa:** Sáb 28 nº 19 Terreiro + nº 23 Turno (os dois **aprovados na fila**) | Dom 29 nº 26 Fita 00 + nº 25 Protocolo 13º (roteiros, esperam o Vitor) | Seg 30 nº 27 + nº 28 (roteiros novos). Fila aprovada: 2 de 6.
- **Alternância:** hoje saem 2 histórias seguidas (Câmera 4 → Turno), porque o Turno é o único principal aprovado. Não mexi na fila. O protocolo nº 25 fica para domingo.
- **Roteirista:** 2 roteiros, só para as faixas de segunda, que estavam sem candidato. Antes, carreguei a skill video-making e fiz quadros de prova.
  - **nº 27 Fita do Canil 01:40** (`roteiros/iscas/isca_15_canil.json`): prequel do Rufus, 33 palavras e 6 cenas, com o falso Rufus no 1º quadro. O Rufus de verdade ficou cortado no "perto", então troquei para "medio" no pé da cama.
  - **nº 28 Férias na Roça Ep. 1: A Tesoura Aberta** (`roteiros/roca_01.json`): VHS, 17 cenas e 95 palavras (~58 s). Continua do Terreiro. A narração da tesoura foi ajustada para "No travesseiro", porque a arte mostra a tesoura em cima do travesseiro.
  - Os dois usam só arte que já existe.
- **Vídeo longo:** o Roteirista (subagente) escreveu "As Fitas da Madrugada" (`roteiros/longo_terror_01_fitas.json`): 1.301 palavras, ~9:50, 7 capítulos, 214 cenas. Proposto como **nº 29**. Tem campos novos para o motor de segunda (`notas_motor`).
  - O `tv_estatica`/`tv_estatica2` se repetem de propósito: é a pista da sala.
- **Diretor de Arte:** os Shorts não precisam de imagem nova. O longo pede 3: `caixa_fitas`, `esp_gravador` e `esp_gravador_lente`. Conferi que nenhuma está no catálogo e mandei os prompts ao Vitor (run 46136627995), cada uma com cenário reserva.
- **Render:** não renderizei.
- **Mesa do Gerente:** no "Aguardando", o nº 25 passou para Dom 29/11 18h47 e o nº 26 ganhou prazo (hoje). Entraram o nº 27 (Seg 11h47), o nº 28 (Seg 18h47) e o nº 29 (longo, sex 4/12 20h).
- **Aviso no Telegram:** mandado (run 46136618354). Domingo está sem vídeo aprovado, com /aprovar 26 e 25 hoje, depois 27, 28 e 29.
- **Aprendizado (Analista):** a história precisa abrir como isca (carimbo, algo errado à vista, frase de 5 a 6 palavras) e ficar perto de 50 s.
- **Ferramenta:** clone novo em /home/claude/terror-bot-git. O gh CLI funcionou apesar de `gh auth status` dizer token inválido. O longo foi feito pelo subagente roteirista; os outros papéis, em sequência.

## 28/11 (10h55): rodada do Revisor e do Publicador
- **Decisões do Vitor desde as 07h25:** nenhuma. Os roteiros nº 25, 26, 27, 28 e 29 seguem pendentes; nada com status "refazer".
- **Revisor:** os "renderizado" (12, 13, 15, 16, 17, 18) já têm vídeo na fila ou postado (19 a 24). Nenhum refazer-video do terror desde 45833867073 (26/11) e nada "renderizando". Nada a revisar.
- **Publicador:** nenhum vídeo novo para mandar. Fila `itens`: nº 23 Turno Ep. 1 (história) e nº 19 Terreiro (isca). As duas faixas de hoje estão cobertas (Terreiro 11h47, Turno 18h47), então o principal de hoje não está faltando. Domingo 29/11 continua sem vídeo aprovado (nº 26 e nº 25 esperam o Vitor; o nº 25 precisa de OK até ~15h).
- **Roteirista:** nada com status "refazer".
- **Mesa do Gerente:** sem mudança. O "Aguardando" já tinha só os nº 25 a 29, e o Histórico não ganhou linha nova.
- **Aviso no Telegram:** não mandado (nada novo; o aviso das 07h25 já pediu /aprovar 26 e 25).
- **Ferramenta:** clone novo em /home/claude/terror-bot-git; gh CLI funcionou. Sem subagentes; papéis em sequência.
