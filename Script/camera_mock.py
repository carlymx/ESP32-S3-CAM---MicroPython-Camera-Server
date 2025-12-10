r"""
  ______  _____ _____ ____ ___        _____ ____     _____          __  __ 
 |  ____|/ ____|  __ \___ \__ \      / ____|___ \   / ____|   /\   |  \/  |
 | |__  | (___ | |__) |__) | ) |____| (___   __) | | |       /  \  | \  / |
 |  __|  \___ \|  ___/|__ < / /______\___ \ |__ <  | |      / /\ \ | |\/| |
 | |____ ____) | |    ___) / /_      ____) |___) | | |____ / ____ \| |  | |
 |______|_____/|_|   |____/____|    |_____/|____/   \_____/_/    \_\_|  |_|
                                                                           
                                                                           
    ESP32-S3 CAM - CAMERA MOCK MODULE
    ================================
    Version: 2.1.0
    Fecha: 2025-12-06
    Descripción: Módulo simulado para cámara ESP32-S3 para pruebas
    Proporciona una implementación simulada de la cámara para entornos sin hardware físico
    Cambios:
        - V2.1.0: Añadidas clases de la nueva API, métodos get/set completos
        - V2.0.0: Actualización completa a la nueva API de cámara con métodos get/set
        - V1.0.0: Versión inicial del módulo simulado
"""
import time

# Constantes para simular la cámara
JPEG = 1
PSRAM = 2
FRAME_VGA = 10
GRAB_LATEST = 0

# Definir las clases para imitar la nueva API
class PixelFormat:
    JPEG = 4
    YUV422 = 1
    YUV420 = 2
    GRAYSCALE = 3
    RGB565 = 0
    RGB888 = 5
    RAW = 6
    RGB444 = 7
    RGB555 = 8

class FrameSize:
    R96X96 = 0
    QQVGA = 1
    R128x128 = 2
    QCIF = 3
    HQVGA = 4
    R240X240 = 5
    QVGA = 6
    R320X320 = 7
    CIF = 8
    HVGA = 9
    VGA = 10
    SVGA = 11
    XGA = 12
    HD = 13
    SXGA = 14
    UXGA = 15
    FHD = 16
    P_HD = 17
    P_3MP = 18
    QXGA = 19
    QHD = 20
    WQXGA = 21
    P_FHD = 22
    QSXGA = 23

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

# Simular valores constantes de cámara
QUALITY = 12
BRIGHTNESS = 0
CONTRAST = 0
SATURATION = 0
SPECIAL_EFFECT = 0
WB_MODE = 1
AE_LEVEL = 0
HMIRROR = 0
VFLIP = 0

# Variables para mantener el estado de configuración
_quality = QUALITY
_brightness = BRIGHTNESS
_contrast = CONTRAST
_saturation = SATURATION
_special_effect = SPECIAL_EFFECT
_wb_mode = WB_MODE
_ae_level = AE_LEVEL
_hmirror = HMIRROR
_vflip = VFLIP

# Variables para otros estados
_frame_size = FrameSize.VGA
_gainceiling = GainCeiling.X2
_colorbar = False
_whitebal = True
_gain_ctrl = True
_exposure_ctrl = True
_aec2 = False
_awb_gain = True
_agc_gain = 0
_aec_value = 0
_dcw = True
_bpc = False
_wpc = True
_raw_gma = True
_lenc = True

