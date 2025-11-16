import os
import asyncio
import sys
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

from commands import cmd_start, cmd_agregar, cmd_listar, cmd_eliminar, cmd_scan, cmd_help
from database import inicializar_db

# Cargar variables de entorno
load_dotenv()

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
        print("💡 Verifica el archivo .env")
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

    # Iniciar polling - método simplificado
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    # Mantener el bot corriendo
    try:
        while True:
            await asyncio.sleep(3600)  # Esperar 1 hora
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo bot...")
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()

if __name__ == "__main__":
    # Crear nuevo event loop explícitamente
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n✅ Bot detenido correctamente")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        loop.close()
