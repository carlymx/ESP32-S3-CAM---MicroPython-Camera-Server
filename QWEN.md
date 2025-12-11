## Variables de entorno:

- Habla, piensa y Escribe, siempre en castellano.
- Tomaras como referencia el archivo ./micropython-camera-API-documentation.md
- En cada cambio actualizaras si es necesario el archivo ./QWEN.md (este archivo)

# MicroPython Camera ESP32-S3 Project

## Project Overview

This is a comprehensive MicroPython project for the ESP32-S3 CAM board that implements a WiFi-enabled camera system. The project provides video streaming and camera configuration capabilities via a web interface, with support for both real hardware and simulated environments.

### Key Features

- **Camera Interface**: Full control of ESP32-S3 camera with new API methods
- **WiFi Management**: Dual-mode operation with Station and Access Point modes
- **Web Interface**: Live video streaming and camera configuration via web UI
- **LED Control**: RGB LED status indicator with different colors for system states
- **Mock Support**: Simulated camera functionality for testing without hardware

### Architecture

The project is structured around several key modules:

1. **main.py**: Main application that orchestrates all modules
2. **video_server.py**: Handles live video streaming via web interface
3. **camera_config_server.py**: Provides camera configuration interface
4. **wifi_manager.py**: Manages WiFi connectivity (Station/AP modes)
5. **led_controller.py**: Controls RGB LED for system status indication
6. **camera_pins.py**: Hardware pin definitions for camera connections
7. **camera_mock.py**: Simulated camera implementation for development

## Building and Running

### Prerequisites

- ESP32-S3 CAM board with PSRAM
- MicroPython firmware with camera module support
- Computer with MicroPython development environment

### Setup Process

1. **Flash MicroPython Firmware**:
   
   - Flash a MicroPython firmware that includes camera support to your ESP32-S3 CAM board
   - The camera module must be compiled into the firmware

2. **Upload Files**:
   
   - Upload all Python files from the `Script` directory to your ESP32-S3 CAM board
   - Ensure `ssid_config.json` is properly configured or will be created during first run

3. **Initial Configuration**:
   
   - On first boot, the device will create an access point "ESP32-CAM-Setup"
   - Connect to this AP and access the configuration portal at 192.168.4.1
   - Enter credentials for your target WiFi network

4. **Operation**:
   
   - After configuration, the device connects to your WiFi
   - Access the live video stream at the device's IP address
   - Camera settings can be adjusted via the web configuration interface

### Running the Application

The main application flow is controlled by `main.py`:

1. Initializes LED controller for status indication
2. Sets up WiFi (attempts connection to saved credentials or creates AP)
3. Starts video streaming server
4. Serves live camera feed via web interface

## WiFi Configuration Process

### Configuration Flow

When the device boots without existing WiFi credentials or fails to connect to a saved network:

1. The device enters Access Point (AP) mode
2. Creates a WiFi network named "ESP32-CAM-Setup" with password "123456789"
3. Starts a web server at IP address 192.168.4.1
4. User accesses the configuration page via web browser
5. User enters WiFi credentials and submits them
6. Upon successful credential storage, the device shows a confirmation page
7. After 15 seconds, the device automatically restarts to apply the new WiFi settings

### Technical Details

- Credentials are stored in `ssid_config.json` file
- SSID names with special characters are properly escaped
- After credential submission, a countdown page shows the device will restart in 15 seconds
- The device automatically restarts after 15 seconds with the new configuration
- If a restart is needed earlier, the user can access `/restart` URL

## Development Conventions

### Code Structure

- All code follows Spanish comments and documentation
- Error handling is implemented throughout the modules
- LED indicators provide visual feedback for different system states:
  - Purple: Initial state
  - Blue: Access Point mode
  - Green: Station mode (connected to WiFi)
  - White: Video streaming
  - Red: Error state

### Camera API Usage

The project uses the new MicroPython Camera API with:

- `Camera` class for camera control
- `PixelFormat`, `FrameSize`, `GrabMode` enums for configuration
- Getter/setter methods for camera properties (e.g., `set_brightness()`, `get_brightness()`)

### Testing and Simulation

- The `camera_mock.py` module provides a complete simulation of the camera API
- This allows for development and testing without physical hardware
- All camera functions are mocked with realistic behavior

## Project Files

