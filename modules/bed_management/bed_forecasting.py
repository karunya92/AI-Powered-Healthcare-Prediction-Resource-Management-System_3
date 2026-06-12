import streamlit as st
import pandas as pd
import plotly.express as px


def bed_forecasting():

    st.subheader("📈 Bed Occupancy Forecasting")

    current_beds = st.number_input(
        "Total Beds",
        min_value=1,
        value=200
    )

    occupied_beds = st.number_input(
        "Occupied Beds",
        min_value=0,
        value=120
    )

    expected_admissions = st.number_input(
        "Expected New Admissions",
        min_value=0,
        value=20
    )

    if st.button("Generate Forecast"):

        future_occupancy = (
            occupied_beds +
            expected_admissions
        )

        occupancy_rate = (
            future_occupancy /
            current_beds
        ) * 100

        st.metric(
            "Forecast Occupancy Rate",
            f"{occupancy_rate:.1f}%"
        )

        df = pd.DataFrame({
            "Category": [
                "Current Occupied",
                "Expected Admissions",
                "Remaining Beds"
            ],
            "Beds": [
                occupied_beds,
                expected_admissions,
                max(
                    current_beds -
                    future_occupancy,
                    0
                )
            ]
        })

        fig = px.pie(
            df,
            values="Beds",
            names="Category",
            title="Bed Forecast Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        if occupancy_rate > 90:
            st.error(
                "Critical Bed Shortage Expected"
            )

        elif occupancy_rate > 75:
            st.warning(
                "High Occupancy Expected"
            )

        else:
            st.success(
                "Bed Availability is Sufficient"
            )