def predict_heart_disease(
    age,
    cholesterol,
    blood_pressure
):
    score = 0

    if age > 50:
        score += 1

    if cholesterol > 220:
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