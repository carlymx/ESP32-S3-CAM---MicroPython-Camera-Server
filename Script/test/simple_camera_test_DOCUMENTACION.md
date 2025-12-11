# Documentación: `simple_camera_test.py`

## 📋 Descripción General

Script simple de prueba para la cámara **ESP32-S3 CAM (AI Thinker)**. Su objetivo es verificar que:

1. **El ESP32-S3 reconoce la cámara** (hardware y firmware)
2. **La cámara captura imágenes** correctamente
3. **Podemos ver lo que captura** a través de un servidor web

**Características clave:**

- Todo en un solo archivo `.py` (sin dependencias externas)
- Configuración WiFi mediante variables editables
- Inicialización de cámara con configuración compatible óptima
- Servidor web con página HTML embebida y streaming de imagen JPEG
- Manejo robusto de errores y Watchdog Timer (WDT)

---

## 🏗️ Contexto del Proyecto

Este script forma parte del proyecto **MicroPython Camera ESP32-S3** ubicado en `/home/carly/Documentos/CLI/camara/`. El proyecto principal tiene una arquitectura modular, pero este script es una versión **independiente y simplificada** creada específicamente para pruebas rápidas.

**Relación con el proyecto principal:**

- Usa la misma **API de cámara MicroPython** (`camera` module)
- Configuración de pines basada en `camera_pins.py` del proyecto
- Similar enfoque de streaming que `video_server.py` (pero simplificado)
- **Diferencia clave**: No usa módulos externos, todo está embebido

---

## 🔧 Requisitos Previos

### Hardware

- **ESP32-S3 CAM** (AI Thinker) con PSRAM
- Conexiones de cámara correctamente soldadas
- Alimentación estable (≥500mA recomendado)

### Firmware

- **MicroPython** con soporte de cámara (API v0.5.0+)
- Módulo `camera` compilado en el firmware
- Módulos estándar: `network`, `socket`, `machine`, `gc`, `time`

### Software

- Editor para modificar variables WiFi
- Herramienta para subir archivos (ampy, rshell, Thonny)
- Navegador web para visualizar stream

---

## ⚙️ Configuración

### Variables Editables (líneas 27-28)

```python
WIFI_SSID = "tu_red_wifi"        # CAMBIAR: nombre de tu red WiFi
WIFI_PASSWORD = "tu_password"    # CAMBIAR: contraseña de tu red WiFi
```

### Configuración de Cámara (líneas 31-47)

```python
CAMERA_CONFIG = {
    'data_pins': [5, 18, 19, 21, 36, 39, 34, 35],  # D0-D7
    'pclk_pin': 22,    # PCLK
    'vsync_pin': 25,   # VSYNC
    'href_pin': 23,    # HREF
    'sda_pin': 26,     # SDA (I2C)
    'scl_pin': 27,     # SCL (I2C)
    'xclk_pin': 0,     # XCLK
    'xclk_freq': 20000000,  # 20MHz para OV2640
    'powerdown_pin': 32,    # PWDN
    'reset_pin': -1,        # No usar reset
    'pixel_format': 4,      # PixelFormat.JPEG (valor 4)
    'frame_size': 10,       # FrameSize.VGA (640x480)
    'jpeg_quality': 85,     # Calidad JPEG (0-100)
    'fb_count': 2,          # 2 buffers para mejor rendimiento
    'grab_mode': 1,         # GrabMode.LATEST
}
```

**Nota sobre pines**: Esta configuración es para **ESP32-S3 CAM AI Thinker**. Si tienes otro modelo, consulta `micropython-camera-API-documentation.md`.

---

## 🏗️ Estructura del Código

### Secciones Principales

```
1. IMPORTS (19-23)           # Módulos MicroPython
2. CONFIGURACIÓN (27-47)     # Variables editables
3. FUNCIONES WIFI (51-91)    # Conexión WiFi
4. FUNCIONES CÁMARA (95-149) # Inicialización cámara
5. HTML EMBEBIDO (153-244)   # Página web completa
6. SERVIDOR HTTP (248-333)   # Manejo de conexiones
7. FUNCIÓN PRINCIPAL (337-387) # Orquestación
8. EJECUCIÓN (391-403)       # Punto de entrada
```

### Flujo de Ejecución

```mermaid
graph TD
    A[main()] --> B[Verificar credenciales WiFi]
    B --> C[Conectar a WiFi]
    C --> D{¿WiFi OK?}
    D -->|Sí| E[Inicializar cámara]
    D -->|No| F[Mostrar error/continuar sin WiFi]
    E --> G{¿Cámara OK?}
    G -->|Sí| H[Ejecutar servidor web]
    G -->|No| I[Mostrar error/salir]
    H --> J[Esperar conexiones HTTP]
    J --> K[Manejar peticiones]
    K --> L[/stream o /]
    L --> M[Servir imagen o HTML]
    M --> J
```

