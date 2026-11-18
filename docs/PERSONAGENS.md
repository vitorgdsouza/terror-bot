# Elenco do canal

Todo protagonista precisa de três coisas para o público se importar: **uma rotina que a pessoa reconhece**, **um afeto concreto** (alguém ou algum bicho que ele quer proteger) e **uma falha pequena** que o põe em perigo.

Todo antagonista precisa de:
- uma **assinatura**: um som ou um visual que o público aprende a temer;
- **regras**: o que ele quer, o que ele não pode fazer e o que o afasta por alguns segundos;
- um **segredo**, revelado aos poucos.

As regras viram protocolos. Os segredos viram continuação.

Visuais disponíveis no boneco (`src/boneco.py`): `homem` (o Lucas, menino de moletom verde), `adulto`, `idosa`, `garota`, `policial`, `mulher`. Personagem novo pode ganhar um visual novo no `VISUAIS`: cor de cabelo, roupa ou acessório. Mantenha o traço.

---

## Séries que já existem

### Lucas Duarte e o Stu: "O Guizo na Escada" (carro-chefe)
- **Quem é:** um menino de uns 10 anos, sozinho no fim de semana na casa que era dos bisavós, porque os pais viajaram. Curioso, teimoso e corajoso por amor ao gato.
- **Afeto:** o Stu, gato laranja de peito branco, com a coleira de guizo.
- **Falha:** não pede ajuda. Acha que dá conta sozinho.
- **Antagonista: O Abismo.** Silhueta preta comprida, rosto pálido, olhos arregalados e um sorriso grande demais.
  - Assinatura: o sorriso que se abre devagar, e a imitação de vozes e miados.
  - Regras: só existe na casa, no poço e nos túneis; a luz direta o faz recuar por segundos; leva os bichos primeiro, para os donos irem atrás.
  - Segredo: nasceu dos desenhos da bisavó do Lucas e esperou um Duarte voltar.
- Cânone completo em `config/serie.json`.

### Sargento Lena Moraes e o Rufus: "As Fitas do Rufus" (VHS)
- **Quem é:** policial do canil, 34 anos. Gravava os treinos do Rufus numa filmadora velha do pai, que também era do canil. Mora sozinha numa casa com quintal na beira da mata.
- **Afeto:** o Rufus, pastor-alemão farejador, parceiro desde a academia.
- **Falha:** confia mais no faro do cão do que nos próprios olhos.
- **Antagonista: O Pele.** O homem que veste a pele do cachorro.
  - Assinatura: unhas no corredor num ritmo errado (duas pernas, não quatro), a coleira lavada, um rabo que não abana.
  - Regras: imita o bicho que você ama e depois a sua voz; não suporta o faro do cão de verdade, porque o Rufus o rastreia.
  - Segredo: ele não é um só. É o que sobra de quem um dia foi "farejado" na mata.

---

## Elenco novo (para estrear quando a direção achar o momento)

### Bia Santos: "Turno da Madrugada"
- **Quem é:** 19 anos, trabalha sozinha no caixa de uma farmácia 24h de beira de estrada para pagar a faculdade. Fone num ouvido só, caderno de anatomia no balcão.
- **Identificação:** o primeiro emprego, a madrugada sozinha, o cliente estranho que todo mundo já atendeu.
- **Afeto:** a irmã mais nova, que liga toda noite às 2h para dar boa-noite.
- **Falha:** é educada demais e não sabe dizer "não" a cliente.
- **Antagonista: O Cliente das 3h17.**
  - Todo dia, às 3h17, entra um homem e compra a mesma coisa: um pacote de balas de hortelã e um rolo de esparadrapo.
  - Assinatura: a campainha da porta tocando duas vezes, embora só uma pessoa entre, e o rosto um pouco diferente a cada noite.
  - Regras: só entra se alguém disser "pode entrar" ou "boa noite"; não aparece na câmera de segurança; tenta copiar quem a Bia ama.
  - Segredo: a ligação das 2h da irmã, numa das noites, não é a irmã.
- **Formato:** animação, com a câmera de segurança em VHS nos momentos de susto (dá para misturar com `estilo: vhs`).
- **Cenários a encomendar:** balcão da farmácia à noite; corredor de prateleiras; a câmera de segurança vista de cima; o estacionamento vazio com o letreiro piscando.

### Seu Joaquim: "Câmera 4"
- **Quem é:** 71 anos, porteiro noturno há 30 anos de um prédio antigo no centro. Viúvo, faz palavras-cruzadas, conhece cada morador pelo passo.
- **Identificação:** o avô de todo mundo, o porteiro que sabe tudo. E a solidão.
- **Afeto:** a dona Zélia, do 8º andar, que desce todo dia com um café. E a memória da esposa.
- **Falha:** a vista já não é boa, e ele duvida de si mesmo.
- **Antagonista: A Moradora do 13º.**
  - O prédio tem 12 andares.
  - Assinatura: o elevador parando no "13", o interfone tocando de um apartamento que não existe e uma mulher de camisola parada no fim do corredor da câmera 4, cada noite um pouco mais perto.
  - Regras: só aparece em tela (câmera ou interfone com vídeo); se ele a encarar por muito tempo, ela aparece numa câmera mais perto da portaria; não atravessa uma porta aberta pelo próprio morador.
  - Segredo: ela pede para ser lembrada. O nome dela foi apagado da lista de moradores de 1979.
