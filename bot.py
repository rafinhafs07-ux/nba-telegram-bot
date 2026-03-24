import os
from telegram.ext import Updater, CommandHandler
from api import get_players_data
from analysis import analisar_jogadores

TOKEN = os.getenv("TOKEN")

def analise(update, context):
    jogadores = get_players_data()
    resultado = analisar_jogadores(jogadores)

    mensagem = "📊 ANÁLISE NBA – UNDER 3 PONTOS\n\n"

    if not resultado:
        mensagem += "Nenhum jogador encontrado hoje."
    else:
        for j in resultado:
            mensagem += f"• {j['name']} | {j['threePointPct']*100:.1f}% | {j['threePointAttempts']} tentativas\n"

    mensagem += "\n💡 Baseado em baixa eficiência + volume"

    update.message.reply_text(mensagem)

def start(update, context):
    update.message.reply_text("🤖 Bot NBA Online! Use /analise")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("analise", analise))

updater.start_polling()
updater.idle()
