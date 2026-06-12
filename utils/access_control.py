import streamlit as st

from config.database import fetch_all, fetch_one


def current_role():
    return st.session_state.get("role", "")


def current_user_id():
    return st.session_state.get("user_id")


def current_username():
    return st.session_state.get("username", "")


def current_patient():
    if not current_user_id():
        return None
    return fetch_one(
        """
        SELECT
            p.*,
            d.doctor_name,
            d.specialization,
            d.phone AS doctor_phone,
            d.email AS doctor_email
        FROM patients p
        LEFT JOIN doctors d ON p.doctor_id = d.doctor_id
        WHERE p.user_id = ? OR p.username = ?
        ORDER BY p.patient_id DESC
        LIMIT 1
        """,
        (current_user_id(), current_username()),
    )


def current_doctor():
    if not current_user_id():
        return None
    return fetch_one(
        """
        SELECT *
        FROM doctors
        WHERE user_id = ? OR username = ?
        ORDER BY doctor_id DESC
        LIMIT 1
        """,
        (current_user_id(), current_username()),
    )


def accessible_doctors():
    role = current_role()

    if role == "Doctor":
        doctor = current_doctor()
        return [doctor] if doctor else []

    return fetch_all(
        """
        SELECT doctor_id, doctor_name, specialization, experience, phone, email, user_id, username
        FROM doctors
        ORDER BY doctor_name
        """
    )


def accessible_patients():
    role = current_role()

    if role == "Patient":
        patient = current_patient()
        return [patient] if patient else []

    if role == "Doctor":
        doctor = current_doctor()
        if not doctor:
            return []
        doctor_id = doctor["doctor_id"]
        return fetch_all(
            """
            SELECT DISTINCT
                p.patient_id,
                p.full_name,
                p.age,
                p.gender,
                p.blood_group,
                p.phone,
                p.address,
                p.insurance_id,
                p.doctor_id,
                d.doctor_name,
                d.specialization
            FROM patients p
            LEFT JOIN doctors d ON p.doctor_id = d.doctor_id
            LEFT JOIN appointments a ON p.patient_id = a.patient_id
            LEFT JOIN medical_records mr ON p.patient_id = mr.patient_id
            WHERE p.doctor_id = ? OR a.doctor_id = ? OR mr.doctor_id = ?
            ORDER BY p.full_name
            """,
            (doctor_id, doctor_id, doctor_id),
        )

    if role == "Admin":
        return fetch_all(
            """
            SELECT
                p.patient_id,
                p.full_name,
                p.age,
                p.gender,
                p.blood_group,
                p.phone,
                p.address,
                p.insurance_id,
                p.doctor_id,
                d.doctor_name,
                d.specialization
            FROM patients p
            LEFT JOIN doctors d ON p.doctor_id = d.doctor_id
            ORDER BY p.patient_id DESC
            """
        )

    return []


def accessible_appointments():
    role = current_role()

    if role == "Patient":
        patient_ids = accessible_patient_ids()
        if not patient_ids:
            return []
        return fetch_all(
            f"""
            SELECT
                a.appointment_id,
                a.patient_id,
                a.doctor_id,
                p.full_name AS patient_name,
                d.doctor_name,
                d.specialization,
                a.appointment_date,
                a.status
            FROM appointments a
            LEFT JOIN patients p ON a.patient_id = p.patient_id
            LEFT JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.patient_id IN ({placeholders(patient_ids)})
            ORDER BY a.appointment_id DESC
            """,
            tuple(patient_ids),
        )

    if role == "Doctor":
        doctor = current_doctor()
        if not doctor:
            return []
        return fetch_all(
            """
            SELECT
                a.appointment_id,
                a.patient_id,
                a.doctor_id,
                p.full_name AS patient_name,
                d.doctor_name,
                d.specialization,
                a.appointment_date,
                a.status
            FROM appointments a
            LEFT JOIN patients p ON a.patient_id = p.patient_id
            LEFT JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.doctor_id = ?
            ORDER BY a.appointment_id DESC
            """,
            (doctor["doctor_id"],),
        )

    if role == "Admin":
        return fetch_all(
            """
            SELECT
                a.appointment_id,
                a.patient_id,
                a.doctor_id,
                p.full_name AS patient_name,
                d.doctor_name,
                d.specialization,
                a.appointment_date,
                a.status
            FROM appointments a
            LEFT JOIN patients p ON a.patient_id = p.patient_id
            LEFT JOIN doctors d ON a.doctor_id = d.doctor_id
            ORDER BY a.appointment_id DESC
            """
        )

    return []


def accessible_medical_records():
    role = current_role()

    if role == "Patient":
        patient_ids = accessible_patient_ids()
        if not patient_ids:
            return []
        return fetch_all(
            f"""
            SELECT
                mr.record_id,
                mr.patient_id,
                mr.doctor_id,
                mr.report_date,
                p.full_name AS patient_name,
                d.doctor_name,
                d.specialization,
                mr.diagnosis,
                mr.treatment,
                mr.prescription
            FROM medical_records mr
            LEFT JOIN patients p ON mr.patient_id = p.patient_id
            LEFT JOIN doctors d ON mr.doctor_id = d.doctor_id
            WHERE mr.patient_id IN ({placeholders(patient_ids)})
            ORDER BY mr.record_id DESC
            """,
            tuple(patient_ids),
        )

    if role == "Doctor":
        doctor = current_doctor()
        if not doctor:
            return []
        return fetch_all(
            """
            SELECT
                mr.record_id,
                mr.patient_id,
                mr.doctor_id,
                mr.report_date,
                p.full_name AS patient_name,
                d.doctor_name,
                d.specialization,
                mr.diagnosis,
                mr.treatment,
                mr.prescription
            FROM medical_records mr
            LEFT JOIN patients p ON mr.patient_id = p.patient_id
            LEFT JOIN doctors d ON mr.doctor_id = d.doctor_id
            WHERE mr.doctor_id = ?
            ORDER BY mr.record_id DESC
            """,
            (doctor["doctor_id"],),
        )

    if role == "Admin":
        return fetch_all(
            """
            SELECT
                mr.record_id,
                mr.patient_id,
                mr.doctor_id,
                mr.report_date,
                p.full_name AS patient_name,
                d.doctor_name,
                d.specialization,
                mr.diagnosis,
                mr.treatment,
                mr.prescription
            FROM medical_records mr
            LEFT JOIN patients p ON mr.patient_id = p.patient_id
            LEFT JOIN doctors d ON mr.doctor_id = d.doctor_id
            ORDER BY mr.record_id DESC
            """
        )

    return []


def doctors_for_patient_booking():
    return fetch_all(
        """
        SELECT doctor_id, doctor_name, specialization, experience, phone, email
        FROM doctors
        WHERE doctor_name IS NOT NULL AND TRIM(doctor_name) != ''
        ORDER BY doctor_name
        """
    )


def patient_options(patients=None):
    patients = patients if patients is not None else accessible_patients()
    return {
        f"{row['full_name'] or 'Unnamed Patient'} (ID: {row['patient_id']})": row["patient_id"]
        for row in patients
    }


def accessible_patient_ids():
    return [row["patient_id"] for row in accessible_patients()]


def placeholders(values):
    return ", ".join("?" for _ in values)
