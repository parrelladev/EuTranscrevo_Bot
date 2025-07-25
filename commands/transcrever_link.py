"""
🔗 TRANSCRIÇÃO DE LINKS COM ÁUDIO

Este módulo detecta links em mensagens, baixa o áudio com yt-dlp
e reutiliza a mesma pipeline de transcrição usada para áudios do Telegram.

Autor: parrelladev
"""

import os
import time
import re
import subprocess

from config import AUDIO, MESSAGES
from services.audio_pipeline import processar_audio
from services.messaging import enviar_mensagem_dividida
from utils.file_utils import ensure_directory_exists

# Regex simples para capturar URLs
URL_REGEX = re.compile(r'(https?://[^\s]+)')

def log(msg):
    from config import DEVELOPMENT
    if DEVELOPMENT.get('enableVerboseLogs'):
        print(msg)

def baixar_audio(link, output_path_template):
    """
    Usa yt-dlp para baixar e converter o áudio do link para MP3.
    """
    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--output", output_path_template,
        link
    ]
    log(f"▶️ Executando: {' '.join(command)}")
    subprocess.run(command, check=True)

def transcrever_link(bot, message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')

        match = URL_REGEX.search(message.text)
        if not match:
            bot.reply_to(message, "❌ Nenhum link válido encontrado.")
            return

        url = match.group(0)
        log(f"🔗 Link detectado: {url}")

        temp_dir = os.path.join(os.getcwd(), AUDIO['tempDir'])
        ensure_directory_exists(temp_dir)

        timestamp = str(int(time.time() * 1000))
        raw_template = os.path.join(temp_dir, f"{timestamp}_original.%(ext)s")
        downloaded_path = os.path.join(temp_dir, f"{timestamp}_original.mp3")

        # Mensagem de status
        status_msg = bot.send_message(message.chat.id, "⏬ Baixando áudio do link...")

        # Baixa e converte para MP3
        baixar_audio(url, raw_template)

        # Confirma se foi baixado
        if not os.path.exists(downloaded_path):
            bot.edit_message_text("❌ Falha ao baixar o áudio.", message.chat.id, status_msg.message_id)
            return

        # Chama pipeline reutilizável
        bot.edit_message_text("⌛️ Transcrevendo áudio...", message.chat.id, status_msg.message_id)
        transcript = processar_audio(downloaded_path)

        bot.delete_message(message.chat.id, status_msg.message_id)
        enviar_mensagem_dividida(bot, message.chat.id, transcript, reply_to_id=message.message_id)
        log("✅ Transcrição enviada.")

    except subprocess.CalledProcessError as e:
        print("❌ Erro ao baixar com yt-dlp:", e)
        bot.reply_to(message, "❌ Não consegui baixar o áudio desse link.")
    except Exception as e:
        print("❌ Erro ao processar link:", e)
        error_msg = str(e)
        if "ultrapassa o limite" in error_msg:
            bot.reply_to(message, MESSAGES['fileTooLarge'])
        else:
            bot.reply_to(message, MESSAGES['audioError'])
