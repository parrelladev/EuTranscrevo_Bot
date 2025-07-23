# services/audio_pipeline.py

"""
🎛️ PIPELINE DE PROCESSAMENTO DE ÁUDIO

Recebe um arquivo de áudio, valida, otimiza com ffmpeg e transcreve com Replicate.

Uso:
    transcript = processar_audio("/caminho/do/audio.mp3")
"""

import os
import mimetypes

from config import SECURITY, DEVELOPMENT, MESSAGES
from services.audio_optimizer import optimize_audio
from services.replicate_client import transcribe_audio
from utils.file_utils import get_file_size

def processar_audio(input_path: str) -> str:
    """
    Processa um arquivo de áudio:
    - Valida tipo e tamanho
    - Otimiza com ffmpeg
    - Transcreve com API Replicate
    - Retorna a transcrição como string

    :param input_path: Caminho absoluto do arquivo de entrada
    :return: Texto transcrito
    :raises: ValueError ou Exception
    """
    # Validação de tipo MIME
    mime, _ = mimetypes.guess_type(input_path)
    if not DEVELOPMENT['skipFileTypeValidation']:
        if not mime or mime not in SECURITY['allowedAudioTypes']:
            raise ValueError("⚠️ O arquivo enviado não é um áudio válido.")

    # Validação de tamanho
    size = get_file_size(input_path)
    if size > SECURITY['maxFileSize']:
        raise ValueError(MESSAGES['fileTooLarge'])

    # Otimiza
    base_path = os.path.splitext(input_path)[0]
    optimized_path = base_path + "_optimized.mp3"
    optimize_audio(input_path, optimized_path)

    # Transcreve
    transcript = transcribe_audio(optimized_path)

    # Limpa arquivos
    os.remove(input_path)
    os.remove(optimized_path)

    return transcript.strip() if transcript else MESSAGES['audioError']
