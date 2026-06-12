import pandas as pd
import streamlit as st

from config.database import execute_query, fetch_all
from utils.access_control import accessible_patients, current_role, placeholders


def emergency_contacts():
    st.subheader("Emergency Contacts")

    execute_query(
        """
        CREATE TABLE IF NOT EXISTS emergency_contacts(
            contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            contact_name TEXT,
            relationship TEXT,
            phone_number TEXT
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

    contact_name = st.text_input("Contact Name")
    relationship = st.text_input("Relationship")
    phone_number = st.text_input("Phone Number")

    if st.button("Save Contact"):
        execute_query(
            """
            INSERT INTO emergency_contacts
            (
                patient_id,
                contact_name,
                relationship,
                phone_number
            )
            VALUES (?,?,?,?)
            """,
            (patient_id, contact_name, relationship, phone_number),
        )
        st.success("Emergency Contact Saved")

    patient_ids = [row["patient_id"] for row in patients]
    contacts = fetch_all(
        f"""
        SELECT ec.*, p.full_name AS patient_name
        FROM emergency_contacts ec
        LEFT JOIN patients p ON ec.patient_id = p.patient_id
        WHERE ec.patient_id IN ({placeholders(patient_ids)})
        ORDER BY ec.contact_id DESC
        """,
        tuple(patient_ids),
    )

    if contacts:
        st.dataframe(pd.DataFrame([dict(row) for row in contacts]), use_container_width=True)
