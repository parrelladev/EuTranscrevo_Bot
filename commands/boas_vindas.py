"""
👋 MÓDULO DE BOAS-VINDAS

Envia mensagem personalizada de boas-vindas para usuários fora de grupo.
"""

def boas_vindas(bot, message):
    # Apenas envia boas-vindas em mensagens privadas (não em grupos)
    if message.chat.type == "private":
        first_name = message.from_user.first_name or "amigo"
        bot.send_message(
            message.chat.id,
            f"🎙️ Olá, {first_name}! Mande um áudio, vídeo ou link para que eu possa transcrever."
        )
