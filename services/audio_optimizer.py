"""
🎛️ SERVIÇO DE OTIMIZAÇÃO DE ÁUDIO (com ffmpeg)

- Converte para mono (1 canal)
- Reduz o bitrate
- Ajusta volume e velocidade
- Converte para MP3

Autor: parrelladev
"""

import subprocess
from config import AUDIO

def optimize_audio(input_path, output_path):
    """
    Converte e otimiza qualquer áudio para MP3 com configurações padronizadas.
    Força a conversão mesmo que já seja .mp3.
    """
    speed = AUDIO['optimization']['speed']
    volume = AUDIO['optimization']['volume']
    bitrate = AUDIO['optimization']['bitrate']
    channels = AUDIO['optimization']['channels']

    filters = f"volume={volume},atempo={speed}"

    cmd = [
        "ffmpeg",
        "-y",                      # Sobrescreve arquivos existentes
        "-i", input_path,          # Entrada
        "-vn",                     # Remove vídeo (se houver)
        "-ac", str(channels),      # Mono
        "-b:a", bitrate,           # Bitrate
        "-ar", "44100",            # Sample rate (padrão comum)
        "-filter:a", filters,      # Filtros de áudio
        "-f", "mp3",               # Formato de saída
        output_path                # Arquivo de saída
    ]

    try:
        print(f"🎧 Executando: {' '.join(cmd)}")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao forçar conversão com ffmpeg: {e}")
        raise