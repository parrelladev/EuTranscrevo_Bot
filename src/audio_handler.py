import os
import requests
import logging
import time
from typing import Optional, Tuple
from datetime import datetime
from replicate_client import ReplicateClient
from errors import ErrorHandler, FileError, APIError
from api_token import BOT_TOKEN

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AudioHandler:
    SUPPORTED_MIME_TYPES = {
        'audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/ogg',
        'audio/x-wav', 'audio/x-mpeg', 'audio/x-mp3'
    }
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
    RATE_LIMIT_WINDOW = 60  # 1 minuto
    MAX_REQUESTS_PER_WINDOW = 5

    def __init__(self, bot):
        self.bot = bot
        self.replicate_client = ReplicateClient()
        self.request_timestamps = {}
        self.temp_dir = self._setup_temp_dir()

    def _setup_temp_dir(self) -> str:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        temp_dir = os.path.join(script_dir, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir

    def _check_rate_limit(self, user_id: int) -> bool:
        current_time = time.time()
        user_requests = self.request_timestamps.get(user_id, [])
        
        # Remove timestamps antigos
        user_requests = [ts for ts in user_requests if current_time - ts < self.RATE_LIMIT_WINDOW]
        
        if len(user_requests) >= self.MAX_REQUESTS_PER_WINDOW:
            return False
        
        user_requests.append(current_time)
        self.request_timestamps[user_id] = user_requests
        return True

    def is_valid_audio_format(self, message) -> bool:
        if message.content_type == 'voice':
            return True
        elif message.content_type == 'audio':
            return message.audio.mime_type in self.SUPPORTED_MIME_TYPES
        elif message.content_type == 'document':
            return message.document.mime_type in self.SUPPORTED_MIME_TYPES
        return False

    def get_file_id(self, message) -> Optional[str]:
        try:
            if message.content_type == 'voice':
                return message.voice.file_id
            elif message.content_type == 'audio':
                return message.audio.file_id
            elif message.content_type == 'document':
                return message.document.file_id
            return None
        except Exception as e:
            logger.error(f"Erro ao obter file_id: {str(e)}")
            return None

    def download_file(self, file_url: str, file_path: str) -> Tuple[str, bool]:
        local_file_path = os.path.join(self.temp_dir, f"{int(time.time())}_{file_path.split('/')[-1]}")
        try:
            response = requests.get(file_url, timeout=30)
            response.raise_for_status()
            
            with open(local_file_path, 'wb') as f:
                f.write(response.content)
            return local_file_path, True
        except Exception as e:
            logger.error(f"Erro ao baixar arquivo: {str(e)}")
            if os.path.exists(local_file_path):
                os.remove(local_file_path)
            return "", False

    def process_audio(self, message):
        temp_file_path = None
        user_id = message.from_user.id
        
        try:
            # Verificar rate limit
            if not self._check_rate_limit(user_id):
                ErrorHandler.handle_rate_limit_error(self.bot, message)
                return

            # Validar formato do arquivo
            if not self.is_valid_audio_format(message):
                ErrorHandler.handle_format_validation_error(self.bot, message)
                return

            file_id = self.get_file_id(message)
            if not file_id:
                ErrorHandler.handle_file_reception_error(self.bot, message)
                return

            file_info = self.bot.get_file(file_id)
            if file_info.file_size > self.MAX_FILE_SIZE:
                ErrorHandler.handle_file_size_error(self.bot, message)
                return

            file_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}'
            
            # Enviar mensagem de feedback
            feedback_message = "⌛ Aguarde, estou transcrevendo seu áudio..."
            if file_info.file_size > 10 * 1024 * 1024:  # 10MB
                feedback_message += "\n\nComo o arquivo é grande, pode demorar alguns minutos."
            sent_message = self.bot.send_message(message.chat.id, feedback_message)

            try:
                if file_info.file_size > 10 * 1024 * 1024:
                    temp_file_path, success = self.download_file(file_url, file_info.file_path)
                    if not success:
                        raise FileError("Falha ao baixar arquivo")
                    output = self.replicate_client.transcribe_audio_file(temp_file_path)
                else:
                    output = self.replicate_client.transcribe_audio_url(file_url)

                transcription = self.get_transcription(output)
                self.send_transcription(message.chat.id, transcription)

            finally:
                # Limpar mensagem de feedback
                try:
                    self.bot.delete_message(message.chat.id, sent_message.message_id)
                except:
                    pass

        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de conexão: {str(e)}")
            ErrorHandler.handle_api_connection_error(self.bot, message)
        except APIError as e:
            logger.error(f"Erro da API: {str(e)}")
            ErrorHandler.handle_api_authentication_error(self.bot, message)
        except FileError as e:
            logger.error(f"Erro de arquivo: {str(e)}")
            ErrorHandler.handle_temp_file_error(self.bot, message)
        except Exception as e:
            logger.error(f"Erro desconhecido: {str(e)}")
            ErrorHandler.handle_unknown_error(self.bot, message)
        finally:
            # Limpar arquivos temporários
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except Exception as e:
                    logger.error(f"Erro ao remover arquivo temporário: {str(e)}")

    def get_transcription(self, output: dict) -> str:
        try:
            return ''.join(segment['text'] for segment in output['segments'])
        except Exception as e:
            logger.error(f"Erro ao processar transcrição: {str(e)}")
            raise APIError("Falha ao processar resultado da transcrição")

    def send_transcription(self, chat_id: int, transcription: str):
        max_length = 4000
        try:
            for i in range(0, len(transcription), max_length):
                chunk = transcription[i:i + max_length]
                self.bot.send_message(chat_id, chunk)
        except Exception as e:
            logger.error(f"Erro ao enviar transcrição: {str(e)}")
            raise APIError("Falha ao enviar transcrição")