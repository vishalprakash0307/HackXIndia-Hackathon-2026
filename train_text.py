import pandas as pd
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Bidirectional, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv("data.csv")

le = LabelEncoder()
y = to_categorical(le.fit_transform(data["label"]))

tokenizer = Tokenizer(num_words=5000, oov_token="<OOV>")
tokenizer.fit_on_texts(data["symptoms"])
X = pad_sequences(tokenizer.texts_to_sequences(data["symptoms"]), maxlen=10)

model = Sequential([
    Embedding(5000, 64, input_length=10),
    Bidirectional(LSTM(64)),
    Dense(64, activation="relu"),
    Dense(y.shape[1], activation="softmax")
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.fit(X, y, epochs=30)

model.save("text_model.h5")
pickle.dump(tokenizer, open("tokenizer.pkl","wb"))
pickle.dump(le, open("label_encoder.pkl","wb"))
