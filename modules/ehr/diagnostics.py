import pandas as pd
import streamlit as st

from config.database import execute_query, fetch_all
from utils.access_control import accessible_patients, current_role, placeholders


def diagnostics():
    st.subheader("Diagnostic Reports")

    execute_query(
        """
        CREATE TABLE IF NOT EXISTS diagnostics(
            diagnostic_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            test_name TEXT,
            result TEXT,
            remarks TEXT,
            test_date TEXT
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

    test_name = st.text_input("Test Name")
    result = st.text_area("Result")
    remarks = st.text_area("Remarks")
    test_date = st.date_input("Test Date")

    if st.button("Save Diagnostic Report"):
        execute_query(
            """
            INSERT INTO diagnostics
            (
                patient_id,
                test_name,
                result,
                remarks,
                test_date
            )
            VALUES (?,?,?,?,?)
            """,
            (patient_id, test_name, result, remarks, str(test_date)),
        )
        st.success("Diagnostic Report Saved")

    patient_ids = [row["patient_id"] for row in patients]
    reports = fetch_all(
        f"""
        SELECT d.*, p.full_name AS patient_name
        FROM diagnostics d
        LEFT JOIN patients p ON d.patient_id = p.patient_id
        WHERE d.patient_id IN ({placeholders(patient_ids)})
        ORDER BY d.diagnostic_id DESC
        """,
        tuple(patient_ids),
    )

    if reports:
        st.dataframe(pd.DataFrame([dict(row) for row in reports]), use_container_width=True)
