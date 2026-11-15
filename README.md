# Você Escaparia?: gerador automático de animações de terror

Este projeto cria sozinho animações de terror em segunda pessoa ("você está sozinho em casa..."), no formato vertical 9:16, com cerca de 2 minutos. Cada vídeo termina com um dilema: "Comente A ou B" e manda o vídeo pronto para o seu Telegram. Tudo roda de graça no GitHub.

**Como funciona:**

1. **Roteiro**: o Gemini (IA do Google, plano gratuito) escreve uma história original em 14 cenas, falando com o espectador e terminando com duas opções (A ou B).
2. **Imagens**: o Pollinations (gratuito) desenha os cenários vazios em estilo desenho 2D noturno. O protagonista e a ameaça são figurinhas fixas coladas por cima, então ficam sempre iguais.
3. **Narração**: as vozes neurais do Microsoft Edge (gratuitas) narram em português.
4. **Montagem**: o FFmpeg anima as imagens com movimentos suaves de câmera e coloca legendas palavra por palavra, com a palavra falada destacada numa caixa roxa, além de um som ambiente sombrio.
5. **Entrega**: o vídeo chega no seu Telegram junto com a legenda pronta para colar no post.

**Dois modos de produção:**
- **Agente diretor (Claude), o de melhor qualidade.** Ele usa a sua assinatura do Claude Pro. O Claude escreve e revisa o roteiro, olha cada imagem gerada, refaz as cenas ruins (personagem diferente, texto na imagem, erro de desenho) e confere o vídeo final antes de enviar. Veja como ativar na seção "Ativar o agente Claude".
- **Modo reserva (Gemini), 100% grátis.** Funciona sem o Claude e entra sozinho quando o agente não está configurado, dá erro ou o limite do Pro acaba. Nesse modo, ninguém revisa as imagens.

O sistema roda de três formas:
- **Todo dia às 18:17**, de forma automática.
- **Quando você manda `/novo`** no Telegram.
- **Pelo botão "Run workflow"** no GitHub.

---

## Passo a passo da configuração (uns 30 minutos, uma vez só)

### 1. Crie a conta no GitHub e o repositório
1. Crie uma conta grátis em https://github.com/signup
2. Clique em **New repository** (botão verde, ou o **+** no canto superior direito).
3. Dê o nome `terror-bot` e marque **Public**.
   - Por que público: no GitHub, a automação (GitHub Actions) é **ilimitada e grátis em repositórios públicos**. Repositórios privados têm só 2.000 minutos por mês.
   - Suas chaves **não** ficam visíveis, porque elas vão para a área de "Secrets" (passo 4).
4. Clique em **Create repository**.

