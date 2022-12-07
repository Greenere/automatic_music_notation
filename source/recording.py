"""
Functions related to sound recording typically have two modules:
- Recording the voice from the USB-Microphones (one channel)
- A control panal that monitors the behavior of the recorder
"""

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

def record_short_piece(seconds, fs = 44100):
  piece = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
  sd.wait()
  return piece

def record_long_piece(seconds, fs = 44100):
  piece = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
  return piece

def write_piece(piece, filename, fs = 44100):
  write(filename, fs, piece)

def save_short_piece(piece, filename):
  piece.dump(filename)

