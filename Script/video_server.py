# video_server.py
# Módulo para servir la imagen de la cámara en tiempo real vía servidor web
# Implementa streaming de video y la interfaz principal para ver la cámara

import socket
import time
from machine import reset
from led_controller import LEDController

# Intentar importar la cámara real, sino usar simulación
try:
    import camera
    CAMERA_AVAILABLE = True
    print("Cámara real disponible")
except ImportError:
    import camera_mock as camera
    CAMERA_AVAILABLE = False
    print("Usando simulación de cámara")

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
        try:
            # Configurar la cámara con la mejor resolución disponible
            camera.init(
                0, 
                format=camera.JPEG, 
                fb_location=camera.PSRAM
            )
            
            # Configurar resolución - usar la más alta disponible
            camera.framesize(camera.FRAME_VGA)  # 640x480
            
            # Ajustes adicionales de la cámara
            camera.quality(12)  # Buena calidad
            camera.brightness(0)  # -2 a 2
            camera.contrast(0)   # -2 a 2
            camera.saturation(0) # -2 a 2
            camera.special_effect(0)  # 0 a 6
            camera.whitebalance(1)  # 0 = off, 1 = auto
            camera.bar(0)  # Black/white bars
            camera.grb_gain(0)  # Grb gain
            camera.awb_gain(1)
            camera.wb_mode(0)  # White balance mode
            camera.ae_effect(0)  # Auto exposure effect
            camera.bpc(0)  # Black pixel correction
            camera.wpc(1)  # White pixel correction
            camera.raw_gma(1)  # Raw gamma
            camera.lenc(1)  # Lens correction
            camera.hmirror(0)  # Horizontal mirror
            camera.vflip(0)    # Vertical flip
            camera.dcw(1)      # Downsize EN
            camera.colorbar(0) # Color bar
            
            print("Cámara inicializada exitosamente")
            return True
        except Exception as e:
            print("Error al inicializar la cámara:", e)
            return False
    
    def stop_camera(self):
        """
        Detiene la cámara y libera recursos
        """
        try:
            camera.deinit()
            print("Cámara detenida")
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