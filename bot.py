import os
import time
import threading
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
# 2) SCANNER – Corre cada 60 segundos (más seguro)
# ---------------------------------------------
def iniciar_scanner():
    """Scanner que corre independientemente"""
    time.sleep(10)  # Espera que el bot se inicie
    while True:
        try:
            print("🔍 Iniciando escaneo...")
            escanear_productos(None)  # Por ahora sin notificaciones
        except Exception as e:
            print(f"Error en scanner: {e}")
        time.sleep(60)  # 60 segundos es más seguro

# ---------------------------------------------
# 3) TELEGRAM – Configuración del Bot
# ---------------------------------------------
def main():
    """Función principal del bot de Telegram"""
    if not BOT_TOKEN:
        print("❌ ERROR: BOT_TOKEN no configurado")
        return

    # Configurar aplicación de Telegram
    app_tg = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers de comandos
    app_tg.add_handler(CommandHandler("start", cmd_start))
    app_tg.add_handler(CommandHandler("agregar", cmd_agregar))
    app_tg.add_handler(CommandHandler("listar", cmd_listar))
    app_tg.add_handler(CommandHandler("eliminar", cmd_eliminar))
    app_tg.add_handler(CommandHandler("scan", cmd_scan))
    app_tg.add_handler(CommandHandler("help", cmd_help))
    
    # Mensajes genéricos
    app_tg.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cmd_help))

    # Iniciar scanner en segundo plano
    scanner_thread = threading.Thread(target=iniciar_scanner, daemon=True)
    scanner_thread.start()
    
    # Ejecutar bot
    print("🤖 Bot de Telegram iniciado - Listo para recibir comandos")
    app_tg.run_polling(
        allowed_updates=['message', 'callback_query'],
        drop_pending_updates=True
    )

# ---------------------------------------------
# MAIN - Arquitectura para Render
# ---------------------------------------------
if __name__ == "__main__":
    # Inicializar base de datos siempre
    print("🔄 Inicializando base de datos...")
    inicializar_db()
    
    # En Render, ejecutar Flask Y el bot en threads separados
    if os.getenv("RENDER"):
        print("🚀 Entorno Render detectado - Iniciando Bot + Flask...")
        
        # Iniciar el bot de Telegram en un thread
        bot_thread = threading.Thread(target=main, daemon=True)
        bot_thread.start()
        
        # Ejecutar Flask en el thread principal (obligatorio para Render)
        port = int(os.getenv("PORT", 10000))
        print(f"🌐 Flask iniciando en puerto {port}")
        app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
    else:
        # En local, solo ejecutar el bot normalmente
        print("💻 Entorno local - Iniciando solo Bot...")
        main()
