
# Bot de Transcrição de Áudio

Este bot Telegram foi desenvolvido para transcrever áudios enviados pelos usuários, utilizando a API da OpenAI via Replicate.

## Instalação

### Via Python

Para instalar as dependências necessárias, execute o seguinte comando:

`pip3 install -U -r requirements.txt` 

Certifique-se de que todas as dependências especificadas em `requirements.txt` estejam atualizadas.

### Via Docker

Para rodar o bot em um container Docker, siga os seguintes passos:

1.  **Construir a imagem Docker:**
    
    No diretório do projeto, execute o comando
        
    `docker build -t whisperaudiobot .` 
    
2.  **Executar o container:**
    
    Após a construção da imagem, você pode rodar o container com o seguinte comando:
        
    `docker run -d -p 5000:5000 whisperaudiobot` 
    
    Isso vai iniciar o bot em um container Docker e mapeá-lo para a porta 5000. Você pode alterar a porta conforme necessário.
    
## Configuração

Antes de executar o bot, certifique-se de configurar os seguintes parâmetros no arquivo `APIs.py`:

`BOT_TOKEN = '<seu_telegram_bot_token>'` 
`REPLICATE_OPENAI_RUN = '<seu_replicate_openai_run_id>'` 
`REPLICATE_API_TOKEN = '<seu_replicate_api_token>'` 

Substitua `<seu_telegram_bot_token>`, `<seu_replicate_openai_run_id>` e `<seu_replicate_api_token>` pelos tokens e IDs apropriados que você obteve ao configurar o bot no Telegram e na API do Replicate.

## Uso

Para iniciar o bot, execute o script `main.py` (ou se estiver utilizando Docker, ele será executado automaticamente no container). O bot estará pronto para receber áudios em formatos como voz, áudio ou documento (no caso de alguns formatos enviados dessa forma). Ele processará a transcrição e enviará o texto transcrito de volta ao usuário no Telegram.

## Funcionalidades

-   Suporte para transcrição de áudios enviados como voz, áudio ou documento.
-   Gerenciamento eficiente de feedback, ajustando-se ao tamanho do arquivo de áudio.
-   Integração com a API da OpenAI via Replicate para realizar a transcrição de áudio.
-   Manipulação de erros, com envio de mensagens apropriadas ao usuário em caso de falha no processamento do áudio.
