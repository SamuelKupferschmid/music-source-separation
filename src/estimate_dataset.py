import sys
import os
import numpy as np
import pandas as pd
from model import create_model
from data import load_al_trainingset, load_sample, load_csv, get_class_weights

# enable memory growth on demand
import tensorflow as tf
gpus = tf.config.experimental.list_physical_devices('GPU')
print(gpus)
if len(gpus) >0: tf.config.experimental.set_memory_growth(gpus[0], True)

dataset_file = os.path.join('data','multitracks_al.txt')
data_root = 'data'

modelpath = os.path.join(f'models/al/{1}.h5')

model = tf.keras.models.load_model(modelpath)
df = load_csv(dataset_file)
for index, row in df.iterrows():
    try:
        sample = load_sample(row['song'],row['track'], data_root, min(16, row['duration']))
        result = np.mean(model.predict(sample),axis=0)

        df.at[index, 'voc_estimated'] = result[0]
        df.at[index, 'instr_estimated'] = result[1]
        df.at[index, 'other_estimated'] = result[2]
    except:
        print("Unexpected error:", sys.exc_info()[0])
        pass
    if index % 10 == 0: 
        df.to_csv(dataset_file, sep='\t', index=False)

df.to_csv(dataset_file, sep='\t', index=False)