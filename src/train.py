import sys
import os
from model import create_model
from data import load_al_trainingset

dataset = load_al_trainingset(os.path.join('data','multitracks_al.txt'), 'data')
model = create_model()

model.fit(dataset, epochs=10)
print(dataset)