r"""
  ______  _____ _____ ____ ___        _____ ____     _____          __  __ 
 |  ____|/ ____|  __ \___ \__ \      / ____|___ \   / ____|   /\   |  \/  |
 | |__  | (___ | |__) |__) | ) |____| (___   __) | | |       /  \  | \  / |
 |  __|  \___ \|  ___/|__ < / /______\___ \ |__ <  | |      / /\ \ | |\/| |
 | |____ ____) | |    ___) / /_      ____) |___) | | |____ / ____ \| |  | |
 |______|_____/|_|   |____/____|    |_____/|____/   \_____/_/    \_\_|  |_|
                                                                           
                                                                           
    ESP32-S3 CAM - WIFI MANAGER MODULE
    =================================
    Version: 2.1.0
    Fecha: 2025-12-09
    Descripción: Módulo para gestionar la conexión WiFi del ESP32-S3 CAM
    Implementa modo AP para configuración inicial y modo Station para conexión normal
    Cambios:
        - V2.1.2: Mejora en el manejo del WDT durante la conexión WiFi
        - V2.1.1: Implementación de alimentación regular al watchdog timer para evitar reinicios
        - V2.1.0: Implementación de reinicio automático tras guardar credenciales,
                   mejora en el manejo de caracteres especiales en SSID,
                   aumento del tiempo de espera a 15 segundos con cuenta regresiva
        - V2.0.0: Actualización de funcionalidades de red
        - V1.0.0: Versión inicial del módulo de gestión WiFi
"""

import network
import socket
import ure
import time
import json
from machine import reset, idle
from led_controller import LEDController


