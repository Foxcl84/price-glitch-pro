import requests
from bs4 import BeautifulSoup
from database import obtener_urls

def obtener_precio(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Buscar elementos de precio
        price_selectors = [
            'span[class*="price"]',
            'p[class*="price"]', 
            'div[class*="price"]',
            '.price',
            '.precio'
        ]
        
        for selector in price_selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text().strip()
                # Extraer números
                numbers = ''.join(filter(str.isdigit, price_text))
                if numbers:
                    return int(numbers)
        
        return None
    except Exception as e:
        print(f"❌ Error obteniendo precio: {e}")
        return None

def escanear_productos(app_tg=None):
    """Función para escanear todos los productos"""
    try:
        productos = obtener_urls()
        if not productos:
            print("📭 No hay productos para escanear")
            return
        
        print(f"🔍 Escaneando {len(productos)} productos...")
        
        for id_producto, url, tienda in productos:
            precio = obtener_precio(url)
            status = f"${precio}" if precio else "No detectado"
            print(f"   📦 {tienda}: {status}")
            
        print("✅ Escaneo completado")
        
    except Exception as e:
        print(f"❌ Error en escaneo: {e}")
