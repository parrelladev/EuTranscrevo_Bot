# commands/donate.py

"""
💸 MÓDULO DE DOAÇÃO

Envia mensagem personalizada orientando como a pessoa pode fazer uma doação.
"""

def responder_doacao(bot, message):
    if message.chat.type == "private":
        first_name = message.from_user.first_name or "amigo"
        bot.send_message(
            message.chat.id,
            f"😁 Fico feliz que você esteja interessado em apoiar o projeto, {first_name}!\n\n"
            f"*Faça uma doação via PIX para:*\n`28992781495`",
            parse_mode="Markdown"
        )
