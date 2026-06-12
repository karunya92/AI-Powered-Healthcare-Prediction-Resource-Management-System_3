import pandas as pd
import streamlit as st

from config.database import fetch_all
from utils.access_control import accessible_patients, current_role


def patient_history():
    st.subheader("Patient History")
    st.caption("Patient records with assigned doctor and medical history.")

    patients = accessible_patients()
    if not patients:
        st.info("No patient records found for this login.")
        return

    patient_options = {
        f"{row['full_name'] or 'Unnamed Patient'} (Patient ID: {row['patient_id']})": row["patient_id"]
        for row in patients
    }

    if current_role() == "Patient" and len(patient_options) == 1:
        selected_patient = next(iter(patient_options))
        st.text_input("Patient", selected_patient, disabled=True)
    else:
        selected_patient = st.selectbox("Select Patient", list(patient_options.keys()))

    patient_id = patient_options[selected_patient]
    patient = next(row for row in patients if row["patient_id"] == patient_id)

    col1, col2, col3 = st.columns(3)
    col1.metric("Patient ID", patient["patient_id"])
    col2.metric("Age", patient["age"] or 0)
    col3.metric("Blood Group", patient["blood_group"] or "NA")

    st.write("### Patient Details")
    st.dataframe(pd.DataFrame([dict(patient)]), use_container_width=True)

    st.write("### Assigned Doctor")
    if patient["doctor_name"]:
        st.success(f"{patient['doctor_name']} - {patient['specialization']}")
    else:
        st.warning("No doctor assigned to this patient yet.")

    records = fetch_all(
        """
        SELECT
            mr.record_id,
            mr.report_date,
            mr.diagnosis,
            mr.treatment,
            mr.prescription,
            d.doctor_name,
            d.specialization
        FROM medical_records mr
        LEFT JOIN doctors d ON mr.doctor_id = d.doctor_id
        WHERE mr.patient_id = ?
        ORDER BY mr.record_id DESC
        """,
        (patient_id,),
    )

    st.write("### Medical Records")
    if records:
        st.dataframe(pd.DataFrame([dict(row) for row in records]), use_container_width=True)
    else:
        st.info("No medical records saved for this patient.")

    if current_role() == "Admin":
        with st.expander("All Patients Overview"):
            st.dataframe(pd.DataFrame([dict(row) for row in patients]), use_container_width=True)
