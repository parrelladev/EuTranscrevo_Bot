"""
📝 MÓDULO DE TRANSCRIÇÃO DE ÁUDIO - TELEGRAM

Autor: parrelladev
"""

import os
import time
from telebot.apihelper import ApiTelegramException

from config import AUDIO, MESSAGES
from services.audio_pipeline import processar_audio
from services.messaging import enviar_mensagem_dividida
from utils.file_utils import ensure_directory_exists

def transcrever(bot, message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')

        file_id = (
            message.voice.file_id if message.voice else
            message.audio.file_id if message.audio else
            message.video.file_id if message.content_type == "video" else
            message.video_note.file_id if message.content_type == "video_note" else
            message.document.file_id if message.content_type == "document" else
            None
        )

        if not file_id:
            bot.reply_to(message, MESSAGES['unsupportedMedia'])
            return

        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)

        temp_dir = os.path.join(os.getcwd(), AUDIO['tempDir'])
        ensure_directory_exists(temp_dir)

        timestamp = str(int(time.time() * 1000))
        ext = "mp4" if message.content_type in ["video", "video_note"] else "mp3"
        original_path = os.path.join(temp_dir, f"{timestamp}_original.{ext}")

        with open(original_path, 'wb') as f:
            f.write(downloaded_file)

        status_msg = bot.send_message(message.chat.id, "⌛️ Aguarde, estou transcrevendo seu áudio...")

        transcript = processar_audio(original_path)

        bot.delete_message(message.chat.id, status_msg.message_id)

        enviar_mensagem_dividida(bot, message.chat.id, transcript, reply_to_id=message.message_id)

    except ApiTelegramException as api_err:
        print("⚠️ Erro API Telegram:", api_err)
        bot.reply_to(message, MESSAGES['fileTooLarge'])
    except Exception as e:
        print("❌ Erro ao transcrever:", e)
        if "Replicate" in str(e):
            bot.reply_to(message, MESSAGES['slowProcessing'])
        else:
            bot.reply_to(message, MESSAGES['audioError'])
