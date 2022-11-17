import librosa
import numpy as np
# librosa.show_versions()
# librosa.hz_to_note(444.0)
rst = librosa.hz_to_note(440.0)
basic_pitch_freq = 440.0 * (2.0 ** np.linspace(0, 1, 12))
basic_pitch_note = librosa.hz_to_note(basic_pitch_freq)
print(basic_pitch_note)
print(librosa.note_to_hz(basic_pitch_note))