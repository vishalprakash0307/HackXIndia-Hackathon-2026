from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)
CORS(app)

# Load trained model
model = tf.keras.models.load_model("dl_model.h5")
tokenizer = pickle.load(open("tokenizer.pkl", "rb"))
label_encoder = pickle.load(open("label_encoder.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    text = data.get("symptoms", "")

    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=10)

    prediction = model.predict(padded)
    label = label_encoder.inverse_transform([prediction.argmax()])[0]

    emergency = label == "Heart Issue"

    return jsonify({
        "prediction": label,
        "emergency": emergency,
        "message": (
            "🚨 Emergency detected! Seek medical help immediately."
            if emergency else
            f"Predicted condition: {label}. Please consult a doctor."
        )
    })

if __name__ == "__main__":
    app.run(debug=True)
