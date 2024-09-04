import chess
import pandas as pd

import time
import os

# This guide can only be run with the TensorFlow backend.
os.environ["KERAS_BACKEND"] = "tensorflow"
TF_ENABLE_ONEDNN_OPTS = 0

import tensorflow as tf
import keras
import numpy as np
from dataoperate import *


def get_model():
    inputs = keras.Input(shape=(768,), dtype=np.int8)
    x = keras.layers.Dense(512, activation="relu")(inputs)
    x = tf.keras.layers.Dropout(.25, input_shape=(768,))(x)
    x = keras.layers.Dense(512, activation="relu")(x)
    x = tf.keras.layers.Dropout(.25, input_shape=(768,))(x)
    x = keras.layers.Dense(512, activation="relu")(x)
    outputs = keras.layers.Dense(1, activation="sigmoid")(x)
    model = keras.Model(inputs=inputs, outputs=outputs)
    return model


model = get_model()

dataset = Dataset(10).values()

optimizer = keras.optimizers.Adam(learning_rate=1e-3)
loss_fn = keras.losses.MeanAbsoluteError()
batch_size = 32

p = []
q = []
r = []
for x in dataset:
    p.append(list(x[0]))
    q.append(list(x[1]))
    r.append(list(x[2]))

epochs = 20

for epoch in range(epochs):
    print(f"\nStart of epoch {epoch}")

    # Iterate over the batches of the dataset.
    for step, p_batch_train in enumerate(p):
        p_batch_train = np.array([p[step], ])
        q_batch_train = np.array([q[step], ])
        r_batch_train = np.array([r[step], ])
        yq_batch_train = model(q_batch_train, training=True)
        yr_batch_train = model(r_batch_train, training=True)

        if np.abs(yq_batch_train) < np.abs(yr_batch_train):

            with tf.GradientTape() as tape:
                # Run the forward pass of the layer.
                # The operations that the layer applies
                # to its inputs are going to be recorded
                # on the GradientTape.
                # Compute the loss value for this minibatch.
                logits = model(q_batch_train, training=True)
                loss_value = loss_fn(yr_batch_train, logits)

            # Use the gradient tape to automatically retrieve
            # the gradients of the trainable variables with respect to the loss.
            grads = tape.gradient(loss_value, model.trainable_weights)

            # Run one step of gradient descent by updating
            # the value of the variables to minimize the loss.
            optimizer.apply(grads, model.trainable_weights)

        yq_batch_train = model(q_batch_train, training=True)*(-1)

        with tf.GradientTape() as tape:
            # Run the forward pass of the layer.
            # The operations that the layer applies
            # to its inputs are going to be recorded
            # on the GradientTape.
            logits = model(p_batch_train, training=True)  # Logits for this minibatch

            # Compute the loss value for this minibatch.
            loss_value = loss_fn(yq_batch_train, logits)

        # Use the gradient tape to automatically retrieve
        # the gradients of the trainable variables with respect to the loss.
        grads = tape.gradient(loss_value, model.trainable_weights)

        # Run one step of gradient descent by updating
        # the value of the variables to minimize the loss.
        optimizer.apply(grads, model.trainable_weights)

        # Log every 100 batches.
        if step % 100 == 0:
            print(
                f"Training loss (for 1 batch) at step {step}: {float(loss_value):.4f}"
            )
            print(f"Seen so far: {(step + 1) * batch_size} samples")

model.save("model.keras")
