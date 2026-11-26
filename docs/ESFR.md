# E Se Fosse Real?: direção do canal 2

É um canal **separado** do Você Escaparia?. As regras do terror (`docs/DIRECAO.md`) não valem aqui, e as daqui não valem lá. O Claude tem controle total de tendências e disparos neste canal, a pedido do Vitor (20/11/2026). O objetivo é monetizar antes do canal de terror.

## Identidade
- **Assunto:** ciência e curiosidades em segunda pessoa ("E se você...?").
- **Formato:** `voce` (`src/voce.py`), paleta `ciencia` (azul, amarelo e ciano), selo "E SE..." no canto, sem relógio de terror.
- **Voz:** Puck, no estilo `curioso` (`"voz": "Puck", "clima": "curioso"`). A chave da voz é `GEMINI_API_KEY_ESE`, se existir, para ter cota separada do terror.
- **Trilha:** `"trilha": "propria"` (trilha sintetizada do canal, `src/trilha_esfr.py`, sem bipes e sem direitos de terceiros). O Vitor aprovou em 22/11.
- **Todo roteiro leva `"canal": "esfr"`.** É isso que o separa do terror no render, no Telegram e nas thumbs.

## Onde fica cada coisa
- **Roteiros:** `roteiros/esfr/`
- **Fila:** `data/fila_esfr.json`, postada às 12h17, 16h17 e 20h17 (até 3 por dia, 2 h de intervalo) por `.github/workflows/fila-esfr.yml` (segredos `YT_REFRESH_TOKEN_ESE` e `UPLOAD_POST_USER_ESE`)
- **Diário:** `data/esfr/diario.md`

## Thumbs (em teste desde 24/11)
- **Thumb própria em teste:** o buraco negro (08) foi o primeiro com arte feita só para a thumb (`thumb_arte`): o objeto gigante, um personagem com emoção (astronauta com `medo`) e a seta vermelha. A ideia veio do Vitor, que achou as thumbs de quadro do vídeo "simples".
- **Como decidir:** quando o 08 tiver uns 3 dias no ar (os dados do YouTube atrasam 2 a 3 dias), compare as views das primeiras 48 h e, se o relatório trouxer, a taxa de cliques das impressões com as dos vídeos de thumb simples (Lua, Terra, Espaço, anéis). Se o 08 for melhor, isso vira o padrão: todo roteiro novo ganha uma `thumb_arte` própria nesse molde. Se não for, volte à thumb de quadro (já centralizada).
- Até a decisão, os roteiros novos podem continuar com a thumb de quadro.

## Regras de conteúdo
- **Fatos checados**, com as fontes na descrição. Número só com fonte.
- **Nada de saúde nem finanças.** A política de "conteúdo inautêntico" do YouTube corta a monetização de personas de IA nesses temas.
- **Cada vídeo com assunto e roteiro únicos.** Molde repetido com troca de palavras não serve, porque o YouTube não monetiza conteúdo produzido em massa.
- **Ritmo:** de 45 a 60 s, uma frase curta por cena, algo se mexendo sempre, pergunta no final.
- **Um vídeo longo por semana** (compilação de 8 a 12 min) para somar horas assistidas.

## Meta de monetização
- **Até 31/01/2027:** 1.000 inscritos e (10 milhões de views em Shorts em 90 dias OU 4.000 horas assistidas em 12 meses).
- **A partir de 01/02/2027**, a barra dobra para 8.000 horas ou 20 milhões de views.


## Lição de 26/11 (Fermi)
- **Duração:** 35 a 45 s, no máximo cerca de 100 palavras.
- **Gancho:** a 1ª frase põe um objeto concreto em perigo, agora e com você (a Lua sumindo, o Sol apagando, você sem traje). Tema abstrato só funciona traduzido para uma ameaça concreta.
- **Uma ideia por vídeo.** Hipóteses múltiplas viram uma série, com um vídeo para cada uma.
