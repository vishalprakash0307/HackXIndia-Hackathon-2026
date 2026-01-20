import os
from gtts import gTTS

def generate_voice_report(pid, data):
    """
    Generates an MP3 voice explanation for the report
    """

    os.makedirs("reports", exist_ok=True)

    text = f"""
    Patient ID {pid}.

    The predicted severity score is {data['severity']}.

    Risk level is {data['risk']}.

    Reasoning behind this prediction is as follows.
    """

    for r in data["reasons"]:
        text += r + ". "

    text += "Trend analysis indicates that the condition is "
    text += data["trend"]["trend"] + ". "

    text += "Clinical interpretation suggests the following. "

    for d in data["disease"]:
        text += d["condition"] + ". "
        text += d["reason"] + ". "

    file_path = os.path.join("reports", f"{pid}_explanation.mp3")

    tts = gTTS(text=text, lang="en")
    tts.save(file_path)

    return file_path
