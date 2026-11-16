#!/usr/bin/env bash
# Gera um vídeo. Usa o agente diretor (Claude Code) se houver credencial do Claude;
# se ele não estiver configurado, falhar ou o limite de uso acabar, usa o modo reserva (Gemini).
set -uo pipefail
TEMA="${1:-}"
export TEMA   # as ferramentas do agente leem o pedido (ex.: "/continuar A")
# secrets vazios atrapalham a autenticação do Claude Code
[ -z "${ANTHROPIC_API_KEY:-}" ] && unset ANTHROPIC_API_KEY
[ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ] && unset CLAUDE_CODE_OAUTH_TOKEN

avisar() {
  python -c "import sys; from src import telegram; telegram.enviar_mensagem(sys.argv[1])" "$1" || true
}

if [ "${USAR_CLAUDE:-sim}" != "nao" ] && { [ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}" ] || [ -n "${ANTHROPIC_API_KEY:-}" ]; }; then
  echo "=== Modo agente: Claude como diretor ==="
  npm install -g @anthropic-ai/claude-code >/dev/null 2>&1
  rm -rf trabalho && mkdir -p trabalho
  PROMPT="$(cat agente/INSTRUCOES.md)

TEMA: ${TEMA}"
  MODELO=()
  [ -n "${CLAUDE_MODEL:-}" ] && MODELO=(--model "$CLAUDE_MODEL")

  timeout 35m claude -p "$PROMPT" "${MODELO[@]}" --max-turns 120 --output-format text \
    --allowedTools "Bash(python -m src.ferramentas:*),Bash(ls:*),Read,Write,Edit,Glob" \
    | tee trabalho/agente.log
  if [ -f trabalho/ENVIADO ]; then
    echo "=== Agente concluiu ==="
    exit 0
  fi
  echo "=== Agente não concluiu; usando o modo reserva (Gemini) ==="
  avisar "O agente Claude não conseguiu terminar (talvez o limite de uso do Pro tenha acabado). Gerando no modo reserva com o Gemini..."
fi

echo "=== Modo reserva: Gemini ==="
python -m src.pipeline --tema "$TEMA"
