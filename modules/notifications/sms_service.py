import streamlit as st
import pandas as pd

from config.database import (
    execute_query,
    fetch_all
)


def sms_service():

    st.subheader("📱 SMS Notification Service")

    execute_query("""
    CREATE TABLE IF NOT EXISTS sms_notifications(
        sms_id INTEGER PRIMARY KEY AUTOINCREMENT,
        mobile_number TEXT,
        message TEXT
    )
    """)

    mobile_number = st.text_input(
        "Mobile Number"
    )

    message = st.text_area(
        "SMS Message"
    )

    if st.button("Send SMS"):

        execute_query(
            """
            INSERT INTO sms_notifications
            (
                mobile_number,
                message
            )
            VALUES (?,?)
            """,
            (
                mobile_number,
                message
            )
        )

        st.success(
            "SMS Notification Sent Successfully"
        )

    records = fetch_all(
        """
        SELECT *
        FROM sms_notifications
        ORDER BY sms_id DESC
        """
    )

    if records:

        df = pd.DataFrame(
            [dict(row) for row in records]
        )

        st.dataframe(
            df,
            use_container_width=True
        )