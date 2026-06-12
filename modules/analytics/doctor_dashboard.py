import pandas as pd
import plotly.express as px
import streamlit as st

from config.database import fetch_one
from utils.access_control import current_doctor


def doctor_dashboard():
    st.subheader("Doctor Dashboard")

    doctor = current_doctor()
    if not doctor:
        st.info("No doctor profile is linked to this login yet.")
        return

    doctor_id = doctor["doctor_id"]
    patient_row = fetch_one(
        """
        SELECT COUNT(DISTINCT p.patient_id) AS total
        FROM patients p
        LEFT JOIN appointments a ON p.patient_id = a.patient_id
        LEFT JOIN medical_records mr ON p.patient_id = mr.patient_id
        WHERE p.doctor_id = ? OR a.doctor_id = ? OR mr.doctor_id = ?
        """,
        (doctor_id, doctor_id, doctor_id),
    )
    appointment_row = fetch_one(
        "SELECT COUNT(*) AS total FROM appointments WHERE doctor_id = ?",
        (doctor_id,),
    )
    record_row = fetch_one(
        "SELECT COUNT(*) AS total FROM medical_records WHERE doctor_id = ?",
        (doctor_id,),
    )
    pending_row = fetch_one(
        "SELECT COUNT(*) AS total FROM appointments WHERE doctor_id = ? AND status = 'Pending'",
        (doctor_id,),
    )

    assigned_patients = int(patient_row["total"]) if patient_row else 0
    appointments = int(appointment_row["total"]) if appointment_row else 0
    records = int(record_row["total"]) if record_row else 0
    pending = int(pending_row["total"]) if pending_row else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Assigned Patients", assigned_patients)
    c2.metric("Appointments", appointments)
    c3.metric("Medical Records", records)
    c4.metric("Pending", pending)

    df = pd.DataFrame(
        {
            "Type": ["Appointments", "Medical Records", "Pending"],
            "Count": [appointments, records, pending],
        }
    )

    if df["Count"].sum() == 0:
        st.info("No doctor activity has been recorded yet.")
        return

    fig = px.bar(df, x="Type", y="Count", title="Doctor Activity")
    st.plotly_chart(fig, use_container_width=True)
