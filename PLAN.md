[Español](./PLAN_ESP.md) - [English](./PLAN.md)

# ESP32-S3 CAM Project Development Plan

## General Description

Project to implement firmware on ESP32-S3 CAM with integrated web server for camera control and visualization, with dark theme web interface and all communications in Spanish.

## Project Requirements

### 1. Language and Environment

- Everything in Spanish
- Dark theme for web interfaces
- Documentation of each step in the TODOlist
- Work with Thonny and MicroPython

### 2. Firmware Features

- Integrated web server with AP mode for initial configuration
- WiFi connection with saved credentials
- Real-time video streaming
- Advanced web configuration interface

### 3. Visual Indicator

- Use RGB LED on pin 48 to show states
  - AP: Blue
  - Station: Green
  - Transmitting: White
  - Error: Red

### 4. Web Interfaces

- Main interface to view real-time video
- Configuration interface (IP/cam) with preview and controls
- Camera hardware information in the configuration interface

## Detailed Implementation Plan

### 1. Initial Research

- Investigate camera library for ESP32-S3 in MicroPython
- Review WiFi connection examples in dual mode (Station/AP)
- Study how to serve real-time video images with MicroPython
- Investigate how to obtain camera hardware information (model, maximum resolution, etc.)
- Review how to control an RGB LED in MicroPython for ESP32-S3

### 2. Configure Development Environment

- Configure Thonny with MicroPython for ESP32-S3
- Verify module connection and script upload
- Create project directory structure

### 3. Develop RGB LED Control

- Create module to control RGB LED on pin 48
- Implement color codes for different states
- Integrate LED control in the system's main functions

### 4. Develop WiFi Manager

- Create script to detect if WiFi credentials are saved
- Implement AP mode with web server for WiFi configuration
- Create HTML/CSS/JS web interface to configure WiFi connection with dark theme
- Implement credential saving to ESP32 files
- Update RGB LED to blue when in AP mode

### 5. Develop Video Web Server

- Create main web server that activates after WiFi connection
- Implement real-time camera image streaming
- Develop web interface to show video with dark theme
- Update RGB LED to green when in Station mode and white when transmitting

### 6. Develop Camera Configuration Web Server

- Create additional web endpoint in sub-URL (IP/cam)
- Implement real-time camera image preview
- Add typical camera configuration controls (brightness, contrast, resolution, etc.)
- Implement real-time camera parameter updates
- Add section in web interface to show camera hardware information (model, maximum resolution, etc.)

### 7. Implement Dark Theme and Style

- Create common CSS with dark theme for both web interfaces
- Ensure visual consistency between configuration and visualization interfaces

### 8. Project Documentation

- Document each development step with detailed comments
- Create README.md file with installation and usage instructions
- Document source code with Spanish comments
- Register each implemented functionality with description
- Document RGB LED color codes
- Create Changelog.md file to maintain change history
- Create TODOlist with possible future improvements in a file or specific section

### 9. Testing and Validation

- Test WiFi connection functionality in AP mode
- Verify real-time video streaming
- Validate camera configuration controls
- Test hardware information display
- Check that RGB LED states update correctly
- Perform complete integration tests

### 10. Optimization and Refinement

- Optimize web server resource consumption
- Refine user interface for better experience
- Adjust video streaming performance
- Optimize RGB LED usage to not interfere with other processes

### 11. Final Preparation and Presentation

- Create complete installation script
- Document possible problems and solutions
- Prepare final project documentation
- Update Changelog.md file with changes made

## Specific Documentation

### Changelog.md

File to document changes in the usual way, following the format:

```
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- [List of new features]

### Changed
- [List of changes made]

### Deprecated
- [List of deprecated features]

### Removed
- [List of removed features]

### Fixed
- [List of bug fixes]

### Security
- [List of security improvements]
```

### TODOlist of Future Improvements

Possible project extensions:

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

## Project Status

- Plan: Approved
- Phase: Module implementation, hardware issue resolution

## Identified Issues

- 'camera' module not available in current MicroPython installation
- Temporary solution implemented with simulation module
- Pending verification of MicroPython version with camera support

## Completed Tasks

- ✅ Implementation of camera simulation module
- ✅ Update of video_server.py to handle available camera modules
- ✅ Update of camera_config_server.py to handle available camera modules
- ✅ Update of main.py to verify camera availability
- ✅ Creation of camera configuration information file
- ✅ Creation of detailed debugging test script for camera
- ✅ Creation of documentation for camera test script