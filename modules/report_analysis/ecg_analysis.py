import streamlit as st


def ecg_analysis():

    st.subheader("❤️ ECG Analysis")

    heart_rate = st.number_input(
        "Heart Rate (BPM)",
        min_value=20,
        max_value=250,
        value=72
    )

    if st.button("Analyze ECG"):

        if heart_rate < 60:
            result = "Bradycardia Detected"

        elif heart_rate > 100:
            result = "Tachycardia Detected"

        else:
            result = "Normal ECG Pattern"

        st.success(result)