---

## 📡 Funciones Clave

### 1. `connect_wifi(ssid, password)` (líneas 51-91)

**Propósito**: Conectar a red WiFi
**Parámetros**: 

- `ssid`: Nombre de la red
- `password`: Contraseña
  **Retorno**: `True` si éxito, `False` si falla
  **Características**:
- Timeout de 20 segundos
- Desactiva modo AP si está activo
- Manejo de excepciones específicas (OSError)

### 2. `init_camera()` (líneas 95-149)

**Propósito**: Inicializar cámara con configuración óptima
**Retorno**: Objeto `Camera` o `None` si falla
**Características**:

- WDT extendido (10 segundos) para inicialización
- Verificación de sensor (`get_sensor_name()`)
- Información de resolución y formato
- Limpieza de recursos en `finally`

### 3. `handle_client(cl, addr, cam)` (líneas 248-288)

**Propósito**: Manejar peticiones HTTP
**Endpoints**:

- `GET /` o `GET /index`: Página HTML embebida
- `GET /stream`: Imagen JPEG capturada
- Otros: 404 Not Found
  **Características**:
- Envío de bytes (compatible MicroPython)
- Manejo de errores en captura de imagen

### 4. `run_mjpeg_server(cam, port=80)` (líneas 290-333)

**Propósito**: Servidor HTTP principal
**Características**:

- Timeout en `accept()` (0.5 segundos)
- WDT de operación normal (2 segundos)
- Alimentación WDT tras cada conexión
- Limpieza de socket y cámara en `finally`

### 5. `main()` (líneas 337-387)

**Propósito**: Orquestar todo el proceso
**Flujo**:

1. Verificar credenciales WiFi
2. Conectar WiFi (con diagnóstico si falla)
3. Inicializar cámara (con diagnóstico si falla)
4. Ejecutar servidor web
5. Limpiar recursos al finalizar

---

## 🌐 Endpoints HTTP

### `GET /` o `GET /index`

**Respuesta**: HTML embebido con:

- Página con estilo dark theme
- Imagen que auto-refresca cada 500ms
- Información del sistema
- Botón de recarga manual

### `GET /stream`

**Respuesta**: Imagen JPEG capturada en tiempo real
**Headers**:

```
HTTP/1.1 200 OK
Content-Type: image/jpeg
Connection: close
```

**Cuerpo**: Bytes JPEG de la captura actual

### Otros endpoints

**Respuesta**: `404 Not Found` con HTML simple

---

## 🎨 HTML Embebido

### Características

- **Totalmente auto-contenido**: CSS y JavaScript inline
- **Auto-refresh**: 500ms (2 FPS aproximados)
- **Responsive**: Se adapta a diferentes tamaños de pantalla
- **Dark theme**: Fácil en la vista
- **Información útil**: Resolución, formato, FPS

### JavaScript

```javascript
// Auto-refresh cada 500ms
setInterval(function() {
    var img = document.getElementById('video');
    img.src = '/stream?t=' + new Date().getTime();
}, 500);
```

**Nota**: El parámetro `?t=` evita cache del navegador.

---

## ⚠️ Manejo de Errores y WDT

### Watchdog Timer (WDT)

| Situación             | Timeout                   | Propósito                         |
| --------------------- | ------------------------- | --------------------------------- |
| Inicialización cámara | 10000ms (10s)             | Dar tiempo a inicialización lenta |
| Operación normal      | 2000ms (2s)               | Detectar bloqueos en servidor     |
| Conexión WiFi         | Alimentación cada segundo | Evitar reinicios durante espera   |

### Manejo de Excepciones

```python
try:
    # Código que puede fallar
except ImportError:
    # Módulo 'camera' no disponible
except OSError:
    # Error de red/hardware
except Exception:
    # Error genérico (último recurso)
finally:
    # Limpieza de recursos (siempre se ejecuta)
```

### Diagnóstico de Fallos

El script proporciona mensajes descriptivos para:

- Credenciales WiFi no configuradas
- Fallo de conexión WiFi (con causas posibles)
- Fallo de inicialización de cámara (3 causas comunes)
- Errores de red en servidor

---

## 🔧 Solución de Problemas

### 1. "Módulo 'camera' no disponible"

**Causas**:

- Firmware sin soporte de cámara
- API de cámara no compilada
- Módulo con nombre diferente

**Soluciones**:

- Usar firmware precompilado con soporte de cámara
- Verificar `import camera` en REPL
- Consultar `micropython-camera-API-documentation.md`

### 2. "No se pudo conectar a WiFi"

**Causas**:

- Credenciales incorrectas
- Red fuera de alcance
- Configuración de red incompatible

**Soluciones**:

