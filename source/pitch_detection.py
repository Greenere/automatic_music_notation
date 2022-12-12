"""
Functions related to pitch detection.
"""
import librosa
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.signal import find_peaks
from typing import List

from logger import log_debug

_NLAGS = 22050
# Single Pitch Detection
# data: Slicing data according to beats
# sample_rate: self-explanatory
def single_pitch_detection(data: List[int], sample_rate: int) -> str:
    # load a file, get the music and the sample_rate
    # May lead to warning: Librosa tries to use libsndfile first, 
    # and if that fails, it will fall back on the audioread package
    N = len(data)
    # N = int(N / 2)
    bass_clef_freq_min = librosa.note_to_hz("C2")
    treble_clef_freq_max = librosa.note_to_hz("C6")

    auto_correlation_function = sm.tsa.acf(data[:N], nlags=_NLAGS)
    #print("Auto Correction function: %s" %str(auto_correlation_function))
    peaks = find_peaks(auto_correlation_function)[0]  # Find peaks of the autocorrelation
    #print("Peaks: %s" %str(peaks))
    if len(peaks) > 0:
        lag = peaks[0]  # Choose the first peak as our pitch component lag
    else:
        return 'R'

    pitch_freq = sample_rate / (3 * lag)  # Transform lag into frequency
    #print("Pitch Frequency: %s hz"%(str(pitch_freq)))
    pitch_note = 'R'
    if pitch_freq <= treble_clef_freq_max and pitch_freq >= bass_clef_freq_min:
        pitch_note = librosa.hz_to_note(pitch_freq*2)

    log_debug("Note: %s" %pitch_note)
    return pitch_note


# beat_itv: the average beat interval recorded on the Raspberry pi
# file_path
# sample_rate

def pitch_detection(file_path: str, beat_itvs: list, sample_rate: int) -> list[str]:
    data, _ = librosa.load(file_path, sr=sample_rate)   # Data acquired from the sound track
    i = 0
    start_ptr = 0   # The start of the data slicing
    N = len(data)   # The length of the data
    pitches = []    # pitches detected

    beat_itv = sum(beat_itvs)/len(beat_itvs)

    while (start_ptr <= N):
        if i < len(beat_itvs):
            data_itv = int(beat_itvs[i] * sample_rate) 
        else:
            data_itv = int(beat_itv * sample_rate)

        pitch = 'R'
        if (start_ptr + data_itv <= N):
            data_piece = data[start_ptr: start_ptr + data_itv]
            pitch = single_pitch_detection(
                    data_piece, sample_rate
                )
        else:
            data_piece = data[start_ptr: N]
            pitch = single_pitch_detection(
                    data_piece, sample_rate
                )
        
        pitches.append(pitch)
        start_ptr += data_itv
        i += 1
    
    return pitches

def pitch_detection_multi_channel(file_path: str, sample_rate: int):
    data, _ = librosa.load(file_path, sr=44100)   # Data acquired from the sound track
    print("Length of data using by pitch detection %d" % len(data))
    pitches, magnitudes = librosa.piptrack(y=data, sr=sample_rate, fmin=65, fmax=2093)

    return pitches, magnitudes

def write_pitch(pitches: List[str], file_path: str):
    with open(file_path,"w") as fp:
        fp.write(" ".join(pitches))

def pitch_duration_detection(note: int, pitches: List[str]):
    pitches_num = len(pitches)
    start_ptr = 0
    pitches_partition = []
    pitches_duration = []

    while start_ptr < pitches_num:
        pitches_partition.append(pitches[start_ptr])
        pitches_duration.append(1 / note)
        if (start_ptr + note <= pitches_num):
            for i in range(note - 1):
                if pitches[start_ptr + i + 1] == pitches_partition[-1]:
                    pitches_duration[-1] += 1 / note
                else:
                    pitches_partition.append(pitches[start_ptr + i + 1])
                    pitches_duration.append(1 / note)
            
        else:
            for i in range(pitches_num - start_ptr - 1):
                if pitches[start_ptr + i + 1] == pitches_partition[-1]:
                    pitches_duration[-1] += 1 / note
                else:
                    pitches_partition.append(pitches[start_ptr + i + 1])
                    pitches_duration.append(1 / note)

        start_ptr += note

    return pitches_partition, pitches_duration

