#!/bin/bash

# Verifica si el proceso ya está corriendo
if pgrep -f "tesla_bot_finnhub.py" > /dev/null
then
    echo "El bot ya está en ejecución. Saliendo..."
    exit 1
fi

# Activa el entorno virtual
source /Users/maytemati/maite828/myenv/bin/activate

# Ejecuta el bot
python /Users/maytemati/maite828/tesla_bot_finnhub.py

