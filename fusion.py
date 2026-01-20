def fuse(text, xray, ecg):
    score = 0
    weight = 0

    score += text * 40
    weight += 40

    if xray > 0:
        score += xray * 30
        weight += 30

    if ecg > 0:
        score += ecg * 30
        weight += 30

    final = int((score / weight) * 100)

    if final >= 80:
        return final, "CRITICAL"
    elif final >= 45:
        return final, "MODERATE"
    else:
        return final, "LOW"
