import streamlit as st
import pandas as pd

from config.database import (
    execute_query,
    fetch_all
)


def bed_tracker():

    st.subheader("🛏️ Bed Tracker")

    ward_name = st.selectbox(
        "Ward",
        [
            "General Ward",
            "ICU",
            "Emergency",
            "Pediatrics",
            "Maternity"
        ]
    )

    bed_number = st.text_input(
        "Bed Number"
    )

    status = st.selectbox(
        "Status",
        [
            "Available",
            "Occupied",
            "Maintenance"
        ]
    )

    if st.button("Add Bed"):

        execute_query(
            """
            INSERT INTO beds
            (
                ward_name,
                bed_number,
                status
            )
            VALUES (?,?,?)
            """,
            (
                ward_name,
                bed_number,
                status
            )
        )

        st.success("Bed Added Successfully")

    st.divider()

    beds = fetch_all(
        """
        SELECT *
        FROM beds
        ORDER BY bed_id DESC
        """
    )

    if beds:

        df = pd.DataFrame(
            [dict(row) for row in beds]
        )

        st.dataframe(
            df,
            use_container_width=True
        )