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
