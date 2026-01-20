def explain_condition(text_risk, xray_risk, ecg_risk, symptoms):
    explanations = []
    s = symptoms.lower()

    if ecg_risk > 0.6 and any(k in s for k in ["chest", "breath", "sweating"]):
        explanations.append({
            "condition": "Possible cardiac stress",
            "reason": "ECG abnormalities combined with chest-related symptoms may indicate cardiac strain",
            "confidence": "HIGH"
        })

    if xray_risk > 0.6 and any(k in s for k in ["cough", "fever", "breath"]):
        explanations.append({
            "condition": "Possible respiratory infection",
            "reason": "X-ray abnormalities with respiratory symptoms may indicate lung involvement",
            "confidence": "MODERATE"
        })

    if text_risk > 0.6 and any(k in s for k in ["fever", "fatigue", "pain"]):
        explanations.append({
            "condition": "Possible systemic infection or inflammation",
            "reason": "Symptom patterns show elevated inflammatory indicators",
            "confidence": "MODERATE"
        })

    if not explanations:
        explanations.append({
            "condition": "No dominant disease pattern detected",
            "reason": "Inputs do not strongly match known high-risk patterns",
            "confidence": "LOW"
        })

    return explanations
