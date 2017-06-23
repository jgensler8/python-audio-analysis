from util import *
import tensorflow as tf
import pyaudio

p = pyaudio.PyAudio()
logging.info(p.get_device_info_by_index(0)['defaultSampleRate'])


# stream = p.open(format=p.get_format_from_width(WIDTH),
#                 channels=CHANNELS,
#                 rate=RATE,
#                 # input=True,
#                 output=True,
#                 frames_per_buffer=CHUNK)

# stream = p.open(format =
#                 p.get_format_from_width(wf.getsampwidth()),
#                 channels = wf.getnchannels(),
#                 rate = wf.getframerate(),
#                 output = True)


with tf.Session() as sess:
    inputs, model = get_default_model()
    model.load(model_name)

    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)

    while True:
        stream.readframes = stream.read
        try:
            word = read_next_word(stream)
            word = np.resize(word, default_size)
            # word = np.reshape(word, (1,default_size))
            logging.debug("writing word out")
            stream.write(word)
            # q = model.predict([word])
            # print q
        except Exception as inst:
            logging.debug(inst)
            break

    stream.stop_stream()
    stream.close()

    p.terminate()