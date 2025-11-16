import os
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from commands import cmd_start, cmd_agregar, cmd_listar, cmd_eliminar, cmd_scan, cmd_help
from database import inicializar_db

async def main():
    """Función principal optimizada para Railway"""
    # Inicializar base de datos
    print("🔄 Inicializando base de datos...")
    inicializar_db()
    
    # Verificar token
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN no configurado")
    
    # Configurar bot
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Registrar comandos
    handlers = [
        CommandHandler("start", cmd_start),
        CommandHandler("agregar", cmd_agregar),
        CommandHandler("listar", cmd_listar),
        CommandHandler("eliminar", cmd_eliminar),
        CommandHandler("scan", cmd_scan),
        CommandHandler("help", cmd_help),
        MessageHandler(filters.TEXT & ~filters.COMMAND, cmd_help)
    ]
    
    for handler in handlers:
        application.add_handler(handler)
    
    print("🤖 Bot iniciado - Polling activo")
    print("✅ Listo para recibir mensajes...")
    
    # Iniciar polling
    await application.run_polling(
        drop_pending_updates=True,
        timeout=30,
        allowed_updates=['message', 'callback_query']
    )

if __name__ == "__main__":
    # Railway maneja asyncio perfectamente
    asyncio.run(main())
