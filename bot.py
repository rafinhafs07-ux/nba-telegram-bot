import os
import sys
# PATCH IMGHDR - FUNCIONA Python 3.14
try:
    import imghdr
except ImportError:
    from PIL import Image
    import io
    def what(file, h=None):
        if h is None:
            if isinstance(file, str):
                file = open(file, 'rb')
            h = file.read(32)
        return Image.open(io.BytesIO(h)).format.lower()
    import imghdr as _imghdr
    _imghdr.what = what
    sys.modules['imghdr'] = _imghdr
    print("✅ imghdr patched com Pillow!")

from telegram.ext import Updater, CommandHandler
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_players_data():
    try:
        from api import get_players_data
        return get_players_data()
    except Exception as e:
        print(f"API error: {e}")
        return []

def analisar_jogadores(jogadores):
    try:
        from analysis import analisar_jogadores
        return analisar_jogadores(jogadores)
    except Exception as e:
        print(f"Analysis error: {e}")
        return []

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    print("❌ TOKEN não definido!")
    exit(1)

def analise(update, context):
    jogadores = get_players_data()
    resultado = analisar_jogadores(jogadores)
    
    mensagem = "📊 ANÁLISE NBA – UNDER 3 PONTOS\n\n"
    if not resultado:
        mensagem += "Nenhum jogador encontrado hoje."
    else:
        for j in resultado:
            pct = j.get('threePointPct', 0) * 100
            tent = j.get('threePointAttempts', 0)
            mensagem += f"• {j['name']} | {pct:.1f}% | {tent} tentativas\n"
    mensagem += "\n💡 Baixa eficiência + volume"
    
    update.message.reply_text(mensagem)

def start(update, context):
    update.message.reply_text("🤖 NBA Bot Online!\n/analise para under 3pts")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("analise", analise))

print("🚀 Bot iniciado!")
updater.start_polling()
updater.idle()
