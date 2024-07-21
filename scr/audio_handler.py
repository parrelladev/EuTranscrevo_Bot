import os
import requests
from replicate_client import ReplicateClient
from errors import handle_unsupported_file_type_error, handle_unknown_error
from api_token import BOT_TOKEN

class AudioHandler:
    def __init__(self, bot):
        self.bot = bot
        self.replicate_client = ReplicateClient()

    def process_audio(self, message):
        try:
            file_id = self.get_file_id(message)
            if not file_id:
                handle_unsupported_file_type_error(self.bot, message)
                return

            file_info = self.bot.get_file(file_id)
            file_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}'
            file_size = file_info.file_size

            feedback_message = self.get_feedback_message(file_size)
            sent_message = self.bot.send_message(message.chat.id, feedback_message)

            if file_size > 19 * 1024 * 1024:
                file_path = self.download_file(file_url, file_info.file_path)
                output = self.replicate_client.transcribe_audio_file(file_path)
                os.remove(file_path)
            else:
                output = self.replicate_client.transcribe_audio_url(file_url)

            transcription = self.get_transcription(output)
            self.send_transcription(message.chat.id, transcription)
            self.bot.delete_message(message.chat.id, sent_message.message_id)
        
        except Exception as e:
            print(f"Error: {e}")
            handle_unknown_error(self.bot, message)

    def get_file_id(self, message):
        if message.content_type == 'voice':
            return message.voice.file_id
        elif message.content_type == 'audio':
            return message.audio.file_id
        elif message.content_type == 'document' and message.document.mime_type.startswith('audio/'):
            return message.document.file_id
        return None

    def get_feedback_message(self, file_size):
        if file_size > 19 * 1024 * 1024:
            return "⌛ Aguarde, estou transcrevendo seu áudio. \n \n Como o arquivo é grande, pode demorar alguns minutos."
        return "⌛ Aguarde, estou transcrevendo seu áudio..."

    def download_file(self, file_url, file_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        temp_dir = os.path.join(script_dir, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        file_data = requests.get(file_url)
        local_file_path = os.path.join(temp_dir, file_path.split('/')[-1])
        with open(local_file_path, 'wb') as f:
            f.write(file_data.content)
        return local_file_path

    def get_transcription(self, output):
        return ''.join(segment['text'] for segment in output['segments'])

    def send_transcription(self, chat_id, transcription):
        max_length = 4000
        for i in range(0, len(transcription), max_length):
            self.bot.send_message(chat_id, transcription[i:i + max_length])