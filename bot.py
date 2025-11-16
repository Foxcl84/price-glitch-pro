import os
import time
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from commands import cmd_start, cmd_agregar, cmd_listar, cmd_eliminar, cmd_ayuda
from database import inicializar_bd
from scanner import escanear_productos

BOT_TOKEN = os.getenv("BOT_TOKEN")

# -------------------------------------------------------------------
# 1) FLASK SERVIDOR KEEP-ALIVE (Render Free exige un puerto abierto)
# -------------------------------------------------------------------
app = Flask(__name__)

@app.get("/")
def home():
    return "Bot Price Glitch funcionando OK"

# -------------------------------------------------------------------
# 2) SCANNER CADA 30 SEGUNDOS
# -------------------------------------------------------------------
def iniciar_scanner(application):
    while True:
        try:
            escanear_productos(application)
        except Exception as e:
            print("Error en scanner:", e)
        time.sleep(30)

# -------------------------------------------------------------------
# 3) TELEGRAM BOT — MODO POLLING SIN ASYNCIO
# -------------------------------------------------------------------
def iniciar_telegram():
    app_tg = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app_tg.add_handler(CommandHandler("start", cmd_start))
    app_tg.add_handler(CommandHandler("agregar", cmd_agregar))
    app_tg.add_handler(CommandHandler("listar", cmd_listar))
    app_tg.add_handler(CommandHandler("eliminar", cmd_eliminar))
    app_tg.add_handler(CommandHandler("ayuda", cmd_ayuda))
    app_tg.add_handler(MessageHandler(filters.TEXT, cmd_ayuda))

    # Scanner paralelo
    threading.Thread(target=iniciar_scanner, args=(app_tg,), daemon=True).start()

    print("BOT iniciado con polling (Render Free Compatible)")
    app_tg.run_polling(close_loop=False)

# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------
if __name__ == "__main__":
    inicializar_bd()

    # Iniciar Bot Telegram en thread
    threading.Thread(target=iniciar_telegram, daemon=True).start()

    # Iniciar Flask en el puerto obligatorio de Render
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

