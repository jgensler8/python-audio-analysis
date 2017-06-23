import numpy as np
import wave
import os
import tflearn
import logging

CHUNK = 1024
MAX_CHUNKS = 5
WIDTH = 2
# CHANNELS = 2
CHANNELS = 1
RATE = 44100
DEGREE = 2
TERMS = DEGREE + 1


model_name = "model.tflearn"
logging.basicConfig(level=logging.DEBUG)


def read_next_word(file_from, chunk=CHUNK, consecutive_for_pause=2):
    word = []
    consecutive_counter = 0
    frames = [""]
    speaking = False
    while len(frames) > 0:
        frames = file_from.readframes(chunk)
        np_arr = np.fromstring(frames, dtype=np.int16)
        mean = np.abs(np.round(np.mean(np_arr)))
        std = np.round(np.std(np_arr))
        logging.debug("{:5} {:7} {}".format(mean, std, speaking))
        if mean > 5 and std > 1000:
            # start speaking or continue speaking
            speaking = True
            word.append(np_arr)
            consecutive_counter = 0
        else:
            if speaking is True:
                # might have stopped speaking
                if consecutive_counter >= consecutive_for_pause:
                    break
                # brief pause, but still speaking
                consecutive_counter += 1
                word.append(np_arr)
    if len(frames) is 0:
        return None
    return np.concatenate(word)


def save_word(word, word_counter, channels=CHANNELS):
    if len(word) > 0:
        wavio.write("audio/words/{}.wav".format(word_counter), word, RATE/2, sampwidth=channels)
        logging.debug("Saving word of length {:3} frame".format(len(word)))
        return True
    else:
        return False


def get_model(num_input, terms):
    inputs = tflearn.input_data(shape=[None, num_input], name="Inputs")
    net = tflearn.fully_connected(inputs, num_input/2, activation='relu', name="fc1")
    net = tflearn.fully_connected(net, terms, activation='relu', name="fc2")
    net = tflearn.regression(net, optimizer='sgd', loss='categorical_crossentropy')
    model = tflearn.DNN(net)
    return inputs, model


default_size = CHUNK*MAX_CHUNKS


def get_default_model():
    return get_model(default_size, TERMS)
