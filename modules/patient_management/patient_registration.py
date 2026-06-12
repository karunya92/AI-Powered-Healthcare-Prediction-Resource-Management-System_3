import streamlit as st

from config.database import execute_query
from utils.access_control import current_patient, current_role, doctors_for_patient_booking


GENDERS = ["Male", "Female", "Other"]
BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


def _option_index(options, value):
    return options.index(value) if value in options else None


def patient_registration():
    st.subheader("Patient Registration")
    st.caption("Register patient details and assign the responsible doctor.")

    role = current_role()
    linked_patient = current_patient() if role == "Patient" else None
    doctors = doctors_for_patient_booking()

    full_name = st.text_input(
        "Full Name",
        value=linked_patient["full_name"] if linked_patient and linked_patient["full_name"] else "",
    )
    age = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        value=int(linked_patient["age"] or 0) if linked_patient else 0,
    )
    gender = st.selectbox(
        "Gender",
        GENDERS,
        index=_option_index(GENDERS, linked_patient["gender"] if linked_patient else None),
        placeholder="Select gender",
    )
    blood_group = st.selectbox(
        "Blood Group",
        BLOOD_GROUPS,
        index=_option_index(BLOOD_GROUPS, linked_patient["blood_group"] if linked_patient else None),
        placeholder="Select blood group",
    )
    phone = st.text_input(
        "Phone",
        value=linked_patient["phone"] if linked_patient and linked_patient["phone"] else "",
    )
    address = st.text_area(
        "Address",
        value=linked_patient["address"] if linked_patient and linked_patient["address"] else "",
    )
    insurance_id = st.text_input(
        "Insurance ID",
        value=linked_patient["insurance_id"] if linked_patient and linked_patient["insurance_id"] else "",
    )

    doctor_options = {
        f"{row['doctor_name']} - {row['specialization']} (ID: {row['doctor_id']})": row["doctor_id"]
        for row in doctors
    }
    doctor_labels = list(doctor_options.keys())
    doctor_index = None
    if linked_patient and linked_patient["doctor_id"]:
        for index, doctor_id in enumerate(doctor_options.values()):
            if doctor_id == linked_patient["doctor_id"]:
                doctor_index = index
                break

    selected_doctor = st.selectbox(
        "Assigned Doctor",
        doctor_labels if doctor_labels else ["No doctor available"],
        index=doctor_index,
        placeholder="Select assigned doctor",
    )

    if st.button("Save Patient Details" if role == "Patient" else "Register Patient"):
        if not full_name.strip():
            st.error("Patient name is required")
            return
        if not gender:
            st.error("Gender is required")
            return
        if not blood_group:
            st.error("Blood group is required")
            return

        doctor_id = doctor_options.get(selected_doctor)
        if not doctor_id:
            st.error("Assigned doctor is required")
            return

        linked_user_id = st.session_state.get("user_id") if role == "Patient" else None
        linked_username = st.session_state.get("username", "") if role == "Patient" else ""

        if role == "Patient" and linked_patient:
            execute_query(
                """
                UPDATE patients
                SET full_name = ?, doctor_id = ?, age = ?, gender = ?, blood_group = ?,
                    phone = ?, address = ?, insurance_id = ?, user_id = ?, username = ?
                WHERE patient_id = ?
                """,
                (
                    full_name,
                    doctor_id,
                    age,
                    gender,
                    blood_group,
                    phone,
                    address,
                    insurance_id,
                    linked_user_id,
                    linked_username,
                    linked_patient["patient_id"],
                ),
            )
            st.success("Patient details updated successfully")
            return

        execute_query(
            """
            INSERT INTO patients
            (
                full_name,
                doctor_id,
                age,
                gender,
                blood_group,
                phone,
                address,
                insurance_id,
                user_id,
                username
            )
            VALUES (?,?,?,?,?,?,?,?,?,?)
            """,
            (
                full_name,
                doctor_id,
                age,
                gender,
                blood_group,
                phone,
                address,
                insurance_id,
                linked_user_id,
                linked_username,
            ),
        )

        st.success("Patient details saved successfully")
