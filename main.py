# main.py
"""
🤖 BOT DE TRANSCRIÇÃO DE ÁUDIO PARA TELEGRAM

- Conecta ao Telegram via pyTelegramBotAPI
- Processa mensagens recebidas
- Roteia comandos e áudios para as funções apropriadas

Autor: parrelladev
Versão: 1.0.0
"""

import os
import sys

# Adiciona a raiz do projeto ao sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

import telebot
from config import TELEGRAM_TOKEN, MESSAGES

# Comandos
from commands.transcrever import transcrever
from commands.boas_vindas import boas_vindas

# Inicializa o bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Handler de texto
@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        boas_vindas(bot, message)
    except Exception as e:
        print("Erro ao processar texto:", e)
        bot.reply_to(message, MESSAGES['error'])

# Handler de voz, áudio, vídeo, documento
@bot.message_handler(content_types=['voice', 'audio', 'video', 'video_note', 'document'])
def handle_audio_or_video(message):
    try:
        print("🎧 Mídia recebida!")
        transcrever(bot, message)
    except Exception as e:
        print("Erro ao processar mídia:", e)
        bot.reply_to(message, MESSAGES['audioError'])

# Inicializa o bot
if __name__ == "__main__":
    print("✅ Bot iniciado!")
    print(MESSAGES['welcome'])
    bot.infinity_polling()
