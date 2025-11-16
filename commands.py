async def cmd_ayuda(update, context):
    texto = (
        "📌 *Comandos Disponibles*\n\n"
        "/start - Inicia el bot\n"
        "/agregar <url> <precio_min> - Agrega un producto\n"
        "/listar - Lista los productos monitoreados\n"
        "/eliminar <id> - Elimina un producto\n"
        "/ayuda - Muestra esta ayuda\n"
    )

    await update.message.reply_text(texto, parse_mode="Markdown")

