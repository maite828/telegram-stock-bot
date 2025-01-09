 │ #!/bin/bash
   2 │ 
   3 │ # Buscar el proceso por nombre
   4 │ echo "Buscando proceso 'tesla_bot_finnhub.py'..."
   5 │ PID=$(pgrep -f "tesla_bot_finnhub.py")
   6 │ 
   7 │ # Verificar si se encontró el proceso
   8 │ if [ -n "$PID" ]; then
   9 │   echo "Proceso encontrado con PID: $PID. Intentando detenerlo..."
  10 │   
  11 │   # Intentar detener con SIGTERM primero
  12 │   kill -SIGTERM "$PID"
  13 │   sleep 2
  14 │   
  15 │   # Verificar si sigue corriendo
  16 │   if ps -p "$PID" > /dev/null; then
  17 │     echo "El proceso no respondió a SIGTERM. Forzando con SIGKILL..."
  18 │     kill -9 "$PID"
  19 │   fi
  20 │ 
  21 │   # Verificar de nuevo si el proceso se detuvo
  22 │   if ! ps -p "$PID" > /dev/null; then
  23 │     echo "Proceso detenido con éxito."
  24 │   else
  25 │     echo "Error: No se pudo detener el proceso."
  26 │   fi
  27 │ else
  28 │   echo "No se encontró ningún proceso ejecutándose con el nombre 'tesla_bot_finnhub.py'."
  29 │ fi
