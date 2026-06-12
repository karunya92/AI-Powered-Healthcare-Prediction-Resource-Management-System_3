import streamlit as st


def symptom_checker():

    st.subheader("🩺 Symptom Checker")

    symptoms = st.multiselect(
        "Select Symptoms",
        [
            "Fever",
            "Cough",
            "Headache",
            "Chest Pain",
            "Shortness of Breath",
            "Fatigue",
            "Nausea",
            "Dizziness"
        ]
    )

    if st.button("Check Symptoms"):

        if (
            "Fever" in symptoms and
            "Cough" in symptoms
        ):
            result = (
                "Possible Viral Infection."
            )

        elif (
            "Chest Pain" in symptoms and
            "Shortness of Breath" in symptoms
        ):
            result = (
                "Possible Cardiac Issue. "
                "Seek immediate medical attention."
            )

        elif (
            "Headache" in symptoms and
            "Dizziness" in symptoms
        ):
            result = (
                "Possible Neurological Condition."
            )

        else:
            result = (
                "Symptoms are inconclusive. "
                "Consult a healthcare provider."
            )

        st.info(result)