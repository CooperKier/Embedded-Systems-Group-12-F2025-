from machine import Pin
import time

# GPIO pins to LEDs
led_pins = [13, 14, 15]
leds = [Pin(pin, Pin.OUT) 
        for pin in led_pins]

while True:
    for led in leds:
        led.value(1)
        time.sleep(0.25)
        led.value(0)