class Camera:
    def __init__(self, *args, **kwargs):
        """
        Inicializa la cámara simulada con los parámetros proporcionados
        """
        print("Inicializando cámara simulada con argumentos:", args, kwargs)
        init_result = init(*args, **kwargs)
        if init_result:
            print("Cámara simulada inicializada exitosamente")
        else:
            print("Error al inicializar cámara simulada")

    def init(self):
        """
        Simula la inicialización de la cámara
        """
        return init()

    def deinit(self):
        """
        Simula la desinicialización de la cámara
        """
        return deinit()

    def capture(self):
        """
        Simula la captura de una imagen
        """
        return capture()

    def reconfigure(self, frame_size=None, pixel_format=None, grab_mode=None, fb_count=None):
        """
        Simula la reconfiguración de la cámara
        """
        settings = {}
        if frame_size is not None:
            settings['frame_size'] = frame_size
        if pixel_format is not None:
            settings['pixel_format'] = pixel_format
        if grab_mode is not None:
            settings['grab_mode'] = grab_mode
        if fb_count is not None:
            settings['fb_count'] = fb_count
        print(f"Reconfigurando cámara simulada con: {settings}")
        return True

    def frame_available(self):
        """
        Simula la verificación de disponibilidad de frame
        """
        print("Verificando disponibilidad de frame simulado")
        return True

    def free_buffer(self):
        """
        Simula liberación de buffer
        """
        print("Liberando buffer simulado")
        return None

    # Métodos get para obtener configuraciones
    def get_frame_size(self):
        return _frame_size

    def get_pixel_format(self):
        return PixelFormat.JPEG  # Default

    def get_grab_mode(self):
        return GrabMode.LATEST  # Default

    def get_fb_count(self):
        return 2  # Default

    def get_quality(self):
        return _quality

    def get_brightness(self):
        return _brightness

    def get_contrast(self):
        return _contrast

    def get_saturation(self):
        return _saturation

    def get_special_effect(self):
        return _special_effect

    def get_wb_mode(self):
        return _wb_mode

    def get_ae_level(self):
        return _ae_level

    def get_hmirror(self):
        return _hmirror

    def get_vflip(self):
        return _vflip

    def get_pixel_width(self):
        # Return width based on frame size
        if _frame_size == FrameSize.VGA:
            return 640
        elif _frame_size == FrameSize.QVGA:
            return 320
        else:
            return 320  # default

    def get_pixel_height(self):
        # Return height based on frame size
        if _frame_size == FrameSize.VGA:
            return 480
        elif _frame_size == FrameSize.QVGA:
            return 240
        else:
            return 240  # default

    def get_sensor_name(self):
        return "OV2640_SIMULADO"

    def get_max_frame_size(self):
        return FrameSize.UXGA

    # Métodos set para configurar parámetros
    def set_frame_size(self, value):
        global _frame_size
        _frame_size = value
        print(f"Configurando frame_size a: {value}")

    def set_quality(self, value):
        global _quality
        _quality = value
        print(f"Configurando calidad a: {value}")

    def set_brightness(self, value):
        global _brightness
        _brightness = value
        print(f"Configurando brillo a: {value}")

    def set_contrast(self, value):
        global _contrast
        _contrast = value
        print(f"Configurando contraste a: {value}")

    def set_saturation(self, value):
        global _saturation
        _saturation = value
        print(f"Configurando saturación a: {value}")

    def set_special_effect(self, value):
        global _special_effect
        _special_effect = value
        print(f"Configurando efecto especial a: {value}")

    def set_wb_mode(self, value):
        global _wb_mode
        _wb_mode = value
        print(f"Configurando wb_mode a: {value}")

    def set_ae_level(self, value):
        global _ae_level
        _ae_level = value
        print(f"Configurando ae_level a: {value}")

    def set_hmirror(self, value):
        global _hmirror
        _hmirror = value
        print(f"Configurando hmirror a: {value}")

    def set_vflip(self, value):
        global _vflip
        _vflip = value
        print(f"Configurando vflip a: {value}")

    def set_gainceiling(self, value):
        global _gainceiling
        _gainceiling = value
        print(f"Configurando gainceiling a: {value}")

    def set_colorbar(self, value):
        global _colorbar
        _colorbar = value
        print(f"Configurando colorbar a: {value}")

    def set_whitebal(self, value):
        global _whitebal
        _whitebal = value
        print(f"Configurando whitebal a: {value}")

    def set_gain_ctrl(self, value):
        global _gain_ctrl
        _gain_ctrl = value
        print(f"Configurando gain_ctrl a: {value}")

    def set_exposure_ctrl(self, value):
        global _exposure_ctrl
        _exposure_ctrl = value
        print(f"Configurando exposure_ctrl a: {value}")

    def set_aec2(self, value):
        global _aec2
        _aec2 = value
        print(f"Configurando aec2 a: {value}")

    def set_awb_gain(self, value):
        global _awb_gain
        _awb_gain = value
        print(f"Configurando awb_gain a: {value}")

    def set_agc_gain(self, value):
        global _agc_gain
        _agc_gain = value
        print(f"Configurando agc_gain a: {value}")

    def set_aec_value(self, value):
        global _aec_value
        _aec_value = value
        print(f"Configurando aec_value a: {value}")

    def set_dcw(self, value):
        global _dcw
        _dcw = value
        print(f"Configurando dcw a: {value}")

    def set_bpc(self, value):
        global _bpc
        _bpc = value
        print(f"Configurando bpc a: {value}")

    def set_wpc(self, value):
        global _wpc
        _wpc = value
        print(f"Configurando wpc a: {value}")

    def set_raw_gma(self, value):
        global _raw_gma
        _raw_gma = value
        print(f"Configurando raw_gma a: {value}")

    def set_lenc(self, value):
        global _lenc
        _lenc = value
        print(f"Configurando lenc a: {value}")

