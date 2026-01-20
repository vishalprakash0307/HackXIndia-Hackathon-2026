from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

PATIENT_HISTORY = {}

# ---------------- LOGIN ----------------
@app.route("/")
def login_page():
    return send_from_directory("static", "login.html")

@app.route("/login", methods=["POST"])
def login():
    # simple hackathon login (no auth)
    return redirect("/dashboard")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    return send_from_directory("static", "dashboard.html")

# ---------------- ANALYSIS ----------------
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        patient_id = request.form.get("patient_id")
        symptoms = request.form.get("symptoms", "").lower()

        if not patient_id or not symptoms:
            return jsonify({"error": "Patient ID and symptoms required"}), 400

        severity = 0
        reasons = []

        if "chest" in symptoms:
            severity += 40
            reasons.append("Chest related symptom")
        if "breath" in symptoms:
            severity += 30
            reasons.append("Breathing issue")
        if "fever" in symptoms:
            severity += 20
            reasons.append("Fever present")
        if "pain" in symptoms:
            severity += 10
            reasons.append("Pain reported")

        if "ecg" in request.files and request.files["ecg"].filename:
            severity += 10
            reasons.append("ECG file submitted")

        if "xray" in request.files and request.files["xray"].filename:
            severity += 10
            reasons.append("X-ray image submitted")

        severity = min(severity, 100)

        previous = PATIENT_HISTORY.get(patient_id)
        trend = "NEW"
        comparison = "No previous data"

        if previous is not None:
            if severity > previous:
                trend = "WORSENING"
                comparison = f"Increased from {previous} to {severity}"
            elif severity < previous:
                trend = "IMPROVING"
                comparison = f"Reduced from {previous} to {severity}"
            else:
                trend = "STABLE"
                comparison = "No change"

        PATIENT_HISTORY[patient_id] = severity

        risk = "HIGH" if severity >= 70 else "MODERATE" if severity >= 40 else "LOW"

        filename = f"{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = os.path.join(REPORT_DIR, filename)

        with open(path, "w") as f:
            f.write(f"Patient ID: {patient_id}\n")
            f.write(f"Previous: {previous}\n")
            f.write(f"Current: {severity}\n")
            f.write(f"Risk: {risk}\n")
            f.write(f"Trend: {trend}\n")
            f.write(f"Comparison: {comparison}\n")
            f.write("Reasons:\n")
            for r in reasons:
                f.write(f"- {r}\n")

        return jsonify({
            "previous": previous,
            "current": severity,
            "risk": risk,
            "trend": trend,
            "comparison": comparison,
            "reasons": reasons,
            "download": f"/report/{filename}"
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500

# ---------------- REPORT ----------------
@app.route("/report/<name>")
def report(name):
    return send_from_directory(REPORT_DIR, name, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
