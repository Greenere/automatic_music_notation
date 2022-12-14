"""
Functions related to sound recording:
- Recording the voice from the USB-Microphones (one channel)
"""

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

from logger import log_debug

_SAMPLE_RATE = 44100


def record_long_piece(seconds: float, fs: int = _SAMPLE_RATE) -> np.ndarray:
    piece = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    return piece


def write_piece(piece: np.ndarray, filename: str, fs: int = _SAMPLE_RATE) -> None:
    write(filename, fs, piece)


def extract_pieces(piece: np.ndarray, event_times: list, fs: int = _SAMPLE_RATE) -> np.ndarray:
    # Stop the recording
    sd.stop()
    log_debug("Recorded events: %s" % (str(event_times)))
    if event_times[0][0] != 'start':
        log_debug("Event logs are corrupted")
        exit(1)
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
    return large_piece
