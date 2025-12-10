# MicroPython Camera API: Firmware Documentation

URL the Project: [Release v0.5.0 · cnadler86/micropython-camera-API · GitHub](https://github.com/cnadler86/micropython-camera-API/releases/tag/v0.5.0)

## 1. Introduction

This document provides a comprehensive overview of the MicroPython Camera API firmware for ESP32-S3 microcontrollers. It includes detailed information about firmware functionality, usage patterns, and implementation details to help resolve the INIT errors reported in the camera module and create new scripts correctly.

## 2. Firmware Architecture

### 2.1 Core Components

The MicroPython Camera API consists of several key files:

- **modcamera.c**: Core C implementation of camera hardware abstraction layer (HAL)
- **modcamera_api.c**: Python API bindings and method implementations
- **modcamera.h**: Header file with definitions and function declarations
- **camera_pins.h**: Board-specific pin configurations
- **acamera.py**: Async extension for camera functionality

### 2.2 Memory Requirements

- **PSRAM Required**: The driver requires PSRAM to be installed and activated on the ESP32-S3
- **RAM Usage**: Frame buffer count affects memory usage (1-2 buffers recommended)
- **IRAM**: Requires ESP-IDF >= 5.2 to avoid IRAM overflow during build

## 3. Hardware Configuration

### 3.1 Pin Configuration

The firmware supports various ESP32-S3 camera boards with predefined pin configurations. For the ESP32-S3 CAM (AI Thinker), the pins are:

```
CAM_PWDN: 32      (Power down pin)
CAM_VSYNC: 25     (Vertical sync)
CAM_HREF: 23      (Horizontal reference)
CAM_PCLK: 22      (Pixel clock)
CAM_XCLK: 0       (External clock)
CAM_D0: 5         (Data pin 0)
CAM_D1: 18        (Data pin 1)
CAM_D2: 19        (Data pin 2)
CAM_D3: 21        (Data pin 3)
CAM_D4: 36        (Data pin 4)
CAM_D5: 39        (Data pin 5)
CAM_D6: 34        (Data pin 6)
CAM_D7: 35        (Data pin 7)
```

### 3.2 Clock Configuration

- **XCLK Frequency**: Typically 20MHz for OV2640 sensors (can be 10MHz or 20MHz depending on sensor)
- **Supported Sensors**: OV7670, OV7725, OV2640, OV3660, OV5640, NT99141, GC2145, GC032A, GC0308, BF3005, BF20A6, SC030IOT

## 4. Module Import and Construction

### 4.1 Importing the Module

```python
from camera import Camera, FrameSize, PixelFormat, GainCeiling, GrabMode
```

Or for async support:

```python
from acamera import Camera, FrameSize, PixelFormat, GainCeiling, GrabMode
```

### 4.2 Camera Object Construction

#### With Default Configuration (Precompiled Firmware)

```python
cam = Camera()  # Uses board-specific defaults
```

#### With Custom Configuration

```python
cam = Camera(
    data_pins=[5, 18, 19, 21, 36, 39, 34, 35],  # D0-D7
    pclk_pin=22,
    vsync_pin=25,
    href_pin=23,
    sda_pin=26,           # SCCB SDA
    scl_pin=27,           # SCCB SCL
    xclk_pin=0,
    xclk_freq=20000000,   # 20MHz
    powerdown_pin=32,
    reset_pin=-1,
    pixel_format=PixelFormat.JPEG,
    frame_size=FrameSize.VGA,
    jpeg_quality=85,
    fb_count=2,
    grab_mode=GrabMode.LATEST,
    init=True  # Auto-initialize (default)
)
```

### 4.3 Constructor Parameters

| Parameter       | Type        | Default                              | Description              |
| --------------- | ----------- | ------------------------------------ | ------------------------ |
| `data_pins`     | List[int]   | Required*                            | Data pins D0-D7          |
| `pclk_pin`      | int         | Required*                            | Pixel clock pin          |
| `vsync_pin`     | int         | Required*                            | Vertical sync pin        |
| `href_pin`      | int         | Required*                            | Horizontal reference pin |
| `sda_pin`       | int         | Required*                            | SCCB SDA pin             |
| `scl_pin`       | int         | Required*                            | SCCB SCL pin             |
| `xclk_pin`      | int         | Required*                            | External clock pin       |
| `xclk_freq`     | int         | 20000000                             | XCLK frequency in Hz     |
| `powerdown_pin` | int         | -1                                   | Power down pin           |
| `reset_pin`     | int         | -1                                   | Reset pin                |
| `pixel_format`  | PixelFormat | RGB565                               | Output pixel format      |
| `frame_size`    | FrameSize   | QQVGA                                | Frame dimensions         |
| `jpeg_quality`  | int         | 85                                   | JPEG quality (0-100)     |
| `fb_count`      | int         | 2 for S3/1 for others                | Frame buffer count       |
| `grab_mode`     | GrabMode    | LATEST for S3, WHEN_EMPTY for others | Frame grab mode          |
| `init`          | bool        | True                                 | Auto-initialize camera   |

*Required if board-specific pins are not defined in firmware

## 5. API Methods

### 5.1 Initialization and Management

#### `init()`

Initialize the camera hardware.

```python
cam.init()
```

#### `deinit()`

Deinitialize the camera hardware.

```python
cam.deinit()
```

#### `reconfigure()`

Reconfigure camera settings after initialization.

```python
cam.reconfigure(
    frame_size=FrameSize.VGA,
    pixel_format=PixelFormat.JPEG,
    grab_mode=GrabMode.LATEST,
    fb_count=2
)
```

### 5.2 Image Capture

#### `capture()`

Capture an image frame.

```python
img = cam.capture()  # Returns memoryview object
if img:
    # Process the image
    img_bytes = bytes(img)  # Convert to bytes if needed
```

#### `acapture()` (Async)

Asynchronous capture method (from acamera module).

```python
img = await cam.acapture()  # Returns memoryview object
```

#### `frame_available()`

Check if a frame is available for capture.

```python
if cam.frame_available():
    img = cam.capture()
```

#### `free_buffer()`

Free the current frame buffer to reduce latency.

```python
img = bytes(cam.capture())  # Create bytes object
cam.free_buffer()           # Free the buffer
```

### 5.3 Camera Properties

#### Get Methods

```python
sensor_name = cam.get_sensor_name()      # Get sensor name
width = cam.get_pixel_width()            # Get pixel width
height = cam.get_pixel_height()          # Get pixel height
format = cam.get_pixel_format()          # Get pixel format
frame_size = cam.get_frame_size()        # Get frame size
quality = cam.get_quality()              # Get JPEG quality
brightness = cam.get_brightness()        # Get brightness (-2 to 2)
contrast = cam.get_contrast()            # Get contrast (-2 to 2)
saturation = cam.get_saturation()        # Get saturation (-2 to 2)
```

#### Set Methods

```python
cam.set_quality(90)                      # Set JPEG quality (0-100)
cam.set_brightness(1)                    # Set brightness (-2 to 2)
cam.set_contrast(1)                      # Set contrast (-2 to 2)
cam.set_saturation(1)                    # Set saturation (-2 to 2)
cam.set_vflip(True)                      # Vertical flip
cam.set_hmirror(True)                    # Horizontal mirror
cam.set_special_effect(2)                # Special effect
cam.set_wb_mode(1)                       # White balance mode
cam.set_ae_level(0)                      # Auto exposure level (-2 to 2)
cam.set_gainceiling(GainCeiling.X2)      # Gain ceiling
```

### 5.4 Supported Property Methods

| Property                | Get Method             | Set Method                  | Range/Values     |
| ----------------------- | ---------------------- | --------------------------- | ---------------- |
| Quality                 | `get_quality()`        | `set_quality(value)`        | 0-100            |
| Brightness              | `get_brightness()`     | `set_brightness(value)`     | -2 to 2          |
| Contrast                | `get_contrast()`       | `set_contrast(value)`       | -2 to 2          |
| Saturation              | `get_saturation()`     | `set_saturation(value)`     | -2 to 2          |
| Special Effect          | `get_special_effect()` | `set_special_effect(value)` | 0-6              |
| White Balance Mode      | `get_wb_mode()`        | `set_wb_mode(value)`        | 0-4              |
| Auto Exposure Level     | `get_ae_level()`       | `set_ae_level(value)`       | -2 to 2          |
| Gain Ceiling            | `get_gainceiling()`    | `set_gainceiling(value)`    | X2, X4, X8, etc. |
| Vertical Flip           | `get_vflip()`          | `set_vflip(value)`          | True/False       |
| Horizontal Mirror       | `get_hmirror()`        | `set_hmirror(value)`        | True/False       |
| Color Bar               | `get_colorbar()`       | `set_colorbar(value)`       | True/False       |
| Auto White Balance      | `get_whitebal()`       | `set_whitebal(value)`       | True/False       |
| Auto Gain Control       | `get_gain_ctrl()`      | `set_gain_ctrl(value)`      | True/False       |
| Auto Exposure Control   | `get_exposure_ctrl()`  | `set_exposure_ctrl(value)`  | True/False       |
| Auto Exposure Control 2 | `get_aec2()`           | `set_aec2(value)`           | True/False       |
| AGC Gain                | `get_agc_gain()`       | `set_agc_gain(value)`       | 0-30             |
| AEC Value               | `get_aec_value()`      | `set_aec_value(value)`      | 0-1200           |
| DCW                     | `get_dcw()`            | `set_dcw(value)`            | True/False       |
| BPC                     | `get_bpc()`            | `set_bpc(value)`            | True/False       |
| WPC                     | `get_wpc()`            | `set_wpc(value)`            | True/False       |
| Raw Gamma               | `get_raw_gma()`        | `set_raw_gma(value)`        | True/False       |
| Lens Correction         | `get_lenc()`           | `set_lenc(value)`           | True/False       |
| Sharpness               | `get_sharpness()`      | `set_sharpness(value)`      | -2 to 2          |
| Denoise                 | `get_denoise()`        | `set_denoise(value)`        | 0-4              |

## 6. Constants and Enumerations

### 6.1 Pixel Formats

```python
PixelFormat.JPEG       # JPEG compressed format
PixelFormat.YUV422     # YUV422 format
PixelFormat.YUV420     # YUV420 format
PixelFormat.GRAYSCALE  # Grayscale format
PixelFormat.RGB565     # RGB565 format
PixelFormat.RGB888     # RGB888 format
PixelFormat.RGB444     # RGB444 format
PixelFormat.RGB555     # RGB555 format
PixelFormat.RAW        # Raw format
```

### 6.2 Frame Sizes

```python
FrameSize.R96X96       # 96x96
FrameSize.QQVGA        # 160x120
FrameSize.R128x128     # 128x128
FrameSize.QCIF         # 176x144
FrameSize.HQVGA        # 240x160
FrameSize.R240X240     # 240x240
FrameSize.QVGA         # 320x240
FrameSize.R320X320     # 320x320
FrameSize.CIF          # 352x288
FrameSize.HVGA         # 480x320
FrameSize.VGA          # 640x480
FrameSize.SVGA         # 800x600
FrameSize.XGA          # 1024x768
FrameSize.HD           # 1280x720
FrameSize.SXGA         # 1280x1024
FrameSize.UXGA         # 1600x1200
FrameSize.FHD          # 1920x1080
FrameSize.P_HD         # 720x1280
FrameSize.P_3MP        # 1536x2048
FrameSize.QXGA         # 2048x1536
FrameSize.QHD          # 2560x1440
FrameSize.WQXGA        # 2560x1600
FrameSize.P_FHD        # 1080x1920
FrameSize.QSXGA        # 2560x1920
```

### 6.3 Grab Modes

```python
GrabMode.WHEN_EMPTY    # Grab when buffer is empty (default for non-S3)
GrabMode.LATEST        # Grab latest frame (default for S3)
```

### 6.4 Gain Ceiling Values

```python
GainCeiling.X2         # 2X gain
GainCeiling.X4         # 4X gain
GainCeiling.X8         # 8X gain
GainCeiling.X16        # 16X gain
GainCeiling.X32        # 32X gain
GainCeiling.X64        # 64X gain
GainCeiling.X128       # 128X gain
```

## 7. Usage Patterns and Examples

### 7.1 Basic Usage Pattern

```python
from camera import Camera, FrameSize, PixelFormat

# Create camera with basic config
cam = Camera(
    frame_size=FrameSize.VGA,
    pixel_format=PixelFormat.JPEG,
    init=False  # Don't auto-initialize
)

try:
    cam.init()  # Initialize manually
    img = cam.capture()
    if img:
        print(f"Captured image: {len(img)} bytes")
        # Process the image
        img_bytes = bytes(img)
    else:
        print("Failed to capture image")
finally:
    cam.deinit()  # Clean up
```

### 7.2 Context Manager Pattern (Recommended)

```python
from camera import Camera, FrameSize, PixelFormat

with Camera(
    frame_size=FrameSize.VGA,
    pixel_format=PixelFormat.JPEG
) as cam:
    # Camera is automatically initialized
    img = cam.capture()
    if img:
        print(f"Captured image: {len(img)} bytes")
    # Camera is automatically deinitialized
```

### 7.3 Streaming Pattern

```python
from camera import Camera, FrameSize, PixelFormat
import socket

# Create camera for streaming
cam = Camera(
    frame_size=FrameSize.VGA,
    pixel_format=PixelFormat.JPEG,
    fb_count=2,
    grab_mode=GrabMode.LATEST
)

try:
    cam.init()
    # Start streaming server...
    while True:
        frame = cam.capture()
        if frame:
            # Send frame over network
            # ...
        else:
            break
finally:
    cam.deinit()
```

### 7.4 Async Usage Pattern

```python
import asyncio
from acamera import Camera, FrameSize, PixelFormat

async def capture_image():
    cam = Camera(
        frame_size=FrameSize.VGA,
        pixel_format=PixelFormat.JPEG
    )

    try:
        img = await cam.acapture()
        if img:
            print(f"Captured: {len(img)} bytes")
    finally:
        cam.deinit()

# Run the async function
asyncio.run(capture_image())
```

## 8. Common Issues and Solutions

### 8.1 "'module' object has no attribute 'init'" Error

**Cause**: The MicroPython firmware doesn't include the camera module or the camera driver is not compiled into the firmware.

**Solutions**:

1. Use a precompiled firmware that includes the camera module from the releases page

2. Build custom firmware with camera support enabled

3. Check if the camera module is available:
   
   ```python
   try:
       import camera
       print("Camera module available")
       print(dir(camera))  # Check available attributes
   except ImportError:
       print("Camera module not available")
   ```

### 8.2 Camera Initialization Failures

**Common causes and solutions**:

1. **Wrong pin configuration**: Ensure pins match your hardware
2. **Missing PSRAM**: The camera driver requires PSRAM
3. **Power issues**: Check camera power supply and connections
4. **Wrong frequency**: Verify XCLK frequency matches sensor requirements

### 8.3 Troubleshooting Steps

1. **Verify firmware**: Ensure using camera-enabled firmware

2. **Check hardware**: Verify physical connections and power

3. **Validate pins**: Use correct pin configuration for your board

4. **Test with minimal code**:
   
   ```python
   try:
       from camera import Camera
       cam = Camera(init=False)
       print("Module loaded successfully")
       cam = None  # Clean up
   except ImportError as e:
       print(f"Import error: {e}")
   except Exception as e:
       print(f"Construction error: {e}")
   ```

## 9. Build Configuration for Custom Firmware

### 9.1 Board Configuration

Add to your board's `mpconfigboard.h`:

```c
// For AI-Thinker ESP32-CAM
#define MICROPY_CAMERA_MODEL_AI_THINKER       1

// Or define specific pins:
#define MICROPY_CAMERA_PIN_D0        (5)
#define MICROPY_CAMERA_PIN_D1        (18)
#define MICROPY_CAMERA_PIN_D2        (19)
#define MICROPY_CAMERA_PIN_D3        (21)
#define MICROPY_CAMERA_PIN_D4        (36)
#define MICROPY_CAMERA_PIN_D5        (39)
#define MICROPY_CAMERA_PIN_D6        (34)
#define MICROPY_CAMERA_PIN_D7        (35)
#define MICROPY_CAMERA_PIN_PCLK      (22)
#define MICROPY_CAMERA_PIN_VSYNC     (25)
#define MICROPY_CAMERA_PIN_HREF      (23)
#define MICROPY_CAMERA_PIN_XCLK      (0)
#define MICROPY_CAMERA_PIN_PWDN      (32)
#define MICROPY_CAMERA_PIN_RESET     (-1)
#define MICROPY_CAMERA_PIN_SIOD      (26)  // SDA
#define MICROPY_CAMERA_PIN_SIOC      (27)  // SCL
#define MICROPY_CAMERA_XCLK_FREQ     (20000000)
#define MICROPY_CAMERA_FB_COUNT      (2)
#define MICROPY_CAMERA_JPEG_QUALITY  (85)
#define MICROPY_CAMERA_GRAB_MODE     (1)   // LATEST
```

### 9.2 Build Commands

```bash
. <path_to_esp_idf>/export.sh
cd micropython/ports/esp32
make USER_C_MODULES=../../../../micropython-camera-API/src/micropython.cmake BOARD=<Your-Board> clean
make USER_C_MODULES=../../../../micropython-camera-API/src/micropython.cmake BOARD=<Your-Board> submodules
make USER_C_MODULES=../../../../micropython-camera-API/src/micropython.cmake BOARD=<Your-Board> all
```

## 10. Performance Considerations

### 10.1 Frame Buffer Count

- `fb_count=1`: Lower memory usage, may have frame drops in streaming
- `fb_count=2`: Higher memory usage, smoother streaming, can double FPS for JPEG

### 10.2 Grab Mode Selection

- `GrabMode.WHEN_EMPTY`: Less resources, may have old data
- `GrabMode.LATEST`: Best quality frames, more resources (recommended for ESP32-S3)

### 10.3 Pixel Format Selection

- JPEG: Best performance, compressed output
- YUV/RGB: Higher quality but slower processing and larger files
- For ESP32-S series, JPEG mode always provides better frame rates

### 10.4 Frame Size vs Performance

Based on benchmarking with ESP32-S3 and OV2640 at 20MHz XCLK:

- Small frames (QQVGA, QVGA): Higher FPS
- Large frames (VGA and above): Lower FPS, especially for non-JPEG formats
- JPEG with fb_count=2 can approximately double FPS

## 11. Testing and Validation

### 11.1 Basic Test Script

```python
"""Basic camera functionality test"""
from camera import Camera, FrameSize, PixelFormat
import gc

def test_camera_basic():
    print("Testing basic camera functionality...")

    try:
        # Create camera object
        cam = Camera(
            frame_size=FrameSize.QVGA,
            pixel_format=PixelFormat.JPEG,
            init=False
        )
        print("✓ Camera object created")

        # Initialize camera
        cam.init()
        print("✓ Camera initialized")

        # Capture test
        img = cam.capture()
        if img:
            print(f"✓ Captured image: {len(img)} bytes")
        else:
            print("✗ Failed to capture image")

        # Test properties
        sensor_name = cam.get_sensor_name()
        print(f"✓ Sensor: {sensor_name}")
        print(f"✓ Pixel format: {cam.get_pixel_format()}")
        print(f"✓ Frame size: {cam.get_frame_size()}")

        # Test property setting
        cam.set_brightness(1)
        print(f"✓ Brightness set to: {cam.get_brightness()}")

        # Cleanup
        cam.deinit()
        print("✓ Camera deinitialized")

    except Exception as e:
        print(f"✗ Error during test: {e}")
        import sys
        sys.print_exception(e)

# Run the test
test_camera_basic()
gc.collect()
```

### 11.2 Troubleshooting Script

```python
"""Camera troubleshooting script"""
import sys

def check_camera_module():
    """Check if camera module is available and functional"""
    print("=== Camera Module Check ===")

    try:
        import camera
        print("✓ Camera module imported successfully")

        # Check available attributes
        attrs = dir(camera)
        print(f"Available attributes: {attrs}")

        # Check if Camera class exists
        if hasattr(camera, 'Camera'):
            print("✓ Camera class is available")
        else:
            print("✗ Camera class is NOT available")

        # Check other important attributes
        for attr in ['FrameSize', 'PixelFormat', 'GrabMode', 'GainCeiling']:
            if hasattr(camera, attr):
                print(f"✓ {attr} is available")
            else:
                print(f"✗ {attr} is NOT available")

    except ImportError as e:
        print(f"✗ Camera module import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

    return True

def test_camera_hardware():
    """Test camera hardware functionality"""
    print("\n=== Camera Hardware Test ===")

    try:
        from camera import Camera, FrameSize, PixelFormat

        # Try to create camera (without initializing first)
        cam = Camera(frame_size=FrameSize.QVGA, pixel_format=PixelFormat.JPEG, init=False)
        print("✓ Camera object created successfully")

        # Now try to initialize
        cam.init()
        print("✓ Camera initialized successfully")

        # Try to capture
        img = cam.capture()
        if img:
            print(f"✓ Capture successful: {len(img)} bytes")
        else:
            print("✗ Capture failed - no image returned")

        # Clean up
        cam.deinit()
        print("✓ Camera deinitialized successfully")

        return True

    except Exception as e:
        print(f"✗ Hardware test failed: {e}")
        import sys
        sys.print_exception(e)
        return False

# Run checks
if check_camera_module():
    test_camera_hardware()
```

This documentation should help resolve the camera INIT errors and provide a comprehensive reference for creating new scripts correctly.