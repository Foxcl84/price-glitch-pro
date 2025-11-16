import os
import time
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from commands import cmd_start, cmd_agregar, cmd_listar, cmd_eliminar, cmd_scan, cmd_help
from database import inicializar_db
from monitor import iniciar_monitoreo
from scanner import escanear_productos


BOT_TOKEN = os.getenv("BOT_TOKEN")


# ---------------------------------------------
# 1) FLASK – Mantiene vivo el servicio en Render
# ---------------------------------------------
app = Flask(__name__)

@app.get("/")
def home():
    return "Bot Price Glitch funcionando OK"


# ---------------------------------------------
# 2) SCANNER – Corre cada 30 segundos en hilo aparte
# ---------------------------------------------
def iniciar_scanner(app_tg):
    while True:
        try:
            escanear_productos(app_tg)
        except Exception as e:
            print("Error en scanner:", e)
        time.sleep(30)


# ---------------------------------------------
# 3) TELEGRAM – Polling normal (sin asyncio)
# ---------------------------------------------
def iniciar_telegram():
    app_tg = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app_tg.add_handler(CommandHandler("start", cmd_start))
    app_tg.add_handler(CommandHandler("agregar", cmd_agregar))
    app_tg.add_handler(CommandHandler("listar", cmd_listar))
    app_tg.add_handler(CommandHandler("eliminar", cmd_eliminar))
    app_tg.add_handler(CommandHandler("scan", cmd_scan))
    app_tg.add_handler(CommandHandler("help", cmd_help))
    app_tg.add_handler(MessageHandler(filters.TEXT, cmd_help))

    # Scanner en paralelo
    threading.Thread(target=iniciar_scanner, args=(app_tg,), daemon=True).start()

    print("BOT iniciado con polling estable (Render Free Ready)")
    app_tg.run_polling(stop_signals=None)  # ← evita señales no soportadas en Render


# ---------------------------------------------
# MAIN
# ---------------------------------------------
if __name__ == "__main__":
    inicializar_db()

    # Lanzamos Telegram Bot en un thread
    threading.Thread(target=iniciar_telegram, daemon=True).start()

    # Flask en el puerto que Render asigna
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

