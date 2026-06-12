import pandas as pd
import streamlit as st

from config.database import execute_query, fetch_all
from utils.access_control import accessible_patients, current_role, placeholders


def medication_reminder():
    st.subheader("Medication Reminder")

    execute_query(
        """
        CREATE TABLE IF NOT EXISTS medication_reminders(
            reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            patient_name TEXT,
            medicine_name TEXT,
            dosage TEXT,
            reminder_time TEXT
        )
        """
    )

    patients = accessible_patients()
    if not patients:
        st.info("No patients are available for this login.")
        return

    patient_options = {
        f"{row['full_name'] or 'Unnamed Patient'} (ID: {row['patient_id']})": row["patient_id"]
        for row in patients
    }
    if current_role() == "Patient" and len(patient_options) == 1:
        selected_patient = next(iter(patient_options))
        st.text_input("Patient", selected_patient, disabled=True)
    else:
        selected_patient = st.selectbox("Patient", list(patient_options.keys()))
    patient_id = patient_options[selected_patient]
    patient = next(row for row in patients if row["patient_id"] == patient_id)

    medicine_name = st.text_input("Medicine Name")
    dosage = st.text_input("Dosage")
    reminder_time = st.time_input("Reminder Time")

    if st.button("Save Reminder"):
        execute_query(
            """
            INSERT INTO medication_reminders
            (
                patient_id,
                patient_name,
                medicine_name,
                dosage,
                reminder_time
            )
            VALUES (?,?,?,?,?)
            """,
            (
                patient_id,
                patient["full_name"],
                medicine_name,
                dosage,
                str(reminder_time),
            ),
        )
        st.success("Reminder Saved Successfully")

    patient_ids = [row["patient_id"] for row in patients]
    reminders = fetch_all(
        f"""
        SELECT mr.*, p.full_name AS patient
        FROM medication_reminders mr
        LEFT JOIN patients p ON mr.patient_id = p.patient_id
        WHERE mr.patient_id IN ({placeholders(patient_ids)})
        ORDER BY mr.reminder_id DESC
        """,
        tuple(patient_ids),
    )

    if reminders:
        st.dataframe(pd.DataFrame([dict(row) for row in reminders]), use_container_width=True)
