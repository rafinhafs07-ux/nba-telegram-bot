import os
import logging
from telegram.ext import Application, CommandHandler

# Logging pra debug no Render
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_players_data():
    # Placeholder - substitua pela sua NBA API real
    from api import get_players_data as _get
    return _get()

def analisar_jogadores(jogadores):
    # Placeholder - substitua pela sua análise
    from analysis import analisar_jogadores as _analyze
    return _analyze(jogadores)

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    logger.error("❌ TOKEN não definido na env var!")
    exit(1)

async def analise(update, context):
    try:
        logger.info("Executando /analise...")
        jogadores = get_players_data()
        resultado = analisar_jogadores(jogadores)
        
        mensagem = "📊 ANÁLISE NBA – UNDER 3 PONTOS\n\n"
        if not resultado:
            mensagem += "Nenhum jogador encontrado hoje."
        else:
            for j in resultado:
                pct = j.get('threePointPct', 0) * 100
                tent = j.get('threePointAttempts', 0)
                mensagem += f"• {j.get('name', 'N/A')} | {pct:.1f}% | {tent} tentativas\n"
        
        mensagem += "\n💡 Baixa eficiência + volume"
        await update.message.reply_text(mensagem)
        logger.info("Análise enviada!")
    except Exception as e:
        logger.error(f"Erro em /analise: {e}")
        await update.message.reply_text(f"❌ Erro: {str(e)}")

async def start(update, context):
    await update.message.reply_text("🤖 NBA Under Bot Online!\nUse /analise para tips under 3pts.")

def main():
    logger.info("🚀 Iniciando NBA Bot...")
    builder = Application.builder().token(TOKEN)
    app = builder.build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analise", analise))
    
    logger.info("✅ Bot configurado - iniciando polling...")
    # PTB v22 + drop_pending_updates + close_loop=False = PERFEITO pro Render
    app.run_polling(
        drop_pending_updates=True,  # Ignora mensagens antigas
        close_loop=False,           # Evita close error
        timeout=10,                 # Timeout pra estabilidade
        bootstrap_retries=-1        # Retry infinito
    )

if __name__ == "__main__":
    main()
