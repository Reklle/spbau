import tensorflow as tf
from tensorflow import keras

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

import testdata
import tools


class Generator():
    def __init__(self):
        self.model = Sequential([
            Dense(12, activation='relu', input_shape=(12,)),
            Dense(24, activation='relu'),
            Dense(16, activation='relu'),
            Dense(2, activation='softmax'),
        ])
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    def fit(self, epochs=300):
        # let's learn some good words
        data = testdata.data
        keys = testdata.keys
        self.model.fit(data, to_categorical(keys), epochs=epochs, batch_size=32)
        self.model.save_weights('model.h5')

    def reviewer(self, word):
        # is word good or bad one?
        self.model.load_weights('model.h5')
        return self.model.predict([tools.word_levels(word)])