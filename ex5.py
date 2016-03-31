""" File imports a midi_ex4a.mid, and finds quarter notes in all tracks,
    changes them to dotted eights of the same pitch, then recompiles and
    saves the file as midi_ex4b.mid. Also changes some notes down a semitone
    (64, 69, and 71), which are the 3rd, sixth, and seventh in a C Major
    scale starting on 60. This process preserves program_change messages,
    along with all other non-note messages. Disclaimer: it's not that
    different from ex3.py!
    (assignment below)
"""
# EX 5:  Create a 3-instrument file in Sibelius that consists of 3 different
# percussion instruments:  marimba, snare drum, and cowbell.  Save it as a
# MIDI file (Export as MIDI).  Write a program that will:
#   - Import the 3-percussion instrumental file.  Access the marimba and
#   change its notes and rhythms.
#   - Access the snare drum and change its rhythms.
#   - Access the cowbell and change its rhythms.  Then change the cowbell
#   instrument to triangle so the new rhythms are played with a triangle
#   sound, not a cowbell.
#   - Output the new MIDI file consisting of the 3 percussion instruments
#   (now marimba, snare drum, and triangle).
#   - Check to make sure the outputted file reflects the rhythmic changes
#   made to each instrumental line.
# You can also drop the outputted MIDI file into Sibelius to check that the
# correct changes were made


import mido

# --- PARAMETERS --- #
midi_source = "midi_ex5a.mid"
midi_destination = "midi_ex5b.mid"


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

        # this I can't figure out. I think it's an anomaly with sibelius.
        # the program value is changed to triangle (79), and confirmed
        # (see console output)
        if message.type == "program_change":
            if track.name == "Cowbell":
                message.program = 79
                print (
                    "'Cowbell' track with program No. {}".format(
                        message.program))

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


def adjust_notes(notes, quarter_ticks, vary_notes="True"):
    """ Processes notes (a list of tuples of on/off messages), altering rhythms
        and adding additional notes. In this case, quarter notes are replaced
        with dotted eighths. Updated_note_messages list is returned (list of
        midi messages with no tuples)
    """
    # now the rhythms are processed and all notes are collected in a list
    updated_note_messages = []
    notes.sort(key=lambda x: (x[0].time, x[0].time))

    if vary_notes:
        alternator = True

        for note_on, note_off in notes:
            # Rules:
            #   Marimba - turn every other eigth note to sixteenths
            #   other - raplace all eighths with sixteenths
            if vary_notes == "Marimba":
                alternator = not alternator
            if alternator:
                if note_off.time - note_on.time == quarter_ticks/2:
                    rhythm_break = (note_on.time + note_off.time) / 2
                    sixteenth_on = note_on.copy(time=rhythm_break)
                    sixteenth_off = note_off.copy(time=note_off.time)
                    note_off.time = rhythm_break

                    # sixeteenth is stored
                    updated_note_messages += [sixteenth_on, sixteenth_off]

            if vary_notes == "Snare Drum":
                note_off.time = note_on.time + quarter_ticks/4
                second_on = note_on.copy(
                    time=note_on.time + quarter_ticks/4)
                second_off = note_off.copy(
                    time=note_off.time + quarter_ticks/4)

                updated_note_messages += [second_on, second_off]

            # original quarter (modified to be a dotted eight) is stored
            updated_note_messages += [note_on, note_off]
    else:
        for note_on, note_off in notes:
            updated_note_messages.append(note_off)
            updated_note_messages.append(note_on)

    return updated_note_messages


def sort_and_recompile(track, updated_messages):
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
        track.append(message)


mido_f = mido.MidiFile(midi_source)

for track in mido_f.tracks:
    track_name = track.name
    notes, updated_messages = pop_notes_list(track)
    updated_messages += adjust_notes(
        notes, mido_f.ticks_per_beat, track_name)
    sort_and_recompile(track, updated_messages)

# save the edited file, and print a short report if the script was run
# from the terminal
mido_f.save(midi_destination)
if __name__ == "__main__":
    print "something smart".format(
        midi_source, midi_destination)
