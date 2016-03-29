""" A Python script designed to parse a simple MIDI file
    and pitch it up one whole step
"""


def parse_midi(hex_bytes):
    if hex_bytes[:4] != ['4d', '54', '68', '64']:
        print "this doesn't appear to be a MIDI file..."
        return

    i = 4

    chunk_size = hex_bytes[i:i+4]
    i += 4

    format_type = hex_bytes[i:i+2]
    i += 2

    num_tracks = hex_bytes[i:i+2]
    i += 2

    time_division = hex_bytes[i:i+2]
    i += 2

    print chunk_size, format_type, num_tracks, time_division

    if hex_bytes[i:1+4] != ['4d', '54', '72', '6b']:
        print "something's wrong with this header/track title..."
    i += 4




with open('test.mid', 'r') as mf:
    midi_string = mf.read()

hex_bytes = ['%02x' % x for x in bytearray(midi_string)]
parse_midi(hex_bytes)
