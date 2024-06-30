Bot de Transcrição de Áudio
===========================

![WhisperAudioBot](https://github.com/parrelladev/CartomanteTarot_Bot/assets/126002318/96500a0d-92fb-4d46-923c-f8ddda593e48)

Este bot Telegram foi desenvolvido para transcrever áudios enviados pelos usuários usando a API da OpenAI via Replicate.

Instalação
----------

Para instalar as dependências necessárias, execute o seguinte comando:

```
pip3 install -U -r requirements.txt
```

Certifique-se de que todas as dependências especificadas em `requirements.txt` estejam atualizadas.

Configuração
------------

Antes de executar o bot, certifique-se de configurar os seguintes parâmetros em `APIs.py`:

Python

```
BOT_TOKEN = '<seu_telegram_bot_token>'
REPLICATE_OPENAI_RUN = '<seu_replicate_openai_run_id>'
REPLICATE_API_TOKEN = '<seu_replicate_api_token>'
```

Substitua `<seu_telegram_bot_token>`, `<seu_replicate_openai_run_id>` e `<seu_replicate_api_token>` pelos tokens e IDs apropriados.

Uso
---

Execute o script `main.py` para iniciar o bot. Ele espera receber áudios em formatos como voz, áudio ou documento (no caso de alguns formatos serem enviados dessa forma). O bot transcreverá o áudio para texto e enviará de volta ao usuário no Telegram.

Funcionalidades
---------------

-   Suporta transcrição de áudios enviados como voz, áudio ou documento.
-   Gerencia o feedback com base no tamanho do arquivo de áudio.
-   Utiliza a API da OpenAI via Replicate para realizar a transcrição.
-   Manipula erros e envia mensagens de erro quando ocorre algum problema durante o processamento do áudio.