def url_decode(s):
    """
    Decodifica una cadena con codificación URL (por ejemplo, %40 para @)
    :param s: Cadena codificada
    :return: Cadena decodificada
    """
    # Reemplazar los códigos URL comunes
    s = s.replace('%20', ' ')  # espacio
    s = s.replace('%40', '@')  # @
    s = s.replace('%23', '#')  # #
    s = s.replace('%24', '$')  # $
    s = s.replace('%25', '%')  # %
    s = s.replace('%5E', '^')  # ^
    s = s.replace('%26', '&')  # &
    s = s.replace('%2A', '*')  # *
    s = s.replace('%28', '(')  # (
    s = s.replace('%29', ')')  # )
    s = s.replace('%2B', '+')  # +
    s = s.replace('%3D', '=')  # =
    s = s.replace('%2F', '/')  # /
    s = s.replace('%3F', '?')  # ?
    s = s.replace('%3C', '<')  # <
    s = s.replace('%3E', '>')  # >
    s = s.replace('%7B', '{')  # {
    s = s.replace('%7D', '}')  # }
    s = s.replace('%5B', '[')  # [
    s = s.replace('%5D', ']')  # ]
    s = s.replace('%7C', '|')  # |
    s = s.replace('%5C', '\\')  # \
    s = s.replace('%60', '`')  # `
    s = s.replace('%7E', '~')  # ~
    s = s.replace('%22', '"')  # "
    s = s.replace('%27', "'")  # '
    s = s.replace('%3B', ';')  # ;
    s = s.replace('%3A', ':')  # :
    s = s.replace('%21', '!')  # !
    s = s.replace('%2C', ',')  # ,

    return s

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
                # Obtener el estado de configuración, por defecto False si no existe
                configured = config.get('configured', False)
                return configured  # Retornar el estado para saber si hay credenciales válidas
        except (OSError, ValueError) as e:
            print("No se pudieron cargar las credenciales WiFi (archivo no encontrado o corrupto):", e)
            return False
    
    def save_credentials(self, ssid, password):
        """
        Guarda las credenciales de WiFi en el archivo
        :param ssid: Nombre de la red WiFi
        :param password: Contraseña de la red WiFi
        """
        config = {
            'ssid': ssid,
            'password': password,
            'configured': True  # Marcar que las credenciales han sido configuradas
        }
        try:
            with open(self.ssid_file, 'w') as f:
                json.dump(config, f)
            print("Credenciales WiFi guardadas exitosamente")
        except OSError as e:
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
            # Alimentar al WDT durante la espera
            idle()

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
    
    def scan_wifi_networks(self):
        """
        Escanea y devuelve las redes WiFi disponibles
        :return: Lista de redes WiFi disponibles
        """
        # Asegurarse de que el modo Station esté activo para escanear
        was_active = self.sta_if.active()
        if not was_active:
            self.sta_if.active(True)

        try:
            # Escanear redes disponibles
            networks = self.sta_if.scan()
            wifi_list = []
            for net in networks:
                ssid = net[0].decode('utf-8')  # SSID
                signal_strength = net[3]  # RSSI
                security = net[4]  # 0: open, 1: WEP, 2: WPA, 3: WPA2, 4: WPA/WPA2
                wifi_list.append({
                    'ssid': ssid,
                    'rssi': signal_strength,
                    'security': security
                })
            return wifi_list
        except OSError as e:
            print("Error al escanear redes WiFi:", e)
            return []
        finally:
            # Restaurar el estado original si era inactivo
            if not was_active:
                self.sta_if.active(False)

    def start_web_server(self):
        """
        Inicia un servidor web simple para configuración de WiFi en modo AP
        """
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)
        ap_ip = self.ap_if.ifconfig()[0]  # Obtener IP real del AP
        print('Servidor web escuchando en', (ap_ip, 80))

        # Escanear redes WiFi disponibles
        available_networks = self.scan_wifi_networks()

        # Generar opciones para el desplegable de redes WiFi
        wifi_options = ""
        for net in available_networks:
            ssid = net['ssid']
            rssi = net['rssi']
            security_icon = "🔒" if net['security'] > 0 else "🔓"
            wifi_options += f'<option value="{ssid}">{security_icon} {ssid} (Señal: {rssi} dBm)</option>'

        # Cargar plantilla HTML para el formulario de configuración
        html = ""
        try:
            with open('html/wifi_form.html', 'r') as f:
                html_template = f.read()
            html = html_template.replace('{{wifi_options}}', wifi_options)
        except Exception as e:
            print("Error: No se pudo cargar la plantilla HTML (html/wifi_form.html).", e)
            html = "<html><head><title>Error</title></head><body><h1>Error 500</h1><p>No se pudo cargar la interfaz de usuario. Verifique que el archivo 'html/wifi_form.html' exista.</p></body></html>"

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
                    # Primero intentar obtener SSID del menú desplegable
                    ssid_match = ure.search("ssid=([^&]*)(?:&|$)", request)
                    # También intentar obtener SSID manual
                    ssid_manual_match = ure.search("ssid_manual=([^&]*)(?:&|$)", request)
                    password_match = ure.search("password=([^&]*)(?:&|$)", request)

                    if password_match:
                        # Priorizar SSID seleccionado del desplegable, sino usar manual
                        ssid = ""
                        if ssid_match:
                            ssid = url_decode(ssid_match.group(1).replace("+", " "))

                        # Si no se seleccionó SSID del desplegable o está vacío, usar el ingresado manualmente
                        if not ssid or ssid == "" or ssid == "Selecciona+una+red...":
                            if ssid_manual_match:
                                ssid = url_decode(ssid_manual_match.group(1).replace("+", " "))

                        password = url_decode(password_match.group(1).replace("+", " "))

                        if ssid and password:  # Asegurarse de que tengamos ambos
                            # Guardar credenciales y tratar de conectar
                            self.save_credentials(ssid, password)
                            # Escapar caracteres especiales en el SSID para evitar problemas en HTML
                            escaped_ssid = ssid.replace('"', '&quot;').replace("'", "&#39;").replace('<', '&lt;').replace('>', '&gt;')

                            html_response = ""
                            try:
                                with open('html/wifi_success.html', 'r') as f:
                                    html_template = f.read()
                                html_response = html_template.replace('{{ssid}}', escaped_ssid)
                            except Exception as e:
                                print("Error: No se pudo cargar la plantilla HTML (html/wifi_success.html).", e)
                                html_response = "<html><body><h1>Credenciales guardadas</h1><p>Conectando a " + escaped_ssid + ". El dispositivo se reiniciará.</p></body></html>"


                            cl.send('HTTP/1.1 200 OK\r\n')
                            cl.send('Content-Type: text/html\r\n')
                            cl.send('Connection: close\r\n\r\n')
                            cl.send(html_response)
                            cl.close()

                            # Reiniciar el dispositivo después de enviar la respuesta
                            time.sleep(15)
                            reset()
                        else:
                            html_error = ""
                            try:
                                with open('html/wifi_error.html', 'r') as f:
                                    html_error = f.read()
                            except Exception as e:
                                print("Error: No se pudo cargar la plantilla HTML (html/wifi_error.html).", e)
                                html_error = "<html><body><h1>Error 400</h1><p>Faltan credenciales. Por favor, vuelva e inténtelo de nuevo.</p></body></html>"
                            
                            cl.send('HTTP/1.1 400 BAD REQUEST\r\n')
                            cl.send('Content-Type: text/html\r\n')
                            cl.send('Connection: close\r\n\r\n')
                            cl.send(html_error)
                            cl.close()
                elif path == "configure" and request.startswith("GET"):
                    # Si se accede a /configure vía GET después de haber guardado las credenciales,
                    # redirigir de vuelta a la página principal
                    cl.send('HTTP/1.1 302 Found\r\n')
                    cl.send('Location: /\r\n')
                    cl.send('Connection: close\r\n\r\n')
                    cl.close()
                elif path == "restart":
                    html_restarting = ""
                    try:
                        with open('html/restarting.html', 'r') as f:
                            html_restarting = f.read()
                    except Exception as e:
                        print("Error: No se pudo cargar la plantilla HTML (html/restarting.html).", e)
                        html_restarting = "<html><body><h1>Reiniciando...</h1></body></html>"
                    
                    cl.send('HTTP/1.1 200 OK\r\n')
                    cl.send('Content-Type: text/html\r\n')
                    cl.send('Connection: close\r\n\r\n')
                    cl.send(html_restarting)
                    cl.close()

                    # Reiniciar el dispositivo después de enviar la respuesta
                    time.sleep(2)
                    reset()
                else:
                    # Enviar página HTML
                    cl.send('HTTP/1.1 200 OK\r\n')
                    cl.send('Content-Type: text/html\r\n')
                    cl.send('Connection: close\r\n\r\n')
                    cl.send(html)

                cl.close()

                # Alimentar al WDT para evitar reinicios
                idle()
            except (OSError, ValueError) as e: # OSError para errores de red, ValueError para parsing
                print('Error de red o procesamiento en el servidor web:', e)
                try:
                    cl.close()
                except:
                    pass

                # Alimentar al WDT para evitar reinicios incluso en caso de error
                idle()
            except Exception as e:
                print('Error inesperado en el servidor web:', e)
                try:
                    cl.close()
                except:
                    pass

                # Alimentar al WDT para evitar reinicios incluso en caso de error
                idle()
    
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
        # load_credentials ahora retorna True si las credenciales están marcadas como configuradas
        if self.load_credentials():
            print("Credenciales configuradas encontradas, intentando conectar...")
            if self.connect_to_wifi():
                print("Conectado a la red guardada")
                return True
            else:
                print("No se pudo conectar con credenciales guardadas")
                # Limpiar el estado de configuración si las credenciales no funcionan
                self.clear_configured_status()
        else:
            print("No hay credenciales configuradas guardadas")

        # Si no se pudo conectar con credenciales guardadas, iniciar modo AP
        print("Iniciando modo AP para configuración WiFi...")
        self.start_ap_mode()

        return False

    def clear_configured_status(self):
        """
        Limpia el estado de configuración en ssid_config.json
        """
        try:
            # Cargar configuración existente
            with open(self.ssid_file, 'r') as f:
                config = json.load(f)

            # Marcar como no configurado
            config['configured'] = False

            # Guardar cambios
            with open(self.ssid_file, 'w') as f:
                json.dump(config, f)

            print("Estado de configuración limpiado")
        except OSError as e:
            print("Error al limpiar el estado de configuración:", e)
