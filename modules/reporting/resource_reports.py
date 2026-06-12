import streamlit as st
import pandas as pd
import plotly.express as px


def resource_reports():

    st.subheader("🏥 Resource Utilization Report")

    data = pd.DataFrame({
        "Resource": [
            "Ventilators",
            "Oxygen Units",
            "Beds",
            "Monitors",
            "Wheelchairs"
        ],
        "Available": [
            25,
            120,
            80,
            60,
            40
        ],
        "In Use": [
            15,
            70,
            120,
            30,
            10
        ]
    })

    st.dataframe(
        data,
        use_container_width=True
    )

    fig = px.bar(
        data,
        x="Resource",
        y=["Available", "In Use"],
        barmode="group",
        title="Resource Utilization"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )