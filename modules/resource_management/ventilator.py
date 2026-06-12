import streamlit as st
import pandas as pd

from config.database import (
    execute_query,
    fetch_all
)


def ventilator():

    st.subheader("🫁 Ventilator Management")

    execute_query("""
    CREATE TABLE IF NOT EXISTS ventilators(
        ventilator_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ventilator_name TEXT,
        status TEXT,
        location TEXT
    )
    """)

    ventilator_name = st.text_input(
        "Ventilator Name"
    )

    status = st.selectbox(
        "Status",
        [
            "Available",
            "In Use",
            "Maintenance"
        ]
    )

    location = st.text_input(
        "Location/Ward"
    )

    if st.button("Add Ventilator"):

        execute_query(
            """
            INSERT INTO ventilators
            (
                ventilator_name,
                status,
                location
            )
            VALUES (?,?,?)
            """,
            (
                ventilator_name,
                status,
                location
            )
        )

        st.success(
            "Ventilator Added Successfully"
        )

    data = fetch_all(
        """
        SELECT *
        FROM ventilators
        ORDER BY ventilator_id DESC
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