import sys
import os
import numpy as np
from model import create_model
from data import load_al_trainingset, load_sample, load_csv



dataset_file = os.path.join('data','multitracks_al.txt')
data_root = 'data'
iteration = 0


dataset = load_al_trainingset(dataset_file , data_root)
model = create_model()

print('run training...')
model.fit(dataset, epochs=10)
model.save(os.path.join(f'models/al/{iteration}.h5'))

print('run inference...')
df = load_csv(dataset_file)
for index, row in df.iterrows():
    sample = load_sample(row['song'],row['track'], data_root, row['duration'])
    result = np.mean(model.predict(sample),axis=0)

    df.at[index, 'voc_estimated'] = result[0]
    df.at[index, 'instr_estimated'] = result[1]
    df.at[index, 'other_estimated'] = result[2]

df.to_csv(dataset_file, sep='\t')