- `main.py`: Main application entry point
- `video_server.py`: Streaming video server
- `camera_config_server.py`: Configuration web interface
- `wifi_manager.py`: WiFi connectivity management
- `led_controller.py`: RGB LED control
- `camera_pins.py`: Hardware pin definitions
- `camera_mock.py`: Mock camera implementation
- `micropython-camera-API-documentation.md`: Comprehensive camera API documentation
- `WIFI_CONFIGURATION_PROCESS.md`: Detailed documentation about WiFi configuration process

## Soluciones Implementadas

### Watchdog Timer (WDT) Problem

Se ha resuelto el problema de reinicios constantes del ESP32-S3 causados por el Watchdog Timer (WDT).

- **Causa Raíz**: La operación de inicialización de la cámara (`camera.init()` o `Camera(...)`) consume una cantidad de tiempo considerable, superior al timeout por defecto del WDT. Esto provocaba que el sistema se reiniciara antes de poder completar el arranque del servidor de vídeo.
- **Solución Implementada**: Se ha modificado la función de inicialización centralizada `init_camera()` en el nuevo módulo `camera_utils.py`. La solución consiste en:
  1. Importar la clase `WDT` desde el módulo `machine`.
  2. Antes de llamar al constructor de la cámara, se crea una instancia del WDT con un tiempo de espera extendido de 10 segundos (`WDT(timeout=10000)`).
  3. Inmediatamente después de que la inicialización de la cámara finaliza, se "alimenta" al watchdog con `wdt.feed()`. Esto restablece el temporizador y confirma que el sistema no está bloqueado.
- **Resultado**: El sistema ahora tiene tiempo suficiente para inicializar el hardware de la cámara sin ser interrumpido por el WDT, eliminando el bucle de reinicios.

## Mejoras y Refactorización del Proyecto (Diciembre 2025)

A partir de un análisis detallado (`ANALISIS_PROYECTO.md`), se han implementado las siguientes mejoras significativas para aumentar la robustez, mantenibilidad y calidad del código:

1. **Corrección de Error Crítico en Pines I2C**:
   
   - Se corrigió un error en `camera_config_server.py` donde los pines I2C (`sda`, `scl`) estaban asignados incorrectamente, lo que impedía la correcta configuración del sensor de la cámara. Ahora utilizan los pines correctos definidos en `camera_pins.py`.

2. **Externalización de la Interfaz Web (HTML)**:
   
   - Todo el código HTML que estaba incrustado como cadenas de texto en los scripts de Python (`video_server.py`, `camera_config_server.py`, `wifi_manager.py`) ha sido movido a archivos `.html` independientes.
   - Estos archivos ahora residen en el nuevo directorio `Script/html/`.
   - Los scripts de Python cargan dinámicamente estas plantillas, haciendo el código mucho más limpio, legible y fácil de mantener.

3. **Centralización de la Lógica de Inicialización de la Cámara**:
   
   - Se creó un nuevo módulo `Script/camera_utils.py` que contiene una función única y centralizada `init_camera()`.
   - Todos los demás módulos (`video_server.py`, `camera_config_server.py`, `test/camera_test_debug.py`) han sido refactorizados para usar esta función, eliminando la duplicación de código y asegurando una inicialización consistente y robusta de la cámara en todo el proyecto.

4. **Consistencia de la API de Simulación (`camera_mock.py`)**:
   
   - Se refactorizó por completo `camera_mock.py` para eliminar la API dual (funciones a nivel de módulo y métodos de clase).
   - Ahora, el módulo solo expone una clase `Camera` que imita fielmente la API de la cámara real, gestionando su propio estado interno. Esto simplifica enormemente el código en otros módulos, que ya no necesitan bifurcaciones lógicas para tratar con la cámara real o la simulada.

5. **Manejo de Excepciones Específico**:
   
   - Se reemplazaron los manejadores de excepciones genéricos (`except Exception`) por excepciones más específicas (`OSError`, `ValueError`, `RuntimeError`) en todos los módulos. Esto permite una depuración más precisa y un mejor entendimiento de los errores de hardware, red o lógicos.

6. **Mejoras en Módulos de Prueba**:
   
   - Se refactorizó `test/test_RGB.py` para que utilice la clase `LEDController` y se ejecute de forma determinista (sin bucles infinitos).
   - Se actualizó `test/camera_test_debug.py` para utilizar la nueva función `init_camera()` y para probar la API de `camera_mock.py` refactorizada.
