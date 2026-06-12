import streamlit as st
import pandas as pd

from config.database import (
    execute_query,
    fetch_all
)
from utils.access_control import accessible_appointments, accessible_patients, doctors_for_patient_booking, current_role


def booking():

    st.subheader("Appointment Booking")

    doctors = doctors_for_patient_booking()
    patients = accessible_patients()

    if not doctors:
        st.info("No doctors found. Add doctor profiles before booking appointments.")
        return

    st.write("### Available Doctors")
    st.dataframe(
        pd.DataFrame([dict(row) for row in doctors]),
        use_container_width=True
    )

    if not patients:
        st.info("No patients found. Register patient details before booking appointments.")
        return

    patient_options = {
        f"{row['full_name']} (ID: {row['patient_id']})": row["patient_id"]
        for row in patients
    }
    doctor_options = {
        f"{row['doctor_name']} - {row['specialization']} (ID: {row['doctor_id']})": row["doctor_id"]
        for row in doctors
    }

    with st.form("appointment_booking_form"):
        if current_role() == "Patient":
            selected_patient = next(iter(patient_options))
            st.text_input("Patient", selected_patient, disabled=True)
        else:
            selected_patient = st.selectbox("Patient", list(patient_options.keys()))
        selected_doctor = st.selectbox("Doctor", list(doctor_options.keys()))
        appointment_date = st.date_input("Appointment Date")
        submitted = st.form_submit_button("Book Appointment")

    if submitted:
        patient_id = patient_options[selected_patient]
        doctor_id = doctor_options[selected_doctor]

        execute_query(
            """
            INSERT INTO appointments
            (
                patient_id,
                doctor_id,
                appointment_date,
                status
            )
            VALUES (?,?,?,?)
            """,
            (
                patient_id,
                doctor_id,
                str(appointment_date),
                "Pending"
            )
        )

        st.success(
            "Appointment booked successfully. Status is Pending until the doctor accepts or rejects it."
        )

    st.divider()

    appointments = accessible_appointments()

    if appointments:
        st.write("### Booked Appointments")

        df = pd.DataFrame(
            [dict(row) for row in appointments]
        )

        st.dataframe(
            df,
            use_container_width=True
        )
