import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from commands import cmd_start, cmd_agregar, cmd_listar, cmd_eliminar, cmd_ayuda
from database import inicializar_bd
from scanner import escanear_productos
import threading
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecreto123")  # genera otro si quieres

app = Flask(__name__)

# ===============================
#  Inicializar aplicación Telegram
# ===============================
application = ApplicationBuilder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler("start", cmd_start))
application.add_handler(CommandHandler("agregar", cmd_agregar))
application.add_handler(CommandHandler("listar", cmd_listar))
application.add_handler(CommandHandler("eliminar", cmd_eliminar))
application.add_handler(CommandHandler("ayuda", cmd_ayuda))
application.add_handler(MessageHandler(filters.TEXT, cmd_ayuda))


# ===============================
#  Webhook que recibe mensajes
# ===============================
@app.post(f"/webhook/{WEBHOOK_SECRET}")
def webhook():
    update = Update.de_json(request.json, application.bot)
    asyncio.get_event_loop().create_task(application.process_update(update))
    return "OK", 200


# ===============================
#   Página raíz (Render healthcheck)
# ===============================
@app.get("/")
def home():
    return "BOT PROFESSIONAL ONLINE"


# ===============================
#     Scanner cada 30 segundos
# ===============================
def iniciar_scanner():
    while True:
        try:
            escanear_productos(application)
        except Exception as e:
            print("Error scanner:", e)
        time.sleep(30)


# ===============================
#       MAIN
# ===============================
if __name__ == "__main__":
    print("Inicializando base de datos...")
    inicializar_bd()

    # Iniciar scanner en paralelo
    threading.Thread(target=iniciar_scanner, daemon=True).start()

    # Establecer webhook automáticamente
    import requests
    URL_WEBHOOK = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook/{WEBHOOK_SECRET}"

    print("Configurando webhook:", URL_WEBHOOK)
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={URL_WEBHOOK}"
    )

    PORT = int(os.environ.get("PORT", 10000))
    print(f"Escuchando Flask en puerto {PORT}...")

    app.run(host="0.0.0.0", port=PORT)

