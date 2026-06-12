import pandas as pd
import numpy as np


def simple_forecast(
    current_value,
    growth_rate,
    periods
):
    """
    Forecast future values
    """

    forecast = []

    value = current_value

    for _ in range(periods):

        value = (
            value *
            (1 + growth_rate)
        )

        forecast.append(
            round(value, 2)
        )

    return forecast


def bed_forecast(
    occupied_beds,
    days=7
):
    """
    Forecast bed usage
    """

    growth_rate = 0.05

    return simple_forecast(
        occupied_beds,
        growth_rate,
        days
    )


def resource_forecast(
    available_units,
    days=7
):
    """
    Forecast resource demand
    """

    growth_rate = 0.03

    return simple_forecast(
        available_units,
        growth_rate,
        days
    )


def forecast_dataframe(
    current_value,
    periods=7
):

    values = simple_forecast(
        current_value,
        0.05,
        periods
    )

    return pd.DataFrame({
        "Day": np.arange(
            1,
            periods + 1
        ),
        "Forecast": values
    })