r"""
    ___  ____  ____  ___  ____  _______  ____
   / _ \/ __ \/ __ \/ _ \/ __ \/_  __/ |/ / /
  / , _/ /_/ / /_/ / , _/ /_/ / / / /    / /
 /_/|_|\____/\____/_/|_|\____/ /_/ /_/|_/_/

    ESP32-S3 CAM - DEBUG SCRIPT
    ===========================
    Version: 2.3.0
    Fecha: 2025-12-06
    Descripción: Script de prueba para depurar la funcionalidad de la cámara ESP32-S3 CAM
    Incluye logs detallados y verificación de configuración de pines
    Cambios:
        - V2.3.0: Mejora en la prueba de I2C, verificaciones previas a inicialización de cámara
        - V2.2.0: Añadidas pruebas de PSRAM, memoria detallada e I2C, optimización de inicialización
        - V2.1.0: Corrección del problema de watchdog timer, actualización a nueva API,
                  implementación de inicialización diferida, corrección de pines SDA/SCL
        - V2.0.0: Actualización completa a la nueva API de cámara con métodos get/set
        - V1.0.0: Versión inicial de script de depuración
"""

import sys
import time
import gc

def print_log(message, level="INFO"):
    """
    Función para imprimir mensajes con marca de tiempo y nivel
    """
    timestamp = time.ticks_ms()
    print(f"[{timestamp}][{level}] {message}")
    # En MicroPython, no todos los sistemas tienen sys.stdout.flush()
    try:
        sys.stdout.flush()
    except AttributeError:
        # En algunos sistemas MicroPython, flush no está disponible
        pass

def test_camera_module():
    """
    Prueba la disponibilidad del módulo de cámara
    """
    print_log("=== INICIANDO PRUEBA DE MÓDULO DE CÁMARA ===")

    try:
        import camera
        print_log("Módulo 'camera' disponible", "SUCCESS")

        # Verificar si es la nueva API orientada a objetos
        if hasattr(camera, 'Camera'):
            print_log("API de cámara nueva detectada (orientada a objetos)", "SUCCESS")
            # Verificar que las clases necesarias existan
            required_classes = ['Camera', 'PixelFormat', 'FrameSize', 'GrabMode']
            for cls in required_classes:
                if hasattr(camera, cls):
                    print_log(f"Clase '{cls}' disponible", "SUCCESS")
                else:
                    print_log(f"Clase '{cls}' NO disponible", "ERROR")
        else:
            print_log("API de cámara antigua detectada (posiblemente incompatible)", "WARNING")
            # Verificar que las funciones necesarias existan
            required_functions = ['init', 'deinit', 'capture', 'framesize', 'quality']
            for func in required_functions:
                if hasattr(camera, func):
                    print_log(f"Función '{func}' disponible", "SUCCESS")
                else:
                    print_log(f"Función '{func}' NO disponible", "ERROR")

        return True
    except ImportError as e:
        print_log(f"Módulo 'camera' NO disponible: {e}", "ERROR")
        return False
    except Exception as e:
        print_log(f"Error inesperado al importar cámara: {e}", "ERROR")
        return False

def test_pins():
    """
    Prueba la configuración de pines para la cámara
    """
    print_log("=== INICIANDO PRUEBA DE PINS ===")
    
    # Importar la configuración de pines
    try:
        import camera_pins
        print_log("Configuración de pines importada exitosamente", "SUCCESS")
        
        # Mostrar la configuración
        if hasattr(camera_pins, 'PINS'):
            print_log("Configuración de pines:")
            for pin_name, pin_value in camera_pins.PINS.items():
                print_log(f"  {pin_name}: {pin_value}")
        else:
            print_log("No se encontró la configuración de pines", "WARNING")
            
        return True
    except ImportError:
        print_log("Archivo camera_pins.py no encontrado", "ERROR")
        return False
    except Exception as e:
        print_log(f"Error al importar configuración de pines: {e}", "ERROR")
        return False

