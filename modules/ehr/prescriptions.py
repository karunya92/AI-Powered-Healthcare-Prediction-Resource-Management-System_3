import pandas as pd
import streamlit as st

from config.database import execute_query, fetch_all
from utils.access_control import accessible_patients, current_role, placeholders


def prescriptions():
    st.subheader("Prescriptions")

    execute_query(
        """
        CREATE TABLE IF NOT EXISTS prescriptions(
            prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            medicine_name TEXT,
            dosage TEXT,
            duration TEXT,
            notes TEXT
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

    medicine_name = st.text_input("Medicine Name")
    dosage = st.text_input("Dosage")
    duration = st.text_input("Duration")
    notes = st.text_area("Doctor Notes")

    if st.button("Save Prescription"):
        execute_query(
            """
            INSERT INTO prescriptions
            (
                patient_id,
                medicine_name,
                dosage,
                duration,
                notes
            )
            VALUES (?,?,?,?,?)
            """,
            (patient_id, medicine_name, dosage, duration, notes),
        )
        st.success("Prescription Saved")

    patient_ids = [row["patient_id"] for row in patients]
    data = fetch_all(
        f"""
        SELECT pr.*, p.full_name AS patient_name
        FROM prescriptions pr
        LEFT JOIN patients p ON pr.patient_id = p.patient_id
        WHERE pr.patient_id IN ({placeholders(patient_ids)})
        ORDER BY pr.prescription_id DESC
        """,
        tuple(patient_ids),
    )

    if data:
        st.dataframe(pd.DataFrame([dict(row) for row in data]), use_container_width=True)
