class error:
    def handle_bot_token_error(bot, message):
        bot.send_message(message.chat.id, "Houve um problema ao iniciar o bot. Por favor, verifique o token do bot e tente novamente.")

    def handle_file_reception_error(bot, message):
        bot.send_message(message.chat.id, "Não foi possível receber o arquivo de áudio. Por favor, tente enviar novamente.")

    def handle_unsupported_file_type_error(bot, message):
        bot.send_message(message.chat.id, "Este tipo de arquivo de áudio não é suportado. Tente convertê-lo para um formato compatível (por exemplo, .mp3 ou .wav).")

    def handle_file_size_error(bot, message):
        bot.send_message(message.chat.id, "O arquivo de áudio é muito grande para ser processado. Por favor, envie um arquivo menor.")

    def handle_api_connection_error(bot, message):
        bot.send_message(message.chat.id, "Houve um problema ao conectar-se à API de transcrição. Por favor, tente novamente mais tarde.")

    def handle_api_authentication_error(bot, message):
        bot.send_message(message.chat.id, "Erro de autenticação ao acessar o serviço de transcrição. Por favor, verifique a configuração do token de API.")

    def handle_audio_processing_error(bot, message):
        bot.send_message(message.chat.id, "Ocorreu um erro ao processar o áudio. Por favor, tente novamente.")

    def handle_unknown_error(bot, message):
        bot.send_message(message.chat.id, "Algo deu errado. Por favor, tente novamente.")