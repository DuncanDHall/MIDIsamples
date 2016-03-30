""" File imports a midi_ex1a.mid, transposes it up two half steps, and
    exports the file as midi-ex1b.mid
    (assignment below)
"""

# EX 1:   Create a simple scale in Sibelius.  Every Olin student has access
# to Sibelius.  You'll find install directions on the IT website.
# Save the simple scale as an SMF file (export as MIDI).  Write a python
# program that imports the MIDI file, changes some notes, and then outputs
# the changed MIDI file so you can listen to it.  (I've attached a .MID file
# I made in Sibelius so you can get started.  You can drop it onto Sibelius
# to see the score.)

# this is the library I have finally chosen after giving up on making my
# own MIDI parser in a week and a half...
import mido

# --- PARAMETERS ---#
midi_source = "midi_ex1a.mid"
midi_destination = "midi_ex1b.mid"
transposition = -2  # in half steps


mid = mido.MidiFile(midi_source)

# for each message in each track, transpose the message if it has to
# do with notes byt the transpose amount
for i, track in enumerate(mid.tracks):
    for message in track:
        if message.type == "note_on" or message.type == "note_off":
            message.note += transposition

# save the edited file, and print a short report if the script was run
# from the terminal
mid.save(midi_destination)
if __name__ == "__main__":
    print "Transposition of {} by {} half steps saved to {}".format(
        midi_source, transposition, midi_destination)
