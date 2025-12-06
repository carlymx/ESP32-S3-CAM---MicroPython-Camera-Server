"""
Módulo simulado para cámara ESP32-S3 para pruebas
"""
import time

# Constantes para simular la cámara
JPEG = 1
PSRAM = 2
FRAME_VGA = 10
GRAB_LATEST = 0

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