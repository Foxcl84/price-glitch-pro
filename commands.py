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
        await update.message.reply_text("✅ URL agregada correctamente")
    except:
        await update.message.reply_text("❌ Formato correcto:\n/agregar <url> <tienda>")

async def cmd_listar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    filas = obtener_urls()
    if not filas:
        await update.message.reply_text("📭 No hay URLs registradas.")
        return

    texto = "📌 *Productos registrados:*\n\n"
    for fila in filas:
        texto += f"🆔 ID: {fila[0]}\n🔗 {fila[1]}\n🏪 TIENDA: {fila[2]}\n\n"

    await update.message.reply_text(texto)

async def cmd_eliminar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        id_url = int(context.args[0])
        eliminar_url(id_url)
        await update.message.reply_text("✅ Eliminado correctamente")
    except:
        await update.message.reply_text("❌ Formato correcto:\n/eliminar <id>")

async def cmd_scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Escanea precios de todos los productos registrados - Versión Mejorada"""
    try:
        # Mensaje de que se está procesando
        mensaje_espera = await update.message.reply_text("🔄 Escaneando precios... Esto puede tomar unos segundos.")
        
        filas = obtener_urls()
        if not filas:
            await mensaje_espera.edit_text("📭 No hay URLs registradas para escanear.")
            return

        resultados = []
        total = len(filas)
        completados = 0
        
        for idu, url, tienda in filas:
            # Mostrar progreso
            completados += 1
            await mensaje_espera.edit_text(f"🔍 Escaneando ({completados}/{total}): {tienda}...")
            
            precio = obtener_precio(url)
            
            if precio:
                # Formatear precio con separadores de miles
                precio_formateado = f"${precio:,.0f}".replace(",", ".")
                resultados.append(f"🏪 *{tienda}*\n💰 {precio_formateado}\n🔗 {url[:50]}...")
                print(f"✅ {tienda}: ${precio}")
            else:
                resultados.append(f"🏪 *{tienda}*\n❌ Precio no detectado\n🔗 {url[:50]}...")
                print(f"❌ {tienda}: Precio no detectado")

        # Construir mensaje final
        if resultados:
            respuesta = "🔎 *Resultados del Escaneo:*\n\n" + "\n\n".join(resultados)
            
            # Estadísticas
            precios_detectados = sum(1 for r in resultados if "💰" in r)
            respuesta += f"\n\n📊 *Resumen:* {precios_detectados}/{total} precios detectados"
            
            # Dividir en mensajes si es muy largo
            if len(respuesta) > 4000:
                partes = [respuesta[i:i+4000] for i in range(0, len(respuesta), 4000)]
                for i, parte in enumerate(partes):
                    if i == 0:
                        await mensaje_espera.edit_text(parte, parse_mode='Markdown')
                    else:
                        await update.message.reply_text(parte, parse_mode='Markdown')
            else:
                await mensaje_espera.edit_text(respuesta, parse_mode='Markdown')
        else:
            await mensaje_espera.edit_text("❌ No se pudieron obtener precios en este momento.")

    except Exception as e:
        error_msg = f"❌ Error durante el escaneo: {str(e)}"
        print(error_msg)
        await update.message.reply_text(error_msg)

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