def test_camera_initialization():
    """
    Prueba la inicialización de la cámara
    """
    print_log("=== INICIANDO PRUEBA DE INICIALIZACIÓN DE CÁMARA ===")

    # Antes de intentar inicializar, verificar que hay PSRAM y comunicación I2C
    try:
        import esp32
        psram_size = esp32.psram_size()
        if psram_size <= 0:
            print_log("ADVERTENCIA: PSRAM no disponible - la cámara probablemente no funcione", "WARNING")
        else:
            print_log(f"PSRAM disponible: {psram_size} bytes", "INFO")
    except:
        print_log("No se pudo verificar PSRAM, intentando de todas formas", "INFO")

    # Verificar si la comunicación I2C está disponible
    if not test_i2c_scan():
        print_log("ADVERTENCIA: No se detectó comunicación I2C, la cámara probablemente no esté conectada o funcione", "WARNING")

    try:
        import camera
        # Verificar primero si es la nueva API
        if not hasattr(camera, 'Camera'):
            print_log("No se detectó la nueva API de cámara, omitiendo prueba de inicialización", "WARNING")
            return False

        from camera import Camera, FrameSize, PixelFormat, GrabMode
        print_log("Usando nueva API de cámara", "SUCCESS")

        # Intentar inicializar la cámara con configuración mínima para evitar problemas de watchdog
        print_log("Intentando inicializar cámara con configuración mínima...")

        try:
            # Create the camera instance with proper configuration
            import camera_pins
            pins = camera_pins.OV2640_PINS

            # Añadir un pequeño retraso antes de la inicialización para evitar problemas de watchdog
            time.sleep_ms(50)

            # Crear la instancia de cámara sin inicializar inmediatamente
            print_log("Creando instancia de cámara...", "INFO")

            # Crear la cámara con una configuración muy reducida para evitar watchdog
            # Adaptada para trabajar mejor con OV5640 si es necesario
            try:
                cam_instance = Camera(
                    data_pins=[pins['pin_d0'], pins['pin_d1'], pins['pin_d2'], pins['pin_d3'],
                              pins['pin_d4'], pins['pin_d5'], pins['pin_d6'], pins['pin_d7']],
                    pclk_pin=pins['pin_pclk'],
                    vsync_pin=pins['pin_vsync'],
                    href_pin=pins['pin_href'],
                    sda_pin=pins['pin_sscb_sda'],  # SDA pin for I2C communication
                    scl_pin=pins['pin_sscb_scl'],  # SCL pin for I2C communication
                    xclk_pin=pins['pin_xclk'],
                    xclk_freq=pins['xclk_freq_hz'],
                    powerdown_pin=pins['pin_pwdn'],
                    reset_pin=-1,  # Adjust if needed - puede que -1 funcione mejor que -1 para OV5640
                    pixel_format=PixelFormat.JPEG,
                    frame_size=FrameSize.QQVGA,  # Resolución mínima - OV5640 puede necesitar QQVGA inicialmente
                    jpeg_quality=10,  # Calidad mínima
                    fb_count=1,  # Frame buffer único - importante para OV5640
                    grab_mode=GrabMode.WHEN_EMPTY,  # Modo menos intensivo
                    init=False  # No inicializar inmediatamente
                )

                print_log("Instancia de cámara creada. Ahora intentando inicialización...", "INFO")

                # Intentar inicializar con manejo de timeout mejorado
                # La inicialización puede tomar más tiempo con OV5640
                try:
                    print_log("Iniciando cámara - puede tomar varios segundos...", "INFO")
                    start_init = time.ticks_ms()
                    cam_instance.init()
                    init_time = time.ticks_diff(time.ticks_ms(), start_init)
                    print_log(f"Cámara inicializada exitosamente en {init_time}ms", "SUCCESS")
                except Exception as init_error:
                    print_log(f"Error en la inicialización: {init_error}", "ERROR")
                    # Intentar con un delay adicional y reintento
                    time.sleep_ms(500)  # Mayor delay para OV5640
                    try:
                        start_init = time.ticks_ms()
                        cam_instance.init()
                        init_time = time.ticks_diff(time.ticks_ms(), start_init)
                        print_log(f"Cámara inicializada después de reintento en {init_time}ms", "SUCCESS")
                    except Exception as retry_error:
                        print_log(f"Error tras reintento: {retry_error}", "ERROR")
                        return False

                # Probar solo configuraciones básicas que sean seguras para OV5640
                try:
                    time.sleep_ms(100)  # Mayor delay para que la cámara se estabilice
                    # Solo probar una configuración simple
                    cam_instance.set_quality(10)  # Calidad menor
                    print_log("Configuración de calidad aplicada", "SUCCESS")

                    # Verificar si es OV5640 probando la resolución máxima
                    max_size = cam_instance.get_max_frame_size()
                    print_log(f"Resolución máxima soportada por el sensor: {max_size}", "INFO")
                except Exception as e:
                    print_log(f"Error al aplicar configuraciones básicas: {e}", "ERROR")

                # Intentar capturar una imagen o no, dependiendo del tiempo
                try:
                    print_log("Intentando captura de imagen...")
                    # Añadir un retraso antes de capturar para dar tiempo a la cámara
                    time.sleep_ms(250)  # Mayor delay para OV5640

                    # Liberar algo de memoria antes de capturar
                    gc.collect()

                    # Intentar captura con timeout
                    img = cam_instance.capture()
                    if img:
                        print_log(f"Imagen capturada exitosamente, tamaño: {len(img)} bytes", "SUCCESS")
                    else:
                        print_log("No se pudo capturar imagen", "WARNING")
                except Exception as e:
                    print_log(f"Error al capturar imagen: {e}", "ERROR")

                # Desinicializar la cámara
                try:
                    print_log("Desinicializando cámara...", "INFO")
                    cam_instance.deinit()
                    print_log("Cámara desinicializada exitosamente", "SUCCESS")
                except Exception as e:
                    print_log(f"Error al desinicializar cámara: {e}", "ERROR")

                # Añadir un pequeño retraso después de desinicializar para evitar problemas de watchdog
                time.sleep_ms(100)

                return True
            except MemoryError:
                print_log("Error de memoria durante la creación de la instancia de cámara", "ERROR")
                return False
            except Exception as creation_error:
                print_log(f"Error durante la creación de la instancia de cámara: {creation_error}", "ERROR")
                import sys
                sys.print_exception(creation_error)
                return False

        except Exception as e:
            print_log(f"No se pudo inicializar la cámara: {e}", "ERROR")
            import sys
            sys.print_exception(e)
            return False

    except ImportError:
        print_log("Módulo 'camera' no disponible, omitiendo prueba de inicialización", "WARNING")
        return False
    except Exception as e:
        print_log(f"Error durante la inicialización de la cámara: {e}", "ERROR")
        return False

