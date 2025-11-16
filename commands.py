from telegram import Update
from telegram.ext import ContextTypes
from database import agregar_url, obtener_urls, eliminar_url
from scanner import obtener_precio

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bienvenido al *Price Glitch Pro*.\n"
        "Usa /agregar, /listar, /eliminar, /scan, /help"
    )

async def cmd_agregar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = context.args[0]
        tienda = context.args[1]
        agregar_url(url, tienda)
        await update.message.reply_text("URL agregada correctamente ✔️")
    except:
        await update.message.reply_text("Formato:\n/agregar <url> <tienda>")

async def cmd_listar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    filas = obtener_urls()
    if not filas:
        await update.message.reply_text("No hay URLs registradas.")
        return

    texto = "📌 *Productos registrados:*\n\n"
    for fila in filas:
        texto += f"ID: {fila[0]}\n{fila[1]}\nTIENDA: {fila[2]}\n\n"

    await update.message.reply_text(texto)

async def cmd_eliminar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        id_url = int(context.args[0])
        eliminar_url(id_url)
        await update.message.reply_text("Eliminado correctamente ✔️")
    except:
        await update.message.reply_text("Formato:\n/eliminar <id>")

async def cmd_scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    filas = obtener_urls()
    if not filas:
        await update.message.reply_text("No hay URLs para escanear.")
        return

    resp = "🔎 *Resultados del escaneo:*\n\n"

    for idu, url, tienda in filas:
        precio = obtener_precio(url)
        resp += f"{tienda}: {url}\nPrecio: {precio if precio else 'No detectado'}\n\n"

    await update.message.reply_text(resp)

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra la ayuda de comandos disponibles"""
    help_text = """
🤖 **Comandos disponibles:**

/start - Iniciar el bot
/agregar <url> <tienda> - Agregar producto a monitorear  
/listar - Ver productos en monitoreo
/eliminar <id> - Eliminar producto del monitoreo
/scan - Escanear precios actuales
/help - Mostrar esta ayuda

📝 **Ejemplos:**
/agregar https://ejemplo.com/producto amazon
/eliminar 1
/scan - para ver precios actuales

⚡ **Funcionalidad:**
El bot monitorea precios y detecta cambios importantes automáticamente.
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')
