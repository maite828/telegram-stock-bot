#!/bin/bash

echo "Buscando proceso 'tesla_bot_finnhub.py'..."
PID=$(ps aux | grep 'python' | grep 'tesla_bot_finnhub.py' | grep -v grep | awk '{print $2}')

if [ -n "$PID" ]; then
  echo "Proceso encontrado con PID: $PID. Intentando detenerlo..."

  kill -SIGTERM "$PID"
  sleep 2

  if ps -p "$PID" > /dev/null; then
    echo "El proceso no respondió a SIGTERM. Forzando con SIGKILL..."
    kill -9 "$PID"
  fi

  if ! ps -p "$PID" > /dev/null; then
    echo "Proceso detenido con éxito."
  else
    echo "Error: No se pudo detener el proceso."
  fi
else
  echo "No se encontró ningún proceso ejecutándose con el nombre 'tesla_bot_finnhub.py'."
fi
