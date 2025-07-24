# commands/codigo_projeto.py

"""
🛠️ MÓDULO DO GITHUB

Envia mensagem personalizada com o link do código aberto do projeto.
"""

def responder_codigo_projeto(bot, message):
    try:
        first_name = message.from_user.first_name or "amigo"
        texto_resposta = (
            f"*{first_name}, quer rodar este projeto também?* 🤔\n\n"
            f"É só clicar no link abaixo:\n"
            f"[🔗 Acessar código no GitHub](https://github.com/parrelladev/EuTranscrevo_Bot)"
        )
        bot.send_message(
            message.chat.id,
            texto_resposta,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"❌ Erro ao responder código do projeto: {e}")
        bot.reply_to(message, "Erro ao enviar o link do projeto.")
