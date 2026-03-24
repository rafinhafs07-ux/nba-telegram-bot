import os
import sys
import logging

# CORRIGE IMGHDR GLOBALMENTE PRIMEIRO
try:
    import imghdr
except ImportError:
    try:
        from PIL import Image
        import io
        def imghdr_what(file, h=None):
            if h is None:
                if isinstance(file, str):
                    with open(file, 'rb') as f:
                        h = f.read(32)
                else:
                    h = file.read(32)
            try:
                img = Image.open(io.BytesIO(h))
                fmt = img.format.lower() if img.format else None
                img.close()
                return fmt
            except:
                return None
        
        # Cria módulo fake imghdr
        class FakeImghdr:
            what = staticmethod(imghdr_what)
            tests = []
        
        sys.modules['imghdr'] = FakeImghdr()
        print("✅ imghdr criado com Pillow!")
    except ImportError:
        print("❌ Pillow não instalado!")
        sys.exit(1)

# AGORA IMPORT PTB
from telegram.ext import Application, CommandHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("❌ TOKEN ausente!")
    sys.exit(1)

def get_players_data():
    try:
        from api import get_players_data
        return get_players_data()
    except:
        return []

def analisar_jogadores(jogadores):
    try:
        from analysis import analisar_jogadores
        return analisar_jogadores(jogadores)
    except:
        return []

async def analise(update, context):
    jogadores = get_players_data()
    resultado = analisar_jogadores(jogadores)
    
    mensagem = "📊 ANÁLISE NBA – UNDER 3 PONTOS\n\n"
    if not resultado:
        mensagem += "Nenhum jogador hoje."
    else:
        for j in resultado:
            pct = j.get('threePointPct', 0) * 100
            tent = j.get('threePointAttempts', 0)
            mensagem += f"• {j.get('name', '?')} | {pct:.1f}% | {tent} tent.\n"
    mensagem += "\n💡 Low efficiency + volume"
    
    await update.message.reply_text(mensagem)

async def start(update, context):
    await update.message.reply_text("🤖 NBA Bot!\n/analise")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("analise", analise))

print("🚀 NBA Bot rodando...")
app.run_polling(drop_pending_updates=True)
