import streamlit as st
import pandas as pd
import plotly.express as px


def forecasting():

    st.subheader("📈 Resource Demand Forecasting")

    current_stock = st.number_input(
        "Current Resource Stock",
        min_value=0,
        value=100
    )

    daily_usage = st.number_input(
        "Daily Usage",
        min_value=0,
        value=10
    )

    forecast_days = st.slider(
        "Forecast Days",
        1,
        30,
        7
    )

    if st.button("Generate Forecast"):

        remaining_stock = (
            current_stock -
            (daily_usage * forecast_days)
        )

        st.metric(
            "Expected Remaining Stock",
            max(remaining_stock, 0)
        )

        days = list(
            range(
                forecast_days + 1
            )
        )

        stock_levels = [
            max(
                current_stock -
                (daily_usage * day),
                0
            )
            for day in days
        ]

        df = pd.DataFrame({
            "Day": days,
            "Stock": stock_levels
        })

        fig = px.line(
            df,
            x="Day",
            y="Stock",
            title="Resource Forecast"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        if remaining_stock <= 20:
            st.error(
                "Resource Shortage Expected"
            )

        elif remaining_stock <= 50:
            st.warning(
                "Resource Levels Becoming Low"
            )

        else:
            st.success(
                "Resource Levels Healthy"
            )