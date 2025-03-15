class BotError(Exception):
    """Classe base para exceções do bot"""
    pass

class APIError(BotError):
    """Exceções relacionadas a APIs externas"""
    pass

class FileError(BotError):
    """Exceções relacionadas a manipulação de arquivos"""
    pass

class ErrorHandler:
    @staticmethod
    def handle_bot_token_error(bot, message):
        if message:
            bot.send_message(message.chat.id, "Houve um problema ao iniciar o bot. Por favor, verifique o token do bot e tente novamente.")

    @staticmethod
    def handle_file_reception_error(bot, message):
        bot.send_message(message.chat.id, "Não foi possível receber o arquivo de áudio. Por favor, tente enviar novamente.")

    @staticmethod
    def handle_unsupported_file_type_error(bot, message):
        bot.send_message(message.chat.id, "Este tipo de arquivo de áudio não é suportado. Tente convertê-lo para um formato compatível (por exemplo, .mp3 ou .wav).")

    @staticmethod
    def handle_file_size_error(bot, message):
        bot.send_message(message.chat.id, "O arquivo de áudio é muito grande para ser processado. Por favor, envie um arquivo menor.")

    @staticmethod
    def handle_api_connection_error(bot, message):
        bot.send_message(message.chat.id, "Houve um problema ao conectar-se à API de transcrição. Por favor, tente novamente mais tarde.")

    @staticmethod
    def handle_api_authentication_error(bot, message):
        bot.send_message(message.chat.id, "Erro de autenticação ao acessar o serviço de transcrição. Por favor, verifique a configuração do token de API.")

    @staticmethod
    def handle_audio_processing_error(bot, message):
        bot.send_message(message.chat.id, "Ocorreu um erro ao processar o áudio. Por favor, tente novamente.")

    @staticmethod
    def handle_unknown_error(bot, message):
        bot.send_message(message.chat.id, "Algo deu errado. Por favor, tente novamente.")

    @staticmethod
    def handle_timeout_error(bot, message):
        bot.send_message(message.chat.id, "O tempo de processamento excedeu o limite. Por favor, tente novamente.")

    @staticmethod
    def handle_format_validation_error(bot, message):
        bot.send_message(message.chat.id, "O formato do arquivo não pôde ser validado. Certifique-se de enviar um arquivo de áudio válido.")

    @staticmethod
    def handle_temp_file_error(bot, message):
        bot.send_message(message.chat.id, "Erro ao manipular arquivo temporário. Por favor, tente novamente.")

    @staticmethod
    def handle_rate_limit_error(bot, message):
        bot.send_message(message.chat.id, "Muitas solicitações em um curto período. Por favor, aguarde alguns minutos antes de tentar novamente.")