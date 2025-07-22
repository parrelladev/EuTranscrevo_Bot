"""
📡 CLIENTE PARA API REPLICATE

- Envia áudio para o modelo Whisper v3
- Faz polling até o resultado estar pronto
- Retorna transcrição como texto

Autor: parrelladev
"""

import base64
import time
import requests
from config import REPLICATE

REPLICATE_TOKEN = REPLICATE['token']
MODEL_VERSION = REPLICATE['modelVersion']
HEADERS = {
    "Authorization": f"Token {REPLICATE_TOKEN}",
    "Content-Type": "application/json"
}


def transcribe_audio(file_path):
    """
    Transcreve um áudio usando a API Replicate (Whisper v3).

    :param file_path: Caminho do arquivo .mp3 otimizado
    :return: Texto transcrito
    :raises: Exception em caso de falha
    """
    try:
        # Codifica o áudio em base64
        with open(file_path, "rb") as f:
            audio_data = base64.b64encode(f.read()).decode("utf-8")

        print("📤 Enviando áudio para o Replicate...")

        # Envia a previsão
        response = requests.post(
            f"{REPLICATE['baseUrl']}/predictions",
            headers=HEADERS,
            json={
                "version": MODEL_VERSION,
                "input": {
                    "audio": f"data:audio/mp3;base64,{audio_data}",
                    **REPLICATE["transcription"]
                }
            }
        )
        response.raise_for_status()
        prediction = response.json()
        prediction_id = prediction["id"]

        # Polling
        print("⏳ Aguardando transcrição...")
        status = prediction["status"]
        output = prediction.get("output")

        attempts = 0
        max_attempts = REPLICATE["polling"]["maxAttempts"]
        interval = REPLICATE["polling"]["interval"] / 1000  # ms -> segundos

        while status not in ["succeeded", "failed"] and attempts < max_attempts:
            time.sleep(interval)
            attempts += 1

            poll = requests.get(
                f"{REPLICATE['baseUrl']}/predictions/{prediction_id}",
                headers=HEADERS
            )
            poll.raise_for_status()
            poll_data = poll.json()
            status = poll_data["status"]
            output = poll_data.get("output")
            print(f"📊 Status: {status} (tentativa {attempts}/{max_attempts})")

        if status == "succeeded":
            transcription = output.get("transcription", "⚠️ Transcrição vazia.")
            print("✅ Transcrição concluída com sucesso!")
            return transcription
        else:
            raise Exception("Transcrição falhou no Replicate.")

    except Exception as e:
        print("🔴 Erro no Replicate:", str(e))
        raise
