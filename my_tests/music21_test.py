# From: https://www.youtube.com/watch?v=7W00dYfMpmw
import music21
sBach = music21.corpus.parse('bach/bwv7.7')
mf = music21.midi.translate.streamToMidiFile(sBach)
mf.open('bach.mid', 'wb')
mf.write()
mf.close()
