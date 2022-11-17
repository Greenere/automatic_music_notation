"""
Functions related to pitch detection.
"""
import librosa
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from scipy.signal import find_peaks

# Single Pitch Detection

def pitch_detection(file_path):
    # load a file, get the music and the sample_freq
    data, sample_freq = librosa.load(file_path)
    N = len(data)

    Y_k = np.fft.fft(data)[0:int(N/2)]/N # FFT
    Y_k[1:] = 2*Y_k[1:] # Single-sided spectrum
    Pxx = np.abs(Y_k) # Power spectrum

    f = sample_freq * np.arange((N/2)) / N; # frequencies

    # plotting
    plt.subplots()
    plt.plot(f[0:5000], Pxx[0:5000], linewidth=2)
    plt.ylabel('Amplitude')
    plt.xlabel('Frequency [Hz]')
    plt.show()

    auto = sm.tsa.acf(data, nlags=2000)
    peaks = find_peaks(auto)[0] # Find peaks of the autocorrelation
    lag = peaks[0] # Choose the first peak as our pitch component lag

    pitch_freq = sample_freq / lag # Transform lag into frequency
    pitch_note = librosa.hz_to_note(pitch_freq)

    return pitch_note



pitch_freq = pitch_detection("/home/pi/automatic_music_notation/sound_track/Tuning fork 9.mp3")
print(pitch_freq)