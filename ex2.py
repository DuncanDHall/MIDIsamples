""" File imports a midi_ex2a.mid, transposes each track individually,
    then writes the result to midi_ex2b.mid.
    (assignment below)
"""

# EX 2:  Create a 2-instrument file in Sibelius and save it as a MIDI
# file (Export as MIDI).

# Now write a program that will:
#     - Import the 2-instrument MIDI file.
#     - Access the 1st instrument and transpose all note/chord events
#     up a major 2nd (M2 = 2 half steps).
#     - Access the 2nd instrument  and transpose all note/chord events
#     up a major 2nd.
#     - Output the new MIDI file consisting of the two transposed tracks
#     and check to make sure it reflects the transposed changes.
#     - You can also drop the outputted MIDI file into Sibelius to check
#     that the correct changes were made.

import mido

# --- PARAMETERS --- #
midi_source = "midi_ex2a.mid"
midi_destination = "midi_ex2b.mid"

# each element corresponds to a single track, detirmining how it will
# be transposed.
transpositions = [2, 2]  # in half steps (major 2nd is )

mid = mido.MidiFile(midi_source)
# in MIDI file type 1 (the 9th and 10th bytes), the first track contains
# only meta information. Also catches if the transpositions list is just
# too short (only the later tracks will be transposed though)
if mid.type == 1:
    while len(transpositions) < len(mid.tracks):
        transpositions.insert(0, 0)

# for each message in each track, transpose the message if it has to
# do with notes byt the transpose amount
for i, track in enumerate(mid.tracks):
    print("Track {}: {}".format(i, track.name or "Meta Information"))
    for message in track:
        if message.type == "note_on" or message.type == "note_off":
            try:
                message.note += transpositions[i]
            except:
                print """something unanticipated was found, make sure the
                    midi file is type 1. """

# save the edited file, and print a short report if the script was run
# from the terminal
mid.save(midi_destination)
if __name__ == "__main__":
    print "Transposition of {} by {} half steps saved to {}".format(
        midi_source, transpositions, midi_destination)
