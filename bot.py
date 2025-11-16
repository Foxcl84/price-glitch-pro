import os
import asyncio
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from commands import cmd_start, cmd_agregar, cmd_listar, cmd_eliminar, cmd_scan, cmd_help
from database import inicializar_db

# Configuración
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Flask app (obligatorio para Render)
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Price Glitch Bot - Online"

@app.route('/health')
def health():
    return "OK", 200

async def run_bot():
    """Función principal async para el bot de Telegram"""
    if not BOT_TOKEN:
        print("❌ ERROR: BOT_TOKEN no está configurado")
        return

    try:
        # Crear aplicación de Telegram
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        
        # Registrar todos los comandos
        application.add_handler(CommandHandler("start", cmd_start))
        application.add_handler(CommandHandler("agregar", cmd_agregar))
        application.add_handler(CommandHandler("listar", cmd_listar))
        application.add_handler(CommandHandler("eliminar", cmd_eliminar))
        application.add_handler(CommandHandler("scan", cmd_scan))
        application.add_handler(CommandHandler("help", cmd_help))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cmd_help))
        
        print("✅ Bot configurado correctamente")
        print("🔄 Iniciando polling...")
        
        # Iniciar polling (más compatible con Render Free)
        await application.run_polling(
            drop_pending_updates=True,
            allowed_updates=['message', 'callback_query']
        )
        
    except Exception as e:
        print(f"❌ Error en el bot: {e}")

def start_services():
    """Iniciar todos los servicios"""
    print("🔄 Inicializando base de datos...")
    inicializar_db()
    
    print("🚀 Iniciando Bot de Telegram...")
    
    # Crear y configurar el event loop para el bot
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(run_bot())
    except KeyboardInterrupt:
        print("Bot detenido manualmente")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        loop.close()

if __name__ == "__main__":
    # ESTRATEGIA RENDER FREE: Solo Flask, no el bot
    # Esto es porque Render Free no soporta procesos largos/polling bien
    
    print("🌐 Modo Render Free Activado")
    print("💡 Nota: El bot necesita un servicio que soporte Webhooks")
    print("📞 Para producción, considera: Railway, Heroku, o un VPS")
    
    # Solo ejecutamos Flask para mantener el servicio "vivo"
    port = int(os.getenv("PORT", 10000))
    print(f"🔧 Servicio Flask en puerto {port}")
    print("⚠️  El bot de Telegram NO está activo en Render Free")
    print("💡 Usa /commands en local para probar la funcionalidad")
    
    app.run(host="0.0.0.0", port=port, debug=False)
