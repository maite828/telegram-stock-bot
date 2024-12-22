# -*- coding: utf-8 -*-

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
import yfinance as yf
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

# Token del bot
TOKEN = 'TOKEN TELEGRAM'

# Valores objetivos
TARGET_PRICE = 422.0  # Notificación si el precio está por debajo
UPPER_TARGET = 445.0  # Notificación si el precio está por encima
STOCK = "TSLA"

# Lista de usuarios suscritos
subscribed_users = {CHAT ID TELEGRAM}

# Comando de inicio
async def start(update: Update, context):
    await update.message.reply_text(
        "Hola, soy tu bot de acciones.\n"
        "Usa /subscribe para recibir notificaciones automáticas.\n"
        "Usa /settarget <valor> para cambiar el precio objetivo inferior.\n"
        "Usa /setupper <valor> para cambiar el precio objetivo superior."
    )

# Comando para cambiar el precio objetivo inferior
async def set_target(update: Update, context):
    global TARGET_PRICE
    try:
        new_target = float(context.args[0])
        TARGET_PRICE = new_target
        await update.message.reply_text(f"El precio objetivo inferior se ha actualizado a ${TARGET_PRICE:.2f}.")
    except (IndexError, ValueError):
        await update.message.reply_text("Por favor, proporciona un número válido. Uso: /settarget <valor>")

# Comando para cambiar el precio objetivo superior
async def set_upper(update: Update, context):
    global UPPER_TARGET
    try:
        new_upper = float(context.args[0])
        UPPER_TARGET = new_upper
        await update.message.reply_text(f"El precio objetivo superior se ha actualizado a ${UPPER_TARGET:.2f}.")
    except (IndexError, ValueError):
        await update.message.reply_text("Por favor, proporciona un número válido. Uso: /setupper <valor>")

# Verificación del precio
async def check_price():
    try:
        stock = yf.Ticker(STOCK)
        data = stock.history(period="1d", interval="1m")
        if not data.empty:
            price = data.iloc[-1]['Close']
            for user_id in subscribed_users:
                if price <= TARGET_PRICE:
                    await application.bot.send_message(
                        chat_id=user_id,
                        text=f"¡Alerta! {STOCK} ha caído a ${price:.2f}, por debajo de tu objetivo de ${TARGET_PRICE:.2f}."
                    )
                if price >= UPPER_TARGET:
                    await application.bot.send_message(
                        chat_id=user_id,
                        text=f"¡Alerta! {STOCK} ha subido a ${price:.2f}, por encima de tu objetivo de ${UPPER_TARGET:.2f}."
                    )
        else:
            logging.error(f"No se encontraron datos para {STOCK}.")
    except Exception as e:
        logging.error(f"Error al consultar el precio: {e}")

# Verificación periódica
async def periodic_check():
    while True:
        await check_price()
        await asyncio.sleep(60)

# Configuración principal del bot
def main():
    global application
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("settarget", set_target))
    application.add_handler(CommandHandler("setupper", set_upper))

    loop = asyncio.get_event_loop()
    loop.create_task(periodic_check())

    application.run_polling()

if __name__ == '__main__':
    main()
