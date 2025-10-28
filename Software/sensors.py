from machine import Pin
import time

# Interupts
def sensor_N_irq(pin):
    print(">>> Move motors in direction N")

def sensor_W_irq(pin):
    print(">>> Move motors in direction W")

def sensor_S_irq(pin):
    print(">>> Move motors in direction S")

def sensor_E_irq(pin):
    print(">>> Move motors in direction E")

sensor_N = Pin(16, Pin.IN, Pin.PULL_DOWN)
sensor_W = Pin(17, Pin.IN, Pin.PULL_DOWN)
sensor_S = Pin(18, Pin.IN, Pin.PULL_DOWN)
sensor_E = Pin(19, Pin.IN, Pin.PULL_DOWN)

sensor_N.irq(trigger=Pin.IRQ_RISING, handler=sensor_N_irq)
sensor_W.irq(trigger=Pin.IRQ_RISING, handler=sensor_W_irq)
sensor_S.irq(trigger=Pin.IRQ_RISING, handler=sensor_S_irq)
sensor_E.irq(trigger=Pin.IRQ_RISING, handler=sensor_E_irq)

while True:
    print("Main going ...")
    time.sleep(1)

