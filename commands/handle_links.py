import os
import time
import re
import mimetypes
import subprocess

from config import AUDIO, SECURITY, MESSAGES, DEVELOPMENT
from services.audio_optimizer import optimize_audio
from services.replicate_client import transcribe_audio
from utils.file_utils import generate_unique_file_name, ensure_directory_exists, get_file_size

# Regex simples para detectar links
URL_REGEX = re.compile(r'(https?://[^\s]+)')

def log(msg):
    if DEVELOPMENT.get('enableVerboseLogs'):
        print(msg)

def baixar_audio(link, output_path):
    """Usa yt-dlp para baixar o áudio em .mp3"""
    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--output", output_path,
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
        raw_audio_path = os.path.join(temp_dir, f"{timestamp}_original.%(ext)s")
        downloaded_mp3_path = os.path.join(temp_dir, f"{timestamp}_original.mp3")
        optimized_path = os.path.join(temp_dir, f"{timestamp}_optimized.mp3")

        status_msg = bot.send_message(message.chat.id, "⏬ Baixando áudio do link...")

        baixar_audio(url, raw_audio_path)

        if not os.path.exists(downloaded_mp3_path):
            bot.reply_to(message, "❌ Falha ao baixar o áudio.")
            return

        mime, _ = mimetypes.guess_type(downloaded_mp3_path)
        log(f"🔍 Tipo MIME detectado: {mime}")

        if not DEVELOPMENT['skipFileTypeValidation']:
            if not mime or mime not in SECURITY['allowedAudioTypes']:
                log(f"❌ Tipo de áudio não permitido: {mime}")
                os.remove(downloaded_mp3_path)
                bot.reply_to(message, MESSAGES['invalidFile'])
                return
        else:
            log("⚠️ Validação de tipo desativada (modo debug)")

        size = get_file_size(downloaded_mp3_path)
        log(f"📏 Tamanho do arquivo: {size / 1024 / 1024:.2f} MB")
        if size > SECURITY['maxFileSize']:
            os.remove(downloaded_mp3_path)
            bot.reply_to(message, "⚠️ Arquivo muito grande. Máximo permitido: 50MB")
            return

        bot.edit_message_text("🎧 Otimizando áudio...", message.chat.id, status_msg.message_id)
        optimize_audio(downloaded_mp3_path, optimized_path)

        transcript = transcribe_audio(optimized_path)
        transcript = transcript.strip() if transcript else MESSAGES['audioError']

        bot.edit_message_text(transcript, message.chat.id, status_msg.message_id)
        log("✅ Transcrição enviada.")

        os.remove(downloaded_mp3_path)
        os.remove(optimized_path)

    except subprocess.CalledProcessError as e:
        print("❌ Erro ao baixar com yt-dlp:", e)
        bot.reply_to(message, "❌ Não consegui baixar o áudio desse link.")
    except Exception as e:
        print("❌ Erro ao processar link:", e)
        bot.reply_to(message, MESSAGES['audioError'])
