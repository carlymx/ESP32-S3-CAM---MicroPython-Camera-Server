"""
    ESP32-S3 CAM - SIMPLE CAMERA TEST
    ==================================
    Versión: 1.0.0
    Fecha: 2025-12-10
    Descripción: Script simple de prueba para cámara ESP32-S3.
    Conexión WiFi mediante variables editables, inicialización de cámara
    y streaming MJPEG vía servidor web.
    
    USO:
    1. Editar WIFI_SSID y WIFI_PASSWORD más abajo
    2. Subir a ESP32-S3 CAM
    3. Ejecutar
    4. Conectar a IP mostrada en consola
    
    Compatibilidad: ESP32-S3 CAM (AI Thinker) con MicroPython camera API
"""

import network
import socket
import time
import gc
from machine import WDT, idle, reset

# ==================== CONFIGURACIÓN EDITABLE ====================
# EDITAR ESTAS VARIABLES CON TUS CREDENCIALES WIFI
WIFI_SSID = "tu_red_wifi"        # Cambiar por el nombre de tu red WiFi
WIFI_PASSWORD = "tu_password"    # Cambiar por la contraseña de tu red WiFi

# Configuración de cámara (compatible ESP32-S3 AI Thinker)
CAMERA_CONFIG = {
    'data_pins': [12, 11, 10, 9, 8, 7, 6, 5],  # D0-D7 para ESP32-S3 CAM AI-Thinker
    'pclk_pin': 36,    # PCLK
    'vsync_pin': 38,   # VSYNC
    'href_pin': 39,    # HREF
    'sda_pin': 26,     # SDA (I2C) - GPIO26 estándar
    'scl_pin': 27,     # SCL (I2C) - GPIO27 estándar
    'xclk_pin': 37,    # XCLK
    'xclk_freq': 20000000,  # 20MHz para OV2640
    'powerdown_pin': 35,    # PWDN
    'reset_pin': -1,        # No usar reset
    'pixel_format': 4,      # PixelFormat.JPEG (valor 4)
    'frame_size': 10,       # FrameSize.VGA (640x480)
    'jpeg_quality': 85,     # Calidad JPEG (0-100)
    'fb_count': 2,          # 2 buffers para mejor rendimiento
    'grab_mode': 1,         # GrabMode.LATEST
}

# ==================== FUNCIONES DE WIFI ====================

def connect_wifi(ssid, password):
    """
    Conecta a la red WiFi especificada.
    Retorna True si éxito, False si falla.
    """
    print(f"Conectando a WiFi: {ssid}")
    
    try:
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        
        # Desactivar AP si está activo
        ap_if = network.WLAN(network.AP_IF)
        if ap_if.active():
            ap_if.active(False)
        
        # Intentar conexión
        sta_if.connect(ssid, password)
        
        # Esperar conexión (máx 20 segundos)
        max_wait = 20
        while max_wait > 0:
            if sta_if.isconnected():
                ip = sta_if.ifconfig()[0]
                print(f"✓ Conectado a WiFi: {ssid}")
                print(f"✓ IP asignada: {ip}")
                return True
            max_wait -= 1
            print(f"Esperando conexión... ({max_wait}s)")
            time.sleep(1)
            idle()  # Mantener vivo el WDT
        
        print("✗ No se pudo conectar a WiFi (timeout)")
        return False
        
    except OSError as e:
        print(f"✗ Error de red al conectar WiFi: {e}")
        return False
    except Exception as e:
        print(f"✗ Error inesperado en WiFi: {e}")
        return False

# ==================== FUNCIONES DE CÁMARA ====================

