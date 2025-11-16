import os
import threading
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from commands import cmd_start, cmd_agregar, cmd_listar, cmd_eliminar, cmd_ayuda
from database import inicializar_bd
from scanner import escanear_productos
import time
import asyncio

# ================================
# VARIABLES DE ENTORNO
# ================================
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecreto123")
RENDER_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")

WEBHOOK_URL = f"https://{RENDER_HOST}/webhook/{WEBHOOK_SECRET}"

# ================================
# FLASK SERVER
# ================================
app = Flask(__name__)


@app.get("/")
def home():
    return "BOT ONLINE OK"


@app.post(f"/webhook/{WEBHOOK_SECRET}")
def webhook():
    update_json = request.get_json(force=True)
    update = Update.de_json(update_json, application.bot)
    application.update_queue.put(update)  # ← SE PROCESA SIN EVENT LOOP
    return "OK", 200


# ================================
# SCANNER CADA 30 SEGUNDOS
# ================================
def iniciar_scanner():
    while True:
        try:
            escanear_productos(application)
        except Exception as e:
            print("Error scanner:", e)
        time.sleep(30)


# ================================
# TELEGRAM BOT THREAD
# ================================
async def iniciar_bot():
    await application.bot.set_webhook(url=WEBHOOK_URL)
    print("Webhook configurado en:", WEBHOOK_URL)

    await application.run_webhook(
        listen="0.0.0.0",
        port=8000,
        url_path=WEBHOOK_SECRET,
        webhook_url=WEBHOOK_URL,
    )


def iniciar_thread_telegram():
    asyncio.run(iniciar_bot())


# ================================
# MAIN SETUP
# ================================
if __name__ == "__main__":
    inicializar_bd()

    # Crear la aplicación Telegram
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", cmd_start))
    application.add_handler(CommandHandler("agregar", cmd_agregar))
    application.add_handler(CommandHandler("listar", cmd_listar))
    application.add_handler(CommandHandler("eliminar", cmd_eliminar))
    application.add_handler(CommandHandler("ayuda", cmd_ayuda))
    application.add_handler(MessageHandler(filters.TEXT, cmd_ayuda))

    # Thread del bot telegram
    threading.Thread(target=iniciar_thread_telegram, daemon=True).start()

    # Thread escáner
    threading.Thread(target=iniciar_scanner, daemon=True).start()

    # Iniciar Flask en el puerto de Render
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

