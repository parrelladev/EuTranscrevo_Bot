# main.py
"""
🤖 BOT DE TRANSCRIÇÃO DE ÁUDIO PARA TELEGRAM
Autor: parrelladev
Versão: 1.0.0
"""

import os
import sys
import re
import telebot

# Ajuste do path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

from config import TELEGRAM_TOKEN, MESSAGES, COMMANDS
from commands.transcrever import transcrever
from commands.boas_vindas import boas_vindas
from commands.transcrever_link import transcrever_link
from commands.donate import responder_doacao
from commands.codigo_projeto import responder_codigo_projeto

# Regex para detectar links
URL_REGEX = re.compile(r"(https?://[^\s]+)")

# Inicializa o bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)


# Handler de mensagens de doação
@bot.message_handler(commands=["pix", "donate"])
def handle_donate(message):
    responder_doacao(bot, message)


# Handler de código fonte - Github
@bot.message_handler(commands=["codigo", "projeto"])
def handle_codigo_projeto(message):
    responder_codigo_projeto(bot, message)


# Handler de link externo
@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        texto = message.text.strip()
        print(f"📨 Texto recebido: {repr(texto)}")

        if URL_REGEX.search(texto):
            print("🔗 Link detectado, iniciando transcrição via link...")
            transcrever_link(bot, message)
        else:
            print("👋 Mensagem padrão recebida, chamando boas_vindas...")
            boas_vindas(bot, message)
    except Exception as e:
        print("❌ Erro ao processar texto:", e)
        bot.reply_to(message, MESSAGES["error"])


# Handler para voz, áudio, vídeo, vídeo curto e documentos
@bot.message_handler(
    content_types=["voice", "audio", "video", "video_note", "document"]
)
def handle_media(message):
    try:
        print(f"🎧 Mídia recebida: {message.content_type}")
        transcrever(bot, message)
    except Exception as e:
        print("❌ Erro ao processar mídia:", e)
        bot.reply_to(message, MESSAGES["audioError"])


# Inicializa o bot
if __name__ == "__main__":
    print("✅ Bot iniciado!")
    print(MESSAGES["welcome"])
    bot.infinity_polling()
