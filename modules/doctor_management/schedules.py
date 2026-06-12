import pandas as pd
import streamlit as st

from config.database import execute_query, fetch_all
from utils.access_control import current_doctor, current_role


def schedules():
    st.subheader("Doctor Schedule Management")

    execute_query(
        """
        CREATE TABLE IF NOT EXISTS doctor_schedules(
            schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER,
            schedule_date TEXT,
            shift TEXT
        )
        """
    )

    if current_role() == "Doctor":
        doctor = current_doctor()
        doctors = [doctor] if doctor else []
    else:
        doctors = fetch_all(
            """
            SELECT doctor_id, doctor_name, specialization
            FROM doctors
            ORDER BY doctor_name
            """
        )

    if not doctors:
        st.info("No doctor profile is available for this login.")
        return

    doctor_options = {
        f"{row['doctor_name']} - {row['specialization']} (ID: {row['doctor_id']})": row["doctor_id"]
        for row in doctors
    }

    if current_role() == "Doctor":
        selected_doctor = next(iter(doctor_options))
        st.text_input("Doctor", selected_doctor, disabled=True)
    else:
        selected_doctor = st.selectbox("Doctor", list(doctor_options.keys()))
    doctor_id = doctor_options[selected_doctor]

    schedule_date = st.date_input("Schedule Date")
    shift = st.selectbox("Shift", ["Morning", "Afternoon", "Evening", "Night"])

    if st.button("Save Schedule"):
        execute_query(
            """
            INSERT INTO doctor_schedules
            (
                doctor_id,
                schedule_date,
                shift
            )
            VALUES (?,?,?)
            """,
            (doctor_id, str(schedule_date), shift),
        )
        st.success("Schedule Saved")

    if current_role() == "Doctor":
        records = fetch_all(
            """
            SELECT ds.*, d.doctor_name, d.specialization
            FROM doctor_schedules ds
            LEFT JOIN doctors d ON ds.doctor_id = d.doctor_id
            WHERE ds.doctor_id = ?
            ORDER BY ds.schedule_id DESC
            """,
            (doctor_id,),
        )
    else:
        records = fetch_all(
            """
            SELECT ds.*, d.doctor_name, d.specialization
            FROM doctor_schedules ds
            LEFT JOIN doctors d ON ds.doctor_id = d.doctor_id
            ORDER BY ds.schedule_id DESC
            """
        )

    if records:
        st.dataframe(pd.DataFrame([dict(row) for row in records]), use_container_width=True)
