import pandas as pd
import streamlit as st

from config.database import execute_query, fetch_all
from utils.access_control import accessible_patients, current_role, placeholders


def vaccinations():
    st.subheader("Vaccination Records")

    execute_query(
        """
        CREATE TABLE IF NOT EXISTS vaccinations(
            vaccination_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            vaccine_name TEXT,
            vaccination_date TEXT,
            next_due_date TEXT
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

    vaccine_name = st.text_input("Vaccine Name")
    vaccination_date = st.date_input("Vaccination Date")
    next_due_date = st.date_input("Next Due Date")

    if st.button("Save Vaccination"):
        execute_query(
            """
            INSERT INTO vaccinations
            (
                patient_id,
                vaccine_name,
                vaccination_date,
                next_due_date
            )
            VALUES (?,?,?,?)
            """,
            (patient_id, vaccine_name, str(vaccination_date), str(next_due_date)),
        )
        st.success("Vaccination Record Saved")

    patient_ids = [row["patient_id"] for row in patients]
    records = fetch_all(
        f"""
        SELECT v.*, p.full_name AS patient_name
        FROM vaccinations v
        LEFT JOIN patients p ON v.patient_id = p.patient_id
        WHERE v.patient_id IN ({placeholders(patient_ids)})
        ORDER BY v.vaccination_id DESC
        """,
        tuple(patient_ids),
    )

    if records:
        st.dataframe(pd.DataFrame([dict(row) for row in records]), use_container_width=True)
