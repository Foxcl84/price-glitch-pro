import os
import threading
import asyncio
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from commands import cmd_start, cmd_agregar, cmd_listar, cmd_eliminar, cmd_ayuda
from scanner import escanear_productos
from database import inicializar_bd

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ============================
#       FLASK SERVER
# ============================
app = Flask(__name__)

@app.get("/")
def home():
    return "BOT Price Glitch profesional corriendo OK."


def iniciar_flask():
    port = int(os.environ.get("PORT", 10000))
    print(f"Servidor Flask escuchando en puerto {port}...")
    app.run(host="0.0.0.0", port=port)


# ============================
#     SCANNER DE PRODUCTOS
# ============================
def iniciar_scanner(app_telegram):
    import time
    while True:
        try:
            escanear_productos(app_telegram)
        except Exception as e:
            print("[ERROR SCANNER]", e)
        time.sleep(30)


# ============================
#    TELEGRAM BOT (MAIN THREAD)
# ============================
async def main_telegram():
    print("Iniciando bot profesional...")

    inicializar_bd()

    app_telegram = ApplicationBuilder().token(BOT_TOKEN).build()

    app_telegram.add_handler(CommandHandler("start", cmd_start))
    app_telegram.add_handler(CommandHandler("agregar", cmd_agregar))
    app_telegram.add_handler(CommandHandler("listar", cmd_listar))
    app_telegram.add_handler(CommandHandler("eliminar", cmd_eliminar))
    app_telegram.add_handler(CommandHandler("ayuda", cmd_ayuda))
    app_telegram.add_handler(MessageHandler(filters.TEXT, cmd_ayuda))

    # Scanner paralelo
    threading.Thread(target=iniciar_scanner, args=(app_telegram,), daemon=True).start()

    print("Bot Telegram iniciado correctamente.")
    await app_telegram.run_polling()


# ============================
#           MAIN
# ============================
if __name__ == "__main__":
    # 1. Iniciar Flask en thread secundario
    threading.Thread(target=iniciar_flask, daemon=True).start()

    # 2. Iniciar Telegram en el hilo principal (OBLIGATORIO)
    asyncio.run(main_telegram())
