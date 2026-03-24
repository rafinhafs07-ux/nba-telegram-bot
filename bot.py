import os
from telegram.ext import Updater, CommandHandler

TOKEN = os.getenv("TOKEN")

def start(update, context):
    update.message.reply_text("🤖 Bot da NBA está online!")

def analise(update, context):
    update.message.reply_text("📊 Análise em breve...")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("analise", analise))

updater.start_polling()
updater.idle()