def init_camera():
    """
    Inicializa la cámara con configuración compatible.
    Retorna objeto cámara o None si falla.
    """
    print("Inicializando cámara...")
    
    # Configurar WDT con timeout extendido para inicialización
    wdt = WDT(timeout=10000)  # 10 segundos
    idle()
    
    try:
        # Verificar PSRAM (requerido para cámara)
        try:
            import esp32
            psram_size = esp32.psram_size()
            if psram_size > 0:
                print(f"✓ PSRAM disponible: {psram_size} bytes")
            else:
                print("⚠️  Advertencia: PSRAM no disponible o tamaño 0")
                print("   La cámara puede no funcionar correctamente")
        except ImportError:
            print("⚠️  Advertencia: No se pudo verificar PSRAM")
        except Exception as e:
            print(f"⚠️  Advertencia al verificar PSRAM: {e}")
        
        # Importar módulo de cámara
        from camera import Camera, PixelFormat, FrameSize, GrabMode
        
        # Crear instancia de cámara
        cam = Camera(
            data_pins=CAMERA_CONFIG['data_pins'],
            pclk_pin=CAMERA_CONFIG['pclk_pin'],
            vsync_pin=CAMERA_CONFIG['vsync_pin'],
            href_pin=CAMERA_CONFIG['href_pin'],
            sda_pin=CAMERA_CONFIG['sda_pin'],
            scl_pin=CAMERA_CONFIG['scl_pin'],
            xclk_pin=CAMERA_CONFIG['xclk_pin'],
            xclk_freq=CAMERA_CONFIG['xclk_freq'],
            powerdown_pin=CAMERA_CONFIG['powerdown_pin'],
            reset_pin=CAMERA_CONFIG['reset_pin'],
            pixel_format=PixelFormat.JPEG,
            frame_size=FrameSize.VGA,
            jpeg_quality=CAMERA_CONFIG['jpeg_quality'],
            fb_count=CAMERA_CONFIG['fb_count'],
            grab_mode=GrabMode.LATEST,
            init=True  # Auto-inicializar
        )
        
        wdt.feed()  # Alimentar WDT tras inicialización exitosa
        
        # Verificar que la cámara funciona
        sensor_name = cam.get_sensor_name()
        print(f"✓ Cámara inicializada: {sensor_name}")
        print(f"✓ Resolución: {cam.get_pixel_width()}x{cam.get_pixel_height()}")
        print(f"✓ Formato: {cam.get_pixel_format()}")
        
        return cam
        
    except ImportError as e:
        print("✗ Error: Módulo 'camera' no disponible")
        print("  Asegúrate de usar firmware MicroPython con soporte de cámara")
        return None
    except Exception as e:
        print(f"✗ Error al inicializar cámara: {e}")
        import sys
        sys.print_exception(e)
        return None
    finally:
        if 'wdt' in locals():
            wdt.feed()

# ==================== HTML EMBEBIDO ====================

HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32-S3 CAM Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #121212;
            color: #ffffff;
            text-align: center;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: #1e1e1e;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
        h1 {
            color: #4CAF50;
            margin-bottom: 5px;
        }
        .status {
            color: #bbbbbb;
            margin-bottom: 20px;
        }
        .video-container {
            margin: 20px auto;
            text-align: center;
        }
        img {
            max-width: 100%;
            border: 2px solid #333;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
        }
        .info {
            margin-top: 20px;
            padding: 15px;
            background: #2a2a2a;
            border-radius: 5px;
            text-align: left;
        }
        .refresh-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px;
        }
        .refresh-btn:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>ESP32-S3 CAM - Test Simple</h1>
        <div class="status">Streaming en vivo desde la cámara</div>
        
        <div class="video-container">
            <img src="/stream" alt="Video en vivo" id="video">
        </div>
        
        <div class="info">
            <h3>Información del sistema:</h3>
            <p><strong>Resolución:</strong> VGA (640x480)</p>
            <p><strong>Formato:</strong> JPEG comprimido</p>
            <p><strong>Actualización:</strong> ~1-2 FPS</p>
            <p><strong>Nota:</strong> Si la imagen no se actualiza, recarga la página</p>
        </div>
        
        <button class="refresh-btn" onclick="window.location.reload()">Recargar página</button>
    </div>
    
    <script>
        // Auto-refresh de la imagen cada 500ms (~2 FPS)
        setInterval(function() {
            var img = document.getElementById('video');
            img.src = '/stream?t=' + new Date().getTime();
        }, 500);
    </script>
