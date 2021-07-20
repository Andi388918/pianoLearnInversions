import random
import mido

NOTES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)

def get_inversion(notes, chord):
    if notes[0][0] == chord[0] and notes[1][0] == chord[1]:
        return (chord[0], 0)
    elif notes[0][0] == chord[1] and notes[1][0] == chord[2]:
        return (chord[0], 1)
    elif notes[0][0] == chord[2] and notes[1][0] == chord[0]:
        return (chord[0], 2)

chord_dict = {"C": ("C", "E", "G"),
              "Db": ("Db", "F", "Ab"),
              "D": ("D", "F#", "A"),
              "Eb": ("Eb", "G", "Bb"),
              "E": ("E", "Ab", "B"),
              "F": ("F", "A", "C"),
              "F#": ("F#", "Bb", "Db")}

def number_to_note(number: int) -> tuple:
    octave = number // NOTES_IN_OCTAVE
    note = NOTES[number % NOTES_IN_OCTAVE]

    return f"{note}"

sequence = []

for chord in NOTES[:7]:
    for i in range(10):
        sequence.append((chord, 0))
        sequence.append((chord, 1))
        sequence.append((chord, 2))

random.shuffle(sequence)

print(f"{sequence[0]}, {len(sequence)}")

notes = []

with mido.open_input() as inport:
    for msg in inport:
        if hasattr(msg, 'note'):
            note = number_to_note(msg.note)
            if msg.type == "note_on":
                notes.append((note, msg.note))
            else:
                notes.remove((note, msg.note))

            if len(notes) == 6:
                notes.sort(key=lambda x: x[1])

                l = [notes[0:3], notes[3:6]]

                r = 0

                for y in l:
                    x, _ = list(zip(*y))
                    for chord, n in chord_dict.items():
                        if set(n) == set(x):
                            if get_inversion(notes, n) == sequence[0]:
                                r += 1

                if r == 2:
                    sequence.pop(0)
                    print(f"{sequence[0]}, {len(sequence)}")
