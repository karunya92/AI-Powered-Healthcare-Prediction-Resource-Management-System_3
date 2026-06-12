import streamlit as st
import pandas as pd

from config.database import (
    execute_query,
    fetch_all
)


def nurse_allocation():

    st.subheader("🩺 Nurse Allocation")

    execute_query(
        """
        CREATE TABLE IF NOT EXISTS nurse_allocations(
            allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nurse_name TEXT,
            ward_name TEXT,
            patient_count INTEGER
        )
        """
    )

    nurse_name = st.text_input(
        "Nurse Name"
    )

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

    patient_count = st.number_input(
        "Assigned Patients",
        min_value=0,
        value=0
    )

    if st.button("Allocate Nurse"):

        execute_query(
            """
            INSERT INTO nurse_allocations
            (
                nurse_name,
                ward_name,
                patient_count
            )
            VALUES (?,?,?)
            """,
            (
                nurse_name,
                ward_name,
                patient_count
            )
        )

        st.success(
            "Nurse Allocated Successfully"
        )

    allocations = fetch_all(
        """
        SELECT *
        FROM nurse_allocations
        ORDER BY allocation_id DESC
        """
    )

    if allocations:

        df = pd.DataFrame(
            [dict(row) for row in allocations]
        )

        st.dataframe(
            df,
            use_container_width=True
        )