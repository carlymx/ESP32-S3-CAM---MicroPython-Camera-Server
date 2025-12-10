## Variables de entorno:

- Habla, piensa y Escribe, siempre en castellano.
- tomaras como referencia el archivo ./micropython-camera-API-documentation.md
- En cada cambio actualizaras si es necesario el archivo QWEN.md

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