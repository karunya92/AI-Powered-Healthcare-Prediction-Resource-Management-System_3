import streamlit as st


def specialist_recommender():

    st.subheader("👨‍⚕️ Specialist Recommendation")

    disease = st.selectbox(
        "Select Condition",
        [
            "Diabetes",
            "Heart Disease",
            "Kidney Disease",
            "Cancer",
            "Skin Disease",
            "Mental Health",
            "Bone Fracture",
            "Child Care"
        ]
    )

    specialist_map = {
        "Diabetes": "Endocrinologist",
        "Heart Disease": "Cardiologist",
        "Kidney Disease": "Nephrologist",
        "Cancer": "Oncologist",
        "Skin Disease": "Dermatologist",
        "Mental Health": "Psychiatrist",
        "Bone Fracture": "Orthopedic Specialist",
        "Child Care": "Pediatrician"
    }

    if st.button("Find Specialist"):

        specialist = specialist_map[disease]

        st.success(
            f"Recommended Specialist: {specialist}"
        )

        st.info(
            f"For {disease}, consult a {specialist}."
        )