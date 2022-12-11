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
    if name == "R":
        return music21.note.Rest(length=duration)
    return music21.note.Note(name, quarterLength=duration*4)

def pitch_name_preprocess(name:str) -> str:
    name = name.replace("♯","#")
    name = name.replace("♭","-")
    return name

def compose_pitches(clef:str, pitches:list, durations:list, meter: str = '4/4') -> music21.stream.Stream:
    stream = music21.stream.Stream()
    stream.timeSignature = music21.meter.TimeSignature(meter)
    if clef in _CLEF:
        stream.clef = _CLEF[clef]
    for pitch, duration in zip(pitches, durations):
        if type(pitch) == list:
            pitch_list = []
            for p in pitch:
                p = pitch_name_preprocess(p)
                pitch_list.append(pitchify(p, duration))
            noted = music21.chord.Chord(pitch_list)
        else:
            pitch = pitch_name_preprocess(pitch)
            noted = pitchify(pitch, duration)
        stream.append(noted)
    return stream

def write_music(stream: music21.stream.Stream, filename:str)->None:
    stream.write("lilypond", fp = "%s.ly"%filename)
    stream.write("midi", fp="%s.mid"%filename)

def export_music(stream: music21.stream.Stream, filename:str)-> None:
    converter = music21.lily.translate.LilypondConverter()
    converter.loadFromMusic21Object(stream)
    converter.createSVG("%s"%(filename))

if __name__ == "__main__":
    pitches = [['C4','D4'],'C4','C4','C4']
    # music21 uses 1 to mark quarter note...
    durations = [1, 1, 1, 1]
    stream = compose_pitches('treble', pitches, durations)
    #write_music(stream, "notation_test")
    export_music(stream, "./results/ntest")