# AETRIS – AI Emergency Triage System

AETRIS is a web-based emergency triage support system that helps doctors and healthcare staff quickly understand a patient’s condition using symptoms and optional diagnostic inputs such as ECG data and X-ray images.

The system focuses on fast severity assessment, risk identification, and tracking how a patient’s condition changes over time.

---

## Problem

In emergency situations, doctors often have very limited time to decide how serious a patient’s condition is.  
Triage is usually done manually and depends heavily on experience and judgment.

Common issues include:
- Delay in decision making under pressure
- Symptoms, ECG, and X-ray data reviewed separately
- No simple way to track whether a patient is improving or worsening
- Limited explainability in automated tools

These challenges are more severe in emergency rooms, ambulances, and rural healthcare centers.

---

## Solution

AETRIS brings symptoms, optional ECG input, and optional X-ray input into a single dashboard.

The system:
- Calculates a severity score
- Assigns a risk level (Low, Moderate, High, Critical)
- Explains why the result was given
- Tracks patient condition across multiple analyses
- Provides voice-based explanations
- Generates downloadable medical reports

---

## Features

- Symptom-based emergency severity analysis  
- Optional ECG file upload with waveform visualization  
- Optional X-ray image upload with preview  
- Risk classification and clear reasoning  
- Trend analysis comparing previous and current patient states  
- Voice explanation for hands-free and quick understanding  
- Downloadable text-based medical report  
- Clean login and dashboard interface for demo use  

---

## Technology Used

- Frontend: HTML, CSS, JavaScript  
- Backend: Python, Flask  
- Visualization: HTML Canvas for ECG, image preview for X-ray  
- Voice: Web Speech API (Text-to-Speech)

---

## How to Run

1. Navigate to the backend folder

2. Install required package

3. Run the application

4. Open the application in browser

---

## Sample Inputs

Critical case:

Improving case:

---

## Use Case and Impact

AETRIS can be used as a decision-support tool in:
- Emergency rooms
- Ambulances
- Rural clinics
- First-response healthcare setups

It helps reduce response time, supports better decisions, and provides clear explanations instead of black-box results.

---

## Future Scope

- Deep learning models for ECG and X-ray interpretation
- User roles for doctors, nurses, and administrators
- Integration with hospital record systems
- Cloud deployment for wider access

---

## Summary

AETRIS is designed to assist healthcare professionals during emergencies by providing fast, explainable, and trend-aware triage decisions.  
The goal is not to replace doctors, but to support them when time matters the most.
