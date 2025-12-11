r"""
  ______  _____ _____ ____ ___        _____ ____     _____          __  __ 
 |  ____|/ ____|  __ \___ \__ \      / ____|___ \   / ____|   /\   |  \/  |
 | |__  | (___ | |__) |__) | ) |____| (___   __) | | |       /  \  | \  / |
 |  __|  \___ \|  ___/|__ < / /______\___ \ |__ <  | |      / /\ \ | |\/| |
 | |____ ____) | |    ___) / /_      ____) |___) | | |____ / ____ \| |  | |
 |______|_____/|_|   |____/____|    |_____/|____/   \_____/_/    \_\_|  |_|
                                                                           
                                                                           
    ESP32-S3 CAM - CAMERA CONFIG SERVER MODULE
    ==========================================
    Version: 2.2.0
    Fecha: 2025-12-09
    Descripción: Módulo para servir la interfaz de configuración de la cámara
    Permite ajustar parámetros y ver previsualización en tiempo real
    Cambios:
        - V2.2.1: Actualización de versión para reflejar cambios en el sistema relacionados con WDT
        - V2.2.0: Compatibilidad con flujo de reinicio automático tras configuración WiFi
        - V2.1.0: Corrección del problema de watchdog timer, actualización a nueva API,
                  implementación de inicialización diferida
        - V2.0.0: Actualización completa a la nueva API de cámara con métodos get/set
        - V1.0.0: Versión inicial del módulo de configuración
"""

import socket
import time
from machine import idle
from led_controller import LEDController
from camera_utils import init_camera

# Intentar importar la cámara real, sino usar simulación
try:
    import camera
    from camera import Camera, FrameSize, PixelFormat, GrabMode
    CAMERA_AVAILABLE = True
    print("Cámara real disponible")
    # Create a camera instance for the real camera
    cam = None
except ImportError:
    import camera_mock as camera
    CAMERA_AVAILABLE = False
    print("Usando simulación de cámara")
    # For the mock, we can use the module directly
    cam = None

