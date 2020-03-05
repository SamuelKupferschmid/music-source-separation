import os

import pandas as pd
import tensorflow as tf
import tensorflow_io as tfio


def load_al_trainingset(filename, data_root):
    df = load_csv(filename)
    df = df[['song', 'track', 'duration', 'voc_oracle',
             'instr_oracle', 'other_oracle']].dropna()

    data_root = data_root + os.path.sep + 'multitracks' + os.path.sep

    dataset = tf.data.Dataset.from_tensor_slices((tf.cast(df['song'].values, tf.string),
                                                  tf.cast(df['track'].values, tf.string),
                                                  tf.cast(df['duration'].values, tf.int64),
                                                  tf.cast(df['voc_oracle'].values, tf.int32),
                                                  tf.cast(df['instr_oracle'].values, tf.int32),
                                                  tf.cast(df['other_oracle'].values, tf.int32)))
    return dataset.map(lambda song, track, duration, voc, instr, other: (
        create_features(data_root + song + os.path.sep + track, duration, 1),
        create_label([voc, instr, other], duration, 1))
        ).unbatch().filter(lambda x,y: has_signal(x)).batch(4)

def load_csv(filename):
    data = pd.read_csv(filename, sep='\t')
    return data

def load_sample(song, track, data_root, duration, chunk_size=1):
    filename = os.path.join(data_root, 'multitracks', song, track)
    dataset = tf.data.Dataset.from_tensors((filename, duration, tf.constant(chunk_size)))
    return dataset.map(lambda file, dur, c: create_features(file, dur, c)).unbatch().filter(has_signal).batch(16)

@tf.function
def has_signal(timestep):
    return tf.math.reduce_max(tf.abs(timestep)) > 0.05

@tf.function
def create_features(ogg_filename, duration, chunk_size):
    wav = tfio.IOTensor.graph(tf.int16).from_audio(ogg_filename)
    duration = tf.cast(duration, tf.int64)
    wav = wav[0:duration*44100]  # loads whole wav data
    wav = tf.cast(wav, tf.float32) / 32767
    mono = tf.math.reduce_mean(wav, axis=1)  # make mono

    # spectrogram (100 steps/sec with 1025 channels)
    fft = tf.signal.stft(mono, 2048, 441, pad_end=True)
    fft = tf.abs(fft)
    spec = fft * fft

    # split into timesteps (10ms * chunk_size)
    spec = tf.reshape(spec, [-1, 100 * chunk_size, 1025])
    return spec


@tf.function
def create_label(y, duration, chunk_size):
    #y=tf.one_hot(tf.strings.to_number(y, tf.int32), 3)
    y = tf.reshape(y, [-1, 3])
    return tf.repeat(y, int(duration / chunk_size), 0)
