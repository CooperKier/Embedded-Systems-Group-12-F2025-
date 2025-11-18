import machine
import time
from machine import Pin
from machine import PWM


pwm_freq = 2000
pwm_duty = 32500

# Define input pins individually
# input19 = Pin(19, Pin.IN, Pin.PULL_DOWN) # Right, D3
# input18 = Pin(18, Pin.IN, Pin.PULL_DOWN) # Left, D2
# input17 = Pin(17, Pin.IN, Pin.PULL_DOWN) # Backwards, D1
# input16 = Pin(16, Pin.IN, Pin.PULL_DOWN) # Forwards, D0

input4 = Pin(4, Pin.IN, Pin.PULL_DOWN) # Right, D3
input5 = Pin(5, Pin.IN, Pin.PULL_DOWN) # Left, D2
input6 = Pin(6, Pin.IN, Pin.PULL_DOWN) # Backwards, D1
input7 = Pin(7, Pin.IN, Pin.PULL_DOWN) # Forwards, D0

# Define output pins individually
output12 = Pin(12, Pin.OUT) # A Phase
output13 = PWM(13, freq = pwm_freq, duty_u16 = 0) # A Enable
output14 = Pin(14, Pin.OUT) # B Phase
output15 = PWM(15, freq = pwm_freq, duty_u16 = 0) # B Enable

# Make sure all outputs start LOW
output12.low()
output13.duty_u16(0)
output14.low()
output15.duty_u16(0)

pwm = pwm_duty

while True:
    # ---input pin 16 FOWARDS---
    while input7.value() == 1:
        print("FOWARDS")
        #A
        output13.duty_u16(pwm)
        output12.high()
        #B
        output15.duty_u16(pwm)
        output14.high()
        time.sleep(0.7)

    # ---input pin 17 BACKWARDS---
    while (input6.value() == 1):
        print("Backwards")
        #A
        output13.duty_u16(pwm)
        output12.low()
        #B
        output15.duty_u16(pwm)
        output14.low()
        time.sleep(0.7)

    # ---input pin 18 LEFT---
    while input5.value() == 1:
        print("Left")
        #A Right Wheel
        output13.duty_u16(pwm)
        output12.high()
        #B Left Wheel
        output15.duty_u16(pwm)
        output14.low()
        time.sleep(0.7)

    # ---input pin 19 RIGHT---
    while input4.value() == 1:
        print("right")
        #A Right Wheel
        output13.duty_u16(pwm)
        output12.low()
        #B Left Wheel
        output15.duty_u16(pwm)
        output14.high()
        time.sleep(0.7)
    
    output13.duty_u16(0)
    output15.duty_u16(0)