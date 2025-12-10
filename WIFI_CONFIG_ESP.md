# Proceso de Configuración WiFi en ESP32-S3 CAM

## Descripción General

El módulo WiFi de la cámara ESP32-S3 CAM permite configurar las credenciales de red WiFi a través de una interfaz web en modo Access Point (AP). Este documento describe el proceso de configuración, guardado de credenciales y reinicio automático del dispositivo.

## Flujo de Configuración WiFi

### 1. Modo Access Point (AP)

- Al iniciar, si no existen credenciales guardadas o si la conexión a la red WiFi falla, el dispositivo entra en modo AP.
- El dispositivo crea una red WiFi con el nombre `ESP32-CAM-Setup` y contraseña `123456789`.
- El servidor web está disponible en la IP: `192.168.4.1`.

### 2. Interfaz de Configuración

- Accediendo a `http://192.168.4.1` desde un navegador, se puede acceder a la interfaz de configuración WiFi. ¡ADVERTENCIA!; Solo usar "http" no funcionará con "https", no ha sido implementada ninguna seguridad avanzada.
- La interfaz permite:
  - Seleccionar una red WiFi de las disponibles
  - Introducir manualmente un nombre de red (SSID)
  - Introducir la contraseña de la red WiFi

### 3. Guardado de Credenciales

- Al hacer clic en el botón "Conectar", las credenciales se envían al dispositivo vía una solicitud POST a `/configure`.
- El dispositivo procesa las credenciales y las guarda en el archivo `ssid_config.json`.
- El archivo `ssid_config.json` contiene:
  - `ssid`: nombre de la red WiFi
  - `password`: contraseña de la red WiFi
  - `configured`: booleano que indica si las credenciales han sido configuradas

### 4. Respuesta y Reinicio Automático

- Tras guardar las credenciales exitosamente, el dispositivo responde con una página web que:
  - Confirma que las credenciales se han guardado exitosamente
  - Muestra el nombre de la red WiFi a la que se conectará
  - Indica que el dispositivo se reiniciará en 15 segundos
- El dispositivo se reinicia automáticamente después de 15 segundos
- Si se accede a la URL `/restart`, el dispositivo reinicia inmediatamente

## Detalles Técnicos del Reinicio

Después de guardar las credenciales, la página de confirmación incluye:

- Un script JavaScript que redirige automáticamente a `/restart` después de 15 segundos
- Un mensaje visual indicando el tiempo restante antes del reinicio
- El reinicio físico del dispositivo se ejecuta mediante la función `reset()` de MicroPython

## Manejo de Errores

- En caso de que el nombre de la red (SSID) contenga caracteres especiales, estos se escapan adecuadamente para evitar problemas de visualización o interpretación HTML
- Si ocurre un error al enviar la respuesta HTML completa, se envía una versión más simple como respaldo
- El sistema maneja adecuadamente solicitudes duplicadas o solicitudes GET a la ruta `/configure` después del envío de credenciales

## Archivos Involucrados

- `wifi_manager.py`: Contiene el módulo principal de gestión WiFi, incluyendo el servidor web y la lógica de configuración
- `ssid_config.json`: Archivo donde se almacenan las credenciales WiFi
- `main.py`: Archivo principal que coordina los módulos y maneja el reinicio en caso de error

## Consideraciones de Seguridad

- La configuración WiFi se realiza en modo AP local, por lo que no hay encriptación HTTPS en este paso inicial
- La contraseña del AP es por defecto `123456789`, y se recomienda usarla solo temporalmente durante la configuración
- Las credenciales WiFi se almacenan en texto plano en el archivo `ssid_config.json`, lo cual es aceptable para dispositivos embebidos locales

## Notas para Desarrolladores

### Código Relevante:

La lógica de configuración WiFi se encuentra principalmente en la clase `WiFiManager` en `wifi_manager.py`, específicamente en el método `start_web_server()` y la sección que maneja la ruta `/configure`.

### Mejoras Futuras:

- Implementar validación adicional de credenciales antes de guardar
- Agregar mecanismo de timeout en caso de que las credenciales no sean correctas
- Potencial implementación de un fallback si la conexión WiFi falla repetidamente