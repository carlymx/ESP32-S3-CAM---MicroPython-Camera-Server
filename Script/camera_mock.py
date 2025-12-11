"""
  ______  _____ _____ ____ ___        _____ ____     _____          __  __ 
 |  ____|/ ____|  __ \___ \__ \      / ____|___ \   / ____|   /\   |  \/  |
 | |__  | (___ | |__) |__) | ) |____| (___   __) | | |       /  \  | \  / |
 |  __|  \___ \|  ___/|__ < / /______\___ \ |__ <  | |      / /\ \ | |\/| |
 | |____ ____) | |    ___) / /_      ____) |___) | | |____ / ____ \| |  | |
 |______|_____/|_|   |____/____|    |_____||____/   \_____/_/    \_\_|  |_|
                                                                           
                                                                           
    ESP32-S3 CAM - CAMERA MOCK MODULE (REFACTORED)
    ==============================================
    Version: 3.0.0
    Fecha: 2025-12-10
    Descripción: Módulo simulado para cámara ESP32-S3.
                 Esta versión elimina la API dual y se comporta como una
                 instancia de clase, igual que la cámara real.
    Cambios:
        - V3.0.0: Refactorización completa a una API orientada a objetos.
                  El estado es manejado por la instancia.
                  Se eliminaron las funciones a nivel de módulo duplicadas.
        - V2.1.0: Añadidas clases de la nueva API, métodos get/set completos
        - V2.0.0: Actualización completa a la nueva API de cámara con métodos get/set
        - V1.0.0: Versión inicial del módulo simulado
"
import time

# --- Clases de constantes para simular la API de la cámara ---
class PixelFormat:
    JPEG = 4
    YUV422 = 1
    GRAYSCALE = 3
    RGB565 = 0

class FrameSize:
    QQVGA = 1
    QVGA = 6
    VGA = 10
    SVGA = 11
    XGA = 12
    HD = 13
    UXGA = 15

class GrabMode:
    WHEN_EMPTY = 0
    LATEST = 1

class GainCeiling:
    X2 = 0
    X4 = 1
    X8 = 2
    X16 = 3
    X32 = 4
    X64 = 5
    X128 = 6

# --- Clase principal de simulación de cámara ---
class Camera:
    def __init__(self, *args, debug_prints=False, **kwargs):
        """
        Inicializa la cámara simulada. El estado se almacena en la instancia.
        """
        self._initialized = False
        self._debug_prints = debug_prints
        if self._debug_prints:
            print("Cámara simulada creada. Llamar a .init() para inicializar.")
        
        # Estado interno de la cámara (valores por defecto)
        self._framesize = FrameSize.VGA
        self._quality = 12
        self._brightness = 0
        self._contrast = 0
        self._saturation = 0
        self._special_effect = 0
        self._wb_mode = 1
        self._ae_level = 0
        self._hmirror = False
        self._vflip = False
        self._gainceiling = GainCeiling.X2
        self._colorbar = False
        self._awb_gain = True
        self._dcw = True
        self._bpc = False
        self._wpc = True
        self._raw_gma = True
        self._lenc = True
        
        # Simular una inicialización completa si se pasan argumentos
        # como en la API real: Camera(param1=value1, ...)
        if 'init' in kwargs and kwargs['init'] is True:
            self.init(*args, **kwargs)

    def init(self, *args, **kwargs):
        """
        Simula la inicialización de la cámara.
        """
        if self._initialized:
            if self._debug_prints:
                print("Cámara simulada ya está inicializada.")
            return True
            
        if self._debug_prints:
            print("Inicializando cámara simulada con argumentos:", args, kwargs)
        self._initialized = True
        return True

    def deinit(self):
        """
        Simula la desinicialización de la cámara.
        """
        if not self._initialized:
            if self._debug_prints:
                print("Cámara simulada no estaba inicializada.")
            return True
            
        if self._debug_prints:
            print("Cámara simulada desinicializada.")
        self._initialized = False
        return True

    def capture(self):
        """
        Simula la captura de una imagen.
        """
        if not self._initialized:
            if self._debug_prints:
                print("Error: La cámara simulada no está inicializada.")
            return None
            
        if self._debug_prints:
            print("Capturando imagen simulada...")
        # Simular un pequeño payload JPEG
        return b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x08\x00\x08\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xd2\xcf \xff\xd9'

    # --- Métodos Get ---
    def get_frame_size(self): return self._framesize
    def get_quality(self): return self._quality
    def get_brightness(self): return self._brightness
    def get_contrast(self): return self._contrast
    def get_saturation(self): return self._saturation
    def get_special_effect(self): return self._special_effect
    def get_wb_mode(self): return self._wb_mode
    def get_ae_level(self): return self._ae_level
    def get_hmirror(self): return self._hmirror
    def get_vflip(self): return self._vflip
    def get_gainceiling(self): return self._gainceiling
    def get_colorbar(self): return self._colorbar
    def get_awb_gain(self): return self._awb_gain
    def get_dcw(self): return self._dcw
    def get_bpc(self): return self._bpc
    def get_wpc(self): return self._wpc
    def get_raw_gma(self): return self._raw_gma
    def get_lenc(self): return self._lenc

    # --- Métodos Set ---
    def set_frame_size(self, value):
        self._framesize = value
        if self._debug_prints:
            print(f"SIM: Frame size -> {value}")
    def set_quality(self, value):
        self._quality = value
        if self._debug_prints:
            print(f"SIM: Quality -> {value}")
    def set_brightness(self, value):
        self._brightness = value
        if self._debug_prints:
            print(f"SIM: Brightness -> {value}")
    def set_contrast(self, value):
        self._contrast = value
        if self._debug_prints:
            print(f"SIM: Contrast -> {value}")
    def set_saturation(self, value):
        self._saturation = value
        if self._debug_prints:
            print(f"SIM: Saturation -> {value}")
    def set_special_effect(self, value):
        self._special_effect = value
        if self._debug_prints:
            print(f"SIM: Special effect -> {value}")
    def set_wb_mode(self, value):
        self._wb_mode = value
        if self._debug_prints:
            print(f"SIM: WB mode -> {value}")
    def set_ae_level(self, value):
        self._ae_level = value
        if self._debug_prints:
            print(f"SIM: AE level -> {value}")
    def set_hmirror(self, value):
        self._hmirror = bool(value)
        if self._debug_prints:
            print(f"SIM: H-Mirror -> {bool(value)}")
    def set_vflip(self, value):
        self._vflip = bool(value)
        if self._debug_prints:
            print(f"SIM: V-Flip -> {bool(value)}")
    def set_gainceiling(self, value):
        self._gainceiling = value
        if self._debug_prints:
            print(f"SIM: Gain ceiling -> {value}")
    def set_colorbar(self, value):
        self._colorbar = bool(value)
        if self._debug_prints:
            print(f"SIM: Colorbar -> {bool(value)}")
    def set_awb_gain(self, value):
        self._awb_gain = bool(value)
        if self._debug_prints:
            print(f"SIM: AWB gain -> {bool(value)}")
    def set_dcw(self, value):
        self._dcw = bool(value)
        if self._debug_prints:
            print(f"SIM: DCW -> {bool(value)}")
    def set_bpc(self, value):
        self._bpc = bool(value)
        if self._debug_prints:
            print(f"SIM: BPC -> {bool(value)}")
    def set_wpc(self, value):
        self._wpc = bool(value)
        if self._debug_prints:
            print(f"SIM: WPC -> {bool(value)}")
    def set_raw_gma(self, value):
        self._raw_gma = bool(value)
        if self._debug_prints:
            print(f"SIM: Raw GMA -> {bool(value)}")
    def set_lenc(self, value):
        self._lenc = bool(value)
        if self._debug_prints:
            print(f"SIM: LENC -> {bool(value)}")
        
    # --- Otros métodos para completar la API ---
    def reconfigure(self, *args, **kwargs):
        if self._debug_prints:
            print("SIM: Reconfiguring camera with", args, kwargs)
        return True
    def frame_available(self):
        return True
    def free_buffer(self):
        pass
    def get_pixel_width(self):
        return 640
    def get_pixel_height(self):
        return 480
    def get_sensor_name(self):
        return "OV2640_SIMULATED"
    def get_max_frame_size(self):
        return FrameSize.UXGA