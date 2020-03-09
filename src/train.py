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


import wandb
from wandb.keras import WandbCallback
wandb.init(project="multitrack", tags=['voc_instr_separation','AL'])
#config={"epochs": 10, "iteration":1}
config = wandb.config
config.epochs = 8
config.iteration = 1

model = create_model()

dataset = load_al_trainingset(dataset_file , data_root)
validation = dataset.take(200)
train = dataset.skip(200)
class_weight = get_class_weights(dataset_file)

#print('run training...')
modelpath = os.path.join(f'models/al/{config.iteration}.h5')
model.fit(train, validation_data=validation, class_weight=class_weight, epochs=config.epochs,callbacks=[WandbCallback()])
model.save(modelpath)
model.save(os.path.join(wandb.run.dir, "model.h5"))