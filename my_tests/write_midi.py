# From:
# http://stackoverflow.com/questions/11059801/how-can-i-write-a-midi-file-with-python

from midiutil.MidiFile import MIDIFile

mf = MIDIFile(1, removeDuplicates=True, deinterleave=True)
track = 0

mf.addTrackName(track, 0, "My Track")
mf.addTempo(track, 0, 100)

# .addNote(track, channel, pitch, time, duration, volume)
mf.addNote(track, 0, 60, 0, 1, 100)
mf.addNote(track, 0, 62, 1, 1, 75)
mf.addNote(track, 0, 64, 2, 1, 50)

print mf

with open("test.mid", 'wb') as newf:
    mf.writeFile(newf)
