"""Comunicação com o Telegram: mensagens, vídeo e leitura de comandos."""
from pathlib import Path

import requests

from .util import env

API = "https://api.telegram.org/bot{token}/{metodo}"


def _url(metodo: str) -> str:
    return API.format(token=env("TELEGRAM_BOT_TOKEN"), metodo=metodo)


def _checar(r: requests.Response, acao: str) -> dict:
    """Mostra um erro claro quando o Telegram recusa o pedido (ex.: token errado)."""
    try:
        dados = r.json()
    except ValueError:
        dados = {"ok": False, "description": r.text[:200]}
    if not dados.get("ok"):
        dica = ""
        if r.status_code == 401:
            dica = " -> O TELEGRAM_BOT_TOKEN está errado. Copie de novo o token do BotFather para o secret."
        elif r.status_code == 400 and "chat not found" in str(dados).lower():
            dica = " -> O TELEGRAM_CHAT_ID está errado, ou você ainda não mandou /start para o bot."
        raise RuntimeError(f"Telegram recusou {acao} ({r.status_code}): {dados.get('description')}{dica}")
    return dados


def enviar_mensagem(texto: str, chat_id: str | None = None, botoes: list[list[str]] | None = None) -> None:
    """botoes: linhas de botões de resposta (ao tocar, o Telegram envia o texto do botão como mensagem)."""
    import json
    chat_id = chat_id or env("TELEGRAM_CHAT_ID")
    partes = [texto[i:i + 4000] for i in range(0, len(texto), 4000)] or [""]  # limite do Telegram por mensagem
    for n, parte in enumerate(partes):
        dados = {"chat_id": chat_id, "text": parte}
        if botoes and n == len(partes) - 1:
            dados["reply_markup"] = json.dumps({"keyboard": [[{"text": b} for b in linha] for linha in botoes],
                                                "resize_keyboard": True, "one_time_keyboard": True})
        r = requests.post(_url("sendMessage"), timeout=30, data=dados)
        _checar(r, "a mensagem")


def enviar_video(caminho, legenda: str) -> None:
    import time
    for tentativa in range(3):                            # o Telegram às vezes devolve 502/504 em vídeo grande
        try:
            with open(caminho, "rb") as f:
                r = requests.post(_url("sendVideo"), timeout=300,
                                  data={"chat_id": env("TELEGRAM_CHAT_ID"), "caption": legenda[:1024],
                                        "supports_streaming": "true", "width": 1080, "height": 1920},
                                  files={"video": ("video.mp4", f, "video/mp4")})
        except requests.RequestException:
            if tentativa == 2:
                raise
            time.sleep(20)
            continue
        if r.status_code < 500 or tentativa == 2:
            break
        time.sleep(20)
    _checar(r, "o vídeo")


def enviar_arquivo(caminho, legenda: str = "") -> None:
    caminho = Path(caminho)
    with open(caminho, "rb") as f:
        r = requests.post(_url("sendDocument"), timeout=120,
                          data={"chat_id": env("TELEGRAM_CHAT_ID"), "caption": legenda[:1024]},
                          files={"document": (caminho.name, f)})
    _checar(r, "o arquivo")


def enviar_audio(caminho, legenda: str) -> None:
    with open(caminho, "rb") as f:
        r = requests.post(_url("sendAudio"), timeout=300,
                          data={"chat_id": env("TELEGRAM_CHAT_ID"), "caption": legenda[:1024], "title": legenda[:60]},
                          files={"audio": (Path(str(caminho)).name, f, "audio/mpeg")})
    _checar(r, "o áudio")


def ler_mensagens_novas() -> list[dict]:
    """Lê as mensagens recebidas desde a última leitura e as marca como lidas."""
    r = _checar(requests.get(_url("getUpdates"), params={"timeout": 0}, timeout=30), "a leitura de mensagens")
    updates = r.get("result", [])
    print(f"Mensagens novas no Telegram: {len(updates)}")
    if updates:  # confirma para o Telegram não mandar as mesmas de novo
        requests.get(_url("getUpdates"), params={"offset": updates[-1]["update_id"] + 1, "timeout": 0},
                     timeout=30)
    mensagens = []
    for u in updates:
        m = u.get("message") or u.get("edited_message")
        if m and m.get("text"):
            mensagens.append({"chat_id": str(m["chat"]["id"]), "texto": m["text"].strip()})
    return mensagens
