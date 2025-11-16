import requests
from bs4 import BeautifulSoup
from database import obtener_urls

def scrape_generic(url, selector):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")
        el = soup.select_one(selector)
        return el.text.strip() if el else None
    except:
        return None

SCRAPERS = {
    "pcfactory": lambda u: scrape_generic(u, ".precioInternet"),
    "falabella": lambda u: scrape_generic(u, "span.copy10.primary.medium.jsx-3240150640"),
    "paris": lambda u: scrape_generic(u, ".pv1.f4"),
    "ripley": lambda u: scrape_generic(u, ".product-price__current-price"),
    "weplay": lambda u: scrape_generic(u, ".price"),
    "adidas": lambda u: scrape_generic(u, ".gl-price-item"),
    "nike": lambda u: scrape_generic(u, "span.is-current-price"),
    "hm": lambda u: scrape_generic(u, ".Price-module--regularPrice__2v1jY"),
}

def escanear_productos():
    urls = obtener_urls()
    resultados = []
    for item in urls:
        tienda = item["tienda"]
        url = item["url"]
        scraper = SCRAPERS.get(tienda)
        if scraper is None:
            resultados.append((tienda, url, "❌ Tienda no soportada"))
            continue
        try:
            precio = scraper(url)
        except:
            precio = None
        if precio:
            resultados.append((tienda, url, precio))
        else:
            resultados.append((tienda, url, "❌ No se pudo obtener precio"))
    return resultados
