"""
Definiciones de pines para ESP32-S3 CAM
"""
# Pines para ESP32-S3 CAM
PINS = {
    # Pines de la cámara
    'CAM_PWDN': 35,
    'CAM_VSYNC': 38,
    'CAM_HREF': 39,
    'CAM_PCLK': 36,
    'CAM_XCLK': 37,
    'CAM_D0': 12,
    'CAM_D1': 11,
    'CAM_D2': 10,
    'CAM_D3': 9,
    'CAM_D4': 8,
    'CAM_D5': 7,
    'CAM_D6': 6,
    'CAM_D7': 5,
    
    # Pin XCLK
    'XCLK_FREQ': 20000000,  # 20MHz
}

# Configuración específica para el sensor OV2640
OV2640_PINS = {
    'pin_pwdn': PINS['CAM_PWDN'],
    'pin_vsync': PINS['CAM_VSYNC'],
    'pin_href': PINS['CAM_HREF'],
    'pin_pclk': PINS['CAM_PCLK'],
    'pin_xclk': PINS['CAM_XCLK'],
    'pin_d0': PINS['CAM_D0'],
    'pin_d1': PINS['CAM_D1'],
    'pin_d2': PINS['CAM_D2'],
    'pin_d3': PINS['CAM_D3'],
    'pin_d4': PINS['CAM_D4'],
    'pin_d5': PINS['CAM_D5'],
    'pin_d6': PINS['CAM_D6'],
    'pin_d7': PINS['CAM_D7'],
    'xclk_freq_hz': PINS['XCLK_FREQ'],
    'pixel_format': 1,  # camera.JPEG
    'frame_size': 10,   # camera.FRAME_VGA
    'fb_count': 2,
    'fb_location': 1,   # camera.PSRAM
    'grab_mode': 0      # camera.GRAB_LATEST
}