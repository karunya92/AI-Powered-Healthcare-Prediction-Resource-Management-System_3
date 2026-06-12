import pandas as pd
import streamlit as st

from config.database import execute_query, fetch_all
from utils.access_control import accessible_doctors, current_doctor, current_role


SPECIALIZATIONS = [
    "General Physician",
    "Cardiologist",
    "Neurologist",
    "Orthopedic",
    "Dermatologist",
    "Pediatrician",
    "Oncologist",
    "Psychiatrist",
    "Endocrinology",
    "Nephrology",
]


def _specialization_index(doctor):
    if not doctor or doctor["specialization"] not in SPECIALIZATIONS:
        return None
    return SPECIALIZATIONS.index(doctor["specialization"])


def doctor_profile():
    st.subheader("Doctor Profile Management")
    st.caption("Doctor details, assigned patients, and patient medical records.")

    role = current_role()
    linked_doctor = current_doctor() if role == "Doctor" else None

    with st.form("doctor_profile_form"):
        doctor_name = st.text_input(
            "Doctor Name",
            value=linked_doctor["doctor_name"] if linked_doctor else "",
        )
        specialization = st.selectbox(
            "Specialization",
            SPECIALIZATIONS,
            index=_specialization_index(linked_doctor),
            placeholder="Select specialization",
        )
        experience = st.number_input(
            "Experience (Years)",
            min_value=0,
            max_value=50,
            value=int(linked_doctor["experience"] or 0) if linked_doctor else 0,
        )
        phone = st.text_input(
            "Phone",
            value=linked_doctor["phone"] if linked_doctor and linked_doctor["phone"] else "",
        )
        email = st.text_input(
            "Email",
            value=linked_doctor["email"] if linked_doctor and linked_doctor["email"] else "",
        )
        submitted = st.form_submit_button(
            "Save Doctor Profile" if role == "Doctor" else "Add Doctor"
        )

    if submitted:
        if not doctor_name.strip():
            st.error("Doctor name is required")
            return
        if not specialization:
            st.error("Specialization is required")
            return

        if role == "Doctor" and linked_doctor:
            execute_query(
                """
                UPDATE doctors
                SET doctor_name = ?, specialization = ?, experience = ?, phone = ?, email = ?
                WHERE doctor_id = ?
                """,
                (
                    doctor_name,
                    specialization,
                    experience,
                    phone,
                    email,
                    linked_doctor["doctor_id"],
                ),
            )
            st.success("Doctor profile updated successfully")
        else:
            linked_user_id = st.session_state.get("user_id") if role == "Doctor" else None
            linked_username = st.session_state.get("username", "") if role == "Doctor" else ""
            execute_query(
                """
                INSERT INTO doctors
                (
                    doctor_name,
                    specialization,
                    experience,
                    phone,
                    email,
                    user_id,
                    username
                )
                VALUES (?,?,?,?,?,?,?)
                """,
                (
                    doctor_name,
                    specialization,
                    experience,
                    phone,
                    email,
                    linked_user_id,
                    linked_username,
                ),
            )
            st.success("Doctor profile saved successfully")

    st.divider()

    doctors = accessible_doctors()
    if not doctors:
        st.info("No doctor profile is linked to this login yet.")
        return

    df = pd.DataFrame([dict(row) for row in doctors])
    st.write("### Doctors" if role == "Admin" else "### My Profile")
    st.dataframe(df, use_container_width=True)

    doctor_options = {
        f"{row['doctor_name']} - {row['specialization']} (ID: {row['doctor_id']})": row["doctor_id"]
        for row in doctors
    }
    if role == "Doctor" and len(doctor_options) == 1:
        selected_doctor = next(iter(doctor_options))
        st.text_input("View Doctor's Patients", selected_doctor, disabled=True)
    else:
        selected_doctor = st.selectbox("View Doctor's Patients", list(doctor_options.keys()))
    doctor_id = doctor_options[selected_doctor]

    assigned_patients = fetch_all(
        """
        SELECT
            patient_id,
            full_name,
            age,
            gender,
            blood_group,
            phone,
            insurance_id
        FROM patients
        WHERE doctor_id = ?
        ORDER BY full_name
        """,
        (doctor_id,),
    )

    st.write("### Assigned Patients")
    if assigned_patients:
        st.dataframe(pd.DataFrame([dict(row) for row in assigned_patients]), use_container_width=True)
    else:
        st.info("No patients assigned to this doctor.")

    doctor_records = fetch_all(
        """
        SELECT
            mr.record_id,
            mr.report_date,
            p.full_name AS patient_name,
            mr.diagnosis,
            mr.treatment,
            mr.prescription
        FROM medical_records mr
        LEFT JOIN patients p ON mr.patient_id = p.patient_id
        WHERE mr.doctor_id = ?
        ORDER BY mr.record_id DESC
        """,
        (doctor_id,),
    )

    st.write("### Patient Records With This Doctor")
    if doctor_records:
        st.dataframe(pd.DataFrame([dict(row) for row in doctor_records]), use_container_width=True)
    else:
        st.info("No medical records linked to this doctor yet.")
