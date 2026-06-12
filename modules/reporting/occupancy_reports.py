import streamlit as st
import pandas as pd
import plotly.express as px


def occupancy_reports():

    st.subheader("🛏️ Bed Occupancy Report")

    data = pd.DataFrame({
        "Ward": [
            "General",
            "ICU",
            "Emergency",
            "Pediatrics",
            "Maternity"
        ],
        "Occupied": [
            80,
            30,
            25,
            20,
            15
        ],
        "Available": [
            20,
            10,
            15,
            10,
            5
        ]
    })

    st.dataframe(
        data,
        use_container_width=True
    )

    fig = px.bar(
        data,
        x="Ward",
        y=["Occupied", "Available"],
        barmode="stack",
        title="Ward Occupancy"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    occupancy_rate = (
        data["Occupied"].sum()
        /
        (
            data["Occupied"].sum()
            +
            data["Available"].sum()
        )
    ) * 100

    st.metric(
        "Occupancy Rate",
        f"{occupancy_rate:.1f}%"
    )