import ir_tx
import ir_rx
import time
import machine
from machine import Pin 
from ir_tx.nec import NEC
from ir_tx.nec import NEC_8
from ir_rx.print_error import print_error
from machine import PWM

''' Uncomment to run in same circuit.
tx_pin = Pin(17, Pin.OUT, value=0)
device_addr = 0x01
commands = [0x01, 0x02, 0x03, 0x04]

ir_pin = Pin(20, Pin.IN, Pin.PULL_UP)
ir_receiver = NEC_8(ir_pin, callback=ir_callback)
ir_receiver.error_function(print_error)
'''

pwm_rate = 2000
ain1_ph = Pin(14, Pin.OUT)
ain1_en = PWM(Pin(15))
ain1_en.freq(pwm_rate)
ain1_en.duty_u16(0)

def ir_callback(data, addr, _):
  print(f"Received NEC Command! Data: 0x{data:02x} , Addr: 0x{addr:02x}")
  if data = 0x01:
    print("MOTOR ON")
    ain1_ph.low()
    ain1_en.duty_u16(0)
  if data = 0x04:
    print("MOTOR OFF")
    ain1_ph.low()
    ain1_en.duty_u16(0)

if __name__ = "__main__":
  while True:
    pass
