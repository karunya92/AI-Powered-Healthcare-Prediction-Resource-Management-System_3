import streamlit as st
import pandas as pd

from config.database import (
    execute_query,
    fetch_all,
)
from utils.access_control import accessible_doctors, current_role


def approval():

    st.subheader("Appointment Approval")

    doctors = accessible_doctors()

    if not doctors:
        st.info("No doctor profiles found.")
        return

    doctor_options = {
        f"{row['doctor_name']} - {row['specialization']} (ID: {row['doctor_id']})": row["doctor_id"]
        for row in doctors
    }
    if current_role() == "Doctor":
        selected_doctor = next(iter(doctor_options))
        st.text_input("Doctor", selected_doctor, disabled=True)
    else:
        selected_doctor = st.selectbox("Doctor", list(doctor_options.keys()))
    doctor_id = doctor_options[selected_doctor]

    appointments = fetch_all(
        """
        SELECT
            a.appointment_id,
            a.patient_id,
            p.full_name AS patient_name,
            p.age,
            p.gender,
            p.phone AS patient_phone,
            a.appointment_date,
            a.status
        FROM appointments a
        LEFT JOIN patients p ON a.patient_id = p.patient_id
        WHERE a.doctor_id = ?
        ORDER BY
            CASE a.status
                WHEN 'Pending' THEN 0
                WHEN 'Accepted' THEN 1
                WHEN 'Approved' THEN 1
                WHEN 'Rejected' THEN 2
                ELSE 3
            END,
            a.appointment_id DESC
        """,
        (doctor_id,)
    )

    if not appointments:
        st.info("No appointments booked for this doctor.")
        return

    appointment_rows = [dict(row) for row in appointments]

    st.write("### Patient Appointment Requests")
    st.dataframe(
        pd.DataFrame(appointment_rows),
        use_container_width=True
    )

    st.write("### Accept or Reject")
    pending_rows = [row for row in appointment_rows if row["status"] == "Pending"]
    if not pending_rows:
        st.info("No pending appointments to review.")
        return

    for row in pending_rows:
        with st.container():
            st.write(
                f"Patient: {row['patient_name'] or 'Unknown'} "
                f"(ID: {row['patient_id']})"
            )
            st.write(
                f"Date: {row['appointment_date']} | "
                f"Age: {row['age'] or 'NA'} | "
                f"Gender: {row['gender'] or 'NA'} | "
                f"Phone: {row['patient_phone'] or 'NA'}"
            )
            accept_col, reject_col = st.columns(2)

            if accept_col.button(
                "Accept",
                key=f"accept_appointment_{row['appointment_id']}",
                use_container_width=True
            ):
                update_appointment_status(row["appointment_id"], "Accepted")
                st.success("Appointment accepted.")
                st.rerun()

            if reject_col.button(
                "Reject",
                key=f"reject_appointment_{row['appointment_id']}",
                use_container_width=True
            ):
                update_appointment_status(row["appointment_id"], "Rejected")
                st.warning("Appointment rejected.")
                st.rerun()


def update_appointment_status(appointment_id, status):
    execute_query(
        """
        UPDATE appointments
        SET status = ?
        WHERE appointment_id = ?
        """,
        (
            status,
            appointment_id
        )
    )
