"""
source: https://realpython.com/playing-and-recording-sound-python/#recording-audio
sounddevice: https://python-sounddevice.readthedocs.io/en/latest/
"""
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

fs = 44100  # Sample rate
seconds = 10  # Duration of recording

print(sd.query_devices())
print(sd.default.device)

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
#myrecording.dump("output.pkl")
write('output.wav', fs, myrecording)  # Save as WAV file 