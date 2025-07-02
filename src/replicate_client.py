import replicate
import time
from typing import Any, Dict
import requests
from api_token import REPLICATE_API_TOKEN, REPLICATE_OPENAI_RUN
from errors import APIError, ErrorHandler
from config import TRANSCRIPTION

class ReplicateClient:
    def __init__(self, api_token=REPLICATE_API_TOKEN, max_retries=3, retry_delay=2):
        self.api_token = api_token
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.setup_client()

    def setup_client(self):
        try:
            self.client = replicate.Client(api_token=self.api_token)
        except Exception as e:
            raise APIError(f"Falha ao inicializar cliente Replicate: {str(e)}")

    def _execute_with_retry(self, operation_func: callable) -> Dict[str, Any]:
        last_error = None
        for attempt in range(self.max_retries):
            try:
                return operation_func()
            except replicate.exceptions.ReplicateError as e:
                last_error = e
                if "authentication" in str(e).lower():
                    raise APIError("Erro de autenticação com a API Replicate")
                time.sleep(self.retry_delay * (attempt + 1))
            except requests.exceptions.RequestException as e:
                last_error = e
                time.sleep(self.retry_delay * (attempt + 1))
            except Exception as e:
                raise APIError(f"Erro inesperado na API Replicate: {str(e)}")
        
        raise APIError(f"Máximo de tentativas excedido. Último erro: {str(last_error)}")

    def transcribe_audio_file(self, file_path: str, timeout: int = None) -> Dict[str, Any]:
        timeout = timeout or TRANSCRIPTION['TIMEOUT']
        def operation():
            with open(file_path, 'rb') as audio_file:
                input_data = {"audio": audio_file, "language": TRANSCRIPTION['DEFAULT_LANGUAGE']}
                return self.client.run(REPLICATE_OPENAI_RUN, input=input_data, timeout=timeout)
        
        return self._execute_with_retry(operation)

    def transcribe_audio_url(self, file_url: str, timeout: int = None) -> Dict[str, Any]:
        timeout = timeout or TRANSCRIPTION['TIMEOUT']
        def operation():
            input_data = {"audio": file_url, "language": TRANSCRIPTION['DEFAULT_LANGUAGE']}
            return self.client.run(REPLICATE_OPENAI_RUN, input=input_data, timeout=timeout)
        
        return self._execute_with_retry(operation)