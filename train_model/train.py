import chess
import numpy as np
import tensorflow as tf
import keras
from dataoperate import Dataset
import os


TF_ENABLE_ONEDNN_OPTS = 0


data = Dataset(10).items()


for i, m in data:
    x_train = []
    y_train = []
    for x in m.values():
        x_train.append(x[0])
        y_train.append(1 if x[3] > 0.5 else 0)

    x_train = np.array(x_train)
    y_train = np.array(y_train)

    print(y_train)

    model_1 = keras.Sequential()
    model_1.add(keras.Input(shape=(768,)))
    model_1.add(keras.layers.Dense(512, activation='relu',))
    model_1.add(keras.layers.Dense(1, activation='sigmoid'))

    myAdam = keras.optimizers.Adam(learning_rate=0.0001)
    model_1.compile(optimizer=myAdam,
                 loss='binary_crossentropy',
                 metrics=['accuracy'])

    Epochs = 100
    history_1 = model_1.fit(x_train, y_train, batch_size=32, epochs=Epochs, validation_split=0.2)

    model_1.save("models/model"+str(i)+".keras")


