r"""
  ______  _____ _____ ____ ___        _____ ____     _____          __  __ 
 |  ____|/ ____|  __ \___ \__ \      / ____|___ \   / ____|   /\   |  \/  |
 | |__  | (___ | |__) |__) | ) |____| (___   __) | | |       /  \  | \  / |
 |  __|  \___ \|  ___/|__ < / /______\___ \ |__ <  | |      / /\ \ | |\/| |
 | |____ ____) | |    ___) / /_      ____) |___) | | |____ / ____ \| |  | |
 |______|_____/|_|   |____/____|    |_____/|____/   \_____/_/    \_\_|  |_|
                                                                           
                                                                           
    ESP32-S3 CAM - PIN DEFINITIONS MODULE
    ===================================
    Version: 2.2.0
    Fecha: 2025-12-06
    Descripción: Definiciones de pines para ESP32-S3 CAM
    Proporciona las configuraciones de pines para diferentes sensores de cámara
    Cambios:
        - V2.2.0: Corrección de pines SDA/SCL estándar para AI-Thinker ESP32-CAM (GPIO26/GPIO27)
        - V2.1.0: Corrección de pines SDA/SCL para AI-Thinker ESP32-CAM
        - V2.0.0: Actualización a nuevos valores constantes para nueva API
        - V1.0.0: Versión inicial del módulo de pines
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
    'pin_sscb_sda': 26,  # GPIO26 for SDA (standard on AI-Thinker ESP32-CAM)
    'pin_sscb_scl': 27,  # GPIO27 for SCL (standard on AI-Thinker ESP32-CAM)
    'xclk_freq_hz': PINS['XCLK_FREQ'],
    'pixel_format': 4,  # PixelFormat.JPEG (from new API)
    'frame_size': 10,   # FrameSize.VGA (from new API)
    'fb_count': 2,
    'grab_mode': 1      # GrabMode.LATEST (from new API)
}
