import streamlit as st


def stay_duration():

    st.subheader("🛏️ Hospital Stay Duration Prediction")

    age = st.number_input(
        "Age",
        min_value=0,
        value=40
    )

    severity = st.selectbox(
        "Disease Severity",
        [
            "Low",
            "Moderate",
            "High"
        ]
    )

    surgery_required = st.selectbox(
        "Surgery Required",
        [
            "No",
            "Yes"
        ]
    )

    if st.button("Predict Stay Duration"):

        days = 2

        if severity == "Moderate":
            days += 3

        elif severity == "High":
            days += 7

        if surgery_required == "Yes":
            days += 5

        if age > 65:
            days += 2

        st.success(
            f"Estimated Hospital Stay: {days} Days"
        )