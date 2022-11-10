"""
Functions related to sound recording typically have two modules:
- Recording the voice from the USB-Microphones (one channel)
- A control panal that monitors the behavior of the recorder

Control Panal:
- GPIO #17 (The First Button): Start Recording
- GPIO #22 (The Second Button): Pause / Continue Recording
- GPIO #23 (The Third Button): End Recording
- GPIO #27 (The Last Button): Quit
"""

import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 3  # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
write('output.wav', fs, myrecording)  # Save as WAV file 


def control():
  pass  

def recording():
  pass