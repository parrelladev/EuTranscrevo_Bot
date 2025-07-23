"""
📝 MÓDULO DE TRANSCRIÇÃO DE ÁUDIO - TELEGRAM

Autor: parrelladev
"""

import os
import time

from config import AUDIO, MESSAGES
from services.audio_pipeline import processar_audio
from utils.file_utils import ensure_directory_exists

def transcrever(bot, message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')

        # Identifica o arquivo da mensagem
        file_id = (
            message.voice.file_id if message.voice else
            message.audio.file_id if message.audio else
            message.video.file_id if message.content_type == "video" else
            message.video_note.file_id if message.content_type == "video_note" else
            message.document.file_id if message.content_type == "document" else
            None
        )

        if not file_id:
            bot.reply_to(message, "⚠️ Mídia não suportada.")
            return

        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)

        # Prepara diretório e nomes
        temp_dir = os.path.join(os.getcwd(), AUDIO['tempDir'])
        ensure_directory_exists(temp_dir)

        timestamp = str(int(time.time() * 1000))
        ext = "mp4" if message.content_type in ["video", "video_note"] else "mp3"
        original_path = os.path.join(temp_dir, f"{timestamp}_original.{ext}")

        # Salva o arquivo
        with open(original_path, 'wb') as f:
            f.write(downloaded_file)

        # Mensagem temporária enquanto transcreve
        status_msg = bot.send_message(message.chat.id, "⌛️ Aguarde, estou transcrevendo seu áudio...")

        # 🔁 Usa pipeline reutilizável
        transcript = processar_audio(original_path)

        # Resposta e limpeza
        bot.delete_message(message.chat.id, status_msg.message_id)
        bot.reply_to(message, f"{transcript}")

    except Exception as e:
        print("❌ Erro ao transcrever:", e)
        bot.reply_to(message, MESSAGES['audioError'])
