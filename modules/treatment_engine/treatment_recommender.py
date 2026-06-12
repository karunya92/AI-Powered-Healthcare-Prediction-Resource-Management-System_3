import streamlit as st


def treatment_recommender():

    st.subheader("🩺 Treatment Recommendation System")

    disease = st.selectbox(
        "Select Disease",
        [
            "Diabetes",
            "Heart Disease",
            "Kidney Disease",
            "Cancer",
            "Hypertension",
            "Asthma",
            "General Fever"
        ]
    )

    recommendations = {
        "Diabetes": [
            "Low sugar diet",
            "Regular exercise",
            "Monitor blood glucose",
            "Periodic doctor consultation"
        ],
        "Heart Disease": [
            "Low cholesterol diet",
            "Daily walking",
            "Blood pressure monitoring",
            "Cardiology consultation"
        ],
        "Kidney Disease": [
            "Low sodium diet",
            "Hydration monitoring",
            "Regular kidney function tests"
        ],
        "Cancer": [
            "Consult oncologist",
            "Regular screenings",
            "Personalized treatment plan"
        ],
        "Hypertension": [
            "Reduce salt intake",
            "Exercise regularly",
            "Monitor blood pressure"
        ],
        "Asthma": [
            "Avoid triggers",
            "Use inhalers as prescribed",
            "Regular pulmonary checkups"
        ],
        "General Fever": [
            "Hydration",
            "Rest",
            "Monitor temperature"
        ]
    }

    if st.button("Recommend Treatment"):

        st.success("Treatment Recommendations")

        for item in recommendations[disease]:
            st.write("✔️", item)