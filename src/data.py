import os

import pandas as pd
import tensorflow as tf
import tensorflow_io as tfio

def load_al_trainingset(filename):
    df = load_csv(filename)
    df = df[['song','track','duration','voc_oracle', 'instr_oracle', 'other_oracle']].dropna()
    
    tf.data.Dataset.from_tensor_slices((tf.cast(training['track'].values, tf.string),tf.cast(training['duration'].values, tf.int64), tf.cast(training['ground_truth'].values, tf.string)))


def load_csv(filename):
    data = pd.read_csv(filename, sep='\t')
    return data

@tf.function
def get_features(ogg_filename, duration, chunk_size):
    
    filename = '..' + os.sep + 'data' + os.sep + ogg_filename
    wav = tfio.IOTensor.graph(tf.int16).from_audio(filename)
    wav = wav[0:duration*44100]
    wav = tf.cast(wav, tf.float32) / 32767
    mono = tf.math.reduce_mean(wav,axis=1)
    #mono = tf.reshape(mono, [441000,-1])
    fft = tf.signal.stft(mono, 2048, 441, pad_end=True)
    fft = tf.abs(fft)
    spec = fft * fft
    spec = tf.reshape(spec, [-1,100 * chunk_size,1025])
    return spec

#training = data[data['ground_truth'] != '?']

@tf.function
def create_label(y, duration, chunk_size):
    y = tf.one_hot(tf.strings.to_number(y, tf.int32),3)
    y = tf.reshape(y, [-1, 3])
    return tf.repeat(y, int(duration / chunk_size),0)

#dataset = tf.data.Dataset.from_tensor_slices((tf.cast(training['track'].values, tf.string),tf.cast(training['duration'].values, tf.int64), tf.cast(training['ground_truth'].values, tf.string)))
#dataset = dataset.map(lambda track, duration ,y: (get_features(track, duration, 1),create_label(y, duration, 1))).filter(lambda x, y: tf.math.count_nonzero(x) > 100).unbatch()


    
@tf.function
def create_pandas_dataset(data, ignore_labels, chunk_size):
    dataset = tf.data.Dataset.from_tensor_slices((tf.cast(data['track'].values, tf.string),tf.cast(data['duration'].values, tf.int64), tf.cast(data['ground_truth'].values, tf.string)))
    if ignore_labels:
        return dataset.map(lambda track, duration ,y: get_features(track, duration, duration)).unbatch()
    else:
        return dataset.map(lambda track, duration ,y: (get_features(track, duration, chunk_size),create_label(y, duration, chunk_size))).unbatch()
    return dataset