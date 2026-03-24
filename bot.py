import os
import asyncio
from telegram.ext import Application, CommandHandler
from api import get_players_data  # Assuma que isso funciona
from analysis import analisar_jogadores  # Assuma que isso funciona

TOKEN = os.getenv("8612950541:AAFENbnJuahCJrEJ9_D-j1tOw4--Af-7YYU")  # Use env var no Render!

async def analise(update, context):
    jogadores = get_players_data()
    resultado = analisar_jogadores(jogadores)

    mensagem = "📊 ANÁLISE NBA – UNDER 3 PONTOS\n\n"

    if not resultado:
        mensagem += "Nenhum jogador encontrado hoje."
    else:
        for j in resultado:
            mensagem += f"• {j['name']} | {j['threePointPct']*100:.1f}% | {j['threePointAttempts']} tentativas\n"

    mensagem += "\n💡 Baseado em baixa eficiência + volume"

    await update.message.reply_text(mensagem)

async def start(update, context):
    await update.message.reply_text("🤖 Bot NBA Online! Use /analise")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analise", analise))
    app.run_polling()

if __name__ == "__main__":
    main()
