import pandas as pd
import streamlit as st

from config.database import execute_query
from utils.access_control import (
    accessible_doctors,
    accessible_medical_records,
    accessible_patients,
    current_doctor,
    current_role,
)


def medical_records():
    st.subheader("Medical Records")
    st.caption("Create records that connect each patient with the responsible doctor.")

    role = current_role()
    patients = accessible_patients()

    if role == "Doctor":
        doctor = current_doctor()
        doctors = [doctor] if doctor else []
    else:
        doctors = accessible_doctors()

    if not patients:
        st.info("No patients are available for this login.")
        return
    if not doctors:
        st.info("No doctor profile is available for this login.")
        return

    patient_options = {
        f"{row['full_name'] or 'Unnamed Patient'} (ID: {row['patient_id']})": row["patient_id"]
        for row in patients
    }
    if role == "Patient" and len(patient_options) == 1:
        selected_patient = next(iter(patient_options))
        st.text_input("Patient", selected_patient, disabled=True)
    else:
        selected_patient = st.selectbox("Patient", list(patient_options.keys()))
    patient_id = patient_options[selected_patient]
    patient = next(row for row in patients if row["patient_id"] == patient_id)

    doctor_options = {
        f"{row['doctor_name']} - {row['specialization']} (ID: {row['doctor_id']})": row["doctor_id"]
        for row in doctors
    }
    assigned_doctor_id = patient["doctor_id"]
    default_index = 0
    if assigned_doctor_id:
        for index, doctor_id in enumerate(doctor_options.values()):
            if doctor_id == assigned_doctor_id:
                default_index = index
                break

    if role == "Doctor":
        selected_doctor = next(iter(doctor_options))
        st.text_input("Doctor", selected_doctor, disabled=True)
    else:
        selected_doctor = st.selectbox("Doctor", list(doctor_options.keys()), index=default_index)
    doctor_id = doctor_options[selected_doctor]

    if patient["doctor_name"]:
        st.info(f"Assigned doctor for this patient: {patient['doctor_name']} - {patient['specialization']}")
    else:
        st.warning("This patient does not have an assigned doctor. The selected doctor will be used for this record.")

    diagnosis = st.text_area("Diagnosis")
    treatment = st.text_area("Treatment")
    prescription = st.text_area("Prescription")
    report_date = st.date_input("Report Date")

    if st.button("Save Medical Record"):
        if not diagnosis.strip():
            st.error("Diagnosis is required.")
            return

        execute_query(
            """
            INSERT INTO medical_records
            (
                patient_id,
                doctor_id,
                diagnosis,
                treatment,
                prescription,
                report_date
            )
            VALUES (?,?,?,?,?,?)
            """,
            (
                patient_id,
                doctor_id,
                diagnosis,
                treatment,
                prescription,
                str(report_date),
            ),
        )

        if not assigned_doctor_id:
            execute_query(
                "UPDATE patients SET doctor_id = ? WHERE patient_id = ?",
                (doctor_id, patient_id),
            )

        st.success("Medical record saved and linked with patient and doctor.")

    records = accessible_medical_records()

    st.write("### Saved Records")
    if records:
        st.dataframe(pd.DataFrame([dict(row) for row in records]), use_container_width=True)
    else:
        st.info("No medical records saved yet.")
