import psycopg2
import os

DB_URL = os.getenv("DATABASE_URL")

def conectar():
    return psycopg2.connect(DB_URL)

def inicializar_db():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            tienda TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def agregar_url(url, tienda):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("INSERT INTO urls (url, tienda) VALUES (%s, %s);", (url, tienda))
    conn.commit()
    conn.close()

def obtener_urls():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, url, tienda FROM urls;")
    datos = cur.fetchall()
    conn.close()
    return datos

def eliminar_url(id_url):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM urls WHERE id = %s;", (id_url,))
    conn.commit()
    conn.close()
