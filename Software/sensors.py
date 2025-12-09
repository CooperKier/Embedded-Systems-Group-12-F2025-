from machine import ADC, Pin
from time import sleep

sensor = ADC(Pin(28))
threshold = 30000   # Tune depending on your surface

while True:
    value = sensor.read_u16()
    print(value)
    if value > threshold:
        print("Black detected")
    else:
        print("White detected")
    
    sleep(0.05)
