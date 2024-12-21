# Telegram Stock Bot

Este bot de Telegram te permite monitorear el precio de acciones en tiempo real y recibir notificaciones automáticas cuando el precio alcanza un valor objetivo.

## Características
- Monitoreo en tiempo real del precio de acciones usando `yfinance`.
- Notificaciones automáticas cuando el precio cae por debajo de un valor objetivo.
- Suscripción y desuscripción para recibir notificaciones.
- Comando para cambiar dinámicamente el precio objetivo desde Telegram.

## Requisitos
- Python 3.7 o superior.
- Bibliotecas de Python:
  - `python-telegram-bot`
  - `yfinance`

## Instalación
1. Clona este repositorio:
   ```bash
   git clone https://github.com/tuusuario/telegram-stock-bot.git
   cd telegram-stock-bot
   ```

2. Crea un entorno virtual y actívalo:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura el token del bot:
   - Obtén un token de BotFather en Telegram.
   - Reemplaza `TOKEN` en el script principal con tu token.

## Uso

### Comandos Disponibles
- `/start`: Inicia el bot y muestra un mensaje de bienvenida.
- `/subscribe`: Te suscribe a las notificaciones automáticas.
- `/unsubscribe`: Cancela tu suscripción a las notificaciones.
- `/settarget <valor>`: Cambia dinámicamente el precio objetivo para las notificaciones.

### Ejecución
Para ejecutar el bot:
```bash
python tesla_bot.py
```

El bot comenzará a monitorear el precio de las acciones y enviará notificaciones si el precio alcanza el valor objetivo configurado.

## Automatización
Si deseas automatizar la ejecución del bot a una hora específica cada día (por ejemplo, a las 15:00):

1. Crea un script bash llamado `run_bot.sh`:
   ```bash
   #!/bin/bash
   source /ruta/a/tu/entorno_virtual/myenv/bin/activate
   python /ruta/a/tu/script/tesla_bot.py
   ```

2. Hazlo ejecutable:
   ```bash
   chmod +x run_bot.sh
   ```

3. Agrega un cron job:
   ```bash
   crontab -e
   ```
   Añade esta línea al archivo para ejecutarlo todos los días a las 15:00:
   ```
   0 15 * * * /ruta/a/tu/script/run_bot.sh
   ```

## Contribuciones
Si deseas contribuir, abre un issue o envía un pull request con tus sugerencias.

## Licencia
Este proyecto está bajo la Licencia MIT. Puedes usarlo libremente con fines personales y comerciales.

