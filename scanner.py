import requests
from bs4 import BeautifulSoup
from database import obtener_urls

def obtener_precio(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        html = requests.get(url, headers=headers, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        posible = soup.find(["span", "p"], class_=lambda x: x and "price" in x.lower())
        if posible:
            precio_texto = posible.get_text().replace("$", "").replace(".", "").strip()
            return int("".join(filter(str.isdigit, precio_texto)))

        return None
    except:
        return None

# NUEVA FUNCIÓN QUE FALTABA
def escanear_productos(app_tg):
    """Escanea todos los productos y notifica cambios"""
    try:
        productos = obtener_urls()
        for id_producto, url, tienda in productos:
            precio_actual = obtener_precio(url)
            if precio_actual:
                # Aquí podrías comparar con precio anterior y notificar cambios
                print(f"💰 {tienda}: ${precio_actual}")
                
                # EJEMPLO: Notificar a un chat específico (debes configurar esto)
                # await app_tg.bot.send_message(
                #     chat_id=CHAT_ID, 
                #     text=f"Precio actual {tienda}: ${precio_actual}"
                # )
    except Exception as e:
        print(f"Error en escaneo: {e}")
