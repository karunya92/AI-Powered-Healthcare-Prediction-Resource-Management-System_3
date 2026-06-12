import streamlit as st

from modules.disease_prediction.diabetes_model import (
    predict_diabetes
)

from modules.disease_prediction.heart_model import (
    predict_heart_disease
)

from modules.disease_prediction.kidney_model import (
    predict_kidney_disease
)

from modules.disease_prediction.cancer_model import (
    predict_cancer_risk
)


def predictor():

    st.subheader("🤖 Disease Prediction System")

    disease = st.selectbox(
        "Select Disease",
        [
            "Diabetes",
            "Heart Disease",
            "Kidney Disease",
            "Cancer Risk"
        ]
    )

    # ---------------- DIABETES ----------------

    if disease == "Diabetes":

        glucose = st.number_input(
            "Glucose",
            min_value=0.0
        )

        bmi = st.number_input(
            "BMI",
            min_value=0.0
        )

        age = st.number_input(
            "Age",
            min_value=0
        )

        if st.button("Predict Diabetes"):

            result, probability = predict_diabetes(
                glucose,
                bmi,
                age
            )

            st.success(
                f"Prediction: {result}"
            )

            st.metric(
                "Probability",
                f"{probability * 100:.0f}%"
            )

    # ---------------- HEART ----------------

    elif disease == "Heart Disease":

        age = st.number_input(
            "Age",
            min_value=0
        )

        cholesterol = st.number_input(
            "Cholesterol",
            min_value=0.0
        )

        blood_pressure = st.number_input(
            "Blood Pressure",
            min_value=0.0
        )

        if st.button("Predict Heart Disease"):

            result, probability = (
                predict_heart_disease(
                    age,
                    cholesterol,
                    blood_pressure
                )
            )

            st.success(
                f"Prediction: {result}"
            )

            st.metric(
                "Probability",
                f"{probability * 100:.0f}%"
            )

    # ---------------- KIDNEY ----------------

    elif disease == "Kidney Disease":

        creatinine = st.number_input(
            "Creatinine",
            min_value=0.0
        )

        age = st.number_input(
            "Age",
            min_value=0
        )

        blood_pressure = st.number_input(
            "Blood Pressure",
            min_value=0.0
        )

        if st.button("Predict Kidney Disease"):

            result, probability = (
                predict_kidney_disease(
                    creatinine,
                    age,
                    blood_pressure
                )
            )

            st.success(
                f"Prediction: {result}"
            )

            st.metric(
                "Probability",
                f"{probability * 100:.0f}%"
            )

    # ---------------- CANCER ----------------

    elif disease == "Cancer Risk":

        age = st.number_input(
            "Age",
            min_value=0
        )

        smoking = st.selectbox(
            "Smoking",
            ["No", "Yes"]
        )

        family_history = st.selectbox(
            "Family History",
            ["No", "Yes"]
        )

        if st.button("Predict Cancer Risk"):

            result, probability = (
                predict_cancer_risk(
                    age,
                    smoking,
                    family_history
                )
            )

            st.success(
                f"Prediction: {result}"
            )

            st.metric(
                "Probability",
                f"{probability * 100:.0f}%"
            )