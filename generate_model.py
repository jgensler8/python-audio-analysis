from util import *
import tensorflow as tf

with tf.Session() as sess:

    inputs, model = get_default_model()

    X = []
    Y = []

    sess.run(tf.global_variables_initializer())
    for filename in os.listdir("audio/words"):
        if filename.endswith(".wav"):
            wf = wave.open(os.path.join("audio", "words", filename))
            # stream = p.open(format =
            #                 p.get_format_from_width(wf.getsampwidth()),
            #                 channels = wf.getnchannels(),
            #                 rate = wf.getframerate(),
            #                 output = True)
            # print(os.path.join(directory, filename))
            data = wf.readframes(CHUNK)
            np_arr = np.fromstring(data, dtype=np.int16)
            # print np_arr.shape
            np_arr = np.resize(np_arr, default_size)
            print np_arr.shape
            analyzed = np.polyfit(range(len(np_arr)), np_arr, deg=DEGREE)
            print analyzed.shape
            X.append(np_arr)
            Y.append(analyzed)
            wf.close()

    print len(X)
    print len(Y)

    print len(X[0])
    print len(Y[0])

    print X[0]
    print Y[0]

    q = model.fit(X, Y)
    model.save(model_name)