# Proyecto MicroPython Camera ESP32-S3

[English](README.md)
[Documentación API](micropython-camera-API-documentation.md) | [Configuración del Proyecto](QWEN.md)

## 📸 Resumen General

Este es un proyecto completo de MicroPython para la placa **ESP32-S3 CAM** que implementa un **sistema de cámara con WiFi**. El proyecto proporciona **streaming de video** y **configuración de cámara** a través de una interfaz web, con soporte para entornos de hardware real y simulados.

### 🎯 Características Principales

- **📸 Interfaz de Cámara**: Control completo de la cámara ESP32-S3 con nuevos métodos de API
- **🌐 Gestión de WiFi**: Operación dual con modos Station y Access Point
- **📺 Interfaz Web**: Streaming de video en vivo y configuración de cámara a través de UI web
- **💡 Control de LED**: Indicador RGB con diferentes colores para estados del sistema
- **🧪 Soporte Mock**: Funcionalidad de cámara simulada para desarrollo y pruebas

---

## 🏗️ Arquitectura

El proyecto está estructurado alrededor de varios módulos clave:

| Módulo                    | Propósito                                                    |
| ------------------------- | ------------------------------------------------------------ |
| `main.py`                 | Aplicación principal que orquesta todos los módulos          |
| `video_server.py`         | Maneja el streaming de video a través de la interfaz web     |
| `camera_config_server.py` | Proporciona la interfaz de configuración de cámara           |
| `wifi_manager.py`         | Gestiona la conectividad WiFi (modos Station/AP)             |
| `led_controller.py`       | Controla el LED RGB para indicación de estado del sistema    |
| `camera_pins.py`          | Definiciones de pines hardware para las conexiones de cámara |
| `camera_mock.py`          | Implementación simulada de cámara para desarrollo            |

---

## 🚀 Inicio Rápido

### Requisitos Previos

- Placa **ESP32-S3 CAM** con PSRAM
- Firmware **MicroPython** con soporte para módulo de cámara
- Computadora con entorno de desarrollo **MicroPython**

### Proceso de Configuración

1. **Flashear Firmware MicroPython**:
   
   - Flashea un firmware MicroPython que incluya soporte para cámara en tu placa ESP32-S3 CAM
   - El módulo de cámara debe estar compilado en el firmware

2. **Cargar Archivos**:
   
   - Sube todos los archivos Python del directorio `Script` a tu placa ESP32-S3 CAM
   - Asegúrate de que `ssid_config.json` esté configurado correctamente o se creará durante la primera ejecución

3. **Configuración Inicial**:
   
   - En el primer arranque, el dispositivo creará un punto de acceso "ESP32-CAM-Setup"
   - Conéctate a este AP y accede al portal de configuración en 192.168.4.1
   - Ingresa las credenciales para tu red WiFi de destino

4. **Operación**:
   
   - Después de la configuración, el dispositivo se conecta a tu WiFi
   - Accede al stream de video en vivo en la IP del dispositivo
   - La configuración de la cámara se puede ajustar a través de la interfaz web de configuración

---

## 📋 Uso

### Iniciando la Aplicación

El flujo principal de la aplicación está controlado por `main.py`:

1. Inicializa el controlador LED para indicación de estado
2. Configura WiFi (intenta conexión con credenciales guardadas o crea AP) [Manual Configuración WIFI](./WIFI_CONFIG_ESP.md)
3. Inicia el servidor de streaming de video
4. Sirve la transmisión en vivo de la cámara a través de la interfaz web

### Indicadores de LED

| Color      | Significado                     |
| ---------- | ------------------------------- |
| 🟣 Púrpura | Estado inicial                  |
| 🔵 Azul    | Modo Punto de Acceso            |
| 🟢 Verde   | Modo Station (conectado a WiFi) |
| ⚪ Blanco   | Streaming de video              |
| 🔴 Rojo    | Estado de error                 |

---

## ⚙️ Uso de la API de Cámara

El proyecto utiliza la nueva API de Cámara de MicroPython con:

- Clase `Camera` para control de cámara
- Enumeraciones `PixelFormat`, `FrameSize`, `GrabMode` para configuración
- Métodos getter/setter para propiedades de cámara (por ejemplo, `set_brightness()`, `get_brightness()`)

---

## 🧪 Pruebas y Simulación

- El módulo `camera_mock.py` proporciona una simulación completa de la API de cámara
- Esto permite desarrollo y pruebas sin hardware físico
- Todas las funciones de cámara están simuladas con comportamiento realista

---

## 📁 Estructura del Proyecto

```
Script/
├── camera_config_info.py    # Información de configuración
├── camera_config_server.py  # Servidor de configuración web
├── camera_mock.py          # Implementación de cámara simulada
├── camera_pins.py          # Definiciones de pines hardware
├── led_controller.py       # Control de LED RGB
├── main.py                # Punto de entrada de la aplicación principal
├── ssid_config.json       # Archivo de configuración WiFi
├── video_server.py        # Servidor de streaming de video
├── wifi_manager.py        # Gestión de conectividad WiFi
└── test/
    ├── camera_test_debug.py # Utilidades de depuración de cámara
    └── test_RGB.py         # Pruebas de LED RGB
```

---

## 🛠️ Convenciones de Desarrollo

### Estructura del Código

- Todo el código sigue comentarios y documentación en español
- El manejo de errores está implementado en todos los módulos
- Los indicadores LED proporcionan retroalimentación visual para diferentes estados del sistema

### Pruebas

- Pruebas exhaustivas con hardware real e implementaciones simuladas
- Manejo de errores e informe de estado para todos los módulos

---

## 🤝 Contribuciones

1. Haz un fork del repositorio
2. Crea una rama de funcionalidad (`git checkout -b feature/caracteristica-asombrosa`)
3. Realiza tus cambios (`git commit -m 'Agrega característica asombrosa'`)
4. Sube a la rama (`git push origin feature/caracteristica-asombrosa`)
5. Abre una Pull Request

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- [MicroPython](https://micropython.org/) por el firmware increíble
- Comunidad de hardware ESP32-S3 CAM
- Todos los contribuyentes a este proyecto

---

## 📞 Soporte

Para soporte, por favor abre un issue en el repositorio o contacta a los mantenedores.
