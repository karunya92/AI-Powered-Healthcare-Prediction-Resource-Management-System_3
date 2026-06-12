import streamlit as st


def medication_advisor():

    st.subheader("💊 Medication Advisor")

    disease = st.selectbox(
        "Select Disease",
        [
            "Diabetes",
            "Heart Disease",
            "Hypertension",
            "Asthma",
            "General Fever"
        ]
    )

    medication_data = {
        "Diabetes": [
            "Metformin",
            "Insulin (if prescribed)"
        ],
        "Heart Disease": [
            "Aspirin (doctor prescribed)",
            "Statins"
        ],
        "Hypertension": [
            "ACE Inhibitors",
            "Beta Blockers"
        ],
        "Asthma": [
            "Bronchodilator Inhalers",
            "Corticosteroids"
        ],
        "General Fever": [
            "Paracetamol",
            "Hydration"
        ]
    }

    st.warning(
        """
        This module is for educational purposes only.
        Always consult a qualified healthcare professional
        before taking any medication.
        """
    )

    if st.button("Get Medication Advice"):

        st.success("Suggested Medications")

        for medicine in medication_data[disease]:
            st.write("💊", medicine)