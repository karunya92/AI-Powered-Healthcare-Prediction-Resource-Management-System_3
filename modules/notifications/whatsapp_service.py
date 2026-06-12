import streamlit as st
import pandas as pd

from config.database import (
    execute_query,
    fetch_all
)


def whatsapp_service():

    st.subheader("💬 WhatsApp Notification Service")

    execute_query("""
    CREATE TABLE IF NOT EXISTS whatsapp_notifications(
        whatsapp_id INTEGER PRIMARY KEY AUTOINCREMENT,
        mobile_number TEXT,
        message TEXT
    )
    """)

    mobile_number = st.text_input(
        "WhatsApp Number"
    )

    message = st.text_area(
        "WhatsApp Message"
    )

    if st.button("Send WhatsApp Message"):

        execute_query(
            """
            INSERT INTO whatsapp_notifications
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
            "WhatsApp Notification Sent Successfully"
        )

    records = fetch_all(
        """
        SELECT *
        FROM whatsapp_notifications
        ORDER BY whatsapp_id DESC
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