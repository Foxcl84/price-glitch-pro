import requests
from bs4 import BeautifulSoup

from database import registrar_check
from telegram import Bot

import os

CHAT_ALERTAS = os.getenv("CHAT_ID_ALERTAS")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def obtener_precio_html(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        # reglas simples para todas las tiendas
        posibles = [
            {"attrs": {"class": "price"}, "type": "text"},
            {"attrs": {"class": "fb-price"}, "type": "text"},
            {"attrs": {"class": "price-tag"}, "type": "text"},
            {"attrs": {"id": "price"}, "type": "text"},
            {"attrs": {"class": "product-price"}, "type": "text"},
        ]

        for regla in posibles:
            encontrado = soup.find(attrs=regla["attrs"])
            if encontrado:
                precio_txt = encontrado.get_text().strip()
                precio = int("".join([c for c in precio_txt if c.isdigit()]))
                return precio

        return None
    except:
        return None


def escanear_productos(app_telegram):
    from database import obtener_urls

    urls = obtener_urls()

    for id_url, url, tienda, precio_min in urls:
        precio = obtener_precio_html(url)

        if precio:
            registrar_check(id_url, precio)

            # alerta por precio bajo
            if precio <= precio_min:
                mensaje = (
                    f"🔥 **GLITCH DETECTADO en {tienda}!**\n\n"
                    f"🔗 {url}\n"
                    f"💸 Precio: **${precio}**\n"
                    f"📉 Umbral: ${precio_min}"
                )

                app_telegram.bot.send_message(
                    chat_id=CHAT_ALERTAS,
                    text=mensaje,
                    parse_mode="Markdown"
                )

