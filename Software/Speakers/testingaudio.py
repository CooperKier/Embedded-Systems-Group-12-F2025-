import array
import board
import audiobusio
import time
from audiocore import RawSample

# I2S pin setup for PCM5102
BCK_PIN = board.GP26
LCK_PIN = board.GP27
DATA_PIN = board.GP28

# I2S output (stereo)
audio = audiobusio.I2SOut(BCK_PIN, LCK_PIN, DATA_PIN)

# Generate a square wave
def generate_square_wave(frequency, duration, sample_rate=8000):
    length = int(sample_rate * duration)
    wave = array.array("H", [0] * length) 
    period = sample_rate / frequency
    for i in range(length):
        wave[i] = 65535 if (i % int(period)) < int(period / 2) else 0
    return wave

# Convert wave to stereo
def mono_to_stereo(mono_wave):
    stereo = array.array("H", [0] * (len(mono_wave) * 2))
    for i, sample in enumerate(mono_wave):
        stereo[i*2] = sample      
        stereo[i*2+1] = sample    
    return stereo

# Simple melody
melody = [
    (440, 0.5),  
    (494, 0.5),  
    (523, 0.5),  
    (587, 0.5),  
]

print("Playing melody...")

# Play the melody in a loop
while True:
    for freq, dur in melody:
        mono_wave = generate_square_wave(freq, dur)
        stereo_wave = mono_to_stereo(mono_wave)
        sample = RawSample(stereo_wave)   # Wrap in RawSample
        audio.play(sample)
        while audio.playing:
            pass