### 2. Envie os arquivos deste projeto
O jeito mais fácil é usar o **GitHub Desktop** (https://desktop.github.com):
1. Faça login no GitHub Desktop.
2. Escolha **File > Clone repository** e selecione `terror-bot`.
3. Copie todos os arquivos deste projeto para a pasta que ele criou, **incluindo a pasta `.github`**.
4. Escreva uma mensagem, clique em **Commit to main** e depois em **Push origin**.

> A pasta `.github` começa com ponto e fica oculta em alguns sistemas. No Mac, aperte `Cmd + Shift + .` no Finder para ver arquivos ocultos. No Windows, ative **Exibir > Itens ocultos**. Sem essa pasta, a automação não funciona.

### 3. Pegue as duas chaves gratuitas

**Chave do Gemini (roteiros):**
1. Acesse https://aistudio.google.com e entre com sua conta Google.
2. Clique em **Get API key** e depois em **Create API key**. Não pede cartão.
3. Copie a chave (começa com `AIza...`).

**Bot do Telegram:**
1. No Telegram, procure **@BotFather** (tem o selo azul de verificado).
2. Mande `/newbot`, escolha um nome (ex.: `Você Escaparia`) e um usuário terminado em `bot` (ex.: `contos_meianoite_bot`).
3. Copie o **token** que ele te enviar (algo como `123456789:AAH...`).
4. Abra o seu bot novo e mande `/start`.

### 4. Cadastre as chaves no GitHub (Secrets)
No repositório, vá em **Settings > Secrets and variables > Actions > New repository secret** e crie:

| Nome do secret | Valor |
|---|---|
| `GEMINI_API_KEY` | a chave do Google AI Studio |
| `TELEGRAM_BOT_TOKEN` | o token do BotFather |

### 5. Descubra o seu chat ID e libere o bot
1. No GitHub, abra a aba **Actions**, clique em **Bot do Telegram** e depois em **Run workflow**.
2. Em até 1 minuto, o bot te responde no Telegram: *"Seu chat ID é 123456789"*.
3. Crie mais um secret, `TELEGRAM_CHAT_ID`, com esse número.

Pronto. Só você consegue dar comandos ao bot. Qualquer outra pessoa que falar com ele recebe apenas o próprio ID.

### 6. Faça o primeiro vídeo
**Actions > Gerar vídeo > Run workflow**. Escreva um tema (ex.: `alguém bate na sua janela do 5º andar às 3 da manhã`) ou deixe vazio. Em cerca de 5 a 10 minutos, o vídeo chega no Telegram.

---

## Ativar o agente Claude (recomendado, depois que o modo grátis funcionar)

O agente usa a sua assinatura do Claude Pro no lugar de uma API paga. Para isso, você gera um token uma única vez no seu computador:

1. **Instale o Claude Code no computador.**
   - Mac ou Linux, no Terminal: `curl -fsSL https://claude.ai/install.sh | bash`
   - Windows, no PowerShell: `irm https://claude.ai/install.ps1 | iex`
   - Se esses comandos mudarem, o jeito atual de instalar está em https://code.claude.com/docs
2. **Gere o token.** No Terminal, rode `claude setup-token`. O navegador abre: entre com a mesma conta do seu Claude Pro e autorize.
3. **Copie o token** que aparece no Terminal (começa com `sk-ant-oat01-`).
4. **Cadastre o token no GitHub.** Crie o secret `CLAUDE_CODE_OAUTH_TOKEN` com esse valor (mesmo caminho do passo 4 da configuração).

Pronto: os próximos vídeos já saem pelo agente. No Telegram chega uma "Nota do diretor" contando o que ele corrigiu.

**Bom saber:**
- **O agente gasta o mesmo limite de uso que você tem no chat do Claude.** Se o limite acabar, o vídeo sai pelo modo reserva e você recebe um aviso. Com vídeos diários, a cota para conversar pode ficar menor.
- **O token vale por cerca de 1 ano.** Depois disso, gere outro com o mesmo comando.
- **Confira as regras do plano.** Antes de deixar rodando no automático, veja se o uso agendado com a assinatura é permitido pelos termos do plano Pro (support.claude.com). Outra opção é a API paga do Claude: crie uma chave em console.anthropic.com e salve no secret `ANTHROPIC_API_KEY` no lugar do token.
- **Para desligar o agente** sem apagar o token: crie a *variable* `USAR_CLAUDE` com o valor `nao`.
- **Para escolher o modelo:** crie a *variable* `CLAUDE_MODEL`, por exemplo `sonnet` (melhor qualidade) ou `haiku` (gasta menos limite).
- **As regras de trabalho do agente** ficam em `agente/INSTRUCOES.md`. Você pode editar esse arquivo para mudar o que ele cobra de qualidade.

---

## Comandos do bot no Telegram

| Comando | O que faz |
|---|---|
| `/novo` | gera um vídeo com o tema padrão da série |
| `/novo você ouve passos no sótão e mora sozinho` | gera um vídeo sobre esse tema |
| `/ideias` | sugere 5 ideias inéditas de histórias |
| `/ajuda` | mostra os comandos |

> O GitHub confere os comandos **a cada 20 minutos** (às vezes atrasa um pouco). Por isso a resposta não é instantânea. Para respostas imediatas seria preciso um servidor ligado 24 horas, o que fica para uma próxima fase.

---

## O personagem fixo

Há duas protagonistas, que se alternam a cada vídeo: um homem de capa amarela e uma mulher loira de jaqueta vermelha. A narração se ajusta ao gênero ("sozinho" ou "sozinha"). Para fixar uma delas, mude `protagonista_modo` em `config/serie.json` para `homem` ou `mulher`; para voltar a alternar, use `alternar`.

O protagonista e a ameaça (o vulto de olhos brancos) **não são desenhados pela IA**. Eles são figurinhas fixas, guardadas em `assets/personagem/`. A IA gera só os cenários vazios, e o sistema cola o personagem por cima, com sombra no chão e tom noturno. Assim ele fica igual em todas as cenas e em todos os vídeos.

- **Poses disponíveis:** `frente`, `medo`, `costas`, `celular`, `lanterna` e `maos_celular` (close das mãos segurando o celular).
- **Ameaças:** `sombra` (o vulto inteiro) e `olhos` (só os olhos no escuro).
- **Mudar o visual:** os desenhos originais ficam em `assets/personagem/fonte/` (as figurinhas da mulher ficam em `assets/personagem/mulher/`). Peça ao Claude para criar novas poses ou mudar as cores; ele gera os PNGs de novo.

## Personalizar a série

Tudo fica em `config/serie.json`, que você pode editar direto no site do GitHub (abra o arquivo e clique no lápis):

- **`tema_padrao`**: o assunto das histórias.
- **`estilo_visual`**: o estilo das imagens, em inglês.
- **`protagonista_modo`**: `alternar` (um vídeo com cada protagonista), `homem` ou `mulher`.
- **`efeitos`**: `limpo` (desenho animado, cores preservadas) ou `terror` (imagem lavada, cintilação, granulado, tremor mais forte).
- **`legenda`**: `estilo` `karaoke` (palavra destacada) ou `simples`, a cor do destaque e se mostra o título no começo.
- **`voz`**: `pt-BR-AntonioNeural` (masculina) ou `pt-BR-FranciscaNeural` (feminina). Para uma voz mais lenta e grave, use velocidade `-15%` e tom `-10Hz`.
- **`numero_de_cenas`** e **`duracao_alvo_segundos`**: o tamanho do vídeo.
- **Horário diário**: no arquivo `.github/workflows/gerar-video.yml`, linha `cron: "17 21 * * *"`. O horário está em UTC, que é Brasília + 3 horas. Apague as duas linhas do `schedule` para desligar.
- **Música**: coloque `.mp3` livres de direitos em `assets/musica/`. Sem nenhuma música lá, o sistema gera um som ambiente sozinho.

---

## Limites dos serviços gratuitos (leia antes de publicar)

- **A animação é feita de "câmera" e efeitos, não de IA de vídeo.** É o formato de *motion comic*, comum em canais de terror. Animação de verdade por IA (Kling, Runway, Hailuo etc.) é paga. Dá para trocar depois, só no passo de montagem.
- **Pollinations sem cadastro:** aceita cerca de 1 imagem a cada 15 segundos e coloca marca d'água. Uma conta grátis em https://enter.pollinations.ai gera uma chave (começa com `sk_`) que tira a marca e aumenta o limite. Salve essa chave no secret `POLLINATIONS_TOKEN`. **Antes de monetizar o canal, confira os termos de uso** do Pollinations e dos modelos de imagem.
- **Gemini grátis:** tem limite de pedidos por dia. Para 1 a 5 vídeos por dia, sobra. No plano gratuito, o Google pode usar o conteúdo enviado para melhorar os produtos dele.
- **Se um modelo do Gemini sair do ar:** o código tenta outros sozinho. Para escolher um específico, crie uma *variable* (não secret) chamada `GEMINI_MODEL` em **Settings > Secrets and variables > Actions > Variables**.
- **Repositório parado:** em repositórios públicos, o GitHub desliga os agendamentos depois de 60 dias sem atividade. Como cada vídeo salva o histórico no repositório, isso não deve acontecer enquanto o sistema estiver rodando.
- **Marque como conteúdo feito com IA** ao publicar no TikTok, YouTube e Instagram.

---

## Problemas comuns

| Sintoma | Solução |
|---|---|
| Nada aparece na aba Actions | Falta a pasta `.github` no repositório (veja o passo 2). |
| Erro "a variável ... não está configurada" | Falta um secret, ou o nome dele está escrito diferente (passo 4). |
| O bot não responde | Mande `/start` para o bot, confira o `TELEGRAM_CHAT_ID` e espere até 20 minutos. |
| Erro 429 do Gemini | O limite gratuito do dia acabou. Tente amanhã ou espere alguns minutos. |
| Cenas com fundo escuro, sem desenho | O Pollinations falhou naquela imagem. Gere de novo, ou cadastre o `POLLINATIONS_TOKEN`. |
| Para ver o vídeo sem o Telegram | Actions > clique na execução > **Artifacts** > `video` (fica guardado por 7 dias). |
| Quero ver o que o agente fez | No mesmo Artifact estão `agente.log` (o relatório dele) e `folha.jpg` (todas as cenas). |
| Chegou o aviso "agente não conseguiu terminar" | O limite do Pro acabou ou o token expirou. O vídeo sai pelo modo reserva; gere um token novo se o problema continuar. |

## Estrutura do projeto
```
config/serie.json          configurações da série (estilo, voz, protagonistas)
src/roteiro.py             agente roteirista (Gemini)
src/imagens.py             imagens das cenas (Pollinations)
src/voz.py                 narração (edge-tts)
src/montagem.py            vídeo final (FFmpeg)
src/personagem.py          cola o personagem fixo e a ameaça sobre os cenários
assets/personagem/         figurinhas do protagonista e da ameaça
src/telegram.py            envio e leitura de mensagens
src/bot.py                 comandos /novo e /ideias
src/pipeline.py            junta tudo (modo reserva)
src/ferramentas.py         ferramentas que o agente Claude usa
agente/INSTRUCOES.md       regras e checklist de qualidade do agente diretor
scripts/gerar.sh           escolhe entre o agente e o modo reserva
.github/workflows/         automação no GitHub Actions
data/historico.json        histórias já feitas (para não repetir)
assets/musica/             suas trilhas livres de direitos (opcional)
```

Para testar no seu computador (opcional, precisa de Python 3.11+ e FFmpeg instalados):
```
pip install -r requirements.txt
export GEMINI_API_KEY=sua_chave
python -m src.pipeline --sem-telegram --tema "Curupira"
```
O vídeo aparece em `saida/`.
