r"""
  ______  _____ _____ ____ ___        _____ ____     _____          __  __ 
 |  ____|/ ____|  __ \___ \__ \      / ____|___ \   / ____|   /\   |  \/  |
 | |__  | (___ | |__) |__) | ) |____| (___   __) | | |       /  \  | \  / |
 |  __|  \___ \|  ___/|__ < / /______\___ \ |__ <  | |      / /\ \ | |\/| |
 | |____ ____) | |    ___) / /_      ____) |___) | | |____ / ____ \| |  | |
 |______|_____/|_|   |____/____|    |_____/|____/   \_____/_/    \_\_|  |_|
                                                                           
                                                                           
    ESP32-S3 CAM - MAIN APPLICATION
    ===============================
    Version: 2.1.0
    Fecha: 2025-12-06
    Descripción: Archivo principal del proyecto ESP32-S3 CAM
    Integra todos los módulos: control de LED, WiFi manager, servidor de video y configuración
    Cambios:
        - V2.1.2: Actualización para reflejar refactorización del bucle de streaming en video server
        - V2.1.1: Implementación de alimentación regular al watchdog timer para evitar reinicios
        - V2.1.0: Integración con nueva API de cámara, corrección de inicialización
        - V2.0.0: Actualización completa a la nueva API de cámara
        - V1.0.0: Versión inicial del proyecto
"""

import time
from machine import reset, idle
from led_controller import LEDController
from wifi_manager import WiFiManager
from video_server import VideoServer, CAMERA_AVAILABLE
from camera_config_server import CameraConfigServer

print("Estado de cámara: ", "Disponible" if CAMERA_AVAILABLE else "No disponible")
if not CAMERA_AVAILABLE:
    print("ADVERTENCIA: Usando simulación de cámara. Funcionalidad limitada.")

def main():
    print("Iniciando proyecto ESP32-S3 CAM...")
    
    # Inicializar controlador de LED
    led = LEDController()
    led.inicial()  # Indicar estado inicial con color púrpura
    time.sleep(1)  # Breve pausa para que se vea el estado inicial
    
    try:
        # Inicializar el gestor de WiFi
        wifi_manager = WiFiManager()
        
        # Configurar WiFi (intentará conectar a una red guardada o iniciar modo AP)
        wifi_connected = wifi_manager.setup_wifi()
        
        if not wifi_connected:
            # Si no se pudo conectar y se inició el modo AP, el servidor ya está corriendo
            print("Entrando en modo AP, esperando configuración de WiFi...")
            return
        
        # Si estamos aquí, estamos conectados a WiFi
        print("Conectado a WiFi exitosamente")
        print("IP asignada:", wifi_manager.get_ip_address())
        
        # Inicializar servidor de video
        video_server = VideoServer()

        # Iniciar el servidor de video
        # El servidor puede ejecutarse indefinidamente, por lo que no debería retornar
        # a menos que ocurra un error o se interrumpa
        video_server.run_server()
        
    except (OSError, RuntimeError) as e:
        print(f"Error de operación (sistema/cámara) en la aplicación principal: {e}")
        led.error()  # Indicar error con LED rojo
        time.sleep(3)  # Mantener el indicador de error por 3 segundos
        reset()  # Reiniciar el dispositivo después de un error
    except Exception as e:
        print(f"Error inesperado en la aplicación principal: {e}")
        led.error()  # Indicar error con LED rojo
        time.sleep(3)  # Mantener el indicador de error por 3 segundos
        reset()  # Reiniciar el dispositivo después de un error
    
    finally:
        # Asegurarse de que el LED esté en estado inicial al salir
        led.inicial()

# Si se ejecuta directamente este archivo
if __name__ == "__main__":
    main()
