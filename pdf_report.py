from reportlab.pdfgen import canvas

def generate_pdf(pid, data):
    file = f"{pid}_report.pdf"
    c = canvas.Canvas(file)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, 800, "AETRIS – AI Emergency Triage Report")

    c.setFont("Helvetica", 12)
    c.drawString(40, 760, f"Patient ID: {pid}")
    c.drawString(40, 730, f"Severity Score: {data['severity']}")
    c.drawString(40, 700, f"Risk Level: {data['risk']}")

    c.drawString(40, 660, "Technical Reasoning:")
    y = 630
    for r in data["reasons"]:
        c.drawString(60, y, "- " + r)
        y -= 20

    c.drawString(40, y-20, "Clinical Interpretation (AI-assisted):")
    y -= 50
    for d in data["disease"]:
        c.drawString(60, y, f"- {d['condition']} ({d['confidence']})")
        y -= 20
        c.drawString(80, y, d["reason"])
        y -= 30

    c.drawString(
        40, y-20,
        f"Trend: {data['trend']['trend']} (Change: {data['trend']['change']})"
    )

    c.save()
    return file
