# WiFi Configuration Process for ESP32-S3 CAM

## Overview

The WiFi module of the ESP32-S3 CAM camera allows configuring WiFi network credentials through a web interface in Access Point (AP) mode. This document describes the configuration process, credential saving, and automatic device restart.

## WiFi Configuration Flow

### 1. Access Point (AP) Mode

- At startup, if there are no saved credentials or if the connection to the WiFi network fails, the device enters AP mode.
- The device creates a WiFi network named `ESP32-CAM-Setup` with password `123456789`.
- The web server is available at IP: `192.168.4.1`.

### 2. Configuration Interface

- Accessing `http://192.168.4.1` from a browser allows access to the WiFi configuration interface. WARNING!; Only use "http" not "https", no advanced security has been implemented.
- The interface allows:
  - Selecting a WiFi network from available ones
  - Manually entering a network name (SSID)
  - Entering the WiFi network password

### 3. Credential Saving

- When clicking the "Connect" button, credentials are sent to the device via a POST request to `/configure`.
- The device processes the credentials and saves them to the `ssid_config.json` file.
- The `ssid_config.json` file contains:
  - `ssid`: WiFi network name
  - `password`: WiFi network password
  - `configured`: boolean indicating if credentials have been configured

### 4. Response and Automatic Restart

- After successfully saving credentials, the device responds with a web page that:
  - Confirms that credentials have been saved successfully
  - Shows the name of the WiFi network to which it will connect
  - Indicates that the device will restart in 15 seconds
- The device automatically restarts after 15 seconds
- If accessing the `/restart` URL, the device restarts immediately

## Technical Details of Restart

After saving credentials, the confirmation page includes:

- A JavaScript script that automatically redirects to `/restart` after 15 seconds
- A visual message indicating the remaining time before restart
- The physical restart of the device is executed using MicroPython's `reset()` function

## Error Handling

- If the network name (SSID) contains special characters, these are properly escaped to avoid HTML display or interpretation issues
- If an error occurs when sending the complete HTML response, a simpler version is sent as a fallback
- The system properly handles duplicate requests or GET requests to the `/configure` route after credential submission

## Files Involved

- `wifi_manager.py`: Contains the main WiFi management module, including the web server and configuration logic
- `ssid_config.json`: File where WiFi credentials are stored
- `main.py`: Main file that coordinates modules and handles restart in case of error

## Security Considerations

- WiFi configuration is done in local AP mode, so there is no HTTPS encryption in this initial step
- The AP password is by default `123456789`, and it is recommended to use it only temporarily during configuration
- WiFi credentials are stored in plain text in the `ssid_config.json` file, which is acceptable for local embedded devices

## Developer Notes

### Relevant Code:

The WiFi configuration logic is mainly located in the `WiFiManager` class in `wifi_manager.py`, specifically in the `start_web_server()` method and the section that handles the `/configure` route.

### Future Improvements:

- Implement additional credential validation before saving
- Add timeout mechanism in case credentials are incorrect
- Potential fallback implementation if WiFi connection fails repeatedly