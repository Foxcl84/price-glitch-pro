import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")

def crear_tablas():
    conn = get_connection(); cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS alertas (id SERIAL PRIMARY KEY, tienda VARCHAR(50), url TEXT, precio_anterior VARCHAR(50), precio_actual VARCHAR(50), fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS urls (id SERIAL PRIMARY KEY, tienda VARCHAR(50), url TEXT);"
    )
    conn.commit(); cur.close(); conn.close()

def insertar_url(tienda, url):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("INSERT INTO urls (tienda, url) VALUES (%s, %s) RETURNING id;", (tienda.lower(), url))
    new_id = cur.fetchone()[0]
    conn.commit(); cur.close(); conn.close()
    return new_id

def obtener_urls():
    conn = get_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, tienda, url FROM urls ORDER BY id ASC;")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

def eliminar_url(id_url):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM urls WHERE id = %s;", (id_url,))
    conn.commit(); cur.close(); conn.close()

def reset_urls():
    conn = get_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM urls;")
    conn.commit(); cur.close(); conn.close()

def guardar_alerta(tienda, url, precio_anterior, precio_actual):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("INSERT INTO alertas (tienda, url, precio_anterior, precio_actual) VALUES (%s, %s, %s, %s);",
                (tienda, url, precio_anterior, precio_actual))
    conn.commit(); cur.close(); conn.close()
