from bot import Bot
from APIs import BOT_TOKEN

if __name__ == "__main__":
    bot_instance = Bot(BOT_TOKEN)
    bot_instance.start()