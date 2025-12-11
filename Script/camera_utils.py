"""
    ESP32-S3 CAM - CAMERA UTILS MODULE
    =================================
    Version: 1.0.0
    Fecha: 2025-12-10
    Descripción: Módulo con funciones de utilidad para la cámara,
                 incluyendo una función de inicialización centralizada.
"""

from machine import idle, WDT

# Intentar importar la cámara real, sino usar simulación
try:
    import camera
    from camera import Camera, FrameSize, PixelFormat, GrabMode
    CAMERA_AVAILABLE = True
except ImportError:
    import camera_mock as camera
    from camera_mock import Camera, FrameSize, PixelFormat, GrabMode
    CAMERA_AVAILABLE = False

def init_camera(initial_setup=True):
    """
    Inicializa la cámara del ESP32-S3 con una configuración estándar,
    gestionando el WDT para evitar reinicios.
    :param initial_setup: Si es True, aplica una configuración detallada inicial.
    :return: Una instancia de la cámara inicializada o None si falla.
    """
    if not CAMERA_AVAILABLE:
        print("Usando simulación de cámara para inicialización.")
        try:
            # Crear una instancia de la cámara simulada
            cam_mock_instance = camera.Camera(debug_prints=True)
            cam_mock_instance.init()
            print("Cámara simulada inicializada.")
            return cam_mock_instance
        except Exception as e:
            print("Error al inicializar la cámara simulada:", e)
            return None

    # --- Configuración para cámara real ---
    wdt = None
    try:
        import camera_pins
        pins = camera_pins.OV2640_PINS

        print("Configurando WDT con timeout largo para inicialización...")
        wdt = WDT(timeout=10000)  # 10 segundos
        idle()

        cam = Camera(
            data_pins=[pins['pin_d0'], pins['pin_d1'], pins['pin_d2'], pins['pin_d3'],
                       pins['pin_d4'], pins['pin_d5'], pins['pin_d6'], pins['pin_d7']],
            pclk_pin=pins['pin_pclk'],
            vsync_pin=pins['pin_vsync'],
            href_pin=pins['pin_href'],
            sda_pin=pins['pin_sscb_sda'],
            scl_pin=pins['pin_sscb_scl'],
            xclk_pin=pins['pin_xclk'],
            xclk_freq=pins['xclk_freq_hz'],
            powerdown_pin=pins['pin_pwdn'],
            reset_pin=-1,
            pixel_format=PixelFormat.JPEG,
            frame_size=FrameSize.VGA,
            jpeg_quality=12,
            fb_count=pins['fb_count'],
            grab_mode=GrabMode.LATEST,
            init=True
        )
        
        wdt.feed() # Alimentar el WDT inmediatamente después de la inicialización

        if initial_setup:
            # Ajustes adicionales de la cámara
            cam.set_brightness(0)
            cam.set_contrast(0)
            cam.set_saturation(0)
            cam.set_special_effect(0)
            cam.set_colorbar(False)
            cam.set_awb_gain(True)
            cam.set_wb_mode(0)
            cam.set_bpc(False)
            cam.set_wpc(True)
            cam.set_raw_gma(True)
            cam.set_lenc(True)
            cam.set_hmirror(False)
            cam.set_vflip(False)
            cam.set_dcw(True)
            wdt.feed() # Alimentar de nuevo tras la configuración

        print("Cámara real inicializada exitosamente")
        return cam
    except Exception as e:
        print("Error al inicializar la cámara real:", e)
        import sys
        sys.print_exception(e)
        return None
    finally:
        # Es buena práctica alimentar el WDT al salir de la función
        if wdt:
            wdt.feed()