- **Formato:** o mosaico das câmeras de segurança é perfeito para analog horror. Rende também um protocolo: "Se você for porteiro da noite...".
- **Cenários a encomendar:** a portaria com o monitor de câmeras; o corredor da câmera 4; o painel do elevador; a garagem.

### Davi e a avó, Dona Cida: "Férias na Roça"
- **Quem é:** Davi, 11 anos, vai passar as férias no sítio da avó no interior de Minas. É da cidade e não acredita em nada. A Dona Cida é benzedeira e conhece cada história do mato.
- **Identificação:** as férias na casa da avó, o fogão a lenha, o "isso é coisa de antigamente".
- **Afeto:** a avó, que está mais esquecida a cada dia. E o cachorro do sítio, o Tição.
- **Falha:** desdenha das regras da avó.
- **Antagonistas, do folclore e de domínio público, numa versão nossa:**
  - **A Pisadeira:** mulher magra de unhas compridas que anda pelos telhados e sobe no peito de quem dormiu de barriga cheia. Assinatura: telhas estalando em cima do quarto e uma risada fina. Regra da avó: nunca deitar de barriga cheia; tesoura aberta debaixo do travesseiro.
  - **O Assobiador do mato:** assobia de noite. Se você responder, ele vem. Ele assobia mais perto quanto mais longe parece.
- **Segredo:** a avó não está esquecida. Está fazendo um trato para proteger o neto.
- **Formato:** animação e protocolos de folclore, que trazem identificação forte em português.
- **Cenários a encomendar:** a cozinha com fogão a lenha; o quarto de madeira com telhado aparente; o terreiro à noite com o mato ao fundo; a porteira; o curral.

### Rafa: "Corrida Noturna"
- **Quem é:** 27 anos, motorista de aplicativo de madrugada, juntando dinheiro para abrir uma barbearia. Fala com todo passageiro e tem um terço pendurado no retrovisor.
- **Identificação:** o app, a nota do passageiro, o endereço estranho às 4h.
- **Afeto:** a filha pequena, a Luiza, cuja foto fica colada no painel.
- **Falha:** aceita qualquer corrida pela tarifa.
- **Antagonista: O Passageiro do Banco de Trás.**
  - Pede corridas para endereços que não existem mais.
  - Assinatura: o cinto do banco de trás fazendo "clique" sozinho e um perfume de flor de velório. Não aparece no retrovisor.
  - Regras: nunca olhe pelo retrovisor depois do clique; não aceite o desvio que ele pede; ele desce quando a corrida "termina", mas a corrida nunca termina.
  - Segredo: todos os endereços formam um caminho até o cemitério onde está alguém que o Rafa conhece.
- **Formato:** animação com a tela do app (mapa e mensagens) desenhada no quadro.
- **Cenários a encomendar:** o interior do carro à noite visto do banco do passageiro; a estrada escura; uma rua sem saída; a frente do cemitério.

### Você (POV) e os visitantes: "Pode Entrar?"
- **Protagonista:** você, em primeira pessoa, sem rosto. Sozinho numa casa com lareira, comida contada e porta com corrente e olho mágico.
- **Traço próprio da série:** mais realista que o Guizo, paleta fria (cinza-azulada da geada) com a luz quente da lareira; visitantes vistos pelo olho mágico (leve olho de peixe). Nada que lembre o jogo No, I'm Not a Human.
- **Os Ocos:** parecem gente e lembram a vida de quem eram, mas são vazios. Não sentem frio; o bafo não embaça o vidro; sabem coisas que não deviam. Nunca aparecem machucados.
- **Visitante do Ep. 1, Tiago:** entregador de app, 19 anos, jaqueta fina de entregador, bag térmica nas costas, capacete na mão, lábios roxos, tremendo. Simpático, cansado, educado demais.
- **Cenários a encomendar (Ep. 1):**
  - `olho_tiago`: vista pelo olho mágico (círculo com olho de peixe, borda preta), varanda com geada cinza, lâmpada fraca, Tiago no centro olhando para a porta;
  - `inverno_rua`: rua de casas apagadas coberta de geada cinza, céu baixo, um carro abandonado, fumaça de uma chaminé ao longe;
  - `caderno_lurdes`: close de um caderno escolar aberto à luz da lareira, anotações à mão (texto ilegível/rabiscos; o texto vai por cima no vídeo), página com canto rasgado;
  - `esp_tiago_vidro` (cena especial): o rosto do Tiago colado no olho mágico, distorcido, a boca aberta respirando perto do vidro e o vidro limpo, sem embaçar; `anima` sugerida: olhos piscando devagar e a cabeça inclinando;
  - `olho_tiago_celular`: pelo olho mágico, ele encosta o celular no vidro mostrando o app de entrega (tela sem texto legível; o texto vai por cima).

---

## Como estrear e soltar continuações
- **Personagem novo** estreia com um episódio que funciona sozinho, mas termina com o dilema A/B e um mistério aberto.
- **Continuação** só se o episódio for bem nos números: retenção acima da média do canal ou comentários A/B. Senão, o personagem descansa e outro estreia.
- **Alterne** entre Guizo, Rufus e um elenco novo. O Guizo é o ouro: continuações dele sempre que houver votação.
- **Toda criatura nova pode ganhar o próprio protocolo**, que serve de isca para a série dela.
- **Cenário que ainda não existe:** use o mais próximo que houver e mande no aviso do Telegram o prompt para o Vitor gerar, com o estilo base da bíblia.
