import os
import time
import threading
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from commands import cmd_start, cmd_agregar, cmd_listar, cmd_eliminar, cmd_ayuda
from database import inicializar_bd
from scanner import escanear_productos


BOT_TOKEN = os.getenv("BOT_TOKEN")

# ===========================
# SCANNER - corre cada 30 segundos
# ===========================
def iniciar_scanner(application):
    while True:
        try:
            escanear_productos(application)
        except Exception as e:
            print("Error scanner:", e)
        time.sleep(30)

# ===========================
# MAIN
# ===========================
async def main():
    inicializar_bd()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("agregar", cmd_agregar))
    app.add_handler(CommandHandler("listar", cmd_listar))
    app.add_handler(CommandHandler("eliminar", cmd_eliminar))
    app.add_handler(CommandHandler("ayuda", cmd_ayuda))
    app.add_handler(MessageHandler(filters.TEXT, cmd_ayuda))

    # Scanner paralelo
    threading.Thread(target=iniciar_scanner, args=(app,), daemon=True).start()

    print("BOT funcionando con polling continuo...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
