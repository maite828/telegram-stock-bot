
# Telegram Stock Bot

Este bot de Telegram te permite monitorear el precio de acciones en tiempo real y recibir notificaciones automáticas cuando el precio alcanza un valor objetivo definido, ya sea por encima o por debajo del precio.

## Características

- **Monitoreo en tiempo real**: Utiliza `finnhub` para obtener precios actualizados.
- **Resumen inicial**: Al iniciar el script, el bot envía un resumen de todas las acciones configuradas con datos clave (apertura, cierre, volumen, etc.).
- **Alertas de precios**: Notificaciones automáticas cuando el precio sube por encima o baja por debajo de los valores configurados.
- **Gestión dinámica desde Telegram**:
  - Agregar nuevas acciones para monitorear.
  - Actualizar precios objetivo de acciones existentes.
- **Persistencia**: Configuraciones guardadas automáticamente en un archivo JSON.

## Requisitos

- **Python 3.7** o superior.
- Bibliotecas de Python:
  - `python-telegram-bot`
  - `requests`

## Instalación

1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/maite828/telegram-stock-bot.git
   cd telegram-stock-bot
   ```

2. **Crea y activa un entorno virtual**:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   ```
   **En caso de querer desactivar entorno virtual**:
   ```bash
   deactivate
   ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura el archivo `config.json`**:
   - Obtén un token de BotFather en Telegram.
   - Obtén una API Key de Finnhub en caso de decidir este script. 
   - Configura tus acciones iniciales para monitorear (consulta el ejemplo más abajo).

## Uso

### Comandos Disponibles

- **`/start`**: Muestra un resumen inicial con todas las acciones configuradas.
- **`/addstock <símbolo> <precio_inferior> <precio_superior>`**: Agrega una nueva acción para monitorear.
  - Ejemplo:
    ```plaintext
    /addstock AAPL 150 170
    ```
- **`/setprices <símbolo> <precio_inferior> <precio_superior>`**: Actualiza los precios objetivo de una acción existente.
  - Ejemplo:
    ```plaintext
    /setprices TSLA 400 450
    ```

## Ejecución

Para iniciar el bot y probar:
```bash
python tesla_bot_finnhub.py
```

Al ejecutarlo:
1. **Envía un resumen inicial**: Datos de todas las acciones configuradas, como:
   - Precio de cierre del día anterior.
   - Precio de apertura.
   - Precio más alto y más bajo del día.
   - Último valor.
2. **Monitorea precios en tiempo real**: Envía notificaciones cuando se cumplen las condiciones configuradas.

## Configuración de `config.json`

Crea un archivo `config.json` con el siguiente formato:

```json
{
  "bot_token": "TU_TOKEN_DE_TELEGRAM",
  "finnhub_api_key": "TU_API_KEY_DE_FINNHUB",
  "finnhub_url": "https://finnhub.io/api/v1/quote",
  "user_id": 123456789,
  "stocks": {
    "TSLA": {
      "target_price": 422.0,
      "upper_price": 445.0
    },
    "AAPL": {
      "target_price": 150.0,
      "upper_price": 170.0
    }
  }
}
```

## ¿Cómo actualizar configuraciones desde Telegram?

### 1. **Agregar una nueva acción**
Comando:
```plaintext
/addstock <símbolo> <precio_inferior> <precio_superior>
```
Ejemplo:
```plaintext
/addstock MSFT 300 350
```
Resultado:
- La acción `MSFT` se agrega con los precios objetivo especificados.

### 2. **Actualizar precios objetivo**
Comando:
```plaintext
/setprices <símbolo> <precio_inferior> <precio_superior>
```
Ejemplo:
```plaintext
/setprices TSLA 400 450
```
Resultado:
- Los precios objetivo de `TSLA` se actualizan automáticamente.

### 3. **Ver un resumen inicial**
Usa el comando:
```plaintext
/start
```
Resultado:
- Un mensaje detallado con todas las acciones configuradas.

## Automatización del Bot

### Configura Cron Jobs
1. **Inicio del Bot**:
   Programa el inicio del bot a las 14:15 de lunes a viernes:
   ```bash
   15 15 * * 1-5 /ruta/a/run_bot.sh
   ```

2. **Detención del Bot**:
   Programa la detención del bot a las 22:01 de lunes a viernes:
   ```bash
   1 22 * * 1-5 /ruta/a/stop_bot.sh
   ```

Para verificar los cron jobs configurados:
```bash
crontab -l
```

## Solución de Problemas

- **No llegan notificaciones**:
  - Asegúrate de que el símbolo de la acción sea válido.
  - Verifica que el mercado esté abierto.
- **Logs del bot**:
  - Habilita los logs en el script:
    ```python
    logging.basicConfig(level=logging.INFO)
    ```

## Contribuciones

Si deseas contribuir, abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Puedes usarlo libremente con fines personales y comerciales.