class CameraConfigServer:
    def __init__(self, port=80):
        """
        Inicializa el servidor de configuración de cámara
        :param port: Puerto en el que escuchará el servidor (por defecto 80)
        """
        self.port = port
        self.led = LEDController()  # Usar el controlador de LED para indicar estados
        self.is_running = False
        
    def get_camera_info(self):
        """
        Obtiene información sobre la cámara
        :return: Diccionario con información del hardware de la cámara
        """
        info = {
            'modelo': 'ESP32-S3 CAM',
            'resolucion_maxima': 'VGA (640x480)',
            'formatos_imagen': 'JPEG',
            'memoria': 'PSRAM disponible',
            'sensores': 'OV2640'
        }
        return info
    
    def get_camera_settings(self):
        """
        Obtiene los ajustes actuales de la cámara
        :return: Diccionario con los ajustes actuales
        """
        global cam
        if CAMERA_AVAILABLE and cam is not None:
            # Using the new API with get_ methods
            settings = {
                'framesize': cam.get_frame_size(),
                'quality': cam.get_quality(),
                'brightness': cam.get_brightness(),
                'contrast': cam.get_contrast(),
                'saturation': cam.get_saturation(),
                'special_effect': cam.get_special_effect(),
                'wb_mode': cam.get_wb_mode(),
                'ae_level': cam.get_ae_level(),
                'hmirror': cam.get_hmirror(),
                'vflip': cam.get_vflip()
            }
        else:
            # Using mock camera
            settings = {
                'framesize': camera.FRAME_VGA,
                'quality': camera.quality(),
                'brightness': camera.brightness(),
                'contrast': camera.contrast(),
                'saturation': camera.saturation(),
                'special_effect': camera.special_effect(),
                'wb_mode': camera.wb_mode(),
                'ae_level': camera.ae_level(),
                'hmirror': camera.hmirror(),
                'vflip': camera.vflip()
            }
        return settings
    
    def set_camera_settings(self, settings):
        """
        Establece los ajustes de la cámara, asegurando la conversión de tipos.
        :param settings: Diccionario con los ajustes a aplicar (valores pueden ser strings).
        """
        global cam
        if not (CAMERA_AVAILABLE and cam is not None):
            print("Error: intentando configurar una cámara no inicializada.")
            return

        try:
            # Convertir valores a int y aplicar settings
            if 'framesize' in settings:
                cam.set_frame_size(int(settings['framesize']))
            if 'quality' in settings:
                cam.set_quality(int(settings['quality']))
            if 'brightness' in settings:
                cam.set_brightness(int(settings['brightness']))
            if 'contrast' in settings:
                cam.set_contrast(int(settings['contrast']))
            if 'saturation' in settings:
                cam.set_saturation(int(settings['saturation']))
            if 'special_effect' in settings:
                cam.set_special_effect(int(settings['special_effect']))
            if 'wb_mode' in settings:
                cam.set_wb_mode(int(settings['wb_mode']))
            if 'ae_level' in settings:
                cam.set_ae_level(int(settings['ae_level']))
            if 'hmirror' in settings:
                cam.set_hmirror(int(settings['hmirror']))
            if 'vflip' in settings:
                cam.set_vflip(int(settings['vflip']))
            
            print("Ajustes de cámara aplicados con éxito.")

        except (ValueError, RuntimeError) as e:
            print(f"Error al aplicar ajustes de cámara (valor inválido o problema de cámara): {e}")
    
    def start_server(self):
        """
        Inicia el servidor de configuración de cámara
        """
        self.is_running = True
        
        # Iniciar el servidor TCP
        addr = socket.getaddrinfo('0.0.0.0', self.port)[0][-1]
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)
        
        print('Servidor de configuración de cámara escuchando en', addr)
        
        # Cargar plantilla HTML y reemplazar placeholders
        cam_info = self.get_camera_info()
        html = ""
        try:
            with open('html/camera_config.html', 'r') as f:
                html = f.read()
            
            html = html.replace('{{modelo}}', cam_info.get('modelo', 'N/A'))
            html = html.replace('{{resolucion_maxima}}', cam_info.get('resolucion_maxima', 'N/A'))
            html = html.replace('{{formatos_imagen}}', cam_info.get('formatos_imagen', 'N/A'))
            html = html.replace('{{memoria}}', cam_info.get('memoria', 'N/A'))
            html = html.replace('{{sensores}}', cam_info.get('sensores', 'N/A'))

        except Exception as e:
            print("Error: No se pudo cargar la plantilla HTML (html/camera_config.html).", e)
            # Provide a fallback minimal HTML page
            html = "<html><head><title>Error</title></head><body><h1>Error 500</h1><p>No se pudo cargar la interfaz de usuario. Verifique que el archivo 'html/camera_config.html' exista.</p></body></html>"
        
        while self.is_running:
            try:
                cl, addr = s.accept()
                print('Cliente de configuración conectado desde', addr)
                request = cl.recv(1024)
                request_str = request.decode('utf-8')

                # Extraer la ruta de la solicitud
                if 'GET /cam' in request_str or 'GET /' in request_str:
                    # Enviar página de configuración
                    cl.send('HTTP/1.1 200 OK\r\n')
                    cl.send('Content-Type: text/html\r\n')
                    cl.send('Connection: close\r\n\r\n')
                    cl.send(html)
                elif 'GET /stream' in request_str:
                    # Enviar frame de previsualización
                    try:
                        # Capturar imagen de la cámara
                        if CAMERA_AVAILABLE and cam is not None:
                            img = cam.capture()
                        else:
                            # Use mock camera if real camera is not available
                            img = camera.capture()

                        if img:
                            cl.send('HTTP/1.1 200 OK\r\n')
                            cl.send('Content-Type: image/jpeg\r\n')
                            cl.send('Connection: close\r\n\r\n')
                            cl.send(img)
                        else:
                            cl.send('HTTP/1.1 500 INTERNAL SERVER ERROR\r\n\r\n')
                    except RuntimeError as e:
                        print(f"Error de tiempo de ejecución al capturar imagen para previsualización: {e}")
                        import sys
                        sys.print_exception(e)
                        cl.send('HTTP/1.1 500 INTERNAL SERVER ERROR\r\n\r\n')
                elif 'POST /update_settings' in request_str:
                    # Extraer el cuerpo de la solicitud POST
                    try:
                        # Buscar el comienzo del cuerpo JSON
                        body_start = request_str.find('\r\n\r\n') + 4
                        json_data = request_str[body_start:]

                        # Aplicar los ajustes recibidos
                        import ujson
                        settings = ujson.loads(json_data)
                        self.set_camera_settings(settings)

                        # Responder con éxito
                        cl.send('HTTP/1.1 200 OK\r\n')
                        cl.send('Content-Type: text/plain\r\n')
                        cl.send('Connection: close\r\n\r\n')
                        cl.send('Configuración aplicada exitosamente')
                    except (ValueError, KeyError, RuntimeError) as e:
                        print(f"Error al procesar o aplicar ajustes: {e}")
                        cl.send('HTTP/1.1 400 BAD REQUEST\r\n\r\n')
                        cl.send('Error al procesar ajustes')
                elif 'GET /reset_camera' in request_str:
                    # Reiniciar la cámara
                    try:
                        if cam is not None:
                            cam.deinit()
                        
                        time.sleep(1)
                        cam = init_camera(initial_setup=False) # No aplicar settings detallados, solo inicializar

                        if cam:
                            # Enviar respuesta de éxito
                            cl.send('HTTP/1.1 200 OK\r\n')
                            cl.send('Content-Type: text/plain\r\n')
                            cl.send('Connection: close\r\n\r\n')
                            cl.send('Cámara reiniciada exitosamente')
                        else:
                            raise RuntimeError("Fallo al re-inicializar la cámara")
                            
                    except RuntimeError as e:
                        print(f"Error de tiempo de ejecución al reiniciar la cámara: {e}")
                        import sys
                        sys.print_exception(e)
                        cl.send('HTTP/1.1 500 INTERNAL SERVER ERROR\r\n\r\n')
                        cl.send('Error al reiniciar cámara')
                else:
                    # Ruta no encontrada
                    cl.send('HTTP/1.1 404 NOT FOUND\r\n\r\n')

                cl.close()

                # Alimentar al WDT para evitar reinicios
                idle()
            except OSError as e:
                print(f'Error de red en el servidor de configuración: {e}')
                try:
                    cl.close()
                except:
                    pass

                # Alimentar al WDT para evitar reinicios incluso en caso de error
                idle()
            except Exception as e:
                print(f'Error inesperado en el servidor de configuración: {e}')
                try:
                    cl.close()
                except:
                    pass

                # Alimentar al WDT para evitar reinicios incluso en caso de error
                idle()

        s.close()
    
    def run_server(self):
        """
        Ejecuta el servidor de configuración de cámara
        """
        global cam
        print("Iniciando servidor de configuración de cámara...")

        # Asegurarse de que la cámara esté inicializada usando la función centralizada
        cam = init_camera()
        if not cam:
            print("Fallo al inicializar la cámara desde camera_utils.")
            self.led.error()
            return False
        
        print("Cámara inicializada exitosamente para el servidor de configuración")

        # Iniciar servidor
        try:
            self.start_server()
        except KeyboardInterrupt:
            print("Servidor de configuración detenido por usuario")
        finally:
            if cam is not None:
                cam.deinit()
                cam = None
