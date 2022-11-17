clef = "alto"
pitches = [0,1,2,3,4,5,6,7,8,9,10,11]
groups =  [5,5,5,5,5,5,5,5,5,5,5,5]
time = [4,4]

bases = ["c","cis","d","dis","e","eis","f","g","gis","a","ais","b"]

def translate_pitch(index, group):
    if group == 5:
        return bases[index]
    elif group > 5:
        return bases[index] + "'"*(group-5)
    elif group < 5:
        return bases[index] + ","*(5-group)

def generate_lilypond_notation(clef, time, pitches):
    return '\\absolute {\n \\clef "%s"\n \\time %d/%d\n %s\n}'% \
           (clef, time[0], time[1], ' '.join(pitches))

with open("sample.ly", "w") as f:
    translated_pitches = [translate_pitch(i, g) 
                          for i,g in zip(pitches, groups)]
    f.write(generate_lilypond_notation(clef, time, translated_pitches))

