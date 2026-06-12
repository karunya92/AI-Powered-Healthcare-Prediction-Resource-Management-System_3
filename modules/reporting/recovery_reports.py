import streamlit as st
import pandas as pd
import plotly.express as px


def recovery_reports():

    st.subheader("📈 Recovery Analysis Report")

    data = pd.DataFrame({
        "Month": [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun"
        ],
        "Recovered": [
            120,
            150,
            180,
            210,
            240,
            280
        ]
    })

    st.dataframe(
        data,
        use_container_width=True
    )

    fig = px.line(
        data,
        x="Month",
        y="Recovered",
        markers=True,
        title="Monthly Recovery Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.metric(
        "Total Recoveries",
        int(data["Recovered"].sum())
    )