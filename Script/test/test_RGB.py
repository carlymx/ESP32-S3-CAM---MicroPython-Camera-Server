from led_controller import LEDController
import time

print("Iniciando test del LED RGB usando LEDController...")

# Inicializamos el objeto LEDController
led = LEDController()

try:
    print("Probando color Rojo...")
    led.error()  # Rojo
    time.sleep(1)

    print("Probando color Verde (Éxito)...")
    led.success()  # Verde
    time.sleep(1)

    print("Probando color Azul (Inicial)...")
    led.inicial()  # Azul
    time.sleep(1)

    print("Probando color Amarillo (Advertencia)...")
    led.warning() # Amarillo
    time.sleep(1)

    print("Probando color Blanco (Conectado a AP)...")
    led.modo_ap() # Blanco
    time.sleep(1)

    print("Probando color Cian (Transmitiendo)...")
    led.transmitiendo() # Cian
    time.sleep(1)

    print("Apagando LED...")
    led.off()
    time.sleep(0.5)

    print("Test del LED RGB finalizado exitosamente.")

except Exception as e:
    print(f"Error durante el test del LED RGB: {e}")
    led.error() # Indicar error con rojo
    time.sleep(2)
finally:
    led.off() # Asegurarse de apagar el LED al finalizar

