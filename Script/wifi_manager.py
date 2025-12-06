# wifi_manager.py
# Módulo para gestionar la conexión WiFi del ESP32-S3 CAM
# Implementa modo AP para configuración inicial y modo Station para conexión normal

import network
import socket
import ure
import time
import json
from machine import reset
from led_controller import LEDController

class WiFiManager:
    def __init__(self, ssid_file="ssid_config.json"):
        """
        Inicializa el gestor de WiFi
        :param ssid_file: Archivo donde se guardan las credenciales de WiFi
        """
        self.sta_if = network.WLAN(network.STA_IF)
        self.ap_if = network.WLAN(network.AP_IF)
        self.ssid_file = ssid_file
        self.led = LEDController()  # Usar el controlador de LED para indicar estados
        self.ssid = None
        self.password = None
        
    def load_credentials(self):
        """
        Carga las credenciales de WiFi desde el archivo
        :return: True si se cargaron correctamente, False si no
        """
        try:
            with open(self.ssid_file, 'r') as f:
                config = json.load(f)
                self.ssid = config.get('ssid')
                self.password = config.get('password')
            return True
        except Exception as e:
            print("No se pudieron cargar las credenciales WiFi:", e)
            return False
    
    def save_credentials(self, ssid, password):
        """
        Guarda las credenciales de WiFi en el archivo
        :param ssid: Nombre de la red WiFi
        :param password: Contraseña de la red WiFi
        """
        config = {
            'ssid': ssid,
            'password': password
        }
        try:
            with open(self.ssid_file, 'w') as f:
                json.dump(config, f)
            print("Credenciales WiFi guardadas exitosamente")
        except Exception as e:
            print("Error al guardar las credenciales WiFi:", e)
    
    def connect_to_wifi(self, ssid=None, password=None):
        """
        Intenta conectar a la red WiFi con las credenciales proporcionadas o las guardadas
        :param ssid: Nombre de la red WiFi (opcional)
        :param password: Contraseña de la red WiFi (opcional)
        :return: True si la conexión fue exitosa, False si no
        """
        # Usar las credenciales proporcionadas o las guardadas
        if ssid and password:
            self.ssid = ssid
            self.password = password
        elif not self.ssid or not self.password:
            if not self.load_credentials():
                print("No se encontraron credenciales guardadas")
                return False
        
        if not self.ssid or not self.password:
            print("No hay credenciales de WiFi disponibles")
            return False
        
        # Desactivar AP mode si está activo
        if self.ap_if.active():
            self.ap_if.active(False)
        
        # Configurar y activar el modo Station
        self.sta_if.active(True)
        self.sta_if.connect(self.ssid, self.password)
        
        # Indicar estado de conexión con el LED
        self.led.modo_station()
        
        # Esperar a que se conecte
        max_wait = 20
        while max_wait > 0:
            if self.sta_if.isconnected():
                print("Conectado a WiFi:", self.ssid)
                print("IP:", self.sta_if.ifconfig()[0])
                return True
            max_wait -= 1
            print("Esperando conexión... Restan:", max_wait, "segundos")
            time.sleep(1)
        
        print("No se pudo conectar a la red WiFi")
        self.led.error()
        return False
    
    def start_ap_mode(self, ap_ssid="ESP32-CAM-Setup", ap_password="123456789"):
        """
        Inicia el modo AP para configuración de WiFi
        :param ap_ssid: Nombre de la red AP (opcional)
        :param ap_password: Contraseña de la red AP (opcional)
        """
        # Desactivar modo Station si está activo
        if self.sta_if.active():
            self.sta_if.active(False)
        
        # Configurar y activar modo AP
        self.ap_if.active(True)
        self.ap_if.config(essid=ap_ssid, password=ap_password)
        
        print("Modo AP iniciado")
        print("SSID:", ap_ssid)
        print("IP del AP:", self.ap_if.ifconfig()[0])
        
        # Indicar estado AP con el LED
        self.led.modo_ap()
        
        # Iniciar el servidor web para configuración
        self.start_web_server()
    
    def start_web_server(self):
        """
        Inicia un servidor web simple para configuración de WiFi en modo AP
        """
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)
        print('Servidor web escuchando en', addr)
        
        # Página HTML para configuración de WiFi
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Configuración WiFi - ESP32-S3 CAM</title>
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
            max-width: 500px;
            margin: 0 auto;
            background-color: #1e1e1e;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
        h1 {
            color: #bb86fc;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            box-sizing: border-box;
            background-color: #2d2d2d;
            color: #e0e0e0;
            border: 1px solid #444;
            border-radius: 5px;
        }
        button {
            background-color: #bb86fc;
            color: white;
            padding: 14px 20px;
            margin: 10px 0;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
            font-size: 16px;
        }
        button:hover {
            background-color: #9a67ea;
        }
        .status {
            margin-top: 20px;
            padding: 10px;
            background-color: #2d2d2d;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Configuración WiFi - ESP32-S3 CAM</h1>
        <form method="POST" action="/configure">
            <label for="ssid">Nombre de la red (SSID):</label>
            <input type="text" id="ssid" name="ssid" required>
            <label for="password">Contraseña:</label>
            <input type="password" id="password" name="password" required>
            <button type="submit">Conectar</button>
        </form>
        <div class="status">
            <p>Conecta tu dispositivo a esta red WiFi:</p>
            <p><strong>SSID:</strong> ESP32-CAM-Setup</p>
            <p><strong>Contraseña:</strong> 123456789</p>
        </div>
    </div>
</body>
</html>"""

        while True:
            try:
                cl, addr = s.accept()
                print('Cliente conectado desde', addr)
                request = cl.recv(1024)
                request = request.decode('utf-8')
                print('Solicitud recibida:', request)
                
                # Extraer la ruta de la solicitud
                route = ure.search("(?:GET|POST) /(.*?)(?:\\?| HTTP)", request)
                if route:
                    path = route.group(1)
                else:
                    path = ""
                
                # Procesar la solicitud
                if path == "configure" and request.startswith("POST"):
                    # Extraer credenciales de la solicitud POST
                    ssid_match = ure.search("ssid=(.*?)(&|$)", request)
                    password_match = ure.search("password=(.*?)(&|$)", request)
                    
                    if ssid_match and password_match:
                        ssid = ssid_match.group(1).replace("+", " ")
                        password = password_match.group(1).replace("+", " ")
                        
                        # Guardar credenciales y tratar de conectar
                        self.save_credentials(ssid, password)
                        cl.send('HTTP/1.1 200 OK\r\n')
                        cl.send('Content-Type: text/html\r\n')
                        cl.send('Connection: close\r\n\r\n')
                        cl.send('<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Configuración WiFi - ESP32-S3 CAM</title><style>body{font-family:Arial,sans-serif;background-color:#121212;color:#e0e0e0;text-align:center;margin:0;padding:20px;}.container{max-width:500px;margin:0 auto;background-color:#1e1e1e;padding:30px;border-radius:10px;box-shadow:0 0 20px rgba(0,0,0,0.5);}h1{color:#bb86fc;}.status{margin-top:20px;padding:10px;background-color:#2d2d2d;border-radius:5px;}</style></head><body><div class="container"><h1>Configuración WiFi</h1><div class="status"><p>Credenciales guardadas exitosamente</p><p>Conectando a la red: {}</p><p>Reiniciando dispositivo...</p></div></body></html>'.format(ssid))
                        cl.close()
                        
                        # Conectar a la red WiFi configurada
                        if self.connect_to_wifi(ssid, password):
                            print("Conectado exitosamente a la nueva red WiFi")
                            # Reiniciar para aplicar cambios
                            time.sleep(2)
                            reset()
                        else:
                            print("Error al conectar a la nueva red WiFi")
                            time.sleep(2)
                            reset()
                        
                        break
                else:
                    # Enviar página HTML
                    cl.send('HTTP/1.1 200 OK\r\n')
                    cl.send('Content-Type: text/html\r\n')
                    cl.send('Connection: close\r\n\r\n')
                    cl.send(html)
                
                cl.close()
            except Exception as e:
                print('Error en el servidor web:', e)
                cl.close()
    
    def is_connected(self):
        """
        Verifica si el ESP32 está conectado a una red WiFi
        :return: True si está conectado, False si no
        """
        return self.sta_if.isconnected()
    
    def get_ip_address(self):
        """
        Obtiene la dirección IP actual
        :return: Dirección IP como string o None si no está conectado
        """
        if self.is_connected():
            return self.sta_if.ifconfig()[0]
        return None
    
    def setup_wifi(self):
        """
        Configura el WiFi según el estado actual (conectado o desconectado)
        """
        print("Iniciando configuración de WiFi...")
        
        # Primero intentar cargar credenciales guardadas y conectar
        if self.load_credentials():
            print("Credenciales encontradas, intentando conectar...")
            if self.connect_to_wifi():
                print("Conectado a la red guardada")
                return True
            else:
                print("No se pudo conectar con credenciales guardadas")
        
        # Si no se pudo conectar con credenciales guardadas, iniciar modo AP
        print("Iniciando modo AP para configuración WiFi...")
        self.start_ap_mode()
        
        return False