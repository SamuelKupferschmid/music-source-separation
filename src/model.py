import tensorflow
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Bidirectional, Dense, LSTM, Conv1D, Flatten

def create_model():
    model = Sequential()
    model.add(Conv1D(8, kernel_size=6, padding='same', input_shape=(None, 1025)))
    model.add(GRU(8, return_sequences=False))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                optimizer='RMSProp', metrics=['accuracy'])
    model.summary()
    return model
