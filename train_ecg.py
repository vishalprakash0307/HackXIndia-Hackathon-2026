import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense

model = Sequential([
    Conv1D(16, 3, activation="relu", input_shape=(500,1)),
    MaxPooling1D(),
    Conv1D(32, 3, activation="relu"),
    MaxPooling1D(),
    Flatten(),
    Dense(64, activation="relu"),
    Dense(1, activation="sigmoid")
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
model.save("ecg_model.h5")
