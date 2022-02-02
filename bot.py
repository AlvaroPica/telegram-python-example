import os
import logging
import telegram
import random
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Configurar Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s -%(levelname)s -%(message)s"
)

logger = logging.getLogger()

# Solicitar TOKEN

TOKEN = os.getenv("TOKEN_TELEGRAM")
mode = os.getenv('RUN_MODE')

if mode == "dev":
    # Acceso Local (Desarrollo)
    def run(updater):
        updater.start_polling()
        print("BOT CARGADO")
        updater.idle() # Permite finalizar el bot con Ctrl + C
        
elif mode == "prod":
    # Acceso Servidor (producción):
    def run(updater):
        PORT = int(os.environ.get('PORT', '8443')) # Telegram API Supported ports for Webhook: 443, 80, 88, 8443
        print(PORT)
        APP_NAME = os.environ.get("APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku

        updater.start_webhook(listen="0.0.0.0",
                            port=PORT,
                            url_path=TOKEN,
                            webhook_url=f"https://{APP_NAME}.herokuapp.com/{TOKEN}")

else:
    logger.info("No se especifico el modo")
    sys.exit()
    
    
def start(update, context):
    logger.info(f"El usuario {update.message.chat['username']} ha iniciado una conversacion")
    name = update.message.chat['username']
    update.message.reply_text(f"Hola {name}")
    
def random_number(update, context):
    user_id = update.message.chat['id']
    logger.info(f"El usuario {user_id} ha solicitado un numero aleatorio")
    number = random.randint(0,10)
    context.bot.sendMessage(chat_id=user_id, parse_mode="HTML", text=f"<b>Numero</b> aleatorio:\n{number}")
    
def echo(update, context):
    user_id = update.message.chat['id']
    logger.info(f"El usuario {user_id} ha enviado un mensaje")
    text = update.message.text
    context.bot.sendMessage(chat_id=user_id, parse_mode="MarkdownV2", text=f"*Mensaje replicado:*\n_{text}_")


if __name__ == "__main__":
    # Obtenemos información de nuestro bot
    my_bot = telegram.Bot(token = TOKEN)
    print(my_bot.getMe())
    
# Enlazamos nuestro updater con nuestro bot
updater = Updater(my_bot.token, use_context=True)

# Creamos un despachador
dp = updater.dispatcher

# Creamos los manejadores
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("random", random_number))
dp.add_handler(MessageHandler(Filters.text, echo))

run(updater)