import streamlit as st
import pandas as pd

from config.database import (
    execute_query,
    fetch_all
)


def ambulance():

    st.subheader("🚑 Ambulance Management")

    execute_query(
        """
        CREATE TABLE IF NOT EXISTS ambulances(
            ambulance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ambulance_number TEXT,
            driver_name TEXT,
            status TEXT
        )
        """
    )

    ambulance_number = st.text_input(
        "Ambulance Number"
    )

    driver_name = st.text_input(
        "Driver Name"
    )

    status = st.selectbox(
        "Status",
        [
            "Available",
            "On Duty",
            "Maintenance"
        ]
    )

    if st.button("Register Ambulance"):

        execute_query(
            """
            INSERT INTO ambulances
            (
                ambulance_number,
                driver_name,
                status
            )
            VALUES (?,?,?)
            """,
            (
                ambulance_number,
                driver_name,
                status
            )
        )

        st.success(
            "Ambulance Registered Successfully"
        )

    data = fetch_all(
        """
        SELECT *
        FROM ambulances
        ORDER BY ambulance_id DESC
        """
    )

    if data:

        df = pd.DataFrame(
            [dict(row) for row in data]
        )

        st.dataframe(
            df,
            use_container_width=True
        )