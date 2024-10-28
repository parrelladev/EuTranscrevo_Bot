import telebot
from audio_handler import AudioHandler

class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.setup_handlers()

    def setup_handlers(self):
        @self.bot.message_handler(content_types=['text'])
        def send_welcome(message):
            user_name = message.from_user.first_name
            self.bot.send_message(message.chat.id, f"🎙️ Olá, {user_name}! Mande um áudio para que eu possa transcrever.")

        @self.bot.message_handler(content_types=['voice', 'audio', 'document'])
        def handle_audio(message):
            audio_handler = AudioHandler(self.bot)
            audio_handler.process_audio(message)

    def start(self):
        self.bot.polling()