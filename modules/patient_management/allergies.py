import pandas as pd
import streamlit as st

from config.database import execute_query, fetch_all
from utils.access_control import accessible_patients, current_role, placeholders


def allergies():
    st.subheader("Allergy Management")

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

    allergy_name = st.text_input("Allergy Name")
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])

    if st.button("Add Allergy"):
        execute_query(
            """
            INSERT INTO allergies
            (
                patient_id,
                allergy_name,
                severity
            )
            VALUES (?,?,?)
            """,
            (patient_id, allergy_name, severity),
        )
        st.success("Allergy Added")

    patient_ids = [row["patient_id"] for row in patients]
    records = fetch_all(
        f"""
        SELECT a.*, p.full_name AS patient_name
        FROM allergies a
        LEFT JOIN patients p ON a.patient_id = p.patient_id
        WHERE a.patient_id IN ({placeholders(patient_ids)})
        ORDER BY a.allergy_id DESC
        """,
        tuple(patient_ids),
    )

    if records:
        st.dataframe(pd.DataFrame([dict(row) for row in records]), use_container_width=True)
