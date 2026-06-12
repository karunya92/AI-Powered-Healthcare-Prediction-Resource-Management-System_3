import streamlit as st
import pandas as pd

from config.database import (
    execute_query,
    fetch_all
)


def equipment():

    st.subheader("⚙️ Medical Equipment Management")

    execute_query("""
    CREATE TABLE IF NOT EXISTS equipment(
        equipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        equipment_name TEXT,
        quantity INTEGER,
        status TEXT
    )
    """)

    equipment_name = st.text_input(
        "Equipment Name"
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
            "In Use",
            "Maintenance"
        ]
    )

    if st.button("Add Equipment"):

        execute_query(
            """
            INSERT INTO equipment
            (
                equipment_name,
                quantity,
                status
            )
            VALUES (?,?,?)
            """,
            (
                equipment_name,
                quantity,
                status
            )
        )

        st.success(
            "Equipment Added Successfully"
        )

    records = fetch_all(
        """
        SELECT *
        FROM equipment
        ORDER BY equipment_id DESC
        """
    )

    if records:

        df = pd.DataFrame(
            [dict(row) for row in records]
        )

        st.dataframe(
            df,
            use_container_width=True
        )