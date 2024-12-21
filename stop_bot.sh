#!/bin/bash
# Encuentra el proceso asociado con el script y envía la señal SIGTERM
PID=$(pgrep -f tesla_bot_finnhub.py)
if [ -n "$PID" ]; then
  kill -SIGTERM "$PID"
  echo "Proceso detenido con éxito."
else
  echo "No se encontró ningún proceso ejecutándose."
fi
