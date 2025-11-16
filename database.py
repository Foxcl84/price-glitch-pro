import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

def conectar():
    return psycopg2.connect(DATABASE_URL)

def inicializar_bd():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            tienda TEXT NOT NULL,
            precio_min INT DEFAULT 0
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS checks_log (
            id SERIAL PRIMARY KEY,
            url_id INT REFERENCES urls(id),
            precio INT,
            fecha TIMESTAMP DEFAULT NOW()
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def agregar_url(url, tienda, precio_min):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("INSERT INTO urls (url, tienda, precio_min) VALUES (%s, %s, %s);",
                (url, tienda, precio_min))
    conn.commit()
    cur.close()
    conn.close()


def obtener_urls():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, url, tienda, precio_min FROM urls;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def eliminar_url(id_url):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM urls WHERE id = %s;", (id_url,))
    conn.commit()
    cur.close()
    conn.close()


def registrar_check(url_id, precio):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("INSERT INTO checks_log (url_id, precio) VALUES (%s, %s);",
                (url_id, precio))
    conn.commit()
    cur.close()
    conn.close()

