from machine import I2C, Pin
import seesaw
import time
import ir_tx
from ir_tx.nec import NEC

# Initialize I2C for gamepad
i2c = I2C(0, scl=Pin(17), sda=Pin(16))  # GP17 for SCL, GP16 for SDA
seesaw_device = seesaw.Seesaw(i2c, addr=0x50)

# Define button and joystick pin numbers
BUTTON_A = 5
BUTTON_B = 1
BUTTON_X = 6
BUTTON_Y = 2
BUTTON_START = 16
BUTTON_SELECT = 0
JOYSTICK_X_PIN = 14
JOYSTICK_Y_PIN = 15

# Button mask
BUTTONS_MASK = (1 << BUTTON_X) | (1 << BUTTON_Y) | (1 << BUTTON_A) | (1 << BUTTON_B) | (1 << BUTTON_SELECT) | (1 << BUTTON_START)

# Initialize IR transmitter
tx_pin = Pin(20, Pin.OUT, value=0)  # GP20 for IR transmitter
device_addr = 0x01
transmitter = NEC(tx_pin)

# Initialize LED for transmission indicator
led = Pin(25, Pin.OUT)  # Use onboard LED (GP25) or change to your LED pin

# Define transmitting commands for each direction
commands = {
    'UP': 0x01,
    'DOWN': 0x02,
    'LEFT': 0x03,
    'RIGHT': 0x04,
    'CENTER': 0x05,
    'BUTTONA': 0x06,
    'BUTTONB': 0x07,
    'BUTTONX': 0x08,
    'BUTTONY': 0x09
}

def setup_buttons():
    """Configure the pin modes for buttons."""
    seesaw_device.pin_mode_bulk(BUTTONS_MASK, seesaw_device.INPUT_PULLUP)

def read_buttons():
    """Read and return the state of each button."""
    return seesaw_device.digital_read_bulk(BUTTONS_MASK)

def read_joystick():
    """Read and return the joystick's X and Y positions."""
    x_value = seesaw_device.analog_read(JOYSTICK_X_PIN)
    y_value = seesaw_device.analog_read(JOYSTICK_Y_PIN)
    return x_value, y_value

def get_joystick_direction(x, y):
    """Determine joystick direction based on X and Y values.
    Returns direction string or None if centered."""
    # Joystick center is typically around 512 (for 10-bit ADC, range 0-1023)
    center = 512
    threshold = 300  # Minimum deflection to register as directional input
    
    x_offset = x - center
    y_offset = y - center
    
    # Check if joystick is significantly moved
    if abs(x_offset) > threshold or abs(y_offset) > threshold:
        # Determine primary direction (larger offset)
        # Flipped X-axis: lower values = RIGHT, higher values = LEFT
        if abs(x_offset) > abs(y_offset):
            return 'LEFT' if x_offset > 0 else 'RIGHT'
        else:
            return 'DOWN' if y_offset > 0 else 'UP'
    
    return None

def main():
    """Main program loop."""
    setup_buttons()
    last_buttons = 0
    last_direction = None
    
    print("=" * 50)
    print("Gamepad IR Controller Ready")
    print("=" * 50)
    print("Joystick Directions:")
    print("  UP     -> Command 0x01")
    print("  DOWN   -> Command 0x02")
    print("  LEFT   -> Command 0x03")
    print("  RIGHT  -> Command 0x04")
    print("  CENTER -> Command 0x05")
    print("=" * 50)
    
    while True:
        # Read current button states
        current_buttons = read_buttons()
        
        # Check for button presses
        if current_buttons != last_buttons:
            if current_buttons & (1 << BUTTON_A) and not last_buttons & (1 << BUTTON_A):
                command = commands['BUTTONA']
                led.on()  # Turn on LED when transmitting
                transmitter.transmit(device_addr,command)
                print(f" -> BUTTON A DETECTED! Command {hex(command)} TRANSMITTED")
                time.sleep(0.1)  # Keep LED on briefly
                led.off()  # Turn off LED
            if current_buttons & (1 << BUTTON_B) and not last_buttons & (1 << BUTTON_B):
                command = commands['BUTTONB']
                led.on()  # Turn on LED when transmitting
                transmitter.transmit(device_addr,command)
                print(f" -> BUTTON B DETECTED! Command {hex(command)} TRANSMITTED")
                time.sleep(0.1)  # Keep LED on briefly
                led.off()  # Turn off LED
            if current_buttons & (1 << BUTTON_X) and not last_buttons & (1 << BUTTON_X):
                command = commands['BUTTONX']
                led.on()  # Turn on LED when transmitting
                transmitter.transmit(device_addr,command)
                print(f" -> BUTTON X DETECTED! Command {hex(command)} TRANSMITTED")
                time.sleep(0.1)  # Keep LED on briefly
                led.off()  # Turn off LED
            if current_buttons & (1 << BUTTON_Y) and not last_buttons & (1 << BUTTON_Y):
                command = commands['BUTTONY']
                led.on()  # Turn on LED when transmitting
                transmitter.transmit(device_addr,command)
                print(f" -> BUTTON Y DETECTED! Command {hex(command)} TRANSMITTED")
                time.sleep(0.1)  # Keep LED on briefly
                led.off()  # Turn off LED
            if current_buttons & (1 << BUTTON_START) and not last_buttons & (1 << BUTTON_START):
                print(">>> Start button pressed")
            if current_buttons & (1 << BUTTON_SELECT) and not last_buttons & (1 << BUTTON_SELECT):
                print(">>> Select button pressed")
            last_buttons = current_buttons
        
        # Read joystick position
        current_x, current_y = read_joystick()
        current_direction = get_joystick_direction(current_x, current_y)
        
        # Print joystick position frequently
        print(f"Joystick: X={current_x}, Y={current_y}", end="")
        
        # Transmit IR signal based on joystick direction
        if current_direction:
            if current_direction != last_direction:
                command = commands[current_direction]
                led.on()  # Turn on LED when transmitting
                transmitter.transmit(device_addr,command)
                print(f" -> {current_direction} DETECTED! Command {hex(command)} TRANSMITTED")
                time.sleep(0.1)  # Keep LED on briefly
                led.off()  # Turn off LED
                last_direction = current_direction
            else:
                print(f" -> {current_direction}")
        else:
            # Joystick is centered
            if last_direction != 'CENTER':
                command = commands['CENTER']
                led.on()  # Turn on LED when transmitting
                transmitter.transmit(device_addr,command)
                print(f" -> CENTER DETECTED! Command {hex(command)} TRANSMITTED")
                time.sleep(0.1)  # Keep LED on briefly
                led.off()  # Turn off LED
                last_direction = 'CENTER'
            else:
                print(" -> CENTER")
        
        time.sleep(0.2)  # Print every 0.2 seconds (5 times per second)

if __name__ == "__main__":
    main()
