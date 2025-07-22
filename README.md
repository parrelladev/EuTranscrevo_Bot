# 🤖 EuTranscrevo Bot

Um bot de Telegram que transcreve áudios e vídeos com fala usando o modelo **Whisper (via API Replicate)**. Suporta mensagens de voz, arquivos de áudio, vídeos e até documentos com mídia.

---

## ✨ Funcionalidades

- 🎙️ Transcrição automática de áudios (voz, arquivos, vídeos)
- 🧠 Integração com Whisper (large-v3) via [Replicate](https://replicate.com/)
- 🎛️ Otimização de mídia com FFmpeg para reduzir custos e melhorar performance
- 🌐 Suporte a múltiplos formatos: `.mp3`, `.wav`, `.ogg`, `.m4a`, `.mp4`, etc.
- 💬 Mensagens de boas-vindas e feedback em tempo real
- 🔐 Validação de tipo e tamanho de arquivo
- 🧹 Limpeza automática de arquivos temporários

---

## 🚀 Como usar

### 1. Clone o projeto

```bash
git clone https://github.com/parrelladev/EuTranscrevo_Bot/
cd EuTranscrevo_Bot
````

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Instale dependências do sistema

#### Ubuntu/Debian:

```bash
sudo apt install ffmpeg telebot
```

#### macOS:

```bash
brew install ffmpeg telebot
```

---

## 🔐 Configuração

### 1. Crie um arquivo `.env` com seu token do Telegram e da API Replicate:

```env
TELEGRAM_TOKEN=seu_token_telegram
REPLICATE_TOKEN=seu_token_replicate
```

### 2. Estrutura esperada:

```
📁 EuTranscrevo_bot_telegram/
├── 📁 commands/
│ ├── 📝 transcrever.py
│ ├── 👋 boas_vindas.py
├── 📁 services/
│ ├── 🎛️ audio_optimizer.py
│ ├── 📡 replicate_client.py
├── 📁 utils/ #
│ └── 📁 file_utils.py
├── 📁 temp/
├── ⚙️ config.py # Configurações centralizadas do bot
├── 🚀 main.py
├── 📦 requirements.txt 
└── 📄 README.md
```

---

## ▶️ Executando o bot

```bash
python main.py
```

---

## 🧪 Testes rápidos

* Envie um áudio de voz no privado → ele será transcrito automaticamente.
* Envie um `.mp4` com fala → o áudio será extraído e transcrito.
* Envie um `.mp3`, `.m4a`, `.ogg` → tudo funciona.
* Arquivos com mais de 50MB ou tipos inválidos serão recusados com mensagem clara.

---

## 🧠 Sobre a transcrição

Este bot usa o modelo Whisper `large-v3`, via API Replicate. É altamente preciso e suporta vários idiomas.

Você pode configurar:

* idioma: automático ou forçado
* tradução: habilitar ou não
* temperatura, thresholds e outros parâmetros

Essas opções estão em `config.py` > `REPLICATE['transcription']`.

---

## 📄 Licença

MIT © [Seu Nome](https://github.com/parrelladev)

---

## 💬 Exemplo de resposta do bot

```
🎙️ Olá, João! Mande um áudio para que eu possa transcrever.
📝 Olá, esse é um exemplo de transcrição gerada automaticamente.
```