"""Lê os comandos enviados ao bot do Telegram (roda a cada 20 minutos no GitHub Actions).

Comandos:
    /novo              gera um vídeo com o tema padrão da série
    /novo <tema>       gera um vídeo sobre o tema escolhido
    /ideias            sugere 5 ideias de histórias (numeradas, com botões)
    /ideias <assunto>  sugere 5 ideias sobre um assunto (ex.: /ideias hospital abandonado)
    /usar <n>          gera o vídeo da ideia n da última lista
    /postar            publica o último vídeo pronto no YouTube Shorts
    /continuar A|B     nova parte da última história, a partir da opção vencedora
    /final A|B         última parte da história, a partir da opção vencedora
    /historia          mostra a última história e as opções dela
    /relatorio         indicadores do canal do YouTube (views, retenção, quem ficou, compartilhamentos)
    /fila              mostra a fila de postagem automática do YouTube (11h47 e 18h47)
    /enfileirar        põe o último vídeo gerado no fim da fila
    /ajuda             mostra os comandos
Quando há um /novo, este script escreve o tema na saída do GitHub Actions para o próximo passo gerar o vídeo.
"""
import json
import os

from . import serie, telegram
from .roteiro import gerar_ideias
from .util import RAIZ, carregar_config, log

IDEIAS = RAIZ / "data" / "ideias.json"   # última lista de ideias (salva no repositório junto com o histórico)

AJUDA = ("Comandos:\n"
         "/novo - gera um vídeo com o tema padrão\n"
         "/novo você ouve passos no sótão - gera um vídeo sobre esse tema\n"
         "/ideias - sugere 5 ideias de histórias\n"
         "/ideias hospital abandonado - 5 ideias sobre esse assunto\n"
         "/usar 3 - gera o vídeo da ideia 3 da última lista\n"
         "/postar - publica o último vídeo no YouTube Shorts\n"
         "/continuar A - nova parte da última história, seguindo a opção A (ou B)\n"
         "/final B - última parte da história, seguindo a opção B (ou A)\n"
         "/historia - mostra a última história e as opções dela\n"
         "/relatorio - indicadores do YouTube (retenção, quem ficou, compartilhamentos)\n"
         "/fila - a fila de postagem automática (11h47 e 18h47)\n"
         "/enfileirar - põe o último vídeo gerado na fila\n\n"
         "Os comandos são lidos a cada 20 minutos, então a resposta pode demorar um pouco.")


def _saida_actions(chave: str, valor: str) -> None:
    arq = os.environ.get("GITHUB_OUTPUT")
    if arq:
        with open(arq, "a", encoding="utf-8") as f:
            f.write(f"{chave}<<FIM\n{valor}\nFIM\n")


def main():
    dono = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    pedido = None
    postar = ""
    relatorio = False
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
        elif comando in ("/continuar", "/final"):
            try:
                info = serie.preparar(texto)
            except ValueError as e:
                telegram.enviar_mensagem(str(e))
                continue
            if pedido is None:
                pedido = f"{comando} {info['opcao']}"
                telegram.enviar_mensagem(f"Pedido recebido: {'última parte' if comando == '/final' else 'parte ' + str(info['parte'])} "
                                         f"de \"{info['serie']}\", seguindo a opção {info['opcao']}. Começando agora.")
            else:
                telegram.enviar_mensagem("Já tem um vídeo na fila. Mande o próximo pedido depois que este chegar.")
        elif comando == "/historia":
            ant = serie.ultimo_episodio()
            if not ant:
                telegram.enviar_mensagem("Ainda não há história com opções salvas.")
            else:
                telegram.enviar_mensagem(f"Última: {ant['titulo']}\n\n{ant['resumo']}\n\n"
                                         + serie.mensagem_proximo_passo(ant))
        elif comando == "/ideias":
            assunto = resto.strip()
            ideias = gerar_ideias(carregar_config(), assunto=assunto)
            IDEIAS.parent.mkdir(parents=True, exist_ok=True)
            IDEIAS.write_text(json.dumps({"assunto": assunto, "ideias": ideias}, ensure_ascii=False, indent=2),
                              encoding="utf-8")
            numeradas = "\n\n".join(f"{n}. {i}" for n, i in enumerate(ideias, 1))
            telegram.enviar_mensagem(f"Ideias{' sobre ' + assunto if assunto else ''}:\n\n{numeradas}\n\n"
                                     "Toque num botão (ou mande /usar 2) para gerar o vídeo dessa ideia. "
                                     "Pode também mandar /novo com a ideia editada do seu jeito.",
                                     botoes=[[f"/usar {n}" for n in range(1, len(ideias) + 1)]])
        elif comando == "/postar":
            from .postar import PENDENTE
            p = json.loads(PENDENTE.read_text(encoding="utf-8")) if PENDENTE.exists() else None
            if not p:
                telegram.enviar_mensagem("Não há vídeo pronto para postar. Gere um com /novo ou /usar.")
            elif p.get("postado"):
                telegram.enviar_mensagem(f"\"{p['titulo']}\" já foi postado. Gere um vídeo novo para postar de novo.")
            else:
                postar = p["run_id"]
                telegram.enviar_mensagem(f"Publicando \"{p['titulo']}\" no YouTube Shorts...")
        elif comando == "/fila":
            from .fila import mostrar
            mostrar()
        elif comando == "/enfileirar":
            from .fila import enfileirar
            enfileirar()
        elif comando == "/relatorio":
            relatorio = True
            telegram.enviar_mensagem("Buscando os números do YouTube...")
        elif comando == "/usar":
            try:
                lista = json.loads(IDEIAS.read_text(encoding="utf-8"))["ideias"]
                ideia = lista[int(resto.strip()) - 1]
            except (FileNotFoundError, ValueError, IndexError, KeyError):
                telegram.enviar_mensagem("Não achei essa ideia. Mande /ideias para uma lista nova e depois /usar 1 a 5.")
                continue
            if pedido is None:
                pedido = ideia
                telegram.enviar_mensagem(f"Pedido recebido: {ideia}\nComeçando agora.")
            else:
                telegram.enviar_mensagem("Já tem um vídeo na fila. Mande o próximo pedido depois que este chegar.")
        else:
            telegram.enviar_mensagem(AJUDA)

    _saida_actions("gerar", "sim" if pedido is not None else "nao")
    _saida_actions("postar", postar)
    _saida_actions("relatorio", "sim" if relatorio else "nao")
    _saida_actions("tema", pedido or "")
    log(f"Pedido de vídeo: {pedido!r}" if pedido is not None else "Nenhum pedido novo.")


if __name__ == "__main__":
    main()
