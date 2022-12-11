"""
Functions related to sound recording:
- Recording the voice from the USB-Microphones (one channel)
"""

import sounddevice as sd
import numpy as np
import noisereduce as nr
from scipy.io.wavfile import write

from logger import log_debug

_SAMPLE_RATE = 44100


def record_short_piece(seconds: float, fs: int = _SAMPLE_RATE) -> np.ndarray:
    piece = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    return piece


def record_long_piece(seconds: float, fs: int = _SAMPLE_RATE) -> np.ndarray:
    piece = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    return piece


def write_piece(piece: np.ndarray, filename: str, fs: int = _SAMPLE_RATE) -> None:
    write(filename, fs, piece)


def save_short_piece(piece: np.ndarray, filename: str) -> None:
    piece.dump(filename)

def preprocessing(piece: np.ndarray, fs: int = _SAMPLE_RATE) -> np.ndarray:
    return piece

def extract_pieces(piece: np.ndarray, event_times: list, fs: int = _SAMPLE_RATE) -> np.ndarray:
    # Stop the recording
    sd.stop()
    log_debug("Recorded events: %s" % (str(event_times)))
    # Cut and concatenate the pieces according to the pause, resume events
    pieces = []
    prev_sec = event_times[0][1]
    paused = False
    for event, sec in event_times:
        if event == "pause":
            short_piece = piece[int(prev_sec*fs):int(sec*fs), :]
            log_debug("Get a piece between %f and %f" % (prev_sec, sec))
            pieces.append(short_piece)
            paused = True
        elif event == "resume":
            prev_sec = sec
            paused = False
        elif event == "end" and not paused:
            short_piece = piece[int(prev_sec*fs):int(sec*fs), :]
            log_debug("Get a piece between %f and %f" % (prev_sec, sec))
            pieces.append(short_piece)
    large_piece = np.vstack(pieces)
    large_piece = preprocessing(large_piece, fs)
    return large_piece
