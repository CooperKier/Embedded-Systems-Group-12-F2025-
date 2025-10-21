import machine
import time
from machine import Pin
from machine import PWM



pwm_rate = 200000

# Define input pins individually
input16 = Pin(16, Pin.IN, Pin.PULL_DOWN) # Fowards, D0
input17 = Pin(17, Pin.IN, Pin.PULL_DOWN) # Bakwards, D1
input18 = Pin(18, Pin.IN, Pin.PULL_DOWN) # Left, D2
input19 = Pin(19, Pin.IN, Pin.PULL_DOWN) # Right, D3

# Define output pins individually
output12 = Pin(12, Pin.OUT) # A Phase
output13 = PWM(15, freq = pwm_rate, duty_u16 = 0) # A Enable
output14 = Pin(14, Pin.OUT) # B Phase
output15 = PWM(13, freq = pwm_rate, duty_u16 = 0) # B Enable

# Make sure all outputs start LOW
output12.low()
output13.duty_u16(0)
output14.low()
output15.duty_u16(0)

pwm = pwm_rate

while True:
    # ---input pin 16 FOWARDS---
    if input16.value() == 1:
        print("FOWARDS")
        #A
        output13.duty_u16(pwm)
        output12.high()
        #B
        output15.duty_u16(pwm)
        output14.low()
    # else:
    #     output13.duty_u16(0)
    #     output15.duty_u16(0)

    # ---input pin 17 BACKWARDS---
    if input17.value() == 1:
        print("Backwards")
        #A
        output13.duty_u16(pwm)
        output12.low()
        #B
        output15.duty_u16(pwm)
        output14.high()
    # else:
    #     output13.duty_u16(0)
    #     output15.duty_u16(0)

    # ---input pin 18 LEFT---
    if input18.value() == 1:
        print("Left")
        #A Right Wheel
        output13.duty_u16(pwm)
        output12.low()
        #B Left Wheel
        output15.duty_u16(pwm)
        output14.high()
    # else:
    #     output13.duty_u16(0)
    #     output15.duty_u16(0)

    # ---input pin 19 RIGHT---
    if input19.value() == 1:
        print("right")
        #A Right Wheel
        output13.duty_u16(pwm)
        output12.high()
        #B Left Wheel
        output15.duty_u16(pwm)
        output14.low()
    # else:
    #     output13.duty_u16(0)
    #     output15.duty_u16(0)

    # Small delay to prevent unnecessary CPU load
    time.sleep(0.05)