def test_memory():
    """
    Prueba el uso de memoria antes y después de operaciones de cámara
    """
    print_log("=== INICIANDO PRUEBA DE MEMORIA ===")

    # Medir memoria antes
    gc.collect()
    mem_free_before = gc.mem_free()
    print_log(f"Memoria libre antes: {mem_free_before} bytes")

    # Simular operación de cámara si está disponible
    try:
        import camera
        # Verificar primero si es la nueva API
        if hasattr(camera, 'Camera'):
            from camera import Camera, FrameSize, PixelFormat, GrabMode

            # Añadir un pequeño retraso antes de la inicialización para evitar problemas de watchdog
            time.sleep_ms(100)

            # Create the camera instance with proper configuration
            import camera_pins
            pins = camera_pins.OV2640_PINS

            # Alimentar el watchdog antes de crear la cámara
            import machine
            machine.idle()

            # Primero crear la instancia sin inicializar para evitar problemas de watchdog
            cam_instance = Camera(
                data_pins=[pins['pin_d0'], pins['pin_d1'], pins['pin_d2'], pins['pin_d3'],
                          pins['pin_d4'], pins['pin_d5'], pins['pin_d6'], pins['pin_d7']],
                pclk_pin=pins['pin_pclk'],
                vsync_pin=pins['pin_vsync'],
                href_pin=pins['pin_href'],
                sda_pin=pins['pin_sscb_sda'],  # SDA pin for I2C communication
                scl_pin=pins['pin_sscb_scl'],  # SCL pin for I2C communication
                xclk_pin=pins['pin_xclk'],
                xclk_freq=pins['xclk_freq_hz'],
                powerdown_pin=pins['pin_pwdn'],
                reset_pin=-1,  # Adjust if needed
                pixel_format=PixelFormat.JPEG,
                frame_size=FrameSize.QQVGA,  # Resolución menor para reducir carga
                jpeg_quality=10,  # Calidad menor
                fb_count=1,  # Frame buffer menor
                grab_mode=GrabMode.WHEN_EMPTY,  # Modo menos intensivo
                init=False  # No inicializar inmediatamente
            )

            # Ahora sí inicializar el objeto de cámara
            cam_instance.init()

            # Añadir un retraso antes de capturar para dar tiempo a la cámara
            time.sleep_ms(200)
            # Alimentar el watchdog
            machine.idle()

            # Capturar imagen
            img = cam_instance.capture()

            if img:
                print_log(f"Tamaño de imagen capturada: {len(img)} bytes")

            # Desinicializar
            cam_instance.deinit()

            # Añadir un pequeño retraso después de desinicializar para evitar problemas de watchdog
            time.sleep_ms(100)
        else:
            print_log("No se detectó la nueva API de cámara, omitiendo prueba de memoria con cámara", "WARNING")

    except ImportError:
        print_log("Módulo 'camera' no disponible, omitiendo prueba de memoria con cámara", "WARNING")
    except Exception as e:
        print_log(f"Error en prueba de memoria con cámara: {e}", "ERROR")

    # Medir memoria después
    gc.collect()
    time.sleep_ms(50)  # Pequeño retraso para estabilidad
    mem_free_after = gc.mem_free()
    print_log(f"Memoria libre después: {mem_free_after} bytes")
    print_log(f"Diferencia de memoria: {mem_free_before - mem_free_after} bytes")

