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
        - V2.2.0: Compatibilidad con flujo de reinicio automático tras configuración WiFi
        - V2.1.0: Corrección del problema de watchdog timer, actualización a nueva API,
                  implementación de inicialización diferida
        - V2.0.0: Actualización completa a la nueva API de cámara con métodos get/set
        - V1.0.0: Versión inicial del módulo de video
"""

import socket
import time
from machine import reset
from led_controller import LEDController

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

class VideoServer:
    def __init__(self, port=80):
        """
        Inicializa el servidor de video
        :param port: Puerto en el que escuchará el servidor (por defecto 80)
        """
        self.port = port
        self.led = LEDController()  # Usar el controlador de LED para indicar estados
        self.is_streaming = False
        
    def initialize_camera(self):
        """
        Inicializa la cámara del ESP32-S3
        :return: True si la inicialización fue exitosa, False si no
        """
        global cam
        try:
            # Create the camera instance with proper configuration
            # Using the pin configuration from camera_pins module
            import camera_pins
            pins = camera_pins.OV2640_PINS

            cam = Camera(
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
                frame_size=FrameSize.VGA,  # 640x480
                jpeg_quality=12,  # Good quality
                fb_count=pins['fb_count'],
                grab_mode=GrabMode.LATEST,
                init=True
            )

            # Ajustes adicionales de la cámara usando los métodos get/set
            cam.set_brightness(0)  # -2 a 2
            cam.set_contrast(0)   # -2 a 2
            cam.set_saturation(0) # -2 a 2
            cam.set_special_effect(0)  # 0 a 6
            #cam.set_whitebal(True)  # 0 = off, 1 = auto - assuming there's no set_whitebal, using set_awb
            cam.set_colorbar(False)  # Black/white bars
            # Note: Some functions may not be available in the new API; we'll use available ones
            cam.set_awb_gain(True)
            cam.set_wb_mode(0)  # White balance mode
            #cam.set_ae_level(0)  # Auto exposure effect - not directly matching old API
            cam.set_bpc(False)  # Black pixel correction
            cam.set_wpc(True)  # White pixel correction
            cam.set_raw_gma(True)  # Raw gamma
            cam.set_lenc(True)  # Lens correction
            cam.set_hmirror(False)  # Horizontal mirror
            cam.set_vflip(False)    # Vertical flip
            cam.set_dcw(True)      # Downsize EN
            #cam.set_colorbar(False) # Color bar - already set above

            print("Cámara inicializada exitosamente")
            return True
        except Exception as e:
            print("Error al inicializar la cámara:", e)
            import sys
            sys.print_exception(e)
            return False
    
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
        except Exception as e:
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
        
        # HTML para la página principal con tema oscuro
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ESP32-S3 CAM - Vista en Vivo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #121212;
            color: #e0e0e0;
            text-align: center;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: #1e1e1e;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
        h1 {
            color: #bb86fc;
        }
        .video-container {
            margin: 20px auto;
            text-align: center;
        }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(0,0,0,0.5);
        }
        .info {
            margin-top: 20px;
            padding: 15px;
            background-color: #2d2d2d;
            border-radius: 5px;
            text-align: left;
        }
        .config-link {
            margin-top: 20px;
            padding: 10px;
            background-color: #2d2d2d;
            border-radius: 5px;
        }
        a {
            color: #bb86fc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Vista en Vivo - ESP32-S3 CAM</h1>
        <div class="video-container">
            <img src="/stream" alt="Flujo de video en vivo" id="videoFeed" width="640" height="480">
        </div>
        <div class="info">
            <h3>Información del dispositivo</h3>
            <p>Esta página muestra la transmisión en vivo de la cámara ESP32-S3 CAM.</p>
            <p>La imagen se actualiza automáticamente en tiempo real.</p>
        </div>
        <div class="config-link">
            <p>Ir a la <a href="/cam">página de configuración de la cámara</a></p>
        </div>
    </div>
</body>
</html>"""
        
        while self.is_streaming:
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
                    
                    while self.is_streaming:
                        try:
                            # Capturar imagen de la cámara
                            if CAMERA_AVAILABLE and cam is not None:
                                img = cam.capture()
                            else:
                                # Use mock camera if real camera is not available
                                img = camera.capture()

                            if img:
                                # Enviar frame al cliente
                                cl.send('--frame\r\n')
                                cl.send('Content-Type: image/jpeg\r\n\r\n')
                                cl.send(img)
                                cl.send('\r\n')
                            # Pequeña pausa para controlar la velocidad del video
                            time.sleep(0.1)
                        except Exception as e:
                            print("Error en el streaming:", e)
                            break
                else:
                    # Ruta no encontrada
                    cl.send('HTTP/1.1 404 NOT FOUND\r\n\r\n')
                
                cl.close()
            except Exception as e:
                print('Error en el servidor de video:', e)
                try:
                    cl.close()
                except:
                    pass
                
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
        if not self.initialize_camera():
            print("No se pudo inicializar la cámara")
            self.led.error()
            return False
        
        # Iniciar streaming
        try:
            self.start_streaming()
        except KeyboardInterrupt:
            print("Servidor de video detenido por usuario")
        finally:
            self.stop_streaming()
            self.stop_camera()
            self.led.modo_station()  # Volver al estado Station
