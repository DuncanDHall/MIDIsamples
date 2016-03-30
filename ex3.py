""" File imports a midi_ex3a.mid, finds quarter notes in all tracks, changes
    them to dotted eights of the same pitch, then recompiles and saves the file
    (assignment below)
"""
# EX 3:   Create a 2-instrument file in Sibelius that has different rhythms
# in each instrumental line. For example, you can make a scale for the 1st
# instrument that has half notes and quarter notes; for the 2nd instrument,
# you can use the same scale but with quarters and eighth notes. Save the
# file as a MIDI file (Export as MIDI). Write a program that will:
#     - Import the 2-instrument MIDI file.
#     - Access the 1st instrument and change its rhythm.
#     - Access the 2nd instrument and change its rhythm
#     - Output the new MIDI file consisting of the 2 instrumental lines
#     whose rhythms have been changed, and check to make sure the outputted
#     file reflects the rhythmic changes.
# You can also drop the outputted MIDI file into Sibelius to check that the
# correct changes were made.

import mido

# --- PARAMETERS --- #
midi_source = "midi_ex3a.mid"
midi_destination = "midi_ex3b.mid"


def pop_notes_list(track):
    """ for track argument, sorts midi messages into note_on, note_off tuples
        in notes, and other messages in other_messages. The .time attribute
        is converted to absolute time in ticks for each message. Returns the
        notes list of tuples and the list of other messages.
    """
    # will collect current notes during current tick
    current_notes = {}
    current_tick = 0

    # a list of note tuples (on, off) for rhythmic processing
    notes = []

    # updated message list
    other_messages = []

    # pop messages into temporary lists other_messages and notes,
    # depending on their type. Also reconfigures .time attribute to
    # be absolute rather than relative for easier processing.
    while track:
        message = track.pop(0)
        current_tick += message.time  # summing the time deltas
        message.time = current_tick  # reassigning absolute time

        # store note_on messages in a temporary dictionary
        if message.type == "note_on":
            current_notes[message.note] = message

        # record note as a tuple in notes list once completed
        elif message.type == "note_off":
            notes.append((current_notes.pop(message.note), message))

        # any other message type is not edited
        else:
            other_messages.append(message)

    return notes, other_messages


def adjust_rhythms(notes, quarter_ticks):
    """ Processes notes (a list of tuples of on/off messages), altering rhythms
        and adding additional notes. In this case, quarter notes are replaced
        with dotted eighths. Updated_note_messages list is returned (list of
        midi messages with no tuples)
    """
    # now the rhythms are processed and all notes are collected in a list
    updated_note_messages = []
    for note_on, note_off in notes:
        # Rule: turn quarter notes to dotted eights
        if note_off.time - note_on.time == quarter_ticks:
            rhythm_break = (note_on.time + 3*note_off.time) / 4
            sixteenth_on = note_on.copy(time=rhythm_break)
            sixteenth_off = note_off.copy(time=note_off.time)
            note_off.time = rhythm_break

            # sixeteenth is stored
            updated_note_messages += [sixteenth_on, sixteenth_off]

        # original quarter (modified to be a dotted eight) is stored
        updated_note_messages += [note_on, note_off]

    return updated_note_messages


def sort_and_recompile(mido_f, updated_messages, track_i):
    """ Sorts the updated_messages list by absolute time, and secondarily
        message type (this fixes an issue with sixteenths starting before
        dotted eighths end). The .time attribute is converted back to time
        delta in ticks, and the messages are written to the original track.
    """
    messages = sorted(updated_messages, key=lambda x: (x.time, x.type))

    current_tick = 0
    for message in messages:
        message.time -= current_tick
        current_tick += message.time

    for message in messages:
        mido_f.tracks[track_i].append(message)


mido_f = mido.MidiFile(midi_source)

for track_i, track in enumerate(mido_f.tracks):
    print("Track {}: {}".format(track_i, track.name or "Meta Information"))
    notes, updated_messages = pop_notes_list(track)
    updated_messages += adjust_rhythms(notes, mido_f.ticks_per_beat)
    sort_and_recompile(mido_f, updated_messages, track_i)

# save the edited file, and print a short report if the script was run
# from the terminal
mido_f.save(midi_destination)
if __name__ == "__main__":
    print "Rewrote quarters of {} as dotted eight rhythms in {}".format(
        midi_source, midi_destination)
