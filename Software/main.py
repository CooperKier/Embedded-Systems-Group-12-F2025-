import ir_tx
import ir_rx
import time
import machine
from machine import Pin
from ir_tx.nec import NEC
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging
from machine import PWM

#Define motor speed through PWM frequency
pwm_rate = 2000

#Define motor A control signals
ain1_ph = Pin(14, Pin.OUT) # Initialize GP14 as an OUTPUT
ain2_en = PWM(15, freq = pwm_rate, duty_u16 = 0)

#Define motor B control signals
bin1_ph = Pin(12, Pin.OUT)
bin2_en = PWM(13, freq = pwm_rate, duty_u16 = 0)

#Define transmitter pins and commands
tx_pin = Pin(17,Pin.OUT,value=0)
device_addr = 0x01
transmitter = NEC(tx_pin)
commands = [0x01,0x02,0x03,0x04]

#Function called when ever signal is recived 
def ir_callback(data, addr, _):
    print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")

    #Check fro value of data recieved
    if data == 0x01:
        print("Motor Forward") # Print to REPL
        #Set polarity and speed of motor A
        ain1_ph.high()
        ain2_en.duty_u16(pwm)

        #Set polarity and speed of motor B
        bin1_ph.low()
        bin2_en.duty_u16(pwm)

    if data == 0x04:
        print("Motor Backward") # Print to REPL
        #Invert polarity of motor A and B
        ain1_ph.low()
        bin1_ph.high()

    if data == 0x03:
        print("Motor OFF") # Print to REPL
        #Turn both motors off
        ain2_en.duty_u16(0)
        bin2_en.duty_u16(0)

#Define IR reciever pins and function call
ir_pin = Pin(20, Pin.IN, Pin.PULL_UP)
ir_receiver = NEC_8(ir_pin, callback=ir_callback)
ir_receiver.error_function(print_error)
pwm = min(max(int(2**16 * abs(1)), 0), 65535)

#Keep curcuit running
if __name__ == "__main__":
    while True:
        #Send transmitter signals
        for command in commands:
            transmitter.transmit(device_addr,command)
            print("COMMANDS",hex(command),"TRANSMITTED.")
            time.sleep(3)