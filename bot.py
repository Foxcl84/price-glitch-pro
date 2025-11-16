import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from commands import cmd_start, cmd_agregar, cmd_listar, cmd_eliminar, cmd_ayuda
from scanner import escanear_productos
from database import inicializar_bd

# ==========================
#    CONFIGURACIONES
# ==========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
CHAT_ALERTAS = os.getenv("CHAT_ID_ALERTAS")

# Flask para mantener vivo el servicio
app = Flask(__name__)

@app.get("/")
def home():
    return "BOT Price Glitch profesional corriendo OK."

# ==========================
#   FUNCIÓN PARA INICIAR SCANNER
# ==========================
def iniciar_scanner(app_telegram):
    """Hilo que ejecuta el escáner cada 30 segundos."""
    import time
    while True:
        try:
            escanear_productos(app_telegram)
        except Exception as e:
            print(f"[ERROR SCANNER] {e}")
        time.sleep(30)

# ==========================
#       MAIN
# ==========================
async def start_bot():
    print("Iniciando bot profesional...")

    inicializar_bd()  # Crear tablas si no existen

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Comandos ADMIN
    application.add_handler(CommandHandler("start", cmd_start))
    application.add_handler(CommandHandler("agregar", cmd_agregar))
    application.add_handler(CommandHandler("listar", cmd_listar))
    application.add_handler(CommandHandler("eliminar", cmd_eliminar))
    application.add_handler(CommandHandler("ayuda", cmd_ayuda))

    # Mensajes regulares
    application.add_handler(MessageHandler(filters.TEXT, cmd_ayuda))

    # Hilo para el escáner
    hilo = threading.Thread(target=iniciar_scanner, args=(application,), daemon=True)
    hilo.start()

    print("Bot Telegram iniciado correctamente.")
    await application.run_polling()

# ==========================
#       EJECUCIÓN FLASK
# ==========================
if __name__ == "__main__":
    # Puerto dinámico para Render
    port = int(os.environ.get("PORT", 10000))

    # Hilo para el bot de Telegram
    threading.Thread(target=lambda: os.system("python bot.py run"), daemon=True)

    print(f"Servidor Flask escuchando en puerto {port}...")
    app.run(host="0.0.0.0", port=port)
