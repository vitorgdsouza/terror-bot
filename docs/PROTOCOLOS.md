# Guia de protocolos (analog horror): o que funciona e como fazemos

Pesquisa de novembro de 2026 sobre o que está em alta no TikTok e no YouTube. A partir dela, a regra da casa: **inspiração no formato, nunca cópia de criatura, arte ou texto de ninguém.** As criaturas são nossas ou de folclore de domínio público.

## O que está funcionando lá fora
- **"Protocolo de sobrevivência" de situação cotidiana.** Os perfis grandes do gênero fazem protocolos para:
  - um parente substituído por um imitador;
  - o cachorro que passa a agir estranho;
  - assobiar voltando sozinho à noite;
  - a escola com os corredores vazios;
  - uma noite no hospital;
  - um ônibus escolar com motorista desconhecido;
  - acordar com a porta do quarto fechada.
  
  Os de imitador e de cachorro passam de dezenas de milhares de curtidas.
- **Imitadores ("mimics") que copiam quem você ama** são o tema mais forte. Os vídeos ensinam os sinais (respiração, piscar, postura, imitar movimentos) e o que fazer.
- **Datas e eventos:** Halloween, "depois da meia-noite", "entre 3h e 4h". Também vale o formato de alerta de emergência aplicado a um assunto do momento, sempre avisando que é ficção.
- **Linguagem visual:** silhuetas e pictogramas rotulados ("real" × "imitação"), ilustrações de manual de segurança, tela de alerta, fita VHS. O texto dos clássicos é seco e oficial, e o medo vem quando a instrução fica específica demais.
- **Regra de ouro do gênero:**
  - Quem assiste entende o formato oficial na hora, e depois percebe que a mensagem "sabe demais": cita o seu quarto, a sua casa, o seu bicho.
  - Uma instrução inofensiva fica perigosa se seguida à risca.
  - Esconda um quadro que só aparece revendo.
- **Aviso de ficção:** os perfis grandes marcam "ficção / para entretenimento" na legenda. Faça o mesmo: "história de ficção".

## Estrutura do nosso protocolo (40 a 55 s, voz Enceladus no estilo alerta)
1. **Gancho (0 a 2 s):** a situação, em uma frase, com o pictograma que define tudo. Exemplo: "Se o seu gato encarar a escada no escuro...". Toca o bipe de alerta.
2. **Tom oficial:** "Preste atenção" ou "Siga cada passo", com o rótulo do protocolo (`rotulo`).
3. **Três regras numeradas** (PRIMEIRO, SEGUNDO, TERCEIRO, com `destaque`):
   - cada regra traz um sinal concreto para reconhecer e uma ação;
   - pelo menos uma tem um detalhe sensorial (som, contar, ritmo, cheiro);
   - uma delas soa estranha ("não deixe ele perceber que você sabe").
4. **"A parte mais importante":** a virada. A instrução contradiz o instinto, ou revela que o perigo já está dentro de casa.
5. **Fecho que prende:**
   - uma frase que liga a uma série nossa, como "Foi assim que a coleira do Rufus apareceu lavada na pia";
   - ou que acusa quem assiste ("Você contou quantas vezes ele piscou?");
   - ou que pede para rever.
6. **Legenda:** a pergunta direta ("Seu cachorro já fez isso?"), "história de ficção" e 5 hashtags (#analoghorror #protocolo #terror + o tema).

## Temas nossos para os próximos (criar à vontade, variando)
- **Folclore brasileiro em formato de protocolo**, nosso diferencial em português, de domínio público:
  - **A Pisadeira:** sobe no peito de quem dorme de barriga cheia. "Se você acordar sem conseguir se mexer...".
  - **O Corpo-Seco**, rejeitado pela terra.
  - **A Mula sem Cabeça** em estrada de terra.
  - **O Homem do Saco** batendo no portão.
  - **A Loira do Banheiro** da escola.
  - **O assobio** ("se ouvir um assobio forte de noite no mato, não responda" é ótimo, e nada sangrento).
- **Imitadores do nosso universo:** o Abismo imitando a voz da mãe, o falso Rufus, e imitadores novos (ver `docs/PERSONAGENS.md`).
- **Cotidiano brasileiro:**
  - o último ônibus da madrugada;
  - o interfone tocando às 3h;
  - o grupo da família mandando áudio de quem já morreu (cuidado: sem luto real);
  - a vizinha que pede para entrar;
  - a farmácia 24h;
  - o elevador que para num andar que não existe.
- **Bichos de estimação** (é o que já performa): gato, cachorro, papagaio que repete uma voz que ninguém da casa tem, peixe que sempre olha para a porta.

## Recursos que temos (src/protocolo.py)
- **Ícones:** cama, janela, olho, porta, porta_aberta, alerta, relogio, casa, prancheta, som, parar, coleira, pegadas, escada, `gato:<acao>`, `cachorro:<acao>`, `falso:<acao>`, `pessoa:<pose>`.
- **Configuração:** `rotulo` ("PROTOCOLO <NOME>") e `sombra` (abismo | falso) para a silhueta gigante no fundo.
- **Criatura nova:** crie o ícone dela em `src/protocolo.py`, uma silhueta desenhada em PIL como as outras. Se fizer sentido, crie também a sombra de fundo dela. Teste com um quadro de prova antes de renderizar.
- **Variação visual:** use o formato `sombra` (silhuetas pretas no vermelho, quadros relogio, quarto, rosto, porta, portas) para variar entre um protocolo e outro.
