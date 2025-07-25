# config.py
"""
⚙️ CONFIGURAÇÕES CENTRALIZADAS DO BOT (Telegram + Python)
"""

import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env

# 🎛️ Configurações de Áudio
AUDIO = {
    "optimization": {
        "speed": 2.0,
        "volume": 1.0,
        "bitrate": "32k",
        "channels": 1,
        "format": "mp3"
    },
    "tempDir": "temp",
    "tempPrefix": "audio-transcribe"
}

# 📡 API Replicate
REPLICATE = {
    "token": os.getenv("REPLICATE_TOKEN"),
    "modelVersion": "3c08daf437fe359eb158a5123c395673f0a113dd8b4bd01ddce5936850e2a981",
    "baseUrl": "https://api.replicate.com/v1",
    "transcription": {
        "language": "auto",
        "translate": False,
        "temperature": 0,
        "transcription": "plain text",
        "suppress_tokens": "-1",
        "logprob_threshold": -1,
        "no_speech_threshold": 0.6,
        "condition_on_previous_text": True,
        "compression_ratio_threshold": 2.4,
        "temperature_increment_on_fallback": 0.2
    },
    "polling": {
        "maxAttempts": 450,     # 450 tentativas
        "interval": 2000,       # 2 segundos entre cada uma (em milissegundos)
        "timeout": 900000       # 15 minutos em milissegundos (apenas para referência)
    }
}

# 📱 Comandos do Bot
COMMANDS = {
    "donate": "/pix"
}

# 📊 Logging
LOGGING = {
    "level": os.getenv("LOG_LEVEL", "info"),
    "enableEmojis": True,
    "enableTimestamps": True
}

# 🛡️ Segurança
SECURITY = {
    "maxFileSize": 20 * 1024 * 1024,  # 20MB
    "allowedAudioTypes": [
        "audio/mp3", "audio/wav", "audio/m4a", "audio/ogg",
        "audio/ogg; codecs=opus", "audio/aac", "audio/webm",
        "audio/opus", "audio/amr", "audio/3gpp",
        "audio/mpeg", "audio/mp4", "video/mp4",
        "video/webm", "video/quicktime"
    ],
    "enableFileTypeValidation": True,
    "autoCleanup": True
}

# ⚡ Performance
PERFORMANCE = {
    "concurrentTranscriptions": 3,
    "cleanupInterval": 300000,  # 5 minutos
    "maxTempFiles": 100
}

# 🌐 Rede
NETWORK = {
    "timeout": 30000,
    "retries": 3,
    "retryDelay": 1000
}

# 📝 Mensagens do Bot
MESSAGES = {
    'audioError': "❌ Ocorreu um erro ao processar o áudio.",
    'invalidFile': "⚠️ O arquivo enviado não é um áudio válido.",
    'unsupportedMedia': '⚠️ Mídia não suportada.',
    'fileTooLarge': "⚠️ Este arquivo ultrapassa o limite de 20MB permitido.",
    'slowProcessing':"⚠️ O processamento demorou muito e foi interrompido. Por favor, tente dividir o áudio.",
    'welcome': "🎙️ Envie um áudio ou link para transcrição!"
}

# 🔧 Desenvolvimento
DEVELOPMENT = {
    "debug": os.getenv("NODE_ENV") == "development",
    "enableVerboseLogs": os.getenv("NODE_ENV") == "development",
    "mockTranscription": False,
    "skipFileTypeValidation": False
}

# 🔑 Token do Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
