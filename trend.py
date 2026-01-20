def compute_trend(previous, current):
    diff = current - previous

    if diff >= 10:
        trend = "WORSENING"
    elif diff <= -10:
        trend = "IMPROVING"
    else:
        trend = "STABLE"

    return {
        "previous": previous,
        "current": current,
        "trend": trend,
        "change": diff
    }
