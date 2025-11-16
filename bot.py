import os
import time
import threading
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from commands import cmd_start, cmd_agregar, cmd_listar, cmd_eliminar, cmd_ayuda
from database import inicializar_bd
from scanner import escanear_productos


BOT_TOKEN = os.getenv("BOT_TOKEN")


# ====================================================
#   SCANNER (corre cada 30 segundos)
# ====================================================
def iniciar_scanner(application):
    while True:
        try:
            escanear_productos(application)
        except Exception as e:
            print("Error en scanner:", e)

        time.sleep(30)


# ====================================================
#               MAIN DEL BOT
# ====================================================
def main():
    inicializar_bd()

    # Crear app Telegram
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("agregar", cmd_agregar))
    app.add_handler(CommandHandler("listar", cmd_listar))
    app.add_handler(CommandHandler("eliminar", cmd_eliminar))
    app.add_handler(CommandHandler("ayuda", cmd_ayuda))
    app.add_handler(MessageHandler(filters.TEXT, cmd_ayuda))

    # Lanzar scanner (thread aparte)
    threading.Thread(target=iniciar_scanner, args=(app,), daemon=True).start()

    print("BOT PROFESIONAL INICIADO (modo polling Render)")

    # *** SIN ASYNCIO ***
    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()
