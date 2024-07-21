import replicate
from APIs import REPLICATE_API_TOKEN, REPLICATE_OPENAI_RUN

class ReplicateClient:
    def __init__(self, api_token=REPLICATE_API_TOKEN):
        self.client = replicate.Client(api_token=api_token)

    def transcribe_audio_file(self, file_path):
        with open(file_path, 'rb') as audio_file:
            input_data = {"audio": audio_file, "language": "pt"}
            return self.client.run(REPLICATE_OPENAI_RUN, input=input_data)

    def transcribe_audio_url(self, file_url):
        input_data = {"audio": file_url, "language": "pt"}
        return self.client.run(REPLICATE_OPENAI_RUN, input=input_data)