import psycopg2
import os
import urllib.parse as urlparse

# Para Render PostgreSQL
DB_URL = os.getenv("DATABASE_URL")

def conectar():
    """Conectar a la base de datos de Render"""
    try:
        if DB_URL:
            # Parsear la URL para Render PostgreSQL
            url = urlparse.urlparse(DB_URL)
            conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port,
                sslmode='require'
            )
            return conn
        else:
            # Fallback para desarrollo local
            return psycopg2.connect("dbname=price_bot user=postgres")
    except Exception as e:
        print(f"❌ Error conectando a DB: {e}")
        return None

def inicializar_db():
    """Inicializar la tabla si no existe"""
    conn = conectar()
    if conn is None:
        return
        
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id SERIAL PRIMARY KEY,
                url TEXT NOT NULL,
                tienda TEXT NOT NULL,
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("✅ Base de datos inicializada")
    except Exception as e:
        print(f"❌ Error inicializando DB: {e}")
    finally:
        conn.close()

def agregar_url(url, tienda):
    """Agregar una nueva URL a monitorear"""
    conn = conectar()
    if conn is None:
        return False
        
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO urls (url, tienda) VALUES (%s, %s);", (url, tienda))
        conn.commit()
        print(f"✅ URL agregada: {tienda}")
        return True
    except Exception as e:
        print(f"❌ Error agregando URL: {e}")
        return False
    finally:
        conn.close()

def obtener_urls():
    """Obtener todas las URLs monitoreadas"""
    conn = conectar()
    if conn is None:
        return []
        
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, url, tienda FROM urls ORDER BY id;")
        datos = cur.fetchall()
        return datos
    except Exception as e:
        print(f"❌ Error obteniendo URLs: {e}")
        return []
    finally:
        conn.close()

def eliminar_url(id_url):
    """Eliminar una URL por ID"""
    conn = conectar()
    if conn is None:
        return False
        
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM urls WHERE id = %s;", (id_url,))
        conn.commit()
        print(f"✅ URL eliminada: ID {id_url}")
        return True
    except Exception as e:
        print(f"❌ Error eliminando URL: {e}")
        return False
    finally:
        conn.close()
