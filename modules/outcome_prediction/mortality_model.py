import streamlit as st


def mortality_model():

    st.subheader("📊 Mortality Risk Prediction")

    age = st.number_input(
        "Age",
        min_value=0,
        value=40
    )

    chronic_conditions = st.number_input(
        "Number of Chronic Conditions",
        min_value=0,
        value=0
    )

    severity = st.selectbox(
        "Current Condition Severity",
        [
            "Low",
            "Moderate",
            "High"
        ]
    )

    if st.button("Predict Mortality Risk"):

        risk = 0

        if age > 70:
            risk += 30

        risk += chronic_conditions * 10

        if severity == "Moderate":
            risk += 20

        elif severity == "High":
            risk += 40

        risk = min(risk, 100)

        st.metric(
            "Mortality Risk",
            f"{risk}%"
        )

        if risk >= 60:
            st.error("High Mortality Risk")

        elif risk >= 30:
            st.warning("Moderate Mortality Risk")

        else:
            st.success("Low Mortality Risk")