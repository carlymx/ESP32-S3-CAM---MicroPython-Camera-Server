r"""
  ______  _____ _____ ____ ___        _____ ____     _____          __  __ 
 |  ____|/ ____|  __ \___ \__ \      / ____|___ \   / ____|   /\   |  \/  |
 | |__  | (___ | |__) |__) | ) |____| (___   __) | | |       /  \  | \  / |
 |  __|  \___ \|  ___/|__ < / /______\___ \ |__ <  | |      / /\ \ | |\/| |
 | |____ ____) | |    ___) / /_      ____) |___) | | |____ / ____ \| |  | |
 |______|_____/|_|   |____/____|    |_____/|____/   \_____/_/    \_\_|  |_|
                                                                           
                                                                           
    ESP32-S3 CAM - LED CONTROLLER MODULE
    ===================================
    Version: 2.1.0
    Fecha: 2025-12-09
    Descripción: Módulo para controlar el LED RGB en el pin 48 del ESP32-S3 CAM
    Implementa códigos de colores para diferentes estados del sistema
    Cambios:
        - V2.1.0: Actualizado para soportar indicación de reinicio automático durante configuración WiFi
        - V2.0.0: Actualización a nueva API de NeoPixel
        - V1.0.0: Versión inicial del módulo de control LED
"""

from machine import Pin
from neopixel import NeoPixel
import time

class LEDController:
    def __init__(self, pin_number=48):
        """
        Inicializa el controlador del LED RGB
        :param pin_number: Pin al que está conectado el LED RGB (por defecto pin 48)
        """
        self.pin = Pin(pin_number, Pin.OUT)
        self.np = NeoPixel(self.pin, 1)  # 1 LED en la tira
        self.estado = "inicial"
        self.encendido = True
        
    def set_color(self, r, g, b):
        """
        Establece el color del LED RGB
        :param r: Componente roja (0-255)
        :param g: Componente verde (0-255)
        :param b: Componente azul (0-255)
        """
        if self.encendido:
            self.np[0] = (r, g, b)
            self.np.write()
    
    def apagar(self):
        """Apaga el LED RGB"""
        self.np[0] = (0, 0, 0)
        self.np.write()
        self.encendido = False
    
    def encender(self):
        """Enciende el LED con el último color establecido"""
        self.encendido = True
    
    def modo_ap(self):
        """Estado AP (Access Point): Azul"""
        self.estado = "ap"
        self.set_color(0, 0, 255)  # Azul
    
    def modo_station(self):
        """Estado Station (conectado a WiFi): Verde"""
        self.estado = "station"
        self.set_color(0, 255, 0)  # Verde
    
    def transmitiendo(self):
        """Estado Transmitiendo video: Blanco"""
        self.estado = "transmitiendo"
        self.set_color(255, 255, 255)  # Blanco
    
    def error(self):
        """Estado Error: Rojo"""
        self.estado = "error"
        self.set_color(255, 0, 0)  # Rojo
    
    def inicial(self):
        """Estado Inicial: Púrpura"""
        self.estado = "inicial"
        self.set_color(128, 0, 128)  # Púrpura
    
    def parpadeo(self, r, g, b, veces=3, delay=0.2):
        """
        Hace parpadear el LED con un color específico
        :param r: Componente roja (0-255)
        :param g: Componente verde (0-255)
        :param b: Componente azul (0-255)
        :param veces: Número de veces a parpadear
        :param delay: Retraso entre parpadeos en segundos
        """
        for _ in range(veces):
            self.set_color(r, g, b)
            time.sleep(delay)
            self.apagar()
            time.sleep(delay)
        
        # Restaurar el estado anterior después de parpadear
        if self.estado == "ap":
            self.modo_ap()
        elif self.estado == "station":
            self.modo_station()
        elif self.estado == "transmitiendo":
            self.transmitiendo()
        elif self.estado == "error":
            self.error()
        else:
            self.inicial()

    def obtener_estado(self):
        """Devuelve el estado actual del LED"""
        return self.estado