</body>
</html>"""

# ==================== SERVIDOR MJPEG ====================

def handle_client(cl, addr, cam):
    """
    Maneja una conexión de cliente HTTP.
    """
    try:
        request = cl.recv(1024)
        request_str = request.decode('utf-8')
        
        if 'GET / ' in request_str or 'GET /index' in request_str:
            # Servir página HTML
            cl.send(b'HTTP/1.1 200 OK\r\n')
            cl.send(b'Content-Type: text/html\r\n')
            cl.send(b'Connection: close\r\n\r\n')
            cl.send(HTML_PAGE.encode())
            
        elif 'GET /stream' in request_str:
            # Enviar un solo frame JPEG (simple, como video_server.py)
            try:
                img = cam.capture()
                if img:
                    cl.send(b'HTTP/1.1 200 OK\r\n')
                    cl.send(b'Content-Type: image/jpeg\r\n')
                    cl.send(b'Connection: close\r\n\r\n')
                    cl.send(img)
                else:
                    cl.send(b'HTTP/1.1 500 INTERNAL SERVER ERROR\r\n\r\n')
                    cl.send(b'Error capturando imagen')
            except Exception as e:
                cl.send(b'HTTP/1.1 500 INTERNAL SERVER ERROR\r\n\r\n')
                cl.send(b'Error interno del servidor')
                print(f"Error capturando imagen: {e}")
                    
        else:
            # Ruta no encontrada
            cl.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
            cl.send(b'<html><body><h1>404 - No encontrado</h1></body></html>')
            
    except Exception as e:
        print(f"Error manejando cliente: {e}")
    finally:
        cl.close()

def run_mjpeg_server(cam, port=80):
    """
    Ejecuta servidor HTTP con imagen JPEG simple.
    """
    print(f"Iniciando servidor web en puerto {port}...")
    
    addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    s.settimeout(0.5)  # Timeout para aceptar conexiones
    
    print(f"✓ Servidor listo en http://{addr[0]}:{port}")
    print("  - Página principal: /")
    print("  - Imagen JPEG: /stream")
    
    # Configurar WDT para operación normal
    wdt = WDT(timeout=2000)  # 2 segundos
    
    try:
        while True:
            try:
                cl, addr = s.accept()
                print(f"Conexión desde: {addr[0]}")
                handle_client(cl, addr, cam)
                wdt.feed()  # Alimentar WDT después de cada conexión
            except OSError as e:
                # Timeout en accept (normal)
                idle()
                wdt.feed()
                continue
            except Exception as e:
                print(f"Error aceptando conexión: {e}")
                idle()
                wdt.feed()
                
    except KeyboardInterrupt:
        print("\nServidor detenido por usuario")
    finally:
        s.close()
        if cam:
            cam.deinit()
        print("Recursos liberados")

# ==================== FUNCIÓN PRINCIPAL ====================

def main():
    """
    Función principal del test.
    """
    print("\n" + "="*50)
    print("ESP32-S3 CAM - TEST SIMPLE DE CÁMARA")
    print("="*50)
    
    # Verificar credenciales WiFi
    if WIFI_SSID == "tu_red_wifi" or WIFI_PASSWORD == "tu_password":
        print("⚠️ ADVERTENCIA: Credenciales WiFi no configuradas")
        print("  Edita WIFI_SSID y WIFI_PASSWORD al inicio del script")
        print("  Script continuará pero WiFi fallará")
    
    # Limpiar memoria
    gc.collect()
    print(f"Memoria libre: {gc.mem_free()} bytes")
    
    # Conectar WiFi
    if not connect_wifi(WIFI_SSID, WIFI_PASSWORD):
        print("\nNo se pudo conectar a WiFi. Verifica:")
        print("  1. Credenciales correctas en el script")
        print("  2. Red WiFi disponible")
        print("  3. ESP32-S3 en rango de la red")
        print("\nContinuando sin WiFi...")
        print("La cámara se inicializará pero no habrá servidor web.")
        print("Presiona Ctrl+C para cancelar en 5 segundos...")
        time.sleep(5)
        return
    
    # Inicializar cámara
    cam = init_camera()
    if not cam:
        print("\n✗ No se pudo inicializar la cámara")
        print("  Posibles causas:")
        print("  1. Firmware sin soporte de cámara")
        print("  2. Pines incorrectos para tu hardware")
        print("  3. Problemas de hardware/conexiones")
        return
    
    # Ejecutar servidor
    try:
        run_mjpeg_server(cam)
    except KeyboardInterrupt:
        print("\nTest interrumpido por usuario")
    except Exception as e:
        print(f"\nError en servidor: {e}")
    finally:
        if cam:
            cam.deinit()
        print("Test finalizado")

# ==================== EJECUCIÓN ====================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido")
    except Exception as e:
        print(f"Error crítico: {e}")
        import sys
        sys.print_exception(e)
    finally:
        print("Reiniciando en 3 segundos...")
        time.sleep(3)
        reset()