- Verificar `WIFI_SSID` y `WIFI_PASSWORD`
- Asegurar ESP32-S3 en rango de red
- Probar con red 2.4GHz (no 5GHz)

### 3. "Error al inicializar la cámara"

**Causas**:

- Pines incorrectos para tu hardware
- Problemas de alimentación
- Sensor de cámara defectuoso/mal conectado

**Soluciones**:

- Verificar pines en `CAMERA_CONFIG`
- Asegurar alimentación estable (≥500mA)
- Revisar conexiones físicas de la cámara

### 4. Servidor web no responde

**Causas**:

- Firewall bloqueando puerto 80
- IP incorrecta
- Script no en ejecución

**Soluciones**:

- Verificar IP en consola (después de "Conectado a WiFi")
- Probar `ping <IP>`
- Revisar si script sigue ejecutándose (REPL)

---

## 🚀 Posibles Mejoras/Extensiones

### Para futuras iteraciones con IA:

1. **Streaming MJPEG verdadero**
   
   ```python
   # En lugar de un frame, enviar múltiples frames con boundary
   cl.send(b'Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n')
   while True:
       cl.send(b'--frame\r\n')
       cl.send(b'Content-Type: image/jpeg\r\n\r\n')
       cl.send(cam.capture())
       cl.send(b'\r\n')
   ```

2. **Configuración vía web**
   
   - Formulario para cambiar WiFi sin editar código
   - Interfaz para ajustar parámetros de cámara

3. **Dual-core con `_thread`**
   
   ```python
   import _thread
   _thread.start_new_thread(capture_loop, ())
   _thread.start_new_thread(server_loop, ())
   ```

4. **Soporte para mock camera**
   
   ```python
   try:
       from camera import Camera
   except ImportError:
       from camera_mock import Camera
   ```

5. **Métricas y logging**
   
   - FPS en tiempo real
   - Uso de memoria
   - Temperatura CPU

6. **Seguridad básica**
   
   - Password para acceso web
   - HTTPS básico (si MicroPython lo soporta)

7. **API REST**
   
   - `GET /api/status`: Estado del sistema
   - `POST /api/config`: Cambiar configuración
   - `GET /api/stats`: Métricas de rendimiento

---

## 📚 Referencias

### Documentación del Proyecto

- `../micropython-camera-API-documentation.md` - API completa de cámara
- `../QWEN.md` - Contexto y mejoras del proyecto
- `../README.md` - Descripción general del proyecto

### Archivos Relacionados

- `../video_server.py` - Servidor de video completo
- `../camera_utils.py` - Inicialización centralizada de cámara
- `../camera_pins.py` - Definiciones de pines
- `../camera_mock.py` - Simulación de cámara

### Enlaces Externos

- [MicroPython Camera API v0.5.0](https://github.com/cnadler86/micropython-camera-API/releases/tag/v0.5.0)
- [ESP32-S3 CAM AI Thinker Pinout](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/hw-reference/esp32s3/user-guide-esp32-s3-cam.html)

---

## 💡 Notas para Futuros Desarrolladores/IA

### Filosofía del Script

- **Simple sobre complejo**: Una sola función por responsabilidad
- **Robusto sobre elegante**: Manejo de errores > código limpio
- **Práctico sobre teórico**: Funciona en hardware real

### Decisiones de Diseño

1. **No usar módulos externos**: Todo embebido para portabilidad
2. **WDT extendido en inicialización**: Problema conocido con ESP32-S3
3. **HTML con auto-refresh**: Más simple que streaming MJPEG real
4. **Reinicio automático**: Mejor que quedarse en estado inconsistente

### Convenciones de Código

- **Comentarios en castellano**: Coherencia con proyecto principal
- **Nombres descriptivos**: `connect_wifi` no `wifi_conn`
- **Manejo explícito de bytes**: `b'string'` para compatibilidad
- **Excepciones específicas**: `OSError` sobre `Exception` genérico

### Para Modificaciones

- **Prueba WiFi primero**: Si falla, el script es inútil
- **Mantén WDT alimentado**: O se reiniciará inesperadamente
- **Limpia recursos**: `deinit()` cámara, `close()` sockets
- **Provee diagnóstico**: Mensajes útiles para debugging

---

## 📊 Esquema de Versiones

| Versión  | Fecha      | Cambios                                       |
| -------- | ---------- | --------------------------------------------- |
| 1.0.0    | 2025-12-10 | Versión inicial: WiFi + cámara + servidor web |
| *Futuro* | *          | Streaming MJPEG verdadero                     |
| *Futuro* | *          | Configuración web                             |
| *Futuro* | *          | Dual-core con threads                         |

---

**Última actualización**: 2025-12-10  
**Mantenedor**: Agente de IA (opencode)  
**Estado**: ✅ Funcional y listo para pruebas en hardware