from telegram import Update
from telegram.ext import ContextTypes
from database import insertar_url, obtener_urls, eliminar_url, reset_urls

ADMIN_ID = 0

async def cmd_agregar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("❌ No estás autorizado.")
    if len(context.args) < 2:
        return await update.message.reply_text("Uso correcto:\n/agregar tienda URL")
    tienda = context.args[0].strip().lower()
    url = context.args[1].strip()
    new_id = insertar_url(tienda, url)
    await update.message.reply_text(f"✔ URL agregada\nID: {new_id}\n{tienda} → {url}")

async def cmd_listar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("❌ No estás autorizado.")
    urls = obtener_urls()
    if not urls:
        return await update.message.reply_text("📭 No hay URLs registradas.")
    texto = "📌 URLs monitoreadas:\n\n"
    for u in urls:
        texto += f"{u['id']} → {u['tienda']} → {u['url']}\n"
    await update.message.reply_text(texto)

async def cmd_eliminar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("❌ No estás autorizado.")
    if len(context.args) != 1:
        return await update.message.reply_text("Uso: /eliminar ID")
    try:
        id_url = int(context.args[0])
    except:
        return await update.message.reply_text("❌ ID inválido")
    eliminar_url(id_url)
    await update.message.reply_text(f"🗑 Eliminado ID {id_url}")

async def cmd_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("❌ No estás autorizado.")
    reset_urls()
    await update.message.reply_text("🔄 URLs reseteadas.")