def test_mock_camera():
    """
    Prueba el módulo de simulación de cámara
    """
    print_log("=== INICIANDO PRUEBA DE CÁMARA SIMULADA ===")
    
    try:
        import camera_mock as mock_camera
        print_log("Módulo de cámara simulada importado exitosamente", "SUCCESS")
        
        # Probar funciones de la cámara simulada
        try:
            result = mock_camera.init()
            print_log(f"Resultado de init(): {result}", "SUCCESS")
        except Exception as e:
            print_log(f"Error al llamar a init(): {e}", "ERROR")
        
        try:
            mock_camera.quality(12)
            print_log("Calidad configurada exitosamente", "SUCCESS")
        except Exception as e:
            print_log(f"Error al configurar calidad: {e}", "ERROR")
        
        try:
            img = mock_camera.capture()
            print_log(f"Imagen simulada capturada, tamaño: {len(img)} bytes", "SUCCESS")
        except Exception as e:
            print_log(f"Error al capturar imagen simulada: {e}", "ERROR")
        
        try:
            mock_camera.deinit()
            print_log("Cámara simulada desinicializada exitosamente", "SUCCESS")
        except Exception as e:
            print_log(f"Error al desinicializar cámara simulada: {e}", "ERROR")
        
        return True
    except ImportError as e:
        print_log(f"No se pudo importar módulo de cámara simulada: {e}", "ERROR")
        return False
    except Exception as e:
        print_log(f"Error en la prueba de cámara simulada: {e}", "ERROR")
        return False

def test_system_info():
    """
    Prueba la información del sistema
    """
    print_log("=== OBTENIENDO INFORMACIÓN DEL SISTEMA ===")

    import os
    import sys

    print_log(f"Versión de MicroPython: {sys.version}")
    print_log(f"Plataforma: {sys.platform}")

    try:
        import machine
        print_log(f"Microcontrolador: {machine.freq()/1000000} MHz")
    except:
        print_log("No se pudo obtener la frecuencia del microcontrolador")

    try:
        import micropython
        print_log(f"Implementación de MicroPython: {micropython.implementation}")
    except:
        print_log("No se pudo obtener la implementación de MicroPython")

    # Mostrar módulos disponibles que contengan 'camera'
    print_log("Módulos disponibles relacionados con cámara:")
    for module in sys.modules:
        if 'camera' in module.lower():
            print_log(f"  - {module}")

