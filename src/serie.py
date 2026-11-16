"""Histórias em série: o próximo vídeo continua a partir da opção (A ou B) que o público escolheu.

O pedido chega como tema especial:
    "/continuar A"   -> nova parte, começando pela opção A do último vídeo, terminando com outro dilema
    "/final B"       -> última parte, começando pela opção B e encerrando a história
Qualquer outro tema cria uma história nova.
"""
from .util import carregar_historico


def interpretar(tema: str | None) -> dict:
    t = (tema or "").strip()
    partes = t.split()
    if partes and partes[0].lower() in ("/continuar", "/final"):
        opcao = partes[1].upper() if len(partes) > 1 and partes[1].upper() in ("A", "B") else ""
        return {"modo": "final" if partes[0].lower() == "/final" else "continuar", "opcao": opcao, "tema": ""}
    return {"modo": "nova", "opcao": "", "tema": t}


def ultimo_episodio() -> dict | None:
    """O vídeo mais recente que tem resumo e opções (os vídeos antigos, de antes desta função, não têm)."""
    return next((h for h in reversed(carregar_historico()) if h.get("resumo") and not h.get("fora_da_serie")), None)


def preparar(tema: str | None) -> dict:
    """Junta tudo o que o roteiro precisa saber. Lança ValueError com mensagem amigável se não der."""
    info = interpretar(tema)
    if info["modo"] == "nova":
        return info
    if not info["opcao"]:
        raise ValueError("Diga qual opção venceu: /continuar A, /continuar B, /final A ou /final B.")
    ant = ultimo_episodio()
    if not ant:
        raise ValueError("Ainda não há um vídeo com opções salvas para continuar. Gere um vídeo novo primeiro.")
    if ant.get("final"):
        raise ValueError(f"A história \"{ant.get('serie', ant['titulo'])}\" já terminou. Mande /novo para começar outra.")
    escolha = ant.get(f"opcao_{info['opcao'].lower()}", "")
    info.update({
        "serie": ant.get("serie") or ant["titulo"],
        "parte": int(ant.get("parte", 1)) + 1,
        "protagonista": ant.get("protagonista") or "homem",
        "resumo_anterior": ant["resumo"],
        "escolha": escolha,
        "tema": ant.get("tema", ""),
    })
    return info


def bloco_para_roteiro(info: dict) -> str:
    """Instruções extras para quem escreve o roteiro (Gemini ou agente)."""
    if info["modo"] == "nova":
        return ""
    fim = ("ESTA É A ÚLTIMA PARTE: encerre a história com um desfecho marcante e surpreendente. NÃO termine com dilema "
           "nem com \"Comente A ou B\"; a última frase convida a seguir o canal para a próxima história."
           if info["modo"] == "final" else
           "Termine com um NOVO dilema (Opção A / Opção B), terminando exatamente com \"Comente A ou B.\"")
    return f"""
=== CONTINUAÇÃO DE SÉRIE ===
Esta é a PARTE {info['parte']} da história "{info['serie']}". Mesma protagonista, mesmo lugar e mesma ameaça.
O que aconteceu até agora: {info['resumo_anterior']}
O público votou na OPÇÃO {info['opcao']}: {info['escolha']}
Comece exatamente a partir dessa escolha (a primeira frase relembra a decisão em poucas palavras, ex.: "Você escolheu ...").
{fim}
O título deve ser exatamente: "{info['serie']} - Parte {info['parte']}"
O campo "resumo" deve contar a história INTEIRA até aqui (partes anteriores + esta), em até 4 frases.
"""


def ajustar_roteiro(roteiro: dict, info: dict) -> None:
    """Garante título, numeração e protagonista corretos depois que o roteiro foi escrito."""
    if info["modo"] == "nova":
        roteiro.setdefault("serie", roteiro.get("titulo", ""))
        roteiro.setdefault("parte", 1)
        roteiro["final"] = False
        return
    roteiro["serie"] = info["serie"]
    roteiro["parte"] = info["parte"]
    roteiro["titulo"] = f"{info['serie']} - Parte {info['parte']}"
    roteiro["protagonista"] = info["protagonista"]
    roteiro["final"] = info["modo"] == "final"
    if roteiro["final"]:
        roteiro["opcao_a"] = roteiro["opcao_b"] = ""


def campos_historico(roteiro: dict) -> dict:
    return {k: roteiro.get(k, "") for k in ("serie", "parte", "resumo", "opcao_a", "opcao_b", "final", "lore")}


def mensagem_proximo_passo(roteiro: dict) -> str:
    if roteiro.get("final"):
        return "Fim da série! Mande /novo para começar outra história."
    return ("Quando souber qual opção ganhou nos comentários, mande:\n"
            f"/continuar A ou /continuar B  (nova parte)\n/final A ou /final B  (última parte)\n\n"
            f"A: {roteiro.get('opcao_a', '')}\nB: {roteiro.get('opcao_b', '')}")
