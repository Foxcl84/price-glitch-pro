import os
import asyncio
from flask import Flask
from telegram.ext import Application, CommandHandler
from database import inicializar_db
import commands as cmd

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))

# ---- Telegram App ----
application = Application.builder().token(TOKEN).build()

application.add_handler(CommandHandler("start", cmd.cmd_start))
application.add_handler(CommandHandler("agregar", cmd.cmd_agregar))
application.add_handler(CommandHandler("listar", cmd.cmd_listar))
application.add_handler(CommandHandler("eliminar", cmd.cmd_eliminar))
application.add_handler(CommandHandler("scan", cmd.cmd_scan))

# ---- Flask para mantener vivo en Render ----
app = Flask(__name__)

@app.route("/")
def home():
    return "Price Glitch Pro activo"

async def iniciar_bot():
    print("BOT funcionando con Polling...")
    await application.run_polling(close_loop=False)

def main():
    inicializar_db()
    loop = asyncio.get_event_loop()
    loop.create_task(iniciar_bot())
    app.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()
