import streamlit as st


def icu_prediction():

    st.subheader("🚑 ICU Admission Prediction")

    oxygen_level = st.number_input(
        "Oxygen Saturation (%)",
        min_value=0,
        max_value=100,
        value=98
    )

    blood_pressure = st.number_input(
        "Blood Pressure",
        min_value=0,
        value=120
    )

    age = st.number_input(
        "Age",
        min_value=0,
        value=40
    )

    if st.button("Predict ICU Need"):

        risk = 0

        if oxygen_level < 90:
            risk += 40

        if blood_pressure > 160:
            risk += 30

        if age > 65:
            risk += 30

        risk = min(risk, 100)

        st.metric(
            "ICU Risk",
            f"{risk}%"
        )

        if risk >= 60:
            st.error("High ICU Admission Risk")

        elif risk >= 30:
            st.warning("Moderate ICU Admission Risk")

        else:
            st.success("Low ICU Admission Risk")