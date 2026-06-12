import pandas as pd
import streamlit as st

from config.database import execute_query, fetch_all
from utils.access_control import accessible_patients, current_role, placeholders


def insurance():
    st.subheader("Insurance Management")

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

    provider_name = st.text_input("Insurance Provider")
    policy_number = st.text_input("Policy Number")
    expiry_date = st.date_input("Policy Expiry Date")

    if st.button("Save Insurance"):
        execute_query(
            """
            INSERT INTO insurance
            (
                patient_id,
                provider_name,
                policy_number,
                expiry_date
            )
            VALUES (?,?,?,?)
            """,
            (patient_id, provider_name, policy_number, str(expiry_date)),
        )
        st.success("Insurance Details Saved")

    patient_ids = [row["patient_id"] for row in patients]
    data = fetch_all(
        f"""
        SELECT i.*, p.full_name AS patient_name
        FROM insurance i
        LEFT JOIN patients p ON i.patient_id = p.patient_id
        WHERE i.patient_id IN ({placeholders(patient_ids)})
        ORDER BY i.insurance_id DESC
        """,
        tuple(patient_ids),
    )

    if data:
        st.dataframe(pd.DataFrame([dict(row) for row in data]), use_container_width=True)
