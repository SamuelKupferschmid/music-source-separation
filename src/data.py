import pandas as pd

def load_dataset(filename):
    
    #3columns=['track','duration','voc_predicted','instr_predicted','other_predicted','ground_truth']
    data = pd.read_csv(filename, sep='\t')
    #data['ground_truth'].hist()
    return data