import os
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from commands import cmd_start, cmd_agregar, cmd_listar, cmd_eliminar, cmd_scan, cmd_help
from database import inicializar_db

async def main():
    print("🚀 Price Glitch Bot - Oracle Cloud AMD")
    print("📍 IP: 161.153.204.231 - 24/7 Active")
    
    # Inicializar base de datos
    print("🔄 Inicializando base de datos...")
    inicializar_db()
    
    # Verificar token
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        print("❌ ERROR: BOT_TOKEN no configurado")
        print("💡 Ejecuta: export BOT_TOKEN='tu_token' o usa archivo .env")
        return
    
    print("✅ BOT_TOKEN encontrado")
    
    # Configurar aplicación de Telegram
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Registrar handlers
    application.add_handler(CommandHandler("start", cmd_start))
    application.add_handler(CommandHandler("agregar", cmd_agregar))
    application.add_handler(CommandHandler("listar", cmd_listar))
    application.add_handler(CommandHandler("eliminar", cmd_eliminar))
    application.add_handler(CommandHandler("scan", cmd_scan))
    application.add_handler(CommandHandler("help", cmd_help))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cmd_help))
    
    print("🤖 Bot ACTIVO en Oracle Cloud")
    print("✅ Comandos: /start, /agregar, /listar, /eliminar, /scan, /help")
    print("⏰ Servicio 24/7 - Esperando mensajes...")
    
    # Iniciar polling
    await application.run_polling(
        drop_pending_updates=True,
        allowed_updates=['message', 'callback_query']
    )

if __name__ == "__main__":
    asyncio.run(main())
