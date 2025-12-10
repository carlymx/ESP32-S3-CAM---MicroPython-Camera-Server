# MicroPython Camera ESP32-S3 Project

[Español](README_ESP.md)
[Documentation API](micropython-camera-API-documentation.md) | [Project Configuration](QWEN.md)

## 📸 Overview

This is a comprehensive MicroPython project for the **ESP32-S3 CAM** board that implements a **WiFi-enabled camera system**. The project provides **video streaming** and **camera configuration** capabilities via a web interface, with support for both real hardware and simulated environments.

### 🎯 Key Features

- **📸 Camera Interface**: Full control of ESP32-S3 camera with new API methods
- **🌐 WiFi Management**: Dual-mode operation with Station and Access Point modes
- **📺 Web Interface**: Live video streaming and camera configuration via web UI
- **💡 LED Control**: RGB LED status indicator with different colors for system states
- **🧪 Mock Support**: Simulated camera functionality for development and testing

---

## 🏗️ Architecture

The project is structured around several key modules:

| Module                    | Purpose                                         |
| ------------------------- | ----------------------------------------------- |
| `main.py`                 | Main application that orchestrates all modules  |
| `video_server.py`         | Handles live video streaming via web interface  |
| `camera_config_server.py` | Provides camera configuration interface         |
| `wifi_manager.py`         | Manages WiFi connectivity (Station/AP modes)    |
| `led_controller.py`       | Controls RGB LED for system status indication   |
| `camera_pins.py`          | Hardware pin definitions for camera connections |
| `camera_mock.py`          | Simulated camera implementation for development |

---

## 🚀 Getting Started

### Prerequisites

- **ESP32-S3 CAM** board with PSRAM
- **MicroPython** firmware with camera module support
- Computer with **MicroPython** development environment

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

---

## 📋 Usage

### Starting the Application

The main application flow is controlled by `main.py`:

1. Initializes LED controller for status indication
2. Sets up WiFi (attempts connection to saved credentials or creates AP) [WIFI Manual](./WIFI_CONFIG.md)
3. Starts video streaming server
4. Serves live camera feed via web interface

### LED Status Indicators

| Color     | Meaning                          |
| --------- | -------------------------------- |
| 🟣 Purple | Initial state                    |
| 🔵 Blue   | Access Point mode                |
| 🟢 Green  | Station mode (connected to WiFi) |
| ⚪ White   | Video streaming                  |
| 🔴 Red    | Error state                      |

---

## ⚙️ Camera API Usage

The project uses the new MicroPython Camera API with:

- `Camera` class for camera control
- `PixelFormat`, `FrameSize`, `GrabMode` enums for configuration
- Getter/setter methods for camera properties (e.g., `set_brightness()`, `get_brightness()`)

---

## 🧪 Testing and Simulation

- The `camera_mock.py` module provides a complete simulation of the camera API
- This allows for development and testing without physical hardware
- All camera functions are mocked with realistic behavior

---

## 📁 Project Structure

```
Script/
├── camera_config_info.py    # Configuration information
├── camera_config_server.py  # Web configuration server
├── camera_mock.py          # Mock camera implementation
├── camera_pins.py          # Hardware pin definitions
├── led_controller.py       # RGB LED control
├── main.py                # Main application entry point
├── ssid_config.json       # WiFi configuration file
├── video_server.py        # Video streaming server
├── wifi_manager.py        # WiFi connectivity management
└── test/
    ├── camera_test_debug.py # Camera debugging utilities
    └── test_RGB.py         # RGB LED testing
```

---

## 🛠️ Development Conventions

### Code Structure

- All code follows Spanish comments and documentation
- Error handling is implemented throughout the modules
- LED indicators provide visual feedback for different system states

### Testing

- Comprehensive testing with both real hardware and mocked implementations
- Error handling and status reporting for all modules

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [MicroPython](https://micropython.org/) for the amazing firmware
- ESP32-S3 CAM hardware community
- All contributors to this project

---

## 📞 Support

For support, please open an issue in the repository or contact the maintainers.
