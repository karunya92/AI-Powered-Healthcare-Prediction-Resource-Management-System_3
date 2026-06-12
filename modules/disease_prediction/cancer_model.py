def predict_cancer_risk(
    age,
    smoking,
    family_history
):
    score = 0

    if age > 50:
        score += 1

    if smoking == "Yes":
        score += 1

    if family_history == "Yes":
        score += 1

    probability = round(score / 3, 2)

    if probability >= 0.67:
        result = "High Risk"
    elif probability >= 0.34:
        result = "Moderate Risk"
    else:
        result = "Low Risk"

    return result, probability