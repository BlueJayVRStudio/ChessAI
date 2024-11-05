import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    layers.InputLayer(input_shape=(19,)),  # Input layer with 19 integer inputs
    layers.Dense(100, activation='relu'),   # First hidden layer with 20 nodes
    layers.Dense(100, activation='relu'),   # Second hidden layer with 20 nodes
    layers.Dense(100, activation='relu'),   # Third hidden layer with 20 nodes
    layers.Dense(1, activation='tanh')
])

model.save('./models/model_base.keras')