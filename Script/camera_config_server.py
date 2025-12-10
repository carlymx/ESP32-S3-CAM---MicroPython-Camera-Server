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
        - V2.2.0: Compatibilidad con flujo de reinicio automático tras configuración WiFi
        - V2.1.0: Corrección del problema de watchdog timer, actualización a nueva API,
                  implementación de inicialización diferida
        - V2.0.0: Actualización completa a la nueva API de cámara con métodos get/set
        - V1.0.0: Versión inicial del módulo de configuración
"""

import socket
import time
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
        Establece los ajustes de la cámara
        :param settings: Diccionario con los ajustes a aplicar
        """
        global cam
        try:
            if CAMERA_AVAILABLE and cam is not None:
                # Using the new API with set_ methods
                if 'framesize' in settings:
                    cam.set_frame_size(settings['framesize'])
                if 'quality' in settings:
                    cam.set_quality(settings['quality'])
                if 'brightness' in settings:
                    cam.set_brightness(settings['brightness'])
                if 'contrast' in settings:
                    cam.set_contrast(settings['contrast'])
                if 'saturation' in settings:
                    cam.set_saturation(settings['saturation'])
                if 'special_effect' in settings:
                    cam.set_special_effect(settings['special_effect'])
                if 'wb_mode' in settings:
                    cam.set_wb_mode(settings['wb_mode'])
                if 'ae_level' in settings:
                    cam.set_ae_level(settings['ae_level'])
                if 'hmirror' in settings:
                    cam.set_hmirror(settings['hmirror'])
                if 'vflip' in settings:
                    cam.set_vflip(settings['vflip'])
            else:
                # Using mock camera
                if 'framesize' in settings:
                    camera.framesize(settings['framesize'])
                if 'quality' in settings:
                    camera.quality(settings['quality'])
                if 'brightness' in settings:
                    camera.brightness(settings['brightness'])
                if 'contrast' in settings:
                    camera.contrast(settings['contrast'])
                if 'saturation' in settings:
                    camera.saturation(settings['saturation'])
                if 'special_effect' in settings:
                    camera.special_effect(settings['special_effect'])
                if 'wb_mode' in settings:
                    camera.wb_mode(settings['wb_mode'])
                if 'ae_level' in settings:
                    camera.ae_level(settings['ae_level'])
                if 'hmirror' in settings:
                    camera.hmirror(settings['hmirror'])
                if 'vflip' in settings:
                    camera.vflip(settings['vflip'])
        except Exception as e:
            print("Error al aplicar ajustes de cámara:", e)
    
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
        
        # Obtener información de la cámara
        cam_info = self.get_camera_info()
        
        # HTML para la página de configuración con tema oscuro
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Configuración de Cámara - ESP32-S3 CAM</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #121212;
            color: #e0e0e0;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        .header {{
            text-align: center;
            color: #bb86fc;
        }}
        .main-content {{
            display: flex;
            flex-direction: row;
            gap: 20px;
        }}
        .video-section {{
            flex: 3;
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.5);
        }}
        .controls-section {{
            flex: 1;
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.5);
            overflow-y: auto;
            max-height: 800px;
        }}
        .video-container {{
            text-align: center;
            margin-bottom: 20px;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(0,0,0,0.5);
        }}
        .info-box {{
            margin-top: 20px;
            padding: 15px;
            background-color: #2d2d2d;
            border-radius: 5px;
        }}
        .control-group {{
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid #333;
        }}
        .control-group h3 {{
            margin-top: 0;
            color: #bb86fc;
        }}
        label {{
            display: block;
            margin: 10px 0 5px 0;
        }}
        input[type="range"], select {{
            width: 100%;
            padding: 5px;
            background-color: #2d2d2d;
            color: #e0e0e0;
            border: 1px solid #444;
            border-radius: 3px;
        }}
        button {{
            background-color: #bb86fc;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
            font-size: 16px;
        }}
        button:hover {{
            background-color: #9a67ea;
        }}
        .camera-info {{
            margin-top: 20px;
        }}
        .camera-info h3 {{
            color: #bb86fc;
        }}
        .camera-info ul {{
            text-align: left;
            padding-left: 20px;
        }}
        .back-link {{
            text-align: center;
            margin-top: 20px;
            padding: 10px;
            background-color: #2d2d2d;
            border-radius: 5px;
        }}
        a {{
            color: #bb86fc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Configuración de Cámara - ESP32-S3 CAM</h1>
        </div>
        <div class="main-content">
            <div class="video-section">
                <div class="video-container">
                    <img src="/stream" alt="Previsualización de la cámara" id="videoPreview" width="640" height="480">
                </div>
                <div class="info-box">
                    <h3>Información de la Cámara</h3>
                    <ul>
                        <li><strong>Modelo:</strong> {cam_info['modelo']}</li>
                        <li><strong>Resolución Máxima:</strong> {cam_info['resolucion_maxima']}</li>
                        <li><strong>Formatos de Imagen:</strong> {cam_info['formatos_imagen']}</li>
                        <li><strong>Memoria:</strong> {cam_info['memoria']}</li>
                        <li><strong>Sensor:</strong> {cam_info['sensores']}</li>
                    </ul>
                </div>
            </div>
            <div class="controls-section">
                <h2>Controles de Cámara</h2>
                
                <div class="control-group">
                    <h3>Calidad y Resolución</h3>
                    <label for="quality">Calidad de Imagen (1-63, menor es mejor):</label>
                    <input type="range" id="quality" name="quality" min="1" max="63" value="12">
                    <label for="framesize">Resolución:</label>
                    <select id="framesize">
                        <option value="5">QQVGA (160x120)</option>
                        <option value="7">QCIF (176x144)</option>
                        <option value="6">HQVGA (240x160)</option>
                        <option value="8" selected="selected">QVGA (320x240)</option>
                        <option value="9">CIF (400x296)</option>
                        <option value="10">VGA (640x480)</option>
                        <option value="12">SVGA (800x600)</option>
                        <option value="13">XGA (1024x768)</option>
                        <option value="14">HD (1280x720)</option>
                        <option value="15">SXGA (1280x1024)</option>
                        <option value="16">UXGA (1600x1200)</option>
                    </select>
                </div>
                
                <div class="control-group">
                    <h3>Ajustes de Imagen</h3>
                    <label for="brightness">Brillo (-2 a 2):</label>
                    <input type="range" id="brightness" name="brightness" min="-2" max="2" value="0">
                    <label for="contrast">Contraste (-2 a 2):</label>
                    <input type="range" id="contrast" name="contrast" min="-2" max="2" value="0">
                    <label for="saturation">Saturación (-2 a 2):</label>
                    <input type="range" id="saturation" name="saturation" min="-2" max="2" value="0">
                </div>
                
                <div class="control-group">
                    <h3>Efectos</h3>
                    <label for="special_effect">Efecto Especial:</label>
                    <select id="special_effect">
                        <option value="0" selected="selected">Normal</option>
                        <option value="1">Negativo</option>
                        <option value="2">Grises</option>
                        <option value="3">Rojo</option>
                        <option value="4">Verde</option>
                        <option value="5">Azul</option>
                        <option value="6">Sepia</option>
                    </select>
                    <label for="wb_mode">Modo de Balance de Blanco:</label>
                    <select id="wb_mode">
                        <option value="0" selected="selected">Off</option>
                        <option value="1">Auto</option>
                        <option value="2">Soleado</option>
                        <option value="3">Nublado</option>
                        <option value="4">Oficina</option>
                        <option value="5">Hogar</option>
                    </select>
                    <label for="ae_level">Nivel de Exposición (-2 a 2):</label>
                    <input type="range" id="ae_level" name="ae_level" min="-2" max="2" value="0">
                </div>
                
                <div class="control-group">
                    <h3>Orientación</h3>
                    <label for="hmirror">Espejo Horizontal:</label>
                    <select id="hmirror">
                        <option value="0" selected="selected">No</option>
                        <option value="1">Sí</option>
                    </select>
                    <label for="vflip">Volteo Vertical:</label>
                    <select id="vflip">
                        <option value="0" selected="selected">No</option>
                        <option value="1">Sí</option>
                    </select>
                </div>
                
                <button onclick="applySettings()">Aplicar Configuración</button>
                <button onclick="resetCamera()">Reiniciar Cámara</button>
            </div>
        </div>
        <div class="back-link">
            <p><a href="/">Volver a la vista en vivo</a></p>
        </div>
    </div>
    
    <script>
        function applySettings() {{
            const settings = {{
                quality: document.getElementById('quality').value,
                framesize: document.getElementById('framesize').value,
                brightness: document.getElementById('brightness').value,
                contrast: document.getElementById('contrast').value,
                saturation: document.getElementById('saturation').value,
                special_effect: document.getElementById('special_effect').value,
                wb_mode: document.getElementById('wb_mode').value,
                ae_level: document.getElementById('ae_level').value,
                hmirror: document.getElementById('hmirror').value,
                vflip: document.getElementById('vflip').value
            }};
            
            // Enviar ajustes al servidor
            fetch('/update_settings', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify(settings)
            }})
            .then(response => response.text())
            .then(data => {{
                console.log('Ajustes aplicados:', data);
                alert('Ajustes de cámara aplicados exitosamente');
            }})
            .catch((error) => {{
                console.error('Error:', error);
                alert('Error al aplicar ajustes de cámara');
            }});
        }}
        
        function resetCamera() {{
            if (confirm('¿Estás seguro de que quieres reiniciar la cámara?')) {{
                fetch('/reset_camera')
                .then(response => response.text())
                .then(data => {{
                    console.log('Cámara reiniciada:', data);
                    location.reload();
                }})
                .catch((error) => {{
                    console.error('Error:', error);
                    alert('Error al reiniciar la cámara');
                }});
            }}
        }}
    </script>
