"""
Functions related to notation generation
"""
import music21
import os

from typing import List

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