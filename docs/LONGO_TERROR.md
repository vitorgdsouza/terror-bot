# Vídeo longo do terror: "As Fitas da Madrugada"

**Aprovado pelo Vitor em 26/11, às 21h19** ("As Fitas da Madrugada é uma boa, bora pra cima"). **Post: sex 4/12, às 20h**, agendado direto no YouTube.

## A ideia
- **Formato:** horizontal 16:9, de 8 a 10 min. Conta para as 4 mil horas da monetização.
- **Conceito:** um narrador (você, em 2ª pessoa) acha uma **caixa de fitas VHS** num brechó, ou no porão de um prédio. Cada fita é um capítulo. Entre as fitas, pistas de que **todas foram gravadas no mesmo lugar**. Na **última fita, inédita**, aparece quem estava gravando, e a câmera vira para quem está assistindo.
- **Capítulos (proposta):**
  1. Abertura, a caixa;
  2. Fita da Farmácia (03:17);
  3. Fita do Terreiro (02:51);
  4. CAM 04 (03:13);
  5. CAM 02 Garagem;
  6. Fita sem etiqueta (final inédito);
  7. Fim, com gancho e "se inscreve".
- **Não é colagem dos Shorts:** narração e cenas novas que ligam as fitas, e cada fita recontada com material novo. Colagem é "conteúdo reutilizado" e prejudica a monetização.
- **Regras da casa (DIRECAO.md, seção 3):** sem gore, bichos nunca feridos, sem marcas ou pessoas reais, terror de suspense.

## Visual
- Os cenários do terror são verticais (9:16). No 16:9, cada fita aparece numa **TV de tubo 4:3** no centro, com moldura de VHS: REC, contador da fita, tracking e barras de chiado. Nos lados, o quarto escuro de quem assiste, com o cenário desfocado.
- Entre as fitas, a "mão" tira e põe a fita no videocassete, com som de mecanismo, e aparece o título do capítulo.
- **Motor:** adaptar `src/longo.py` do E Se Fosse Real? (blocos, narração guardada, capítulos, `reusar_narracao`) num módulo próprio do terror (`src/longo_terror.py`). Os canais são separados: não mexer no módulo do E Se Fosse Real? sem necessidade.
- **Voz:** Enceladus (terror), na cota do projeto Gemini do terror, separada da do E Se Fosse Real?.
- **Thumb 16:9:** TV de tubo com uma silhueta na tela, a pilha de fitas e a frase "AS FITAS DA MADRUGADA", em vermelho e VHS (identidade nova).

## Calendário
- **Sáb 29/11:** o Roteirista escreve o roteiro (`roteiros/longo_terror_01_fitas.json`) e manda para aprovação do Vitor (tipo roteiro).
- **Seg 30/11 a ter 1/12:** motor horizontal do terror e render de prova da abertura e da 1ª fita, com a prévia para o Vitor.
- **Qui 3/12:** render completo e revisão.
- **Sex 4/12, 20h:** post agendado (`agendar`), com capítulos na descrição.
