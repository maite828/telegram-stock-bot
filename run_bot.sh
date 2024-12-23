#!/bin/bash

# Cambia al directorio donde se encuentra el script y sus dependencias
cd /Users/maytemati/maite828 || exit 1

# Verifica si el proceso ya está corriendo
if pgrep -f "tesla_bot_finnhub.py" > /dev/null
then
    echo "El bot ya está en ejecución. Saliendo..."
    exit 1
fi

# Activa el entorno virtual
source /Users/maytemati/maite828/myenv/bin/activate

# Ejecuta el bot
python tesla_bot_finnhub.py

