import os
import requests
import logging
import time
import subprocess
import tempfile
from typing import Optional, Tuple
from datetime import datetime
from replicate_client import ReplicateClient
from errors import ErrorHandler, FileError, APIError
from api_token import BOT_TOKEN
from config import AUDIO_OPTIMIZATION, RATE_LIMIT, FILE, LOGGING

# Configuração do logging
logging.basicConfig(
    level=getattr(logging, LOGGING['LEVEL']),
    format=LOGGING['FORMAT'],
    handlers=[
        logging.FileHandler(LOGGING['FILE']),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AudioOptimizer:
    """
    Classe para otimizar áudio antes da transcrição, acelerando o áudio
    para reduzir custos e tempo de processamento"
    """
    
    def __init__(self, speed_multiplier: float = None, bitrate: str = None, volume_multiplier: float = None):
        self.speed_multiplier = speed_multiplier or AUDIO_OPTIMIZATION['SPEED_MULTIPLIER']
        self.bitrate = bitrate or AUDIO_OPTIMIZATION['BITRATE']
        self.volume_multiplier = volume_multiplier or AUDIO_OPTIMIZATION.get('VOLUME_MULTIPLIER', 1.0)
        
    def _check_ffmpeg_available(self) -> bool:
        """Verifica se o ffmpeg está disponível no sistema"""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def optimize_audio(self, input_path: str, output_path: str) -> bool:
        """
        Acelera o áudio usando ffmpeg para reduzir custos de transcrição
        
        Args:
            input_path: Caminho do arquivo de áudio original
            output_path: Caminho onde salvar o áudio otimizado
            
        Returns:
            bool: True se a otimização foi bem-sucedida, False caso contrário
        """
        if not self._check_ffmpeg_available():
            logger.warning("ffmpeg não encontrado. Usando áudio original.")
            return False
            
        try:
            filter_str = f'volume={self.volume_multiplier},atempo={self.speed_multiplier}'
            cmd = [
                'ffmpeg',
                '-i', input_path,
                '-filter:a', filter_str,
                '-ac', '1',
                '-b:a', self.bitrate,
                '-y',
                output_path
            ]
            
            logger.info(f"Otimizando áudio: {input_path} -> {output_path} (volume: {self.volume_multiplier}x, velocidade: {self.speed_multiplier}x)")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=AUDIO_OPTIMIZATION['FFMPEG_TIMEOUT']
            )
            
            if result.returncode == 0:
                # Verificar se o arquivo foi criado e tem tamanho > 0
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    original_size = os.path.getsize(input_path)
                    optimized_size = os.path.getsize(output_path)
                    reduction = ((original_size - optimized_size) / original_size) * 100
                    
                    logger.info(f"Áudio otimizado com sucesso. "
                              f"Tamanho original: {original_size/1024:.1f}KB, "
                              f"Otimizado: {optimized_size/1024:.1f}KB, "
                              f"Redução: {reduction:.1f}%")
                    return True
                else:
                    logger.error("Arquivo otimizado não foi criado ou está vazio")
                    return False
            else:
                logger.error(f"Erro no ffmpeg: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Timeout ao otimizar áudio com ffmpeg")
            return False
        except Exception as e:
            logger.error(f"Erro inesperado ao otimizar áudio: {str(e)}")
            return False

class AudioHandler:
    SUPPORTED_MIME_TYPES = FILE['SUPPORTED_MIME_TYPES']
    MAX_FILE_SIZE = FILE['MAX_SIZE']
    RATE_LIMIT_WINDOW = RATE_LIMIT['WINDOW']
    MAX_REQUESTS_PER_WINDOW = RATE_LIMIT['MAX_REQUESTS']

    def __init__(self, bot):
        self.bot = bot
        self.replicate_client = ReplicateClient()
        self.audio_optimizer = AudioOptimizer() if AUDIO_OPTIMIZATION['ENABLED'] else None
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

    def _optimize_audio_file(self, file_path: str) -> Tuple[str, bool]:
        """
        Otimiza o arquivo de áudio acelerando-o para reduzir custos
        
        Args:
            file_path: Caminho do arquivo original
            
        Returns:
            Tuple[str, bool]: (caminho do arquivo otimizado, sucesso)
        """
        # Verificar se a otimização está habilitada
        if not self.audio_optimizer:
            return file_path, False
            
        # Verificar se o arquivo é grande o suficiente para se beneficiar da otimização
        file_size = os.path.getsize(file_path)
        if file_size < AUDIO_OPTIMIZATION['MIN_FILE_SIZE_FOR_OPTIMIZATION']:
            logger.info(f"Arquivo muito pequeno ({file_size/1024:.1f}KB), pulando otimização")
            return file_path, False
            
        try:
            # Criar nome para arquivo otimizado
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            optimized_path = os.path.join(self.temp_dir, f"{base_name}_optimized.mp3")
            
            # Tentar otimizar o áudio
            if self.audio_optimizer.optimize_audio(file_path, optimized_path):
                return optimized_path, True
            else:
                # Se falhar, usar arquivo original
                logger.warning("Falha na otimização, usando arquivo original")
                return file_path, False
                
        except Exception as e:
            logger.error(f"Erro ao otimizar áudio: {str(e)}")
            return file_path, False

    def process_audio(self, message):
        temp_file_path = None
        optimized_file_path = None
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
                    # Baixar arquivo grande
                    temp_file_path, success = self.download_file(file_url, file_info.file_path)
                    if not success:
                        raise FileError("Falha ao baixar arquivo")
                    
                    # Otimizar áudio antes da transcrição
                    optimized_file_path, was_optimized = self._optimize_audio_file(temp_file_path)
                    
                    # Usar arquivo otimizado para transcrição
                    output = self.replicate_client.transcribe_audio_file(optimized_file_path)
                else:
                    # Para arquivos pequenos, tentar otimizar via URL
                    # Primeiro baixar, otimizar e depois enviar
                    temp_file_path, success = self.download_file(file_url, file_info.file_path)
                    if not success:
                        raise FileError("Falha ao baixar arquivo")
                    
                    # Otimizar áudio
                    optimized_file_path, was_optimized = self._optimize_audio_file(temp_file_path)
                    
                    # Usar arquivo otimizado para transcrição
                    output = self.replicate_client.transcribe_audio_file(optimized_file_path)

                transcription = self.get_transcription(output)
                
                # Adicionar informação sobre otimização na resposta
                if was_optimized:
                    transcription = f"{transcription}"
                
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
            for file_path in [temp_file_path, optimized_file_path]:
                if file_path and os.path.exists(file_path):
                    try:
                        os.remove(file_path)
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