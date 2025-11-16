from telegram import Update
from telegram.ext import ContextTypes

from database import agregar_url, obtener_urls, eliminar_url
import os

ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bienvenido al Bot Price Glitch Profesional.\nEscribe /ayuda para ver comandos."
    )

async def cmd_ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 *Comandos disponibles:*\n\n"
        "/agregar URL TIENDA PRECIO_MIN\n"
        "/listar\n"
        "/eliminar ID\n",
        parse_mode="Markdown"
    )

async def cmd_agregar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    
    try:
        _, url, tienda, precio_min = update.message.text.split(" ", 3)
        precio_min = int(precio_min)

        agregar_url(url, tienda, precio_min)
        await update.message.reply_text("✅ URL agregada correctamente.")
    except:
        await update.message.reply_text("⚠️ Formato incorrecto.\nEj: /agregar URL TIENDA 50000")

async def cmd_listar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    urls = obtener_urls()

    if not urls:
        await update.message.reply_text("No hay productos registrados.")
        return

    mensaje = "📦 *Productos monitoreados:*\n\n"
    for id_url, url, tienda, precio_min in urls:
        mensaje += f"ID {id_url} — {tienda}\n{url}\nMin: ${precio_min}\n\n"

    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def cmd_eliminar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    try:
        _, id_url = update.message.text.split(" ", 1)
        eliminar_url(int(id_url))
        await update.message.reply_text("🗑️ Eliminado.")
    except:
        await update.message.reply_text("⚠️ Uso: /eliminar ID")
