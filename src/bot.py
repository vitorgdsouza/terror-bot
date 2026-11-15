"""Lê os comandos enviados ao bot do Telegram (roda a cada 20 minutos no GitHub Actions).

Comandos:
    /novo              gera um vídeo com o tema padrão da série
    /novo <tema>       gera um vídeo sobre o tema escolhido
    /ideias            sugere 5 ideias de histórias
    /ajuda             mostra os comandos
Quando há um /novo, este script escreve o tema na saída do GitHub Actions para o próximo passo gerar o vídeo.
"""
import os

from . import telegram
from .roteiro import gerar_ideias
from .util import carregar_config, log

AJUDA = ("Comandos:\n"
         "/novo - gera um vídeo com o tema padrão\n"
         "/novo lenda do Corpo Seco - gera um vídeo sobre esse tema\n"
         "/ideias - sugere 5 ideias de histórias\n\n"
         "Os comandos são lidos a cada 20 minutos, então a resposta pode demorar um pouco.")


def _saida_actions(chave: str, valor: str) -> None:
    arq = os.environ.get("GITHUB_OUTPUT")
    if arq:
        with open(arq, "a", encoding="utf-8") as f:
            f.write(f"{chave}<<FIM\n{valor}\nFIM\n")


def main():
    dono = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    pedido = None
    for msg in telegram.ler_mensagens_novas():
        chat, texto = msg["chat_id"], msg["texto"]
        if not dono or chat != dono:
            telegram.enviar_mensagem(f"Seu chat ID é {chat}. Cadastre esse número no secret TELEGRAM_CHAT_ID do GitHub para liberar o bot.", chat)
            continue
        comando, _, resto = texto.partition(" ")
        comando = comando.split("@")[0].lower()
        if comando == "/novo":
            if pedido is None:
                pedido = resto.strip()
                telegram.enviar_mensagem(f"Pedido recebido: {pedido or 'tema padrão da série'}. Começando agora.")
            else:
                telegram.enviar_mensagem("Já tem um vídeo na fila. Mande o próximo /novo depois que este chegar.")
        elif comando == "/ideias":
            ideias = gerar_ideias(carregar_config())
            telegram.enviar_mensagem("Ideias:\n\n" + "\n".join(f"- {i}" for i in ideias)
                                     + "\n\nPara usar uma: /novo <cole a ideia aqui>")
        else:
            telegram.enviar_mensagem(AJUDA)

    _saida_actions("gerar", "sim" if pedido is not None else "nao")
    _saida_actions("tema", pedido or "")
    log(f"Pedido de vídeo: {pedido!r}" if pedido is not None else "Nenhum pedido novo.")


if __name__ == "__main__":
    main()
