import os
import time
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler

from scanner import escanear_productos
from database import crear_tablas, guardar_alerta
import commands

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHAT_ID_ALERTAS = int(os.getenv("CHAT_ID_ALERTAS"))
SCAN_INTERVAL = 30

commands.ADMIN_ID = ADMIN_ID

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Price Glitch activo."

def scanner_thread(app_telegram):
    ultimo_precio = {}
    while True:
        resultados = escanear_productos()
        for tienda, url, precio in resultados:
            if "❌" in precio:
                continue
            clave = f"{tienda}:{url}"
            if clave not in ultimo_precio:
                ultimo_precio[clave] = precio
                continue
            if precio != ultimo_precio[clave]:
                mensaje = (
                    "⚠️ *PRICE GLITCH DETECTADO*\n\n"
                    f"🏬 *Tienda:* {tienda}\n"
                    f"🔗 {url}\n\n"
                    f"💵 Antes: `{ultimo_precio[clave]}`\n"
                    f"💵 Ahora: `{precio}`"
                )
                guardar_alerta(tienda, url, ultimo_precio[clave], precio)
                app_telegram.bot.send_message(
                    chat_id=CHAT_ID_ALERTAS,
                    text=mensaje,
                    parse_mode="Markdown"
                )
                ultimo_precio[clave] = precio
        time.sleep(SCAN_INTERVAL)

def main():
    crear_tablas()
    app_tg = ApplicationBuilder().token(TOKEN).build()
    app_tg.add_handler(CommandHandler("agregar", commands.cmd_agregar))
    app_tg.add_handler(CommandHandler("listar", commands.cmd_listar))
    app_tg.add_handler(CommandHandler("eliminar", commands.cmd_eliminar))
    app_tg.add_handler(CommandHandler("reseturls", commands.cmd_reset))
    t = threading.Thread(target=scanner_thread, args=(app_tg,), daemon=True)
    t.start()
    app_tg.run_polling()

if __name__ == "__main__":
    main()
