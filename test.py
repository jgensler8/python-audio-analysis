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

import pyaudio
import numpy as np
import wave
import wavio
import math

CHUNK = 1024
# CHUNK = 512
# CHUNK = 256
WIDTH = 2
# CHANNELS = 2
CHANNELS = 1
RATE = 44100
# RECORD_SECONDS = 5

consecutive_for_pause = 2

wf = wave.open("audio/followingthecolorline_00_baker_64kb.wav")

p = pyaudio.PyAudio()

# stream = p.open(format=p.get_format_from_width(WIDTH),
#                 channels=CHANNELS,
#                 rate=RATE,
#                 # input=True,
#                 output=True,
#                 frames_per_buffer=CHUNK)

stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

def pack_arr(arr):
    ''.join(arr)

word_counter = 0
def save_word(word_arr, word_counter):
    if len(word) > 0:
        arr = np.concatenate(word_arr)
        wavio.write("audio/words/{}.wav".format(word_counter), arr, RATE/2, sampwidth=CHANNELS)
        print "Saving word of length {:3} frame".format(len(word))
        return True
    else:
        return False

word = []
consecutive_counter = 0

# read data (based on the chunk size)
data = wf.readframes(CHUNK)
i = 0
# play stream (looping from beginning of file to the end)
while data != '':
    # writing to the stream is what *actually* plays the sound.
    stream.write(data)
    data = wf.readframes(CHUNK)
    np_arr = np.fromstring(data, dtype=np.int16)
    mean = np.abs(np.round(np.mean(np_arr)))
    std = np.round(np.std(np_arr))
    if mean > 5 and std > 1000:
        speaking = True
        word.append(np_arr)
        consecutive_counter = 0
    else:
        consecutive_counter += 1
        if consecutive_counter >= consecutive_for_pause:
            saved = save_word(word, word_counter)
            if saved:
                word_counter += 1
            word = []
        speaking = False
    print "{:5} {:5} {:7} {}".format(i, mean, std, speaking)

    i += 1

# cleanup stuff.
stream.close()
p.terminate()

while True:
    data = stream.read(CHUNK)
    data = stream.read(1)
    np_arr = np.fromstring(data, dtype=np.int16)
    print "==================== before ======================="
    np_arr = np.multiply(np_arr, 1)
    mean = np.mean(np.abs(np_arr))
    np_arr = np.sin(np_arr)

print("* done")

# stream.stop_stream()
# stream.close()
#
# p.terminate()
