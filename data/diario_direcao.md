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
