"""
Functions related to pitch detection.
"""
import librosa
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from scipy.signal import find_peaks
import soundfile
import os

# Single Pitch Detection

def pitch_detection(file_path):
    # load a file, get the music and the sample_freq
    data, sample_freq = librosa.load(soundfile.SoundFile(file_path))
    T = 1 / sample_freq
    N = len(data)

    Y_k = np.fft.fft(data)[0:int(N/2)]/N # FFT
    Y_k[1:] = 2*Y_k[1:] # Single-sided spectrum
    Pxx = np.abs(Y_k) # Power spectrum

    f = sample_freq * np.arange((N/2)) / N; # frequencies

    # plotting
    fig,ax = plt.subplots()
    plt.plot(f[0:5000], Pxx[0:5000], linewidth=2)
    plt.ylabel('Amplitude')
    plt.xlabel('Frequency [Hz]')
    plt.show()(path)


pitch_freq = pitch_detection("/home/zhao/Documents/automatic_music_notation/sound_track/dou1.mp3")
print(pitch_freq)