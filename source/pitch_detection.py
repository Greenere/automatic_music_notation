"""
Functions related to pitch detection.
"""
import librosa
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from scipy.signal import find_peaks
from typing import List

_NLAGS = 2000
# Single Pitch Detection
# data: Slicing data according to beats
# sample_rate: self-explanatory
def single_pitch_detection(data: List[int], sample_rate: int) -> str:
    # load a file, get the music and the sample_rate
    # May lead to warning: Librosa tries to use libsndfile first, 
    # and if that fails, it will fall back on the audioread package
    N = len(data)
    # N = int(N / 2)

    data_freq = np.fft.fft(data[:N])[0:int(N/2)]/N  # FFT
    data_freq[1:] = 2*data_freq[1:]     # Single-sided spectrum
    power_spectrum = np.abs(data_freq)  # Power spectrum

    f = sample_rate * np.arange((N/2)) / N;     # frequencies

    auto = sm.tsa.acf(data[:N], nlags=_NLAGS)
    peaks = find_peaks(auto)[0]  # Find peaks of the autocorrelation
    lag = peaks[0]  # Choose the first peak as our pitch component lag

    pitch_freq = sample_rate / lag  # Transform lag into frequency
    pitch_note = librosa.hz_to_note(pitch_freq)

    return pitch_note


# beat_itv: the average beat interval recorded on the Raspberry pi
# file_path
# sample_rate

def pitch_detection(file_path: str, beat_itv: int, sample_rate: int) -> list[str]:
    data, _ = librosa.load(file_path)   # Data acquired from the sound track
    data_itv = int(beat_itv * sample_rate)  # Slicing data according to beats
    start_ptr = 0   # The start of the data slicing
    N = len(data)   # The length of the data
    pitches = []    # pitches detected

    while (start_ptr <= N):
        if (start_ptr + data_itv <= N):
            pitch = single_pitch_detection(
                data[start_ptr: start_ptr + data_itv], sample_rate
            )
        else:
            pitch = single_pitch_detection(
                data[start_ptr: N], sample_rate
            )
        
        pitches.append(pitch)
        start_ptr += data_itv

    return pitches

file_path = "/home/pi/automatic_music_notation/sound_track/A#4.mp3"
pitch_freqs = pitch_detection(file_path, 0.5, 22050)
print(pitch_freqs)