</body>
</html>"""
        
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
                    except Exception as e:
                        print("Error al capturar imagen para previsualización:", e)
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
                    except Exception as e:
                        print("Error al procesar ajustes:", e)
                        cl.send('HTTP/1.1 400 BAD REQUEST\r\n\r\n')
                        cl.send('Error al procesar ajustes')
                elif 'GET /reset_camera' in request_str:
                    # Reiniciar la cámara
                    try:
                        if CAMERA_AVAILABLE and cam is not None:
                            cam.deinit()
                            time.sleep(1)
                            # Recreate the camera instance with proper configuration
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
                        else:
                            # For mock camera, just call the deinit/init functions
                            camera.deinit()
                            time.sleep(1)
                            camera.init(format=camera.JPEG, fb_location=camera.PSRAM)
                            camera.framesize(camera.FRAME_VGA)

                        # Enviar respuesta de éxito
                        cl.send('HTTP/1.1 200 OK\r\n')
                        cl.send('Content-Type: text/plain\r\n')
                        cl.send('Connection: close\r\n\r\n')
                        cl.send('Cámara reiniciada exitosamente')
                    except Exception as e:
                        print("Error al reiniciar la cámara:", e)
                        import sys
                        sys.print_exception(e)
                        cl.send('HTTP/1.1 500 INTERNAL SERVER ERROR\r\n\r\n')
                        cl.send('Error al reiniciar cámara')
                else:
                    # Ruta no encontrada
                    cl.send('HTTP/1.1 404 NOT FOUND\r\n\r\n')
                
                cl.close()
            except Exception as e:
                print('Error en el servidor de configuración:', e)
                try:
                    cl.close()
                except:
                    pass
                
        s.close()
    
    def run_server(self):
        """
        Ejecuta el servidor de configuración de cámara
        """
        global cam
        print("Iniciando servidor de configuración de cámara...")

        # Asegurarse de que la cámara esté inicializada
        if CAMERA_AVAILABLE:
            try:
                # Create the camera instance with proper configuration
                import camera_pins
                pins = camera_pins.OV2640_PINS

                cam = Camera(
                    data_pins=[pins['pin_d0'], pins['pin_d1'], pins['pin_d2'], pins['pin_d3'],
                              pins['pin_d4'], pins['pin_d5'], pins['pin_d6'], pins['pin_d7']],
                    pclk_pin=pins['pin_pclk'],
                    vsync_pin=pins['pin_vsync'],
                    href_pin=pins['pin_href'],
                    sda_pin=pins['pin_pwdn'],  # This might need adjustment based on actual board
                    scl_pin=pins['pin_vsync'],  # This might need adjustment based on actual board
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

                print("Cámara inicializada exitosamente para el servidor de configuración")
            except Exception as e:
                print("Error al inicializar la cámara:", e)
                import sys
                sys.print_exception(e)
                self.led.error()
                return False
        else:
            # For mock camera, initialize it
            try:
                if not camera.init(format=camera.JPEG, fb_location=camera.PSRAM):
                    print("No se pudo inicializar la cámara simulada para el servidor de configuración")
                    self.led.error()
                    return False
            except Exception as e:
                print("Error al inicializar la cámara simulada:", e)
                self.led.error()
                return False

        # Iniciar servidor
        try:
            self.start_server()
        except KeyboardInterrupt:
            print("Servidor de configuración detenido por usuario")
        finally:
            if CAMERA_AVAILABLE and cam is not None:
                cam.deinit()
                cam = None
            elif not CAMERA_AVAILABLE:  # For mock camera
                try:
                    camera.deinit()
                except:
                    pass
