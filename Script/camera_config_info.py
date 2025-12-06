# camera_config_info.py
# Información sobre la configuración de la cámara ESP32-S3 CAM

"""
Este archivo proporciona información sobre la configuración de pines típica para
una cámara ESP32-S3 CAM con sensor OV2640 u otro sensor compatible.

El error "'module' object has no attribute 'init'" indica que el módulo 'camera' 
no está disponible en tu versión de MicroPython. Esto puede suceder por:

1. La versión de MicroPython no incluye el soporte para cámara
2. El firmware específico no tiene el driver de cámara incluido
3. El hardware es diferente al esperado

Para solucionar este problema:

1. Asegúrate de que estés usando un firmware de MicroPython que incluya soporte para cámara
2. Verifica que tu modelo específico de ESP32-S3 CAM esté soportado
3. Confirma que los pines estén conectados correctamente
"""

CAMERA_PIN_CONFIGS = {
    "ESP32-S3 CAM_AITHINKER": {
        # Configuración típica para el modelo AI Thinker ESP32-S3 CAM
        "CAM_PWDN": 35,
        "CAM_VSYNC": 38,
        "CAM_HREF": 39,
        "CAM_PCLK": 36,
        "CAM_XCLK": 37,
        "CAM_D0": 12,
        "CAM_D1": 11,
        "CAM_D2": 10,
        "CAM_D3": 9,
        "CAM_D4": 8,
        "CAM_D5": 7,
        "CAM_D6": 6,
        "CAM_D7": 5,
        "XCLK_FREQ": 20000000,  # 20MHz
    },
    "ESP32-S3-KORVO-2": {
        # Configuración para ESP32-S3-Korvo-2 (tiene dos cámaras)
        "CAM1_PWDN": -1,
        "CAM1_VSYNC": 21,
        "CAM1_HREF": 39,
        "CAM1_PCLK": 40,
        "CAM1_XCLK": 22,
        "CAM1_D0": 43,
        "CAM1_D1": 42,
        "CAM1_D2": 41,
        "CAM1_D3": 4,
        "CAM1_D4": 5,
        "CAM1_D5": 33,
        "CAM1_D6": 37,
        "CAM1_D7": 36,
    }
}

def get_camera_config(board_type="ESP32-S3 CAM_AITHINKER"):
    """
    Obtiene la configuración de pines para la cámara según el tipo de placa
    """
    if board_type in CAMERA_PIN_CONFIGS:
        return CAMERA_PIN_CONFIGS[board_type]
    else:
        print(f"Advertencia: Configuración para {board_type} no encontrada, usando configuración por defecto")
        return CAMERA_PIN_CONFIGS["ESP32-S3 CAM_AITHINKER"]

def check_camera_support():
    """
    Verifica si el módulo de cámara está disponible
    """
    try:
        import camera
        print("Módulo de cámara disponible")
        return True
    except ImportError:
        print("Módulo de cámara no disponible en esta instalación de MicroPython")
        print("Necesitas instalar una versión de MicroPython con soporte para cámara")
        return False

if __name__ == "__main__":
    print("Información de configuración de cámara:")
    print("Configuraciones disponibles:")
    for config_name in CAMERA_PIN_CONFIGS:
        print(f"  - {config_name}")
    
    print(f"\nSoporte de cámara disponible: {check_camera_support()}")
    
    config = get_camera_config()
    print(f"\nConfiguración de pines para ESP32-S3 CAM:")
    for pin_name, pin_num in config.items():
        print(f"  {pin_name}: {pin_num}")