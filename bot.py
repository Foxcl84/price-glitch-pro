import os
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from commands import cmd_start, cmd_agregar, cmd_listar, cmd_eliminar, cmd_scan, cmd_help
from database import inicializar_db

async def main():
    print("🚀 Price Glitch Bot - Iniciando...")
    
    # Inicializar DB
    inicializar_db()
    print("✅ Base de datos lista")
    
    # Token
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        print("❌ Error: BOT_TOKEN no configurado")
        print("💡 Agrega BOT_TOKEN en las variables de entorno")
        return
    
    # Configurar bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Comandos
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("agregar", cmd_agregar))
    app.add_handler(CommandHandler("listar", cmd_listar))
    app.add_handler(CommandHandler("eliminar", cmd_eliminar))
    app.add_handler(CommandHandler("scan", cmd_scan))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cmd_help))
    
    print("🤖 Bot ACTIVO - Esperando mensajes...")
    await app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
