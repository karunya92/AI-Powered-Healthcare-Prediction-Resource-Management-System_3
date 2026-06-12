import streamlit as st
import pandas as pd
import plotly.express as px


def disease_statistics():

    st.subheader("🦠 Disease Statistics Report")

    data = pd.DataFrame({
        "Disease": [
            "Diabetes",
            "Heart Disease",
            "Cancer",
            "Kidney Disease",
            "Asthma"
        ],
        "Cases": [
            250,
            180,
            90,
            120,
            160
        ]
    })

    st.dataframe(
        data,
        use_container_width=True
    )

    fig = px.bar(
        data,
        x="Disease",
        y="Cases",
        title="Disease Cases"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.metric(
        "Total Cases",
        int(data["Cases"].sum())
    )