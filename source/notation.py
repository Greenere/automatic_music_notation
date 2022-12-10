"""
Functions related to notation generation
"""
import music21
import os

from logger import log_debug
from typing import List

_CLEF = {
    "treble": music21.clef.TrebleClef(),
    "bass": music21.clef.BassClef(),
    "alto": music21.clef.AltoClef(),
    "tenor": music21.clef.TenorClef()
}

def pitchify(name:str, duration:float) -> music21.note.Note:
    return music21.note.Note(name, quarterLength=duration)

def compose_pitches(clef:str, pitches:list, durations:list, meter: str = '4/4') -> music21.stream.Stream:
    stream = music21.stream.Stream()
    stream.timeSignature = music21.meter.TimeSignature(meter)
    if clef in _CLEF:
        stream.clef = _CLEF[clef]
    for pitch, duration in zip(pitches, durations):
        if type(pitch) == list:
            pitch_list = []
            for p in pitch:
                pitch_list.append(pitchify(p, duration))
            noted = music21.chord.Chord(pitch_list)
        else:
            noted = pitchify(pitch, duration)
        stream.append(noted)
    return stream

def write_music(stream: music21.stream.Stream, filename:str)->None:
    stream.write("lilypond", fp = "%s.ly"%filename)
    stream.write("midi", fp="%s.mid"%filename)

def generate_lilypond_source_file(pitches: List[str], filename:str) -> None:
    stream = music21.stream.Stream()
    for pitch in pitches:
        pitch = pitch.replace("♯","#")
        pitch = pitch.replace("♭","-")
        note = music21.note.Note(pitch)
        stream.append(note)
    stream.write("lilypond", fp = "%s.ly"%filename)
    stream.write("midi", fp="%s.mid"%filename)

def generate_music_notation(filename:str) -> None:
    os.system("sudo lilypond -dbackend=svg %s.ly"%(filename))

if __name__ == "__main__":
    pitches = [['C4','D4'],'C4','C4','C4']
    # music21 uses 1 to mark quarter note...
    durations = [1, 1, 1, 1]
    stream = compose_pitches('treble', pitches, durations)
    write_music(stream, "notation_test")
    generate_music_notation("notation_test")