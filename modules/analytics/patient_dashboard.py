import pandas as pd
import plotly.express as px
import streamlit as st

from config.database import fetch_one
from utils.access_control import accessible_patient_ids, placeholders


def patient_dashboard():
    st.subheader("Patient Dashboard")

    patient_ids = accessible_patient_ids()
    if not patient_ids:
        st.info("No patient details are linked to this login yet.")
        return

    id_placeholders = placeholders(patient_ids)
    params = tuple(patient_ids)
    total_patients = len(patient_ids)
    appointment_row = fetch_one(
        f"SELECT COUNT(*) AS total FROM appointments WHERE patient_id IN ({id_placeholders})",
        params,
    )
    record_row = fetch_one(
        f"SELECT COUNT(*) AS total FROM medical_records WHERE patient_id IN ({id_placeholders})",
        params,
    )
    diagnostic_row = fetch_one(
        f"SELECT COUNT(*) AS total FROM diagnostics WHERE patient_id IN ({id_placeholders})",
        params,
    )

    appointments = int(appointment_row["total"]) if appointment_row else 0
    health_records = int(record_row["total"]) if record_row else 0
    diagnostics = int(diagnostic_row["total"]) if diagnostic_row else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Patients", total_patients)
    col2.metric("Appointments", appointments)
    col3.metric("Health Records", health_records)
    col4.metric("Diagnostics", diagnostics)

    data = pd.DataFrame(
        {
            "Category": ["Appointments", "Health Records", "Diagnostics"],
            "Count": [appointments, health_records, diagnostics],
        }
    )

    if data["Count"].sum() == 0:
        st.info("No activity has been recorded yet.")
        return

    fig = px.pie(data, values="Count", names="Category", title="Patient Activity")
    st.plotly_chart(fig, use_container_width=True)
