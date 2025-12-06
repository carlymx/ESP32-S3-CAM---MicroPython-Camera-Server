<img title="" src="./data/imgs/IMG_20251202_104513.jpg" alt="Img-01" width="503" data-align="center">

[Español](./README_ESP.md) - [English](./README.md)

# ESP32-S3 CAM - Web Server Camera Project

This project implements firmware for the ESP32-S3 CAM module that includes an integrated web server for camera control and visualization.

## Features

- **Dark theme**: All web interfaces have a dark theme as requested
- **RGB LED Control**: The LED on pin 48 indicates the device status:
  - Purple: Initial state
  - Blue: AP (Access Point) mode
  - Green: Station mode (connected to WiFi)
  - White: Video transmission
  - Red: Error
- **AP mode for configuration**: If there are no saved credentials or cannot connect, the ESP32 creates its own WiFi network for configuration
- **Real-time video streaming**: Real-time camera view through the browser
- **Configuration interface**: Web page to adjust camera parameters with real-time preview
- **Hardware information**: The configuration interface shows technical details of the camera hardware

## Installation

1. Make sure you have MicroPython installed on your ESP32-S3 CAM
2. Copy all project files to the ESP32-S3 CAM memory:
   - `main.py`
   - `led_controller.py`
   - `wifi_manager.py`
   - `video_server.py`
   - `camera_config_server.py`
3. Restart the device

## Usage

1. On startup, the device will try to connect to a WiFi network with saved credentials
2. If there are no saved credentials or cannot connect, it will start in AP mode
3. In AP mode, you can connect to the "ESP32-CAM-Setup" network and access the web configuration at the device IP
4. Once connected to WiFi, you can access the live view at the device IP
5. To access camera configuration, visit IP/cam

## Project Files

- `main.py`: Main file that integrates all modules
- `led_controller.py`: RGB LED controller with status codes
- `wifi_manager.py`: WiFi connection manager with AP mode for configuration
- `video_server.py`: Web server for real-time video streaming
- `camera_config_server.py`: Web server for camera configuration interface
- `README.md`: Project documentation
- `PLAN.md`: Detailed project plan
- `Changelog.md`: Project change history

## Camera Configuration

The configuration interface allows adjusting:

- Image quality and resolution
- Brightness, contrast and saturation
- Special effects
- White balance
- Exposure level
- Orientation (horizontal mirror and vertical flip)

## Possible Future Improvements (TODOlist)

- Add authentication to protect web interfaces
- Implement video recording and SD card storage
- Add motion detection and notifications
- Implement remote control via API commands
- Add object tracking functionality
- Incorporate face recognition
- Develop mobile app for remote control
- Implement streaming to multiple simultaneous clients
- Add smart doorbell functionality with notifications
- Create AI-based alert system
- Implement video compression to reduce bandwidth
- Add support for multiple cameras
- Integrate with cloud services for remote storage

## License

This project is developed for educational and learning purposes. It is distributed under the MIT License.