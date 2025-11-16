import requests
from bs4 import BeautifulSoup
import re
from database import obtener_urls

def obtener_precio(url):
    """
    Función mejorada para detectar precios en diferentes sitios web
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        
        print(f"🔍 Escaneando: {url}")
        
        # Hacer la petición
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Parsear HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Eliminar scripts y styles para limpiar el HTML
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Estrategias de búsqueda de precios
        estrategias = [
            # Por atributos comunes de precio
            {'attrs': {'class': re.compile(r'price|precio|cost|value', re.I)}},
            {'attrs': {'id': re.compile(r'price|precio', re.I)}},
            {'attrs': {'data-price': True}},
            {'attrs': {'itemprop': 'price'}},
            
            # Por selectores CSS comunes
            {'name': 'span', 'attrs': {'class': re.compile(r'price', re.I)}},
            {'name': 'div', 'attrs': {'class': re.compile(r'price', re.I)}},
            {'name': 'p', 'attrs': {'class': re.compile(r'price', re.I)}},
            {'name': 'strong', 'attrs': {'class': re.compile(r'price', re.I)}},
            
            # Por contenido que contenga símbolos de moneda
            {'text': re.compile(r'[\$\€\£]?\s*\d+[.,]\d+')}
        ]
        
        precio_encontrado = None
        
        for estrategia in estrategias:
            elementos = soup.find_all(**estrategia)
            for elemento in elementos:
                texto = elemento.get_text().strip()
                precio = extraer_numero_precio(texto)
                if precio and 10 <= precio <= 10000000:  # Rango razonable para precios
                    print(f"✅ Precio detectado: ${precio} - Estrategia: {estrategia}")
                    return precio
        
        # Si no encontramos con estrategias específicas, buscar patrones numéricos en todo el texto
        texto_completo = soup.get_text()
        precios = re.findall(r'[\$\€\£]?\s*(\d{1,3}[.,]?\d{0,3}[.,]?\d{0,3})', texto_completo)
        
        for precio_str in precios:
            precio = extraer_numero_precio(precio_str)
            if precio and 10 <= precio <= 10000000:
                print(f"✅ Precio detectado (búsqueda general): ${precio}")
                return precio
        
        print("❌ No se pudo detectar el precio")
        return None
        
    except requests.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

def extraer_numero_precio(texto):
    """
    Extrae el número del precio del texto
    """
    try:
        # Limpiar el texto: quitar símbolos de moneda y espacios
        texto_limpio = re.sub(r'[^\d.,]', '', texto)
        
        # Manejar diferentes formatos de decimales
        if ',' in texto_limpio and '.' in texto_limpio:
            # Formato 1.000,00 (Europa)
            if texto_limpio.rfind(',') > texto_limpio.rfind('.'):
                texto_limpio = texto_limpio.replace('.', '').replace(',', '.')
            # Formato 1,000.00 (US)
            else:
                texto_limpio = texto_limpio.replace(',', '')
        elif ',' in texto_limpio:
            # Solo comas, podría ser decimal o separador de miles
            if texto_limpio.count(',') == 1 and len(texto_limpio.split(',')[1]) == 2:
                # Probablemente decimal: 123,45 → 123.45
                texto_limpio = texto_limpio.replace(',', '.')
            else:
                # Separador de miles: 1,000 → 1000
                texto_limpio = texto_limpio.replace(',', '')
        
        # Convertir a número
        precio = float(texto_limpio)
        return int(precio) if precio.is_integer() else int(precio * 100)  # Convertir a centavos si hay decimales
        
    except (ValueError, AttributeError):
        return None

def escanear_productos(app_tg=None):
    """
    Función para escanear todos los productos registrados
    """
    try:
        productos = obtener_urls()
        if not productos:
            print("📭 No hay productos registrados para escanear")
            return []
        
        print(f"🔍 Iniciando escaneo de {len(productos)} productos...")
        resultados = []
        
        for id_producto, url, tienda in productos:
            print(f"   📦 Escaneando: {tienda}")
            precio = obtener_precio(url)
            
            if precio:
                resultado = {
                    'id': id_producto,
                    'tienda': tienda,
                    'url': url,
                    'precio': precio,
                    'status': '✅ Detectado'
                }
                print(f"      💰 Precio: ${precio}")
            else:
                resultado = {
                    'id': id_producto,
                    'tienda': tienda,
                    'url': url,
                    'precio': None,
                    'status': '❌ No detectado'
                }
                print(f"      ❌ Precio no detectado")
            
            resultados.append(resultado)
        
        print("✅ Escaneo completado")
        return resultados
        
    except Exception as e:
        print(f"❌ Error en escaneo general: {e}")
        return []
