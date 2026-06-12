import streamlit as st
import pandas as pd

from config.database import (
    execute_query,
    fetch_all
)


def oxygen_units():

    st.subheader("🫧 Oxygen Unit Management")

    execute_query("""
    CREATE TABLE IF NOT EXISTS oxygen_units(
        oxygen_id INTEGER PRIMARY KEY AUTOINCREMENT,
        unit_name TEXT,
        quantity INTEGER,
        status TEXT
    )
    """)

    unit_name = st.text_input(
        "Oxygen Unit Name"
    )

    quantity = st.number_input(
        "Quantity",
        min_value=0,
        value=1
    )

    status = st.selectbox(
        "Status",
        [
            "Available",
            "Low Stock",
            "Out of Stock"
        ]
    )

    if st.button("Add Oxygen Unit"):

        execute_query(
            """
            INSERT INTO oxygen_units
            (
                unit_name,
                quantity,
                status
            )
            VALUES (?,?,?)
            """,
            (
                unit_name,
                quantity,
                status
            )
        )

        st.success(
            "Oxygen Unit Added"
        )

    data = fetch_all(
        """
        SELECT *
        FROM oxygen_units
        ORDER BY oxygen_id DESC
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