"""
Configurações do EuTranscrevoBot
Centraliza parâmetros de otimização de áudio e outras configurações
"""

# Configurações de otimização de áudio
AUDIO_OPTIMIZATION = {
    'SPEED_MULTIPLIER': 1.0,
    'VOLUME_MULTIPLIER': 10.0,  # Aumenta o volume em 10x
    'BITRATE': '64k',
    'ENABLED': True,
    'MIN_FILE_SIZE_FOR_OPTIMIZATION': 0,
    'FFMPEG_TIMEOUT': 300,  # 5 minutos
}

# Configurações de transcrição
TRANSCRIPTION = {
    # Idioma padrão para transcrição
    'DEFAULT_LANGUAGE': 'pt',
    
    # Timeout para transcrição (em segundos)
    'TIMEOUT': 300,  # 5 minutos
}

# Configurações de rate limiting
RATE_LIMIT = {
    # Janela de tempo para rate limiting (em segundos)
    'WINDOW': 60,  # 1 minuto
    
    # Máximo de requisições por janela
    'MAX_REQUESTS': 5,
}

# Configurações de arquivo
FILE = {
    # Tamanho máximo de arquivo (em bytes)
    'MAX_SIZE': 20 * 1024 * 1024,  # 20MB
    
    # Tipos MIME suportados
    'SUPPORTED_MIME_TYPES': {
        'audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/ogg',
        'audio/x-wav', 'audio/x-mpeg', 'audio/x-mp3',
        'audio/x-flac', 'audio/flac', 'audio/aac', 'audio/x-aac',
        'audio/mp4', 'audio/x-m4a', 'audio/webm', 'audio/opus'
    }
}

# Configurações de logging
LOGGING = {
    'LEVEL': 'INFO',
    'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'FILE': 'bot.log'
}