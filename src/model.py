import tensorflow
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import GRU, Bidirectional, Dense, LSTM, Conv1D, Flatten, BatchNormalization, Dropout

def create_model():
    model = Sequential()
    model.add(Conv1D(20, kernel_size=6, padding='valid', input_shape=(None, 1025)))
    model.add(Conv1D(8, kernel_size=6, padding='valid'))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))
    model.add(GRU(16, return_sequences=True))
    model.add(BatchNormalization())
    model.add(Dropout(0.1))
    model.add(GRU(12, return_sequences=False))
    model.add(BatchNormalization())
    model.add(Dense(3, activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                optimizer='adam', metrics=['accuracy','binary_accuracy'])
    model.summary()
    return model