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

def extract_pieces(piece, event_times, fs = 44100):
  # Stop the recording
  sd.stop()
  #print(event_times)
  pieces = []
  prev_sec = 0
  paused = False
  for event, sec in event_times:
    if event == "pause":
      short_piece = piece[int(prev_sec*fs):int(sec*fs),:]
      print("Get a piece between %f and %f"%(prev_sec, sec))
      pieces.append(short_piece)
      paused = True
    elif event == "resume":
      prev_sec = sec
      paused = False
    elif event == "end":
      if not paused:
        short_piece = piece[int(prev_sec*fs):int(sec*fs),:]
        print("Get a piece between %f and %f"%(prev_sec, sec))
        pieces.append(short_piece)
  
  large_piece = np.vstack(pieces)
  #print(large_piece.shape)
  return large_piece