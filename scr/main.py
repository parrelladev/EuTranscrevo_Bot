import replicate
import telebot
import requests
import errors
import os
from APIs import BOT_TOKEN, REPLICATE_OPENAI_RUN, REPLICATE_API_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(content_types=['text'])
def send_welcome(message):
    bot.send_message(message.chat.id, "🎙️ Olá! Mande um áudio para que eu possa transcrever.")

@bot.message_handler(content_types=['voice', 'audio', 'document'])
def handle_audio(message):
    try:
        if message.content_type == 'voice':
            file_id = message.voice.file_id
        elif message.content_type == 'audio':
            file_id = message.audio.file_id
        elif message.content_type == 'document' and message.document.mime_type.startswith('audio/'):
            # Caso o áudio seja enviado como documento (alguns formatos podem vir assim)
            file_id = message.document.file_id
        else:
            errors.handle_unsupported_file_type_error(bot, message)
            return

        file_info = bot.get_file(file_id)
        file_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}'
        
        # Obter o tamanho do arquivo em bytes
        file_size = file_info.file_size
        
        # Definir a mensagem de feedback com base no tamanho do arquivo
        if file_size > 2 * 1024 * 1024:  # Exemplo de 2 MB (em bytes)
            feedback_message = "⌛ Aguarde, estou transcrevendo seu áudio. Como o arquivo é grande, pode demorar um pouco."
        else:
            feedback_message = "⌛ Aguarde, estou transcrevendo seu áudio..."

        # Enviar mensagem de feedback
        sent_message = bot.send_message(message.chat.id, feedback_message)

        # Obter o diretório do script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        temp_dir = os.path.join(script_dir, 'temp')

        # Verificar e criar o diretório temporário se não existir
        os.makedirs(temp_dir, exist_ok=True)

        # Baixar o arquivo do Telegram
        file_path = os.path.join(temp_dir, file_info.file_path.split('/')[-1])
        file_data = requests.get(file_url)

        # Salvar o arquivo no sistema local
        with open(file_path, 'wb') as f:
            f.write(file_data.content)

        # Exibir o diretório do arquivo salvo
        print(f"Arquivo salvo em: {file_path}")

        # Enviar o arquivo baixado para a API do Replicate
        with open(file_path, 'rb') as audio_file:
            input_data = {
                "audio": audio_file,
                "language": "pt"
            }

            client = replicate.Client(api_token=REPLICATE_API_TOKEN)

            output = client.run(
                REPLICATE_OPENAI_RUN,
                input=input_data
            )

        transcription = ''.join(segment['text'] for segment in output['segments'])
        
        # Enviar a transcrição obtida
        bot.send_message(message.chat.id, transcription)
        
        # Remover a mensagem temporária
        bot.delete_message(message.chat.id, sent_message.message_id)
        
        # Remover o arquivo temporário local
        os.remove(file_path)

    except Exception as e:
        print(f"Error: {e}")
        errors.handle_unknown_error(bot, message)

bot.polling()