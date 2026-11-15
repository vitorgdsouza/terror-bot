"""Comunicação com o Telegram: mensagens, vídeo e leitura de comandos."""
import requests

from .util import env

API = "https://api.telegram.org/bot{token}/{metodo}"


def _url(metodo: str) -> str:
    return API.format(token=env("TELEGRAM_BOT_TOKEN"), metodo=metodo)


def enviar_mensagem(texto: str, chat_id: str | None = None) -> None:
    chat_id = chat_id or env("TELEGRAM_CHAT_ID")
    for i in range(0, len(texto), 4000):  # limite do Telegram por mensagem
        requests.post(_url("sendMessage"), timeout=30,
                      data={"chat_id": chat_id, "text": texto[i:i + 4000]})


def enviar_video(caminho, legenda: str) -> None:
    with open(caminho, "rb") as f:
        r = requests.post(_url("sendVideo"), timeout=300,
                          data={"chat_id": env("TELEGRAM_CHAT_ID"), "caption": legenda[:1024],
                                "supports_streaming": "true", "width": 1080, "height": 1920},
                          files={"video": ("video.mp4", f, "video/mp4")})
    if not r.ok:
        raise RuntimeError(f"Telegram recusou o vídeo: {r.text[:300]}")


def ler_mensagens_novas() -> list[dict]:
    """Lê as mensagens recebidas desde a última leitura e as marca como lidas."""
    r = requests.get(_url("getUpdates"), params={"timeout": 0}, timeout=30).json()
    updates = r.get("result", [])
    if updates:  # confirma para o Telegram não mandar as mesmas de novo
        requests.get(_url("getUpdates"), params={"offset": updates[-1]["update_id"] + 1, "timeout": 0},
                     timeout=30)
    mensagens = []
    for u in updates:
        m = u.get("message") or u.get("edited_message")
        if m and m.get("text"):
            mensagens.append({"chat_id": str(m["chat"]["id"]), "texto": m["text"].strip()})
    return mensagens
