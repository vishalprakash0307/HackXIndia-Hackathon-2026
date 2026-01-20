import pandas as pd
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Bidirectional, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder

# Load dataset
data = pd.read_csv("data.csv")

# Encode labels
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(data["label"])
labels = to_categorical(labels)

# Tokenization (FROM SCRATCH)
tokenizer = Tokenizer(num_words=5000, oov_token="<OOV>")
tokenizer.fit_on_texts(data["symptoms"])

sequences = tokenizer.texts_to_sequences(data["symptoms"])
padded = pad_sequences(sequences, maxlen=10)

# Deep Learning Model (NO PRETRAINED WEIGHTS)
model = Sequential([
    Embedding(input_dim=5000, output_dim=64, input_length=10),
    Bidirectional(LSTM(64)),
    Dense(64, activation="relu"),
    Dense(labels.shape[1], activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Train model
model.fit(padded, labels, epochs=30, verbose=1)

# Save model and tools
model.save("dl_model.h5")
pickle.dump(tokenizer, open("tokenizer.pkl", "wb"))
pickle.dump(label_encoder, open("label_encoder.pkl", "wb"))

print("✅ Deep Learning Model Trained From Scratch")
