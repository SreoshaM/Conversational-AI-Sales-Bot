import time
import sounddevice as sd
from scipy.io.wavfile import write

def generate_voice(voice_path):
    start = time.time()
    """Record voice and save in local"""
    freq = 44100
    duration = 5
    recording = sd.rec(int(duration * freq), 
                    samplerate=freq, channels=2)
    sd.wait()
    write(voice_path, freq, recording)
    end = time.time()
    print(f"Sound writing time : {end - start}")