"""
camera_test_debug.py
Script de prueba para depurar la funcionalidad de la cámara ESP32-S3 CAM
Incluye logs detallados y verificación de configuración de pines
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
    
    try:
        import camera
        
        # Intentar inicializar la cámara con configuración estándar
        print_log("Intentando inicializar cámara...")
        
        # Configuración estándar
        result = camera.init(
            format=camera.JPEG,
            fb_location=camera.PSRAM
        )
        
        if result:
            print_log("Cámara inicializada exitosamente", "SUCCESS")
            
            # Probar configuraciones adicionales
            try:
                camera.framesize(camera.FRAME_VGA)  # 640x480
                camera.quality(12)
                print_log("Configuraciones aplicadas exitosamente", "SUCCESS")
            except Exception as e:
                print_log(f"Error al aplicar configuraciones: {e}", "ERROR")
            
            # Intentar capturar una imagen
            try:
                print_log("Intentando captura de imagen...")
                img = camera.capture()
                if img:
                    print_log(f"Imagen capturada exitosamente, tamaño: {len(img)} bytes", "SUCCESS")
                else:
                    print_log("No se pudo capturar imagen", "WARNING")
            except Exception as e:
                print_log(f"Error al capturar imagen: {e}", "ERROR")
            
            # Desinicializar la cámara
            try:
                camera.deinit()
                print_log("Cámara desinicializada exitosamente", "SUCCESS")
            except Exception as e:
                print_log(f"Error al desinicializar cámara: {e}", "ERROR")
            
            return True
        else:
            print_log("No se pudo inicializar la cámara", "ERROR")
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
        
        # Inicializar cámara
        camera.init(format=camera.JPEG, fb_location=camera.PSRAM)
        
        # Capturar imagen
        img = camera.capture()
        
        if img:
            print_log(f"Tamaño de imagen capturada: {len(img)} bytes")
        
        # Desinicializar
        camera.deinit()
        
    except ImportError:
        print_log("Módulo 'camera' no disponible, omitiendo prueba de memoria con cámara", "WARNING")
    except Exception as e:
        print_log(f"Error en prueba de memoria con cámara: {e}", "ERROR")
    
    # Medir memoria después
    gc.collect()
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

def run_full_camera_test():
    """
    Ejecuta todas las pruebas de cámara
    """
    print_log("INICIANDO PRUEBA COMPLETA DE CÁMARA", "INFO")
    
    results = {}
    
    print_log("1. Probando módulo de cámara...")
    results['camera_module'] = test_camera_module()
    
    print_log("2. Probando pines de cámara...")
    results['pins'] = test_pins()
    
    print_log("3. Probando inicialización de cámara...")
    results['initialization'] = test_camera_initialization()
    
    print_log("4. Probando memoria...")
    test_memory()
    
    print_log("5. Probando cámara simulada...")
    results['mock_camera'] = test_mock_camera()
    
    print_log("6. Obteniendo información del sistema...")
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

if __name__ == "__main__":
    print_log("Script de prueba de cámara con depuración iniciado", "INFO")
    run_full_camera_test()