import streamlit as st
import pandas as pd

from config.database import (
    execute_query,
    fetch_all
)


def email_service():

    st.subheader("📧 Email Notification Service")

    execute_query("""
    CREATE TABLE IF NOT EXISTS email_notifications(
        email_id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipient TEXT,
        subject TEXT,
        message TEXT
    )
    """)

    recipient = st.text_input(
        "Recipient Email"
    )

    subject = st.text_input(
        "Subject"
    )

    message = st.text_area(
        "Message"
    )

    if st.button("Send Email"):

        execute_query(
            """
            INSERT INTO email_notifications
            (
                recipient,
                subject,
                message
            )
            VALUES (?,?,?)
            """,
            (
                recipient,
                subject,
                message
            )
        )

        st.success(
            "Email Notification Sent Successfully"
        )

    records = fetch_all(
        """
        SELECT *
        FROM email_notifications
        ORDER BY email_id DESC
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