import streamlit as st
import pandas as pd
import plotly.express as px


def workload_prediction():

    st.subheader("📈 Staff Workload Prediction")

    total_staff = st.number_input(
        "Total Staff Available",
        min_value=1,
        value=20
    )

    expected_patients = st.number_input(
        "Expected Patients",
        min_value=0,
        value=100
    )

    if st.button("Predict Workload"):

        workload = (
            expected_patients /
            total_staff
        )

        st.metric(
            "Patients per Staff",
            f"{workload:.1f}"
        )

        if workload > 10:
            status = "High"

        elif workload > 5:
            status = "Moderate"

        else:
            status = "Low"

        st.info(
            f"Predicted Workload: {status}"
        )

        chart_data = pd.DataFrame({
            "Category": [
                "Staff",
                "Patients"
            ],
            "Count": [
                total_staff,
                expected_patients
            ]
        })

        fig = px.bar(
            chart_data,
            x="Category",
            y="Count",
            title="Workload Analysis"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )