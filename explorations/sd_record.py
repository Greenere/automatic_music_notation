"""
source: https://realpython.com/playing-and-recording-sound-python/#recording-audio
sounddevice: https://python-sounddevice.readthedocs.io/en/latest/
"""
import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 3  # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
write('output.wav', fs, myrecording)  # Save as WAV file 
