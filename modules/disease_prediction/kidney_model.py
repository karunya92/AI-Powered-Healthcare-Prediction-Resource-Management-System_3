def predict_kidney_disease(
    creatinine,
    age,
    blood_pressure
):
    score = 0

    if creatinine > 1.5:
        score += 1

    if age > 60:
        score += 1

    if blood_pressure > 140:
        score += 1

    probability = round(score / 3, 2)

    if probability >= 0.67:
        result = "High Risk"
    elif probability >= 0.34:
        result = "Moderate Risk"
    else:
        result = "Low Risk"

    return result, probability