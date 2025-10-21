import ir_tx
import time
import machine
from ir_tx.nec import NEC
from machine import Pin

tx_pin = Pin(17, Pin.OUT, value=0)
device_addr = 0x01
transmitter = NEC(tx_pin)

commands = [0x01, 0x02, 0x03, 0x04]

if __name__ == "__main__":
  while True:
    for command in commands:
      transmitter.transmit(device_addr,command)
      print("COMMANDS" , hex(command) , "TRANSMITTED")
      with open('transmitter_log.txt' , 'a') as log_file:
        log_file.write(f"Command: 0x{command:02x}, Time: {time.time()}\n")
      
      time.sleep(3)
