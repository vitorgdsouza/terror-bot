# terror-bot: canal "Você Escaparia?"

Automação de Shorts de terror em português. O dono é o Vitor, que é o gerente e aprova roteiros e vídeos finais.

- Leia `docs/DIRECAO.md` antes de criar qualquer coisa. A seção 3, "Gosto do Vitor", é lei.
- **Equipe:** as fichas dos agentes estão em `.claude/agents/`. Para conversar com um agente específico, use as skills `/analista`, `/roteirista`, `/diretor-de-arte`, `/revisor` e `/publicador`. Se o Vitor pedir para "falar com o Roteirista" (ou outro), carregue a skill correspondente.
- **Aprovações:** ficam em `data/aprovacoes.json`. A Mesa do Gerente está em https://claude.ai/artifact/6fLXTMtRQiX4XvTNFcg92f. Nada entra em `data/fila.json` sem a aprovação do Vitor.
- **Renders:** são feitos pelo GitHub Actions (`refazer-video.yml`), um de cada vez.
- **Segredos:** só no GitHub Secrets. Nunca em arquivos ou mensagens.