def test_psram():
    """
    Prueba la disponibilidad y tamaño de PSRAM
    """
    print_log("=== INICIANDO PRUEBA DE PSRAM ===")

    try:
        import esp32
        # En MicroPython, psram_size() es el método correcto
        if hasattr(esp32, 'psram_size'):
            psram_size = esp32.psram_size()
            if psram_size > 0:
                print_log(f"PSRAM disponible: {psram_size} bytes", "SUCCESS")
                return True
            else:
                print_log("PSRAM no disponible o tamaño 0", "WARNING")
                return False
        else:
            print_log("Método psram_size() no disponible en este puerto de MicroPython", "WARNING")
            # Intentar con un enfoque alternativo
            import gc
            gc.collect()
            free_memory = gc.mem_free()
            print_log(f"Memoria libre total: {free_memory} bytes", "INFO")

            # La cámara típicamente necesita PSRAM para funcionar
            if free_memory > 2000000:  # Más de 2MB
                print_log("Suficiente memoria disponible", "INFO")
                return True
            else:
                print_log("Memoria disponible limitada", "WARNING")
                return False
    except Exception as e:
        print_log(f"Error al verificar PSRAM: {e}", "ERROR")
        # Intentar con un enfoque alternativo si psram_size no está disponible
        try:
            # Verificar si hay suficiente memoria disponible para la cámara
            import gc
            gc.collect()
            free_memory = gc.mem_free()
            print_log(f"Memoria libre total: {free_memory} bytes", "INFO")

            # La cámara típicamente necesita PSRAM para funcionar
            if free_memory > 2000000:  # Más de 2MB
                print_log("Suficiente memoria disponible para operar cámara", "INFO")
                return True
            else:
                print_log("Memoria disponible limitada - puede afectar operación de cámara", "WARNING")
                return False
        except Exception as e2:
            print_log(f"Error en verificación alternativa de memoria: {e2}", "ERROR")
            return False

def test_memory_detailed():
    """
    Prueba detallada de la memoria disponible
    """
    print_log("=== INICIANDO PRUEBA DETALLADA DE MEMORIA ===")

    # Medir memoria antes de cualquier operación intensiva
    gc.collect()
    mem_free_before = gc.mem_free()
    print_log(f"Memoria libre antes de operaciones: {mem_free_before} bytes")

    try:
        # Medir heap total si es posible
        import micropython
        heap_size = micropython.heap_locked()
        print_log(f"Tamaño del heap: {heap_size} bytes")
    except:
        print_log("No se pudo obtener el tamaño del heap")

    # Medir después de importar módulos de cámara
    try:
        import camera
        gc.collect()
        mem_after_import = gc.mem_free()
        print_log(f"Memoria libre después de importar cámara: {mem_after_import} bytes")
        print_log(f"Memoria usada por importación de cámara: {mem_free_before - mem_after_import} bytes")
    except ImportError:
        print_log("Módulo de cámara no disponible para prueba de memoria", "WARNING")

    # Medir después de crear objetos
    try:
        from camera import FrameSize
        gc.collect()
        mem_after_objs = gc.mem_free()
        print_log(f"Memoria libre después de crear objetos: {mem_after_objs} bytes")
    except ImportError:
        pass  # No hacer nada si no hay cámara

    return True

def test_i2c_scan():
    """
    Prueba la comunicación I2C para detectar dispositivos (como el sensor de cámara)
    """
    print_log("=== INICIANDO PRUEBA DE COMUNICACIÓN I2C ===")

    try:
        from machine import Pin, I2C
        import camera_pins

        # Usar los pines SDA/SCL definidos en el archivo de pines
        pins = camera_pins.OV2640_PINS

        # Probar diferentes configuraciones de I2C
        i2c_configs = [
            {"freq": 100000, "name": "Baja velocidad"},
            {"freq": 200000, "name": "Velocidad media"},
            {"freq": 400000, "name": "Alta velocidad"}
        ]

        for config in i2c_configs:
            try:
                print_log(f"Probando I2C a {config['name']} ({config['freq']} Hz)...")

                # Crear objeto I2C con pull-ups activados
                i2c = I2C(0, scl=Pin(pins['pin_sscb_scl']), sda=Pin(pins['pin_sscb_sda']), freq=config['freq'])

                # Escanear dispositivos I2C
                devices = i2c.scan()

                if devices:
                    print_log(f"Dispositivos I2C encontrados con {config['name']}: {[hex(device) for device in devices]}", "SUCCESS")

                    # Verificar si se encuentra un dispositivo que podría ser la cámara
                    # El sensor OV2640 típicamente se encuentra en dirección 0x30 o 0x60
                    # El sensor OV5640 típicamente se encuentra en dirección 0x3C o 0x21
                    camera_addresses = [0x21, 0x30, 0x3C, 0x60]  # Comunes para sensores de cámara (OV2640, OV5640)
                    found_camera = [addr for addr in devices if addr in camera_addresses]

                    if found_camera:
                        print_log(f"Sensor de cámara potencial encontrado en: {[hex(addr) for addr in found_camera]}", "SUCCESS")
                        return True
                    else:
                        print_log(f"Dispositivos encontrados pero ninguno coincide con dirección de cámara típica: {[hex(addr) for addr in devices]}", "WARNING")
                        print_log(f"Direcciones comunes para cámara: {[hex(addr) for addr in camera_addresses]}", "INFO")
                        return True  # Se encontraron dispositivos, aunque no sea la cámara
                else:
                    print_log(f"No se encontraron dispositivos I2C con {config['name']}", "INFO")

            except Exception as e:
                print_log(f"Error con I2C en {config['name']}: {e}", "ERROR")
                continue  # Probar la siguiente configuración

        print_log("No se encontraron dispositivos I2C en ninguna configuración", "WARNING")
        return False

    except ImportError as e:
        print_log(f"Error al importar módulos I2C: {e}", "ERROR")
        return False
    except Exception as e:
        print_log(f"Error en la prueba de comunicación I2C: {e}", "ERROR")
        return False