def init(*args, **kwargs):
    """
    Simula la inicialización de la cámara
    """
    print("Cámara simulada inicializada con argumentos:", args, kwargs)
    return True

def deinit():
    """
    Simula la desinicialización de la cámara
    """
    print("Cámara simulada desinicializada")
    return True

def capture():
    """
    Simula la captura de una imagen
    """
    # En un entorno real, esto devolvería datos de imagen JPEG
    # En esta simulación, creamos un pequeño buffer simulado
    print("Capturando imagen simulada...")
    # Simular un pequeño payload JPEG
    mock_jpeg_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x08\x00\x08\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xd2\xcf \xff\xd9'
    return mock_jpeg_data

def framesize(size=None):
    """
    Simula configuración de resolución
    """
    global _framesize
    if size is not None:
        _framesize = size
        print(f"Configurando resolución de imagen a: {size}")
    else:
        return _framesize

def quality(qual=None):
    """
    Simula configuración de calidad
    """
    global _quality
    if qual is not None:
        _quality = qual
        print(f"Configurando calidad de imagen a: {qual}")
    else:
        return _quality

def brightness(bright=None):
    """
    Simula configuración de brillo
    """
    global _brightness
    if bright is not None:
        _brightness = bright
        print(f"Configurando brillo a: {bright}")
    else:
        return _brightness

def contrast(contr=None):
    """
    Simula configuración de contraste
    """
    global _contrast
    if contr is not None:
        _contrast = contr
        print(f"Configurando contraste a: {contr}")
    else:
        return _contrast

def saturation(sat=None):
    """
    Simula configuración de saturación
    """
    global _saturation
    if sat is not None:
        _saturation = sat
        print(f"Configurando saturación a: {sat}")
    else:
        return _saturation

def special_effect(effect=None):
    """
    Simula configuración de efecto especial
    """
    global _special_effect
    if effect is not None:
        _special_effect = effect
        print(f"Configurando efecto especial a: {effect}")
    else:
        return _special_effect

def whitebalance(wb=None):
    """
    Simula configuración de balance de blanco
    """
    global _wb_mode
    if wb is not None:
        _wb_mode = wb
        print(f"Configurando balance de blanco a: {wb}")
    else:
        return _wb_mode

def wb_mode(mode=None):
    """
    Simula configuración de modo de balance de blanco
    """
    global _wb_mode
    if mode is not None:
        _wb_mode = mode
        print(f"Configurando modo de balance de blanco a: {mode}")
    else:
        return _wb_mode

def ae_level(level=None):
    """
    Simula configuración de nivel de exposición automática
    """
    global _ae_level
    if level is not None:
        _ae_level = level
        print(f"Configurando nivel de exposición automática a: {level}")
    else:
        return _ae_level

def hmirror(mirror=None):
    """
    Simula configuración de espejo horizontal
    """
    global _hmirror
    if mirror is not None:
        _hmirror = mirror
        print(f"Configurando espejo horizontal a: {mirror}")
    else:
        return _hmirror

def vflip(flip=None):
    """
    Simula configuración de volteo vertical
    """
    global _vflip
    if flip is not None:
        _vflip = flip
        print(f"Configurando volteo vertical a: {flip}")
    else:
        return _vflip

def bar(bar_val=None):
    """
    Simula configuración de barras B/W
    """
    print(f"Configurando barras B/W a: {bar_val}")
    return 0

def grb_gain(gain=None):
    """
    Simula configuración de ganancia GRB
    """
    print(f"Configurando ganancia GRB a: {gain}")
    return 0

def awb_gain(gain=None):
    """
    Simula configuración de ganancia AWB
    """
    print(f"Configurando ganancia AWB a: {gain}")
    return 1

def bpc(bpc_val=None):
    """
    Simula configuración de corrección de píxeles negros
    """
    print(f"Configurando corrección de píxeles negros a: {bpc_val}")
    return 0

def wpc(wpc_val=None):
    """
    Simula configuración de corrección de píxeles blancos
    """
    print(f"Configurando corrección de píxeles blancos a: {wpc_val}")
    return 1

def raw_gma(gma=None):
    """
    Simula configuración de gamma raw
    """
    print(f"Configurando gamma raw a: {gma}")
    return 1

def lenc(lenc_val=None):
    """
    Simula configuración de corrección de lente
    """
    print(f"Configurando corrección de lente a: {lenc_val}")
    return 1

def dcw(dcw_val=None):
    """
    Simula configuración DCW
    """
    print(f"Configurando DCW a: {dcw_val}")
    return 1

def colorbar(cb_val=None):
    """
    Simula configuración de barra de color
    """
    print(f"Configurando barra de color a: {cb_val}")
    return 0
