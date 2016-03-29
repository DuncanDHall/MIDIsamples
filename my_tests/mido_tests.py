import mido

mid = mido.MidiFile('test.mid')

print
print

for i, track in enumerate(mid.tracks):
    print("Track {}: {}".format(i, track.name))
    for message in track:
        print message
