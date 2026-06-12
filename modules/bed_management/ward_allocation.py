import pandas as pd
import streamlit as st

from config.database import execute_query, fetch_all
from utils.access_control import accessible_patients, placeholders


def ward_allocation():
    st.subheader("Ward Allocation")

    execute_query(
        """
        CREATE TABLE IF NOT EXISTS ward_allocations(
            allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            bed_id INTEGER,
            allocation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    patients = accessible_patients()
    if not patients:
        st.info("No patients are available for this login.")
        return

    beds = fetch_all(
        """
        SELECT bed_id, ward_name, bed_number, status
        FROM beds
        ORDER BY bed_id
        """
    )
    if not beds:
        st.info("Add beds before allocating wards.")
        return

    patient_options = {
        f"{row['full_name'] or 'Unnamed Patient'} (ID: {row['patient_id']})": row["patient_id"]
        for row in patients
    }
    bed_options = {
        f"{row['ward_name'] or 'Ward'} - Bed {row['bed_number'] or row['bed_id']} ({row['status'] or 'Unknown'})": row["bed_id"]
        for row in beds
    }

    selected_patient = st.selectbox("Patient", list(patient_options.keys()))
    selected_bed = st.selectbox("Bed", list(bed_options.keys()))
    patient_id = patient_options[selected_patient]
    bed_id = bed_options[selected_bed]

    if st.button("Allocate Bed"):
        execute_query(
            """
            INSERT INTO ward_allocations
            (
                patient_id,
                bed_id
            )
            VALUES (?,?)
            """,
            (patient_id, bed_id),
        )
        execute_query(
            """
            UPDATE beds
            SET status='Occupied'
            WHERE bed_id=?
            """,
            (bed_id,),
        )
        st.success("Bed Allocated Successfully")

    patient_ids = [row["patient_id"] for row in patients]
    allocations = fetch_all(
        f"""
        SELECT wa.*, p.full_name AS patient_name, b.ward_name, b.bed_number
        FROM ward_allocations wa
        LEFT JOIN patients p ON wa.patient_id = p.patient_id
        LEFT JOIN beds b ON wa.bed_id = b.bed_id
        WHERE wa.patient_id IN ({placeholders(patient_ids)})
        ORDER BY wa.allocation_id DESC
        """,
        tuple(patient_ids),
    )

    if allocations:
        st.write("### Current Allocations")
        st.dataframe(pd.DataFrame([dict(row) for row in allocations]), use_container_width=True)
