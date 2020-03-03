import sys
import os
#from model import create_model
from data import load_dataset

dataset = load_dataset(os.path.join('data','multitracks.txt'))

print(dataset)