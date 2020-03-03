import sys
import os
#from model import create_model
from data import load_al_trainingset

dataset = load_al_trainingset(os.path.join('data','multitracks_al.txt'))
print(dataset)