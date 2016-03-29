# A python script to read and parse midi files
import re


# def get_notes_list(midi_string):
#     # string interpolation to convert to lowercase hexadecimal
#     # ('x') with leading zeros ('02')
#     hex_bytes = ['%02x' % x for x in bytearray(midi_string)]
#     hex_string = ''.join(hex_bytes)
#     return hex_string

#     notes_pattern = get_notes_pattern()
#     re.match(notes_pattern, hex_string)


def get_patterns():
    # file header is always this
    file_head_p = '4d54686400000006'
    # 0, 1, or 2 for format type
    format_type_p = '(....)'
    # catch number of tracks
    num_tracks_p = '(....)'
    # don't care about timing yet
    ticks_p = '(....)'
    header_chunk_p = file_head_p + format_type_p + num_tracks_p + ticks_p
    # track chunk header
    track_head_p = '4d54726b'
    track_length_p = '........'
    # for now, any number of pairs before 00ff2f00
    # TODO: figure out a good way to fix this-00ff2f00
    # could occur prematurely...
    track_body_p = '(?:..)*00ff2f00'
    track_chunk_p = '(' + track_head_p + track_length_p + track_body_p + ')'

    return header_chunk_p, track_chunk_p


def parse_midi(midi_string):
    hex_bytes = ['%02x' % x for x in bytearray(midi_string)]
    print hex_bytes
    hex_string = ''.join(hex_bytes)

    header_chunk_p, track_chunk_p = get_patterns()

    matches = re.match(
        '{0}{1}*'.format(header_chunk_p, track_chunk_p),
        hex_string)
    for i in range(0,5):
        print matches.group(i)



if __name__ == '__main__':
    with open('test.mid', 'r') as mf:
        midi_string = mf.read()
        print parse_midi(midi_string)
