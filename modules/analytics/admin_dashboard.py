import pandas as pd
import plotly.express as px
import streamlit as st

from config.database import fetch_one


def _count(table_name):
    row = fetch_one(f"SELECT COUNT(*) AS total FROM {table_name}")
    return int(row["total"]) if row else 0


def admin_dashboard():
    st.subheader("Admin Dashboard")

    patients = _count("patients")
    doctors = _count("doctors")
    appointments = _count("appointments")

    a1, a2, a3 = st.columns(3)
    a1.metric("Patients", patients)
    a2.metric("Doctors", doctors)
    a3.metric("Appointments", appointments)

    df = pd.DataFrame(
        {
            "Category": ["Patients", "Doctors", "Appointments"],
            "Amount": [patients, doctors, appointments],
        }
    )

    if df["Amount"].sum() == 0:
        st.info("No system records have been added yet.")
        return

    fig = px.bar(df, x="Category", y="Amount", title="System Overview")
    st.plotly_chart(fig, use_container_width=True)
