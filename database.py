import sqlite3
import os

def conectar():
    """Conectar a SQLite (más simple para empezar)"""
    return sqlite3.connect('bot_database.db')

def inicializar_db():
    """Inicializar la base de datos SQLite"""
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            tienda TEXT NOT NULL,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()
    print("✅ Base de datos SQLite inicializada")

def agregar_url(url, tienda):
    """Agregar una nueva URL a monitorear"""
    conn = conectar()
    cur = conn.cursor()
    cur.execute("INSERT INTO urls (url, tienda) VALUES (?, ?);", (url, tienda))
    conn.commit()
    conn.close()
    return True

def obtener_urls():
    """Obtener todas las URLs monitoreadas"""
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, url, tienda FROM urls ORDER BY id;")
    datos = cur.fetchall()
    conn.close()
    return datos

def eliminar_url(id_url):
    """Eliminar una URL por ID"""
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM urls WHERE id = ?;", (id_url,))
    conn.commit()
    conn.close()
    return True
