""" File imports a midi_ex4a.mid, and finds quarter notes in all tracks,
    changes them to dotted eights of the same pitch, then recompiles and
    saves the file as midi_ex4b.mid. Also changes some notes down a semitone
    (64, 69, and 71), which are the 3rd, sixth, and seventh in a C Major
    scale starting on 60. This process preserves program_change messages,
    along with all other non-note messages. Disclaimer: it's not that
    different from ex3.py!
    (assignment below)
"""
# EX 4:  write a program that will:
# Import a short guitar midi file (which you can find online), change some
# notes, and then output the changed MIDI file but make sure it still retains
# its instrument designation, i.e., the user hears a guitar sound when
# listening to the outputted file.


import mido

# --- PARAMETERS --- #
midi_source = "midi_ex4a.mid"
midi_destination = "midi_ex4b.mid"


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

        # this next bit of code is completely useless, but shows
        # how to change programs. Right now, program_change and
        # and all other non-note messages are preserved.
        if message.type == "program_change":
            message.program = message.program

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


def adjust_notes(notes, quarter_ticks):
    """ Processes notes (a list of tuples of on/off messages), altering rhythms
        and adding additional notes. In this case, quarter notes are replaced
        with dotted eighths. Updated_note_messages list is returned (list of
        midi messages with no tuples)
    """
    # now the rhythms are processed and all notes are collected in a list
    updated_note_messages = []
    for note_on, note_off in notes:
        # change to minor
        if note_on.note in [64, 69, 71]:
            note_on.note -= 1
            note_off.note -= 1
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
    sort_priority = {
        "note_off": 1,
        "note_on": 2,
        "end_of_track": 3
    }
    messages = sorted(
        updated_messages, key=lambda x: (x.time, sort_priority.get(x.type, 0)))

    current_tick = 0
    for message in messages:
        message.time -= current_tick
        current_tick += message.time

    for message in messages:
        mido_f.tracks[track_i].append(message)


mido_f = mido.MidiFile(midi_source)

for track_i, track in enumerate(mido_f.tracks):
    notes, updated_messages = pop_notes_list(track)
    updated_messages += adjust_notes(notes, mido_f.ticks_per_beat)
    sort_and_recompile(mido_f, updated_messages, track_i)

# save the edited file, and print a short report if the script was run
# from the terminal
mido_f.save(midi_destination)
if __name__ == "__main__":
    print "Rewrote quarters of {} as dotted eight rhythms in {}, and changed 3rd, 6th, and 7th of the scale to minor intervals.".format(
        midi_source, midi_destination)
