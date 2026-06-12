import streamlit as st


def recovery_model():

    st.subheader("🏥 Recovery Prediction")

    age = st.number_input(
        "Patient Age",
        min_value=0,
        max_value=120,
        value=30
    )

    severity = st.selectbox(
        "Disease Severity",
        [
            "Low",
            "Moderate",
            "High"
        ]
    )

    if st.button("Predict Recovery"):

        score = 100

        if age > 60:
            score -= 20

        if severity == "Moderate":
            score -= 20

        elif severity == "High":
            score -= 40

        score = max(score, 10)

        st.success(
            f"Recovery Probability: {score}%"
        )

        if score >= 80:
            st.success("Excellent Recovery Expected")

        elif score >= 50:
            st.warning("Moderate Recovery Expected")

        else:
            st.error("Slow Recovery Expected")