from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import os
import uuid

from utils.pdf_report import generate_pdf
from utils.voice_report import generate_voice_report

app = Flask(__name__)
CORS(app)

# ---------------- LOAD MODELS ----------------
text_model = tf.keras.models.load_model("text_model/text_model.h5")
xray_model = tf.keras.models.load_model("xray_model/xray_model.h5")
ecg_model = tf.keras.models.load_model("ecg_model/ecg_model.h5")

# ---------------- CACHE ----------------
patient_cache = {}
previous_severity = {}

# ---------------- HELPERS ----------------
def symptom_score(text):
    keywords = {
        "chest pain": 30,
        "breathlessness": 30,
        "sweating": 20,
        "fever": 15,
        "cough": 10,
        "stomach pain": 5,
        "nausea": 5
    }
    score = 0
    for k, v in keywords.items():
        if k in text.lower():
            score += v
    return score

def classify_risk(score):
    if score >= 80: return "CRITICAL"
    if score >= 60: return "HIGH"
    if score >= 40: return "MODERATE"
    return "LOW"

# ---------------- PREDICT ----------------
@app.route("/predict", methods=["POST"])
def predict():
    pid = str(uuid.uuid4())[:8]
    symptoms = request.form.get("symptoms", "")

    severity = symptom_score(symptoms)

    reasons = []
    if "chest pain" in symptoms.lower():
        reasons.append("Chest pain detected")
    if "breathlessness" in symptoms.lower():
        reasons.append("Breathing difficulty detected")

    # X-RAY (OPTIONAL)
    if "xray" in request.files:
        img = tf.keras.preprocessing.image.load_img(
            request.files["xray"], target_size=(224, 224), color_mode="grayscale"
        )
        arr = tf.keras.preprocessing.image.img_to_array(img) / 255.0
        arr = np.expand_dims(arr, axis=0)
        xray_conf = float(xray_model.predict(arr)[0][0])
        if xray_conf > 0.6:
            severity += 20
            reasons.append("X-ray indicates lung abnormality")

    # ECG (OPTIONAL)
    if "ecg" in request.files:
        data = np.loadtxt(request.files["ecg"])
        data = np.expand_dims(data, axis=0)
        ecg_conf = float(ecg_model.predict(data)[0][0])
        if ecg_conf > 0.6:
            severity += 20
            reasons.append("ECG indicates cardiac abnormality")

    severity = min(severity, 100)
    risk = classify_risk(severity)

    # TREND
    prev = previous_severity.get(pid, severity)
    trend = "WORSENING" if severity > prev + 5 else "IMPROVING" if severity < prev - 5 else "STABLE"
    previous_severity[pid] = severity

    trend_data = {"previous": prev, "current": severity, "trend": trend}

    disease = [{
        "condition": "Possible cardiopulmonary stress",
        "reason": "Combined symptom and signal analysis"
    }]

    # SAVE CACHE (FOR VOICE)
    patient_cache[pid] = {
        "severity": severity,
        "risk": risk,
        "reasons": reasons,
        "trend": trend_data,
        "disease": disease
    }

    # PDF ONLY (NO VOICE HERE)
    pdf_path = generate_pdf(pid, patient_cache[pid])
    pdf_name = os.path.basename(pdf_path)

    return jsonify({
        "patient_id": pid,
        "severity": severity,
        "risk": risk,
        "reasoning": reasons,
        "trend": trend_data,
        "pdf_url": f"http://127.0.0.1:5000/download/{pdf_name}"
    })

# ---------------- ON-DEMAND VOICE ----------------
@app.route("/generate-voice/<pid>", methods=["POST"])
def generate_voice(pid):
    if pid not in patient_cache:
        return jsonify({"error": "No report found"}), 404

    voice_path = generate_voice_report(pid, patient_cache[pid])
    voice_name = os.path.basename(voice_path)

    return jsonify({
        "voice_url": f"http://127.0.0.1:5000/download/{voice_name}"
    })

# ---------------- DOWNLOAD ----------------
@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(os.path.abspath("reports"), filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

