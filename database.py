import psycopg2
import os
import urllib.parse as urlparse

# Para Render PostgreSQL
DB_URL = os.getenv("DATABASE_URL")

def conectar():
    # Parsear la URL de la base de datos para Render
    if DB_URL:
        url = urlparse.urlparse(DB_URL)
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        return conn
    else:
        # Fallback local (para desarrollo)
        return psycopg2.connect("dbname=price_bot user=postgres")

def inicializar_db():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            tienda TEXT NOT NULL,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada")

# Las demás funciones (agregar_url, obtener_urls, eliminar_url) se mantienen igual
