# main.py
# Archivo principal del proyecto ESP32-S3 CAM
# Integra todos los módulos: control de LED, WiFi manager, servidor de video y configuración

import time
from machine import reset
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
        video_server.run_server()
        
    except Exception as e:
        print("Error en la aplicación principal:", e)
        led.error()  # Indicar error con LED rojo
        time.sleep(3)  # Mantener el indicador de error por 3 segundos
        reset()  # Reiniciar el dispositivo después de un error
    
    finally:
        # Asegurarse de que el LED esté en estado inicial al salir
        led.inicial()

# Si se ejecuta directamente este archivo
if __name__ == "__main__":
    main()