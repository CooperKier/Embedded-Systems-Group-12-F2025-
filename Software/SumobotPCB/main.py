import time
from machine import Pin, PWM, ADC, Timer
import ir_rx
from ir_rx.nec import NEC_8       # NEC 8-bit IR decoder
from ir_rx.print_error import print_error

# ================================
# Motor setup (shared by IR & RF)
# ================================
pwm_rate = 2000
pwm = 20000  # Full speed (adjust to taste)

# Motor A control (same pins as your IR code)
ain1_ph = Pin(14, Pin.OUT)                     # Motor A direction
ain2_en = PWM(15, freq=pwm_rate, duty_u16=0)   # Motor A speed (PWM)

# Motor B control
bin1_ph = Pin(12, Pin.OUT)                     # Motor B direction
bin2_en = PWM(13, freq=pwm_rate, duty_u16=0)   # Motor B speed (PWM)

music = Pin(17, Pin.OUT)
music.high()

# LED for feedback
led = Pin(25, Pin.OUT)

# ================================
# Black line detection sensor
# ================================
sensor = ADC(Pin(28))
threshold = 50000   # Tune depending on your surface
black_detected = False  # Global flag for black detection

# ================================
# RF receiver input pins
# ================================
input4 = Pin(4, Pin.IN, Pin.PULL_DOWN)  # Right, D3
input5 = Pin(5, Pin.IN, Pin.PULL_DOWN)  # Left, D2
input6 = Pin(6, Pin.IN, Pin.PULL_DOWN)  # Backwards, D1
input7 = Pin(7, Pin.IN, Pin.PULL_DOWN)  # Forwards, D0

# ================================
# Mode lock state
# ================================
MODE_NONE = 0
MODE_IR   = 1
MODE_RF   = 2

current_mode = MODE_NONE  # Start unlocked (listening for first source)

# ================================
# Motor helper functions
# ================================
def motor_forward():
    # Use same behavior as your IR code
    print("Motor FORWARD")
    ain1_ph.high()
    ain2_en.duty_u16(pwm)
    bin1_ph.low()
    bin2_en.duty_u16(pwm)

def motor_backward():
    print("Motor BACKWARD")
    ain1_ph.low()
    ain2_en.duty_u16(pwm)
    bin1_ph.high()
    bin2_en.duty_u16(pwm)

def motor_left():
    print("Motor TURN LEFT")
    # Motor A backward, Motor B forward
    ain1_ph.low()
    ain2_en.duty_u16(pwm)
    bin1_ph.low()
    bin2_en.duty_u16(pwm)

def motor_right():
    print("Motor TURN RIGHT")
    # Motor A forward, Motor B backward
    ain1_ph.high()
    ain2_en.duty_u16(pwm)
    bin1_ph.high()
    bin2_en.duty_u16(pwm)

def motor_stop():
    print("Motor STOP")
    ain2_en.duty_u16(0)
    bin2_en.duty_u16(0)

# ================================
# Black line detection (Timer-based polling)
# ================================
def check_black_line(timer):
    global black_detected
    
    value = sensor.read_u16()
    print(value)
    
    if value > threshold:
        if not black_detected:
            print("\n!!! BLACK LINE DETECTED - FORCING FORWARD !!!")
            led.high()  # Turn on LED as indicator
        black_detected = True
        motor_forward()  # Override all controls - go forward
    else:
        if black_detected:
            print("Black line cleared - resuming normal control")
            led.low()
        black_detected = False

# Initialize timer for sensor checking (checks every 50ms)
sensor_timer = Timer()
sensor_timer.init(period=50, mode=Timer.PERIODIC, callback=check_black_line)

# ================================
# IR callback
# ================================
def ir_callback(data, addr, _):
    global current_mode

    # BLACK LINE OVERRIDE: Ignore IR if black is detected
    if black_detected:
        return

    # If we already locked to RF, ignore IR completely
    if current_mode not in (MODE_NONE, MODE_IR):
        # Already locked to RF
        return

    # Lock into IR mode on first valid IR command
    if current_mode == MODE_NONE:
        current_mode = MODE_IR
        print("\n=== LOCKED TO IR MODE ===")

    # ----- interpret IR commands -----
    if data == 0x01:        # UP
        motor_forward()

    elif data == 0x02:      # DOWN
        motor_backward()

    elif data == 0x03:      # LEFT
        motor_left()

    elif data == 0x04:      # RIGHT
        motor_right()

    elif data == 0x05:      # CENTER (Stop)
        motor_stop()
    
    elif data == 0x06:
        music.toggle()

    else:
        print("Unknown IR command:", data)
        # Simple feedback & a default movement if you want
        led.toggle()

# ================================
# IR receiver setup
# ================================
ir_pin = Pin(18, Pin.IN, Pin.PULL_UP)
ir_receiver = NEC_8(ir_pin, callback=ir_callback)
ir_receiver.error_function(print_error)

# ================================
# Info printout
# ================================
print("=" * 50)
print("IR + RF Motor Control with Black Line Detection")
print("=" * 50)
print("IR commands:")
print("  0x01 (UP)    -> Forward")
print("  0x02 (DOWN)  -> Backward")
print("  0x03 (LEFT)  -> Turn Left")
print("  0x04 (RIGHT) -> Turn Right")
print("  0x05 (CENTER)-> Stop")
print("-" * 50)
print("RF buttons:")
print("  D0 (GP7)  -> Forward")
print("  D1 (GP6)  -> Backward")
print("  D2 (GP5)  -> Left")
print("  D3 (GP4)  -> Right")
print("-" * 50)
print("BLACK LINE SENSOR:")
print("  Pin: GP28 (ADC2)")
print("  Threshold:", threshold)
print("  OVERRIDES ALL CONTROLS - Forces forward motion")
print("-" * 50)
print("First input wins: once IR or RF is used,")
print("it locks into that mode until reset.")
print("=" * 50)

# ================================
# Main loop (RF handling + idle)
# ================================
if __name__ == "__main__":
    while True:
        # BLACK LINE OVERRIDE: Skip normal control if black detected
        if black_detected:
            time.sleep(0.2)
            continue
        
        # If not locked to IR, we are allowed to look at RF
        if current_mode in (MODE_NONE, MODE_RF):

            # Check RF inputs
            if input7.value() == 1:      # Forward
                if current_mode == MODE_NONE:
                    current_mode = MODE_RF
                    print("\n=== LOCKED TO RF MODE (FORWARD pressed) ===")
                motor_forward()
                time.sleep(0.7)

            elif input6.value() == 1:    # Backward
                if current_mode == MODE_NONE:
                    current_mode = MODE_RF
                    print("\n=== LOCKED TO RF MODE (BACKWARD pressed) ===")
                motor_backward()
                time.sleep(0.7)

            elif input5.value() == 1:    # Left
                if current_mode == MODE_NONE:
                    current_mode = MODE_RF
                    print("\n=== LOCKED TO RF MODE (LEFT pressed) ===")
                motor_left()
                time.sleep(0.7)

            elif input4.value() == 1:    # Right
                if current_mode == MODE_NONE:
                    current_mode = MODE_RF
                    print("\n=== LOCKED TO RF MODE (RIGHT pressed) ===")
                motor_right()
                time.sleep(0.7)
            else:
                # No RF input: if we're in RF mode (or still NONE),
                # keep motors stopped.
                if current_mode in (MODE_NONE, MODE_RF):
                    motor_stop()

        time.sleep(0.02)  # Main loop delay (adjust as needed)
