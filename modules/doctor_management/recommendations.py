import streamlit as st


def recommendations():

    st.subheader("🤖 Specialist Recommendation System")

    disease = st.selectbox(
        "Select Condition",
        [
            "Heart Disease",
            "Diabetes",
            "Kidney Disease",
            "Cancer",
            "Skin Disorder",
            "Bone Fracture",
            "Mental Health",
            "Child Care",
            "General Checkup"
        ]
    )

    specialist_map = {
        "Heart Disease": "Cardiologist",
        "Diabetes": "Endocrinologist",
        "Kidney Disease": "Nephrologist",
        "Cancer": "Oncologist",
        "Skin Disorder": "Dermatologist",
        "Bone Fracture": "Orthopedic",
        "Mental Health": "Psychiatrist",
        "Child Care": "Pediatrician",
        "General Checkup": "General Physician"
    }

    if st.button("Get Recommendation"):

        specialist = specialist_map.get(
            disease,
            "General Physician"
        )

        st.success(
            f"Recommended Specialist: {specialist}"
        )

        st.info(
            f"For {disease}, consult a {specialist}."
        )