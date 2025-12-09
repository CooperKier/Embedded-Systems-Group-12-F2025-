import time
import board
import digitalio
from audiocore import WaveFile
from audiopwmio import PWMAudioOut

# Input on GP13 
play_input = digitalio.DigitalInOut(board.GP13)
play_input.direction = digitalio.Direction.INPUT
play_input.pull = digitalio.Pull.DOWN   

# Audio setup
wave_file = open("theme.wav", "rb")
wave = WaveFile(wave_file)

# Audio output on GP13
audio = PWMAudioOut(board.GP14)

while True:
    if play_input.value:  # GP13 is HIGH
        if not audio.playing:
            # Rewind and start playing
            wave_file.seek(0)
            audio.play(wave)
    else:  # GP13 is LOW
        if audio.playing:
            audio.stop()

    time.sleep(0.01)  
