import streamlit as st
import pandas as pd
import plotly.express as px


def visualizations():

    st.subheader("📊 Healthcare Visualizations")

    chart_type = st.selectbox(
        "Select Visualization",
        [
            "Patients By Department",
            "Monthly Admissions",
            "Disease Statistics"
        ]
    )

    if chart_type == "Patients By Department":

        df = pd.DataFrame({
            "Department": [
                "Cardiology",
                "Neurology",
                "Orthopedics",
                "Pediatrics",
                "General"
            ],
            "Patients": [
                120,
                80,
                150,
                95,
                200
            ]
        })

        fig = px.bar(
            df,
            x="Department",
            y="Patients",
            title="Patients By Department"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    elif chart_type == "Monthly Admissions":

        df = pd.DataFrame({
            "Month": [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun"
            ],
            "Admissions": [
                180,
                220,
                210,
                250,
                280,
                300
            ]
        })

        fig = px.line(
            df,
            x="Month",
            y="Admissions",
            title="Monthly Admissions"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        df = pd.DataFrame({
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

        fig = px.pie(
            df,
            values="Cases",
            names="Disease",
            title="Disease Statistics"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )