"""
Functions related to pitch detection:
- Slice the audio into small pieces
- Detect the pitch of each piece
- Decide the durations and clefs
"""

import librosa
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.signal import find_peaks
from typing import List, Tuple

_NLAGS = 5000
_VIS_POINTS = 10000
_SPECTRAL_NAME = "spectral"


def single_pitch_detection(data: List[int], sample_rate: int) -> str:
    """
    Single Pitch Detection
    - data: Slicing data according to beats
    - sample_rate: self-explanatory
    It loads a file, get the music and the sample_rate
    May lead to warning: Librosa tries to use libsndfile first,
    and if that fails, it will fall back on the audioread package
    """
    pitch_note = 'R'
    # The range of the allowed frequencies
    bass_clef_freq_min = librosa.note_to_hz("C2")
    treble_clef_freq_max = librosa.note_to_hz("C6")

    auto_correlation_function = sm.tsa.acf(data, nlags=_NLAGS)
    # Find peaks of the autocorrelation
    peaks = find_peaks(auto_correlation_function)[0]
    if len(peaks) > 0:
        # Choose the first peak as our pitch component lag
        lag = peaks[0]
    else:
        return pitch_note

    # Transform lag into frequency
    pitch_freq = sample_rate / lag
    if pitch_freq <= treble_clef_freq_max and pitch_freq >= bass_clef_freq_min:
        pitch_note = librosa.hz_to_note(pitch_freq)
    return pitch_note


def pitch_detection(file_path: str, beat_itvs: list, sample_rate: int) -> list[str]:
    """
    Detect pitches
    - file_path: the path of the target audio file
    - beat_itvs: beat intervals used to slice the audio
    - sample_rate: the sample rate
    """
    # Data acquired from the sound track
    data, _ = librosa.load(file_path, sr=sample_rate)
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


def write_pitch(pitches: List[str], file_path: str) -> None:
    with open(file_path, "w") as fp:
        fp.write(" ".join(pitches))


def pitch_duration_detection(note: int, pitches: List[str]) -> Tuple[list, list]:
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


def clef_detection(pitches: list[str]) -> str:
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
        if pitch == 'R':
            continue
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


def wave_plot(data: int, start_time: float, sample_rate: int, beats: List[int], time_duration: int = 5) -> None:
    start_ptr = int(start_time * sample_rate)
    end_ptr = int((start_time + time_duration) * sample_rate)
    sample_itv_plot = int(sample_rate*time_duration//_VIS_POINTS)
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

    time_plot = [(start_time + time * time_duration / data_plot_len)
                 for time in range(data_plot_len)]
    fig, ax = plt.subplots()
    ax.plot(time_plot, data_plot, 'k', linewidth=1)
    for beat in beats_plot:
        plt.axvline(beat, linestyle='--', color='r',
                    label='axvline - full height', linewidth=2)
    fig.set_figwidth(12)
    fig.set_figheight(3)
    plt.grid(False)
    plt.axis('off')
    fig.savefig("%s.svg"%(_SPECTRAL_NAME), format='svg')
    plt.close(fig=fig)


if __name__ == "__main__":
    file_path = "/home/pi/automatic_music_notation/sound_track/C2Long.wav"
    data, _ = librosa.load(file_path, sr=22050)
    wave_plot(data, 0, 22050, [1, 2, 3, 4])
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
    # pitch_freqs = pitch_detection(file_path, [0.5], 22050)
    # print(pitch_freqs)
