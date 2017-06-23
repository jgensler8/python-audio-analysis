"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

https://stackoverflow.com/questions/33513522/when-installing-pyaudio-pip-cannot-find-portaudio-h-in-usr-local-include
numpy.fromstring
https://stackoverflow.com/questions/24974032/reading-realtime-audio-data-into-numpy-array
playing one note
http://milkandtang.com/blog/2013/02/16/making-noise-in-python/

```
$ ffmpeg -i followingthecolorline_00_baker_64kb.mp3 followingthecolorline_00_baker_64kb.wav
```
"""

from util import *

wf = wave.open("audio/followingthecolorline_00_baker_64kb.wav")

p = pyaudio.PyAudio()

i = 0
while True:
    word = read_next_word(wf)
    if word is None:
        break
    logging.info("Finished Readming Word {:5}".format(i))
    save_word(word, i)
    i += 1

print("* done")

# cleanup stuff.
p.terminate()
# stream.stop_stream()
# stream.close()
