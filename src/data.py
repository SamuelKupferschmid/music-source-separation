import os

import pandas as pd
import tensorflow as tf
import tensorflow_io as tfio


def load_al_trainingset(filename, data_root):
    df = load_csv(filename)
    df = df[['song', 'track', 'duration', 'voc_oracle',
        'instr_oracle', 'other_oracle']].dropna()

    dataset = tf.data.Dataset.from_tensor_slices((tf.cast(df['song'].values, tf.string), tf.cast(df['track'].values, tf.string), tf.cast(df['duration'].values, tf.int64), tf.cast(df['voc_oracle'].values, tf.int32), tf.cast(df['instr_oracle'].values, tf.int32), tf.cast(df['other_oracle'].values, tf.int32)))
    return dataset.map(lambda song, track, duration, voc, instr, other: (create_features(song + os.path.sep + track, duration, 1), create_label([voc, instr, other], duration, 1)))
def load_csv(filename):
    data=pd.read_csv(filename, sep='\t')
    return data

@tf.function
def create_features(ogg_filename, duration, chunk_size):

    filename= 'data' + os.path.sep + 'multitracks' + os.path.sep + ogg_filename
    wav=tfio.IOTensor.graph(tf.int16).from_audio(filename)
    wav=wav[0:duration*44100] # loads whole wav data
    wav=tf.cast(wav, tf.float32) / 32767
    mono=tf.math.reduce_mean(wav, axis=1) # make mono
    
    # spectrogram (100 steps/sec with 1025 channels)
    fft=tf.signal.stft(mono, 2048, 441, pad_end=True)
    fft=tf.abs(fft)
    spec=fft * fft
    spec=tf.reshape(spec, [-1, 100 * chunk_size, 1025])
    return spec

@tf.function
def create_label(y, duration, chunk_size):
    #y=tf.one_hot(tf.strings.to_number(y, tf.int32), 3)
    y=tf.reshape(y, [-1, 3])
    return tf.repeat(y, int(duration / chunk_size), 0)

@tf.function
def create_pandas_dataset(data, ignore_labels, chunk_size):
    dataset=tf.data.Dataset.from_tensor_slices((tf.cast(data['track'].values, tf.string), tf.cast(
        data['duration'].values, tf.int64), tf.cast(data['ground_truth'].values, tf.string)))
    if ignore_labels:
        return dataset.map(lambda track, duration, y: get_features(track, duration, duration)).unbatch()
    else:
        return dataset.map(lambda track, duration, y: (get_features(track, duration, chunk_size), create_label(y, duration, chunk_size))).unbatch()
    return dataset
