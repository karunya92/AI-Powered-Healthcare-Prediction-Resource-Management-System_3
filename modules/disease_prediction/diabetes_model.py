def predict_diabetes(
    glucose,
    bmi,
    age
):
    score = 0

    if glucose > 140:
        score += 1

    if bmi > 30:
        score += 1

    if age > 45:
        score += 1

    probability = round(score / 3, 2)

    if probability >= 0.67:
        result = "High Risk"
    elif probability >= 0.34:
        result = "Moderate Risk"
    else:
        result = "Low Risk"

    return result, probability