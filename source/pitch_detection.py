"""
Functions related to pitch detection.
"""
import time
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

    f = sample_rate * np.arange((N/2)) / N;     # frequencies

    auto_correlation_function = sm.tsa.acf(data[:N])
    print("Auto Correction function: %s" %str(auto_correlation_function))
    peaks = find_peaks(auto_correlation_function)[0]  # Find peaks of the autocorrelation
    print("Peaks: %s" %str(peaks))
    if len(peaks) > 0:
        lag = peaks[0]  # Choose the first peak as our pitch component lag
    else:
        lag = max(auto_correlation_function)

    pitch_freq = sample_rate / lag  # Transform lag into frequency
    pitch_note = librosa.hz_to_note(pitch_freq)


    # pitch_freq = librosa.yin(y=data, frame_length=N, sr=sample_rate, fmin=65, fmax=2093)
    # pitch_note = librosa.hz_to_note(pitch_freq)
    print("Note: %s" %pitch_note)
    return pitch_note


# beat_itv: the average beat interval recorded on the Raspberry pi
# file_path
# sample_rate

def pitch_detection(file_path: str, beat_itv: int, sample_rate: int) -> list[str]:
    data, _ = librosa.load(file_path, sr=44100)   # Data acquired from the sound track
    print("Length of data using by pitch detection %d" % len(data))
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

def pitch_detection_multi_channel(file_path: str, sample_rate: int):
    data, _ = librosa.load(file_path, sr=44100)   # Data acquired from the sound track
    print("Length of data using by pitch detection %d" % len(data))
    pitches, magnitudes = librosa.piptrack(y=data, sr=sample_rate, fmin=65, fmax=2093)

    return pitches, magnitudes

def write_pitch(pitches: List[str], file_path: str):
    with open(file_path,"w") as fp:
        for pitch in pitches:
            fp.write("%s " % pitch)

if __name__ == "__main__":
    file_path = "/home/pi/automatic_music_notation/sound_track/A#4.mp3"
    pitch_freqs = pitch_detection(file_path, 0.5, 22050)
    print(pitch_freqs)