import telebot
import logging
import time
from audio_handler import AudioHandler
from errors import ErrorHandler, BotError

# Configuração do logging
logger = logging.getLogger(__name__)

class Bot:
    MAX_RETRIES = 5
    RETRY_DELAY = 10  # segundos

    def __init__(self, token):
        try:
            self.token = token
            self.bot = telebot.TeleBot(token)
            self.audio_handler = None
            self.setup_handlers()
            logger.info("Bot inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar o bot: {str(e)}")
            raise BotError("Falha ao inicializar o bot")

    def setup_handlers(self):
        try:
            self.audio_handler = AudioHandler(self.bot)

            @self.bot.message_handler(content_types=['text'])
            def send_welcome(message):
                try:
                    user_name = message.from_user.first_name
                    self.bot.send_message(
                        message.chat.id,
                        f"🎙️ Olá, {user_name}! Mande um áudio para que eu possa transcrever."
                    )
                except Exception as e:
                    logger.error(f"Erro ao enviar mensagem de boas-vindas: {str(e)}")
                    ErrorHandler.handle_unknown_error(self.bot, message)

            @self.bot.message_handler(content_types=['voice', 'audio', 'document'])
            def handle_audio(message):
                try:
                    self.audio_handler.process_audio(message)
                except Exception as e:
                    logger.error(f"Erro ao processar áudio: {str(e)}")
                    ErrorHandler.handle_unknown_error(self.bot, message)

            logger.info("Handlers configurados com sucesso")
        except Exception as e:
            logger.error(f"Erro ao configurar handlers: {str(e)}")
            raise BotError("Falha ao configurar handlers do bot")

    def start(self):
        retry_count = 0
        while retry_count < self.MAX_RETRIES:
            try:
                logger.info("Iniciando o bot...")
                self.bot.polling(none_stop=True, timeout=60)
            except Exception as e:
                retry_count += 1
                logger.error(f"Erro na execução do bot (tentativa {retry_count}/{self.MAX_RETRIES}): {str(e)}")
                
                if retry_count < self.MAX_RETRIES:
                    logger.info(f"Tentando reconectar em {self.RETRY_DELAY} segundos...")
                    time.sleep(self.RETRY_DELAY)
                else:
                    logger.critical("Número máximo de tentativas excedido. Encerrando o bot.")
                    raise BotError("Falha ao manter o bot em execução após várias tentativas")