def run_full_camera_test():
    """
    Ejecuta todas las pruebas de cámara
    """
    print_log("INICIANDO PRUEBA COMPLETA DE CÁMARA", "INFO")

    results = {}

    print_log("1. Probando módulo de cámara...")
    results['camera_module'] = test_camera_module()

    # Añadir un pequeño retraso entre pruebas para evitar watchdog
    time.sleep_ms(50)

    print_log("2. Probando pines de cámara...")
    results['pins'] = test_pins()

    # Añadir un pequeño retraso entre pruebas para evitar watchdog
    time.sleep_ms(50)

    print_log("3. Probando PSRAM...")
    results['psram'] = test_psram()

    # Añadir un pequeño retraso entre pruebas para evitar watchdog
    time.sleep_ms(50)

    print_log("4. Probando memoria detallada...")
    test_memory_detailed()

    # Añadir un pequeño retraso entre pruebas para evitar watchdog
    time.sleep_ms(50)

    print_log("5. Probando comunicación I2C...")
    results['i2c_scan'] = test_i2c_scan()

    # Añadir un pequeño retraso entre pruebas para evitar watchdog
    time.sleep_ms(50)

    print_log("6. Probando inicialización de cámara...")
    # Añadir un timeout adicional para la inicialización de la cámara
    start_time = time.ticks_ms()
    results['initialization'] = test_camera_initialization()
    elapsed = time.ticks_diff(time.ticks_ms(), start_time)
    print_log(f"Tiempo transcurrido en inicialización: {elapsed}ms", "INFO")

    # Añadir un pequeño retraso entre pruebas para evitar watchdog
    time.sleep_ms(50)

    print_log("7. Probando memoria general...")
    test_memory()

    # Añadir un pequeño retraso entre pruebas para evitar watchdog
    time.sleep_ms(50)

    print_log("8. Probando cámara simulada...")
    results['mock_camera'] = test_mock_camera()

    # Añadir un pequeño retraso entre pruebas para evitar watchdog
    time.sleep_ms(50)

    print_log("9. Obteniendo información del sistema...")
    test_system_info()

    # Resumen de resultados
    print_log("=== RESUMEN DE PRUEBAS ===", "INFO")
    for test_name, result in results.items():
        status = "EXITOSO" if result else "FALLIDO"
        print_log(f"{test_name}: {status}")

    # Contar pruebas exitosas
    successful_tests = sum(1 for result in results.values() if result)
    total_tests = len(results)
    print_log(f"Pruebas exitosas: {successful_tests}/{total_tests}")

    print_log("PRUEBA COMPLETA FINALIZADA", "INFO")

    # Añadir un retraso final para permitir que el mensaje de finalización se imprima antes de que el sistema pueda reiniciar
    time.sleep_ms(100)

if __name__ == "__main__":
    print_log("Script de prueba de cámara con depuración iniciado", "INFO")
    run_full_camera_test()