def within_the_range(val, min, max) -> bool:
    return (val >= min and val <= max)

def clef_detection(pitches: list[str]):
    treble_clef_freq_min = librosa.note_to_hz("C4")
    treble_clef_freq_max = librosa.note_to_hz("C6")
    alto_clef_freq_min = librosa.note_to_hz("C3")
    alto_clef_freq_max = librosa.note_to_hz("C5")
    bass_clef_freq_min = librosa.note_to_hz("C2")
    bass_clef_freq_max = librosa.note_to_hz("C4")

    treble_cnt = 0
    alto_cnt = 0
    bass_cnt = 0

    clef = ""

    for pitch in pitches:
        if pitch == 'R': continue
        if within_the_range(librosa.note_to_hz(pitch), treble_clef_freq_min, treble_clef_freq_max):
            treble_cnt += 1
        if within_the_range(librosa.note_to_hz(pitch), alto_clef_freq_min, alto_clef_freq_max):
            alto_cnt += 1
        if within_the_range(librosa.note_to_hz(pitch), bass_clef_freq_min, bass_clef_freq_max):
            bass_cnt += 1
    
    max_cnt = max(treble_cnt, alto_cnt, bass_cnt)
    if max_cnt == treble_cnt:
        clef = "treble"
    elif max_cnt == alto_cnt:
        clef = "alto"
    else:
        clef = "bass"

    return clef

def wave_plot(data: int, start_time: float, sample_rate: int, beats: List[int], time_duration=5):
    start_ptr = int(start_time * sample_rate)
    end_ptr = int((start_time + time_duration) * sample_rate)
    sample_itv_plot = sample_rate//400
    data_plot = data[start_ptr:end_ptr:sample_itv_plot]
    data_plot_len = len(data_plot)
    beats_plot = []
    j = len(beats) - 1
    while j >= 0:
        beat = beats[j]
        if beat >= start_time and beat <= start_time + time_duration:
            beats_plot.append(beat)
        if beat < start_time:
            break
        j -= 1

    time_plot = [(start_time + time * time_duration / data_plot_len) for time in range(data_plot_len)]
    fig, ax = plt.subplots()
    ax.plot(time_plot, data_plot, 'k', linewidth=2)
    for beat in beats_plot:
        plt.axvline(beat, color='r', label = 'axvline - full height', linewidth = 3)
    fig.set_figwidth(12)
    fig.set_figheight(3)
    plt.grid(False)
    plt.axis('off')
    fig.savefig("spectral.svg", format='svg')
    plt.close(fig=fig)

if __name__ == "__main__":
    file_path = "/home/pi/automatic_music_notation/sound_track/C2Long.wav"
    data, _ = librosa.load(file_path, sr=22050)
    wave_plot(data, 0, 22050, [1,2,3,4])
    # pitch_note = single_pitch_detection(data, 22050)
    # print(pitch_note)
    # pitches = []
    # np.random.seed(1)
    # pitches_range = np.random.randint(65, 71, 16 * 2)
    # pitches_random = [chr(i) for i in pitches_range]
    # pitches_all_A = ['A'] * 32
    # pitches_test1 = ['A'] * 4 + ['B'] * 4 + ['A'] * 4 + ['C'] * 2 + ['A'] * 4 + ['D'] * 4
    # pitches_test2 = ['A'] * 6 + ['B']
    # pitches_partition, pitches_duration = pitch_duration_detection(16, pitches_test2)
    # clef = clef_detection(pitches_test2)
    # print("pitches: %s" %str(pitches))
    # print("pitches_partition: %s" %str(pitches_partition))
    # print("pitches_duration: %s" %str(pitches_duration))
    # print("clef: %s" %str(clef))
    # pitch_freqs = pitch_detection(file_path, 0.5, 22050)
    # print(pitch_freqs)