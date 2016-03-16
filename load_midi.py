# From: https://www.youtube.com/watch?v=7W00dYfMpmw
# import music21
# sBach = music21.corpus.parse('bach/bwv7.7')
# mf = music21.midi.translate.streamToMidiFile(sBach)
# mf.open('bach.mid', 'wb')
# mf.write()
# mf.close()

# From:
# http://stackoverflow.com/questions/11059801/how-can-i-write-a-midi-file-with-python

from midiutil.MidiFile import MIDIFile

mf = MIDIFile(1)
track = 0

mf.addTrackName(track, 0, "My Track")
mf.addTempo(track, 0, 100)

# .addNote(track, channel, pitch, time, duration, volume)
mf.addNote(track, 0, 60, 0, 1, 100)
mf.addNote(track, 0, 62, 1, 1, 75)
mf.addNote(track, 0, 64, 2, 1, 50)

with open("test.mid", 'wb') as newf:
    mf.writeFile(newf)
