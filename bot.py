import os
import time
import threading
import asyncio
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from commands import cmd_start, cmd_agregar, cmd_listar, cmd_eliminar, cmd_scan, cmd_help
from database import inicializar_db
from scanner import escanear_productos

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ---------------------------------------------
# 1) FLASK – Mantiene vivo el servicio en Render
# ---------------------------------------------
app = Flask(__name__)

@app.get("/")
def home():
    return "Bot Price Glitch funcionando OK"

@app.get("/health")
def health():
    return "OK", 200

# ---------------------------------------------
# 2) SCANNER – Corre cada 60 segundos
# ---------------------------------------------
def iniciar_scanner():
    """Scanner que corre independientemente"""
    time.sleep(15)  # Espera que el bot se inicie completamente
    while True:
        try:
            print("🔍 Ejecutando escaneo programado...")
            # Escaneo básico sin notificaciones por ahora
            productos = obtener_urls_simple()
            for producto in productos:
                print(f"📦 Producto: {producto[2]} - URL: {producto[1][:50]}...")
            print(f"✅ Escaneo completado - {len(productos)} productos")
        except Exception as e:
            print(f"❌ Error en scanner: {e}")
        time.sleep(60)

def obtener_urls_simple():
    """Función simplificada para obtener URLs sin depender de commands"""
    try:
        from database import obtener_urls
        return obtener_urls()
    except Exception as e:
        print(f"Error obteniendo URLs: {e}")
        return []

# ---------------------------------------------
# 3) TELEGRAM – Configuración del Bot (ASYNCIO)
# ---------------------------------------------
async def run_bot():
    """Ejecutar el bot de Telegram con asyncio"""
    if not BOT_TOKEN:
        print("❌ ERROR: BOT_TOKEN no configurado")
        return

    try:
        # Configurar aplicación de Telegram
        application = ApplicationBuilder().token(BOT_TOKEN).build()

        # Handlers de comandos
        application.add_handler(CommandHandler("start", cmd_start))
        application.add_handler(CommandHandler("agregar", cmd_agregar))
        application.add_handler(CommandHandler("listar", cmd_listar))
        application.add_handler(CommandHandler("eliminar", cmd_eliminar))
        application.add_handler(CommandHandler("scan", cmd_scan))
        application.add_handler(CommandHandler("help", cmd_help))
        
        # Mensajes genéricos
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cmd_help))

        print("🤖 Bot de Telegram iniciado - Listo para recibir comandos")
        
        # Iniciar polling
        await application.run_polling(
            allowed_updates=['message', 'callback_query'],
            drop_pending_updates=True
        )
    except Exception as e:
        print(f"❌ Error en el bot: {e}")

def run_bot_sync():
    """Ejecutar el bot en un event loop propio"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_bot())
    except KeyboardInterrupt:
        print("Bot detenido")
    finally:
        loop.close()

# ---------------------------------------------
# MAIN - Arquitectura corregida para Render
# ---------------------------------------------
def start_services():
    """Iniciar todos los servicios"""
    print("🔄 Inicializando base de datos...")
    inicializar_db()
    
    # Iniciar scanner en segundo plano
    scanner_thread = threading.Thread(target=iniciar_scanner, daemon=True)
    scanner_thread.start()
    print("🔍 Scanner iniciado en segundo plano")
    
    # Iniciar bot de Telegram
    print("🚀 Iniciando Bot de Telegram...")
    run_bot_sync()

if __name__ == "__main__":
    # En Render, necesitamos una estrategia diferente
    if os.getenv("RENDER"):
        print("🌐 Entorno Render detectado")
        
        # En Render, iniciamos todo en el thread principal
        # pero Flask se ejecuta en un thread separado
        flask_thread = threading.Thread(
            target=lambda: app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=False, use_reloader=False),
            daemon=True
        )
        flask_thread.start()
        print("✅ Flask iniciado en thread separado")
        
        # Iniciar servicios principales en el thread principal
        start_services()
    else:
        # En local, solo el bot
        print("💻 Entorno local detectado")
        start_services()
