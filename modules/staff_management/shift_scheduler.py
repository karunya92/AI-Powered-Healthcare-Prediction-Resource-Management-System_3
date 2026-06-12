import streamlit as st
import pandas as pd

from config.database import (
    execute_query,
    fetch_all
)


def shift_scheduler():

    st.subheader("👨‍⚕️ Staff Shift Scheduler")

    execute_query(
        """
        CREATE TABLE IF NOT EXISTS staff_shifts(
            shift_id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_name TEXT,
            role TEXT,
            shift_date TEXT,
            shift_type TEXT
        )
        """
    )

    staff_name = st.text_input(
        "Staff Name"
    )

    role = st.selectbox(
        "Role",
        [
            "Doctor",
            "Nurse",
            "Technician",
            "Administrator"
        ]
    )

    shift_date = st.date_input(
        "Shift Date"
    )

    shift_type = st.selectbox(
        "Shift",
        [
            "Morning",
            "Afternoon",
            "Evening",
            "Night"
        ]
    )

    if st.button("Assign Shift"):

        execute_query(
            """
            INSERT INTO staff_shifts
            (
                staff_name,
                role,
                shift_date,
                shift_type
            )
            VALUES (?,?,?,?)
            """,
            (
                staff_name,
                role,
                str(shift_date),
                shift_type
            )
        )

        st.success(
            "Shift Assigned Successfully"
        )

    data = fetch_all(
        """
        SELECT *
        FROM staff_shifts
        ORDER BY shift_id DESC
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