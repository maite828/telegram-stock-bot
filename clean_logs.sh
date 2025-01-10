#!/bin/bash

LOG_DIR="/var/services/homes/maite828/telegram_stock_bot"
LOG_FILE="$LOG_DIR/bot.log"

# 1) Rotar el log actual
#    Añadimos fecha al nombre para identificar cuándo se generó
if [ -f "$LOG_FILE" ]; then
  mv "$LOG_FILE" "$LOG_FILE.$(date +%Y%m%d%H%M)"
fi

# 2) Crear un archivo vacío para el nuevo log
: > "$LOG_FILE"

# 3) Borrar logs con más de 3 días de antigüedad
#    Se asume que todos los archivos "bot.log.*" son logs rotados
find "$LOG_DIR" -type f -name "bot.log.*" -mtime +3 -exec rm -f {} \;

echo "Rotación completada. Logs antiguos (>3 días) eliminados."
