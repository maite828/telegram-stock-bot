# -*- coding: utf-8 -*-

import json
import signal
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
import requests

logging.basicConfig(level=logging.INFO)

# Configuración inicial desde JSON
CONFIG_FILE = 'config.json'

# Cargar configuraciones desde JSON
with open(CONFIG_FILE, 'r') as file:
    config = json.load(file)

TOKEN = config['bot_token']
FINNHUB_API_KEY = config['finnhub_api_key']
FINNHUB_URL = config['finnhub_url']
USER_ID = config['user_id']

# Inicializar configuraciones de acciones
stocks = config['stocks']

# Aplicación de Telegram
application = None

# Comando de inicio
async def start(update: Update, context):
    summary = "Hola, soy tu bot de acciones.\n"
    summary += "Estas son las acciones que estás siguiendo:\n"

    for stock, details in stocks.items():
        summary += (
            f"\nAcción: {stock}\n"
            f"Precio objetivo inferior: ${details['target_price']:.2f}\n"
            f"Precio objetivo superior: ${details['upper_price']:.2f}\n"
        )

    await update.message.reply_text(summary)

# Comando para agregar una nueva acción
async def add_stock(update: Update, context):
    try:
        symbol = context.args[0].upper()
        target_price = float(context.args[1])
        upper_price = float(context.args[2])

        if symbol in stocks:
            await update.message.reply_text(f"La acción {symbol} ya está configurada.")
        else:
            stocks[symbol] = {
                "target_price": target_price,
                "upper_price": upper_price
            }
            save_config()
            await update.message.reply_text(f"La acción {symbol} se ha añadido con éxito.")
    except (IndexError, ValueError):
        await update.message.reply_text("Uso: /addstock <símbolo> <precio_inferior> <precio_superior>")

# Comando para actualizar precios objetivo de una acción existente
async def set_prices(update: Update, context):
    try:
        symbol = context.args[0].upper()
        target_price = float(context.args[1])
        upper_price = float(context.args[2])

        if symbol in stocks:
            stocks[symbol]["target_price"] = target_price
            stocks[symbol]["upper_price"] = upper_price
            save_config()
            await update.message.reply_text(f"Los precios de {symbol} se han actualizado.")
        else:
            await update.message.reply_text(f"La acción {symbol} no está configurada.")
    except (IndexError, ValueError):
        await update.message.reply_text("Uso: /setprices <símbolo> <precio_inferior> <precio_superior>")

# Verificación del precio y generación de alertas
async def check_prices():
    try:
        for stock, details in stocks.items():
            params = {
                "symbol": stock,
                "token": FINNHUB_API_KEY
            }
            response = requests.get(FINNHUB_URL, params=params)
            data = response.json()

            if "c" in data:  # 'c' es el precio actual en Finnhub
                price = data["c"]

                if price <= details["target_price"]:
                    await application.bot.send_message(
                        chat_id=USER_ID,
                        text=f"\u00a1Alerta! {stock} ha caído a ${price:.2f}, por debajo de ${details['target_price']:.2f}."
                    )

                if price >= details["upper_price"]:
                    await application.bot.send_message(
                        chat_id=USER_ID,
                        text=f"\u00a1Alerta! {stock} ha subido a ${price:.2f}, por encima de ${details['upper_price']:.2f}."
                    )
            else:
                logging.error(f"No se encontraron datos válidos para {stock}. Respuesta: {data}")
    except Exception as e:
        logging.error(f"Error al consultar los precios: {e}")

# Resumen diario de todas las acciones
async def fetch_daily_summary():
    try:
        summary = "Resumen inicial de todas las acciones configuradas:\n"

        for stock, details in stocks.items():
            params = {
                "symbol": stock,
                "token": FINNHUB_API_KEY
            }
            response = requests.get(FINNHUB_URL, params=params)
            data = response.json()

            if "c" in data:  # 'c' es el precio actual en Finnhub
                closing_price_previous_day = data.get("pc", "N/A")  # Precio de cierre día anterior
                open_price = data.get("o", "N/A")  # Precio de apertura
                high_price = data.get("h", "N/A")  # Precio más alto del día
                low_price = data.get("l", "N/A")  # Precio más bajo del día
                latest_price = data["c"]

                summary += (
                    f"\nAcción: {stock}\n"
                    f"Precio de cierre día anterior: ${closing_price_previous_day}\n"
                    f"Precio de apertura: ${open_price}\n"
                    f"Precio más alto: ${high_price}\n"
                    f"Precio más bajo: ${low_price}\n"
                    f"\u00daltimo precio: ${latest_price:.2f}\n"
                )
            else:
                summary += f"\nAcción: {stock}\nNo se encontraron datos válidos.\n"

        await application.bot.send_message(chat_id=USER_ID, text=summary)
    except Exception as e:
        logging.error(f"Error al obtener el resumen diario: {e}")

# Guardar configuraciones en JSON
def save_config():
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)

# Verificación periódica
async def periodic_check():
    while not asyncio.get_event_loop().is_closed():
        await check_prices()
        await asyncio.sleep(60)  # Verificar cada 60 segundos

# Manejador de señales para detener el bot de forma limpia
def handle_exit_signal(signal, frame):
    logging.info("Recibida señal para detener el bot.")
    loop = asyncio.get_event_loop()
    loop.stop()

# Configuración principal del bot
def main():
    global application
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addstock", add_stock))
    application.add_handler(CommandHandler("setprices", set_prices))

    signal.signal(signal.SIGINT, handle_exit_signal)
    signal.signal(signal.SIGTERM, handle_exit_signal)

    loop = asyncio.get_event_loop()
    loop.create_task(fetch_daily_summary())  # Enviar el resumen inicial al iniciar el bot
    loop.create_task(periodic_check())

    application.run_polling()

if __name__ == '__main__':
    main()
