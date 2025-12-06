from machine import Pin
from neopixel import NeoPixel
import time

# Definimos el pin GPIO 48 para el LED RGB NeoPixel
PIN_NUM = 48
NUM_PIXELS = 1
# Inicializamos el objeto NeoPixel
np_pin = Pin(PIN_NUM, Pin.OUT)
np = NeoPixel(np_pin, NUM_PIXELS)

# Función auxiliar para establecer el color usando formato hexadecimal (0xRRGGBB)
def set_rgb_hex(hex_color):
    # Extraemos los componentes R, G, B del valor hexadecimal
    r = (hex_color >> 16) & 0xFF
    g = (hex_color >> 8) & 0xFF
    b = hex_color & 0xFF
    
    # Asignamos el color al primer (y único) pixel [0]
    np[0] = (r, g, b)
    # Escribimos el color en el hardware del LED
    np.write()

# El equivalente a pycom.heartbeat(False) para evitar comportamientos por defecto
# No es estrictamente necesario en MicroPython genérico, pero lo mantenemos conceptualmente.

print("Cambiando colores del LED RGB en Pin 48...")

while True:
    set_rgb_hex(0xFF0000)  # Rojo
    time.sleep(1)
    set_rgb_hex(0x00FF00)  # Verde
    time.sleep(1)
    set_rgb_hex(0x0000FF)  # Azul
    time.sleep(1)
