import replicate
import telebot
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
            bot.reply_to(message, "Este tipo de arquivo de áudio não é suportado. Tente converte-lo!")
            return

        file_info = bot.get_file(file_id)
        file_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}'
        
        # Obter o tamanho do arquivo em bytes
        file_size = file_info.file_size
        
        # Definir a mensagem de feedback com base no tamanho do arquivo
        if file_size > 10 * 1024 * 1024:  # Exemplo de 10 MB (em bytes)
            feedback_message = "⌛ Aguarde, estou transcrevendo seu áudio. Como o arquivo é grande, pode demorar um pouco."
        else:
            feedback_message = "⌛ Aguarde, estou transcrevendo seu áudio..."

        # Enviar mensagem de feedback
        sent_message = bot.send_message(message.chat.id, feedback_message)

        input_data = {
            "audio": file_url,
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

    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "Ocorreu um erro ao processar o áudio. Por favor, tente novamente.")

bot.polling()
