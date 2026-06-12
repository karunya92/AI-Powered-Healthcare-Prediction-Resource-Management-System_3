import streamlit as st
import pandas as pd

from config.database import (
    execute_query,
    fetch_all
)


def alerts():

    st.subheader("🚨 Emergency Alerts")

    execute_query(
        """
        CREATE TABLE IF NOT EXISTS emergency_alerts(
            alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_type TEXT,
            message TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    alert_type = st.selectbox(
        "Alert Type",
        [
            "Medical Emergency",
            "Fire Emergency",
            "ICU Emergency",
            "Equipment Failure",
            "Security Alert"
        ]
    )

    message = st.text_area(
        "Alert Message"
    )

    if st.button("Send Alert"):

        execute_query(
            """
            INSERT INTO emergency_alerts
            (
                alert_type,
                message,
                status
            )
            VALUES (?,?,?)
            """,
            (
                alert_type,
                message,
                "Active"
            )
        )

        st.success(
            "Emergency Alert Sent Successfully"
        )

    alerts_data = fetch_all(
        """
        SELECT *
        FROM emergency_alerts
        ORDER BY alert_id DESC
        """
    )

    if alerts_data:

        df = pd.DataFrame(
            [dict(row) for row in alerts_data]
        )

        st.dataframe(
            df,
            use_container_width=True
        )