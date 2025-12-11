r"""
  ______  _____ _____ ____ ___        _____ ____     _____          __  __ 
 |  ____|/ ____|  __ \___ \__ \      / ____|___ \   / ____|   /\   |  \/  |
 | |__  | (___ | |__) |__) | ) |____| (___   __) | | |       /  \  | \  / |
 |  __|  \___ \|  ___/|__ < / /______\___ \ |__ <  | |      / /\ \ | |\/| |
 | |____ ____) | |    ___) / /_      ____) |___) | | |____ / ____ \| |  | |
 |______|_____/|_|   |____/____|    |_____/|____/   \_____/_/    \_\_|  |_|
                                                                           
                                                                           
    ESP32-S3 CAM - VIDEO SERVER MODULE
    ==================================
    Version: 2.2.0
    Fecha: 2025-12-09
    Descripción: Módulo para servir la imagen de la cámara en tiempo real vía servidor web
    Implementa streaming de video y la interfaz principal para ver la cámara
    Cambios:
        - V2.2.3: Implementación de modelo de conexión efímera para evitar bloqueos del WDT
        - V2.2.2: Refactorización del bucle de streaming para mejor manejo del WDT
        - V2.2.1: Implementación de alimentación regular al watchdog timer para evitar reinicios
        - V2.2.0: Compatibilidad con flujo de reinicio automático tras configuración WiFi
        - V2.1.0: Corrección del problema de watchdog timer, actualización a nueva API,
                  implementación de inicialización diferida
        - V2.0.0: Actualización completa a la nueva API de cámara con métodos get/set
        - V1.0.0: Versión inicial del módulo de video
"""

import socket
import time
from machine import reset, idle
from led_controller import LEDController

from camera_utils import init_camera, CAMERA_AVAILABLE

# Instancia de cámara global que será gestionada por los servidores
cam = None

class VideoServer:
    def __init__(self, port=80):
        """
        Inicializa el servidor de video
        :param port: Puerto en el que escuchará el servidor (por defecto 80)
        """
        self.port = port
        self.led = LEDController()  # Usar el controlador de LED para indicar estados
        self.is_streaming = False
        
    def stop_camera(self):
        """
        Detiene la cámara y libera recursos
        """
        global cam
        try:
            if cam is not None:
                cam.deinit()
                print("Cámara detenida")
                cam = None
        except RuntimeError as e: # More specific for camera deinit issues
            print("Error al detener la cámara:", e)
    
    def start_streaming(self):
        """
        Inicia el streaming de video
        """
        self.is_streaming = True
        self.led.transmitiendo()  # Indicar estado de transmisión con LED

        # Iniciar el servidor TCP
        addr = socket.getaddrinfo('0.0.0.0', self.port)[0][-1]
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)

        print('Servidor de video escuchando en', addr)

        # Cargar la página HTML desde el archivo
        html = ""
        try:
            with open('html/video_server.html', 'r') as f:
                html = f.read()
        except Exception as e:
            print("Error: No se pudo cargar la plantilla HTML (html/video_server.html).", e)
            html = "<html><head><title>Error</title></head><body><h1>Error 500</h1><p>No se pudo cargar la interfaz de usuario. Verifique que el archivo 'html/video_server.html' exista.</p></body></html>"

        # Establecer un timeout para aceptar conexiones, para no bloquear indefinidamente
        s.settimeout(0.5)  # 500ms timeout para aceptar conexiones

        while self.is_streaming:
            try:
                cl = None  # Inicializar cl para asegurar que no quede de iteraciones anteriores
                try:
                    cl, addr = s.accept()
                    print('Cliente de video conectado desde', addr)
                    request = cl.recv(1024)
                    request_str = request.decode('utf-8')

                    # Extraer la ruta de la solicitud
                    if 'GET / ' in request_str:
                        # Enviar página principal
                        cl.send('HTTP/1.1 200 OK\r\n')
                        cl.send('Content-Type: text/html\r\n')
                        cl.send('Connection: close\r\n\r\n')
                        cl.send(html)
                    elif 'GET /stream' in request_str:
                        # Comenzar streaming de video
                        cl.send('HTTP/1.1 200 OK\r\n')
                        cl.send('Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n')

                        # Enviar un frame inmediato
                        if CAMERA_AVAILABLE and cam is not None:
                            img = cam.capture()
                        else:
                            # Use mock camera if real camera is not available
                            img = cam.capture()

                        if img:
                            # Enviar frame al cliente
                            cl.send('--frame\r\n')
                            cl.send('Content-Type: image/jpeg\r\n\r\n')
                            cl.send(img)
                            cl.send('\r\n')

                        # Cerrar la conexión inmediatamente después de enviar un frame
                        # Esto cambia el modelo de streaming a un modelo más sencillo
                        # que no mantiene conexiones abiertas indefinidamente
                    else:
                        # Ruta no encontrada
                        cl.send('HTTP/1.1 404 NOT FOUND\r\n\r\n')

                except OSError as e:
                    # Si el timeout se alcanza, simplemente continuar y alimentar el WDT
                    if e.errno == socket.ETIMEDOUT or e.errno == 110:  # ETIMEDOUT o timeout
                        pass
                    else:
                        raise e  # Si es otro error, lanzarlo para manejarlo
                finally:
                    if cl:
                        cl.close()

                # Alimentar al WDT en cada iteración del bucle principal
                idle()

                # Pequeña pausa para permitir que otros procesos se ejecuten
                time.sleep_ms(10)

            except OSError as e:
                print('Error de red en el servidor de video:', e)
                idle()
                time.sleep_ms(100)
            except Exception as e:
                print('Error inesperado en el servidor de video:', e)
                idle()
                time.sleep_ms(100)

        s.close()
    
    def stop_streaming(self):
        """
        Detiene el streaming de video
        """
        self.is_streaming = False
        self.led.modo_station()  # Volver al estado Station cuando deja de transmitir
    
    def run_server(self):
        """
        Ejecuta el servidor de video principal
        """
        print("Iniciando servidor de video...")

        # Inicializar la cámara
        global cam
        cam = init_camera()
        if not cam:
            print("No se pudo inicializar la cámara")
            self.led.error()
            return False

        # Iniciar streaming
        try:
            self.start_streaming()
        except KeyboardInterrupt:
            print("Servidor de video detenido por usuario")
        except (OSError, RuntimeError) as e:
            print(f"Error de operación (red/cámara) en el servidor de video: {e}")
        except Exception as e:
            print(f"Error inesperado en el servidor de video: {e}")
        finally:
            self.stop_streaming()
            self.stop_camera()
            self.led.modo_station()  # Volver al estado Station
