import music21
import music21.chord as chord

# define a list of pitches
pitches = [chord.Chord(['C4','E5']), 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']

# create a music21 Stream
stream = music21.stream.Stream()

# add the pitches to the Stream as Music21 Notes
for pitch in pitches:
    if type(pitch) == str:
        note = music21.note.Note(pitch)
    else:
        note = pitch
    stream.append(note)

# display the musical notation
stream.write("lilypond", fp="recorded.ly")

