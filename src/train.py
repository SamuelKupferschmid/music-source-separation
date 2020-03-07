import sys
import os
import numpy as np
import pandas as pd
from model import create_model
from data import load_al_trainingset, load_sample, load_csv

# enable memory growth on demand
import tensorflow as tf
gpus = tf.config.experimental.list_physical_devices('GPU')
print(gpus)
if len(gpus) >0: tf.config.experimental.set_memory_growth(gpus[0], True)

dataset_file = os.path.join('data','multitracks_al.txt')
data_root = 'data'

import wandb
from wandb.keras import WandbCallback
wandb.init(project="multitrack", tags=['voc_instr_separation','AL'])
#config={"epochs": 10, "iteration":1}
config = wandb.config
config.epochs = 10
config.iteration = 1
dataset = load_al_trainingset(dataset_file , data_root)
model = create_model()

#print('run training...')
modelpath = os.path.join(f'models/al/{config.iteration}.h5')
model.fit(dataset, epochs=config.epochs,callbacks=[WandbCallback()])
model.save(modelpath)
#model = tf.keras.models.load_model(modelpath)
print('run inference...')
df = load_csv(dataset_file)
for index, row in df.iterrows():
    try:
        sample = load_sample(row['song'],row['track'], data_root, row['duration'])
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