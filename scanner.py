import requests
from bs4 import BeautifulSoup

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
