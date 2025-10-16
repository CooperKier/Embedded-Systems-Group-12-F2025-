import ir_rx
import machine
from machine import Pin
from ir_rx.nec import NEC_8
from ir_rx.print_error import print_error

def ir_callback(data, addr, _):
  print(f"Received NEC Command! Data: 0x{data:02x} , Addr: 0x{addr:02x}" }

ir_pin = Pin(17, Pin.IN, Pin.PULL_UP)
ir_receiver = NEC_8(ir_pin, callback=ir_callback)
ir_receiver.error_function(print_error)

while (1):
  pass
