# 🤖 EuTranscrevo Bot

Um bot de Telegram que transcreve áudios, vídeos e **links com mídia** usando o modelo **Whisper (via API Replicate)**. Suporta mensagens de voz, arquivos de áudio, vídeos, documentos e links de YouTube.

---

## ✨ Funcionalidades

- 🎙️ Transcrição automática de áudios (voz, arquivos, vídeos)
- 🔗 Transcrição de áudio extraído de links (YouTube, etc.) usando `yt-dlp`
- 🧠 Integração com Whisper (large-v3) via [Replicate](https://replicate.com/)
- 🎛️ Otimização de mídia com FFmpeg para reduzir custos e melhorar performance
- 🌐 Suporte a múltiplos formatos: `.mp3`, `.wav`, `.ogg`, `.m4a`, `.mp4`, etc.
- 💬 Mensagens de boas-vindas e feedback em tempo real
- 🔐 Validação de tipo e tamanho de arquivo (até 1GB ou mais)
- 🧹 Limpeza automática de arquivos temporários

---

## 🚀 Como usar

### 1. Clone o projeto

```bash
git clone https://github.com/parrelladev/EuTranscrevo_Bot/
cd EuTranscrevo_Bot
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
pip install yt-dlp
```

### 3. Instale dependências do sistema

#### Ubuntu/Debian:

```bash
sudo apt install ffmpeg
```

#### macOS:

```bash
brew install ffmpeg
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
📁 EuTranscrevo_Bot/
├── 📁 commands/
│   ├── 📝 transcrever.py
│   ├── 🔗 transcrever_link.py
│   ├── 👋 boas_vindas.py
├── 📁 services/
│   ├── 🎛️ audio_optimizer.py
│   ├── 📡 replicate_client.py
│   ├── 🔁 audio_pipeline.py
├── 📁 utils/
│   └── 🧰 file_utils.py
├── 📁 temp/
├── ⚙️ config.py
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

* Envie um áudio de voz → será transcrito automaticamente.
* Envie um `.mp4` com fala → áudio extraído e transcrito.
* Envie um `.mp3`, `.m4a`, `.ogg` → tudo funciona.
* Envie um link do YouTube → áudio baixado e transcrito.
* Arquivos com tipo inválido ou muito grandes serão recusados com mensagem clara.

---

## 🌐 Suporte a links

Você pode enviar links como:

- YouTube (inclusive Shorts)
- Outros sites compatíveis com `yt-dlp`

O bot irá:

1. Baixar o áudio automaticamente
2. Otimizar o arquivo
3. Transcrever com Whisper

📌 *Nota*: vídeos longos podem ser recusados conforme `SECURITY['maxFileSize']` em `config.py`.

---

## 🧠 Sobre a transcrição

Este bot usa o modelo Whisper `large-v3`, via API Replicate. É altamente preciso e suporta vários idiomas.

Você pode configurar:

* Idioma: automático ou forçado
* Tradução: habilitar ou não
* Temperatura, thresholds e outros parâmetros

Essas opções estão em `config.py` > `REPLICATE['transcription']`.

---

## 📄 Licença

MIT © [parrelladev](https://github.com/parrelladev)

---

## 💬 Exemplo de resposta do bot

```
🎙️ Olá, João! Mande um áudio ou link para que eu possa transcrever.
📝 Olá, esse é um exemplo de transcrição gerada automaticamente.
```