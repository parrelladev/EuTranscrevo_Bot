"""Utilities for sending long messages via Telegram."""

from typing import Optional


def enviar_mensagem_dividida(bot, chat_id: int, texto: str, limite: int = 3500, reply_to_id: Optional[int] = None) -> None:
    """Send a long message in chunks respecting Telegram limits."""
    partes = [texto[i:i+limite] for i in range(0, len(texto), limite)]
    for idx, parte in enumerate(partes):
        if idx == 0 and reply_to_id is not None:
            bot.send_message(chat_id, parte, reply_to_message_id=reply_to_id)
        else:
            bot.send_message(chat_id, parte)

