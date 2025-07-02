# EuTranscrevoBot

Este bot Telegram foi desenvolvido para transcrever áudios enviados pelos usuários, utilizando o modelo Whisper da OpenAI via API do Replicate.

<img src="EuTranscrevo_bot.gif" width="400">

## 🚀 Pré-requisitos

- Ubuntu 20.04+ (ou qualquer Linux com Python 3.8+)
- Python 3 e pip
- ffmpeg
- Conta no Telegram (para criar o bot)
- Conta no Replicate (para transcrição)

---

## ⚙️ Instalação

1. **Instale dependências do sistema:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv ffmpeg -y
   ```

2. **Clone o repositório:**
   ```bash
   git clone <url-do-seu-repositorio>
   cd EuTranscrevoBot
   ```

3. **Crie e ative o ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Instale as dependências Python:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔑 Configuração

1. **Crie o arquivo de credenciais:**
   Crie o arquivo `src/api_token.py` com o seguinte conteúdo:
   ```python
   BOT_TOKEN = "seu_token_do_telegram"
   REPLICATE_API_TOKEN = "seu_token_do_replicate"
   REPLICATE_OPENAI_RUN = "seu_token_da_openAI"
   ```

2. **(Opcional) Ajuste as configurações em `src/config.py`:**
   - Velocidade de áudio (`SPEED_MULTIPLIER`)
   - Volume (`VOLUME_MULTIPLIER`)
   - Bitrate (`BITRATE`)
   - Tamanho mínimo para otimização (`MIN_FILE_SIZE_FOR_OPTIMIZATION`)

---

## ▶️ Execução

1. **Ative o ambiente virtual (se ainda não estiver ativo):**
   ```bash
   source venv/bin/activate
   ```

2. **Execute o bot:**
   ```bash
   python src/main.py
   ```

3. **Envie um áudio para o bot no Telegram e veja a transcrição otimizada!**

---

## 🛡️ .gitignore recomendado

```
venv/
__pycache__/
bot.log
src/temp/
src/api_token.py
```

---

## 📁 Estrutura mínima do projeto

```
EuTranscrevoBot/
├── src/
│   ├── main.py
│   ├── bot.py
│   ├── audio_handler.py
│   ├── replicate_client.py
│   ├── config.py
│   ├── errors.py
│   └── api_token.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 💡 Dicas
- O bot aceita qualquer formato de áudio suportado pelo ffmpeg.
- O volume dos áudios é aumentado automaticamente (ajustável em `config.py`).
- O arquivo `bot.log` registra todas as operações e pode ser útil para debug.
- Para rodar em produção, use um serviço como systemd para manter o bot ativo.

---

## 📝 Licença
MIT
