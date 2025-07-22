"""
📝 MÓDULO DE TRANSCRIÇÃO DE ÁUDIO - TELEGRAM

1. Baixa o áudio da mensagem
2. Salva temporariamente
3. Otimiza com ffmpeg
4. Envia para a API Replicate
5. Retorna a transcrição
6. Limpa arquivos temporários

Autor: parrelladev
"""

"""
📝 MÓDULO DE TRANSCRIÇÃO DE ÁUDIO - TELEGRAM

1. Baixa o áudio da mensagem
2. Salva temporariamente
3. Otimiza com ffmpeg
4. Envia para a API Replicate
5. Retorna a transcrição
6. Limpa arquivos temporários

Autor: parrelladev
"""

import os
import time
import mimetypes

from config import AUDIO, SECURITY, MESSAGES, DEVELOPMENT
from services.audio_optimizer import optimize_audio
from services.replicate_client import transcribe_audio
from utils.file_utils import generate_unique_file_name, ensure_directory_exists, get_file_size

# 🔍 Função auxiliar para logs verbosos
def log(msg):
    if DEVELOPMENT.get('enableVerboseLogs'):
        print(msg)

def transcrever(bot, message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')

        file_id = (
            message.voice.file_id if message.voice else
            message.audio.file_id if message.audio else
            message.video.file_id if message.video else
            message.video_note.file_id if message.video_note else
            message.document.file_id if message.document else
            None
        )

        if not file_id:
            bot.reply_to(message, "⚠️ Mídia não suportada.")
            return

        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)

        temp_dir = os.path.join(os.getcwd(), AUDIO['tempDir'])
        ensure_directory_exists(temp_dir)

        timestamp = str(int(time.time() * 1000))

        if message.video_note:
            ext = "mp4"
        elif message.video:
            ext = "mp4"
        elif message.document:
            ext = message.document.file_name.split('.')[-1] or "mp3"
        else:
            ext = AUDIO['optimization']['format']

        original_path = os.path.join(temp_dir, f"{timestamp}_original.{ext}")
        optimized_path = os.path.join(temp_dir, f"{timestamp}_optimized.mp3")

        with open(original_path, 'wb') as f:
            f.write(downloaded_file)
        log(f"📥 Áudio salvo: {original_path}")

        status_msg = bot.send_message(message.chat.id, "⌛️ Aguarde, estou transcrevendo seu áudio...")

        mime, _ = mimetypes.guess_type(original_path)
        log(f"🔍 Tipo MIME detectado: {mime}")

        if not DEVELOPMENT['skipFileTypeValidation']:
            if not mime or mime not in SECURITY['allowedAudioTypes']:
                log(f"❌ Tipo de áudio não permitido: {mime}")
                os.remove(original_path)
                bot.reply_to(message, MESSAGES['invalidFile'])
                return
            log("✅ Tipo de arquivo válido.")
        else:
            log("⚠️ Validação de tipo desativada (modo debug)")

        size = get_file_size(original_path)
        log(f"📏 Tamanho do arquivo: {size / 1024 / 1024:.2f} MB")
        if size > SECURITY['maxFileSize']:
            os.remove(original_path)
            bot.reply_to(message, "⚠️ Arquivo muito grande. Tamanho máximo: 50MB")
            return

        log("🎛️ Otimizando áudio...")
        optimize_audio(original_path, optimized_path)

        transcript = transcribe_audio(optimized_path)
        transcript = transcript.strip() if transcript else MESSAGES['audioError']

        bot.delete_message(message.chat.id, status_msg.message_id)
        bot.reply_to(message, f"{transcript}")
        log("✅ Transcrição enviada.")

        os.remove(original_path)
        os.remove(optimized_path)

    except Exception as e:
        print("❌ Erro ao processar áudio:", e)
        bot.reply_to(message, MESSAGES['audioError'])