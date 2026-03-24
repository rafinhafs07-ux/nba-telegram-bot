import os
import nest_asyncio  # Fix para Python 3.14 + PTB
import asyncio
from telegram.ext import Application, CommandHandler
from api import get_players_data
from analysis import analisar_jogadores

nest_asyncio.apply()  # Permite nested loops no Render

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("❌ ERRO: Defina TOKEN na env var!")
    exit(1)

async def analise(update, context):
    try:
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
    except Exception as e:
        await update.message.reply_text(f"Erro: {str(e)}")

async def start(update, context):
    await update.message.reply_text("🤖 Bot NBA Online! Use /analise")

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analise", analise))
    print("🚀 Bot iniciado com polling...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
