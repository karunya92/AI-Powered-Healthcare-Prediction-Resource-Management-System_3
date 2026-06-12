import streamlit as st
import pandas as pd

from config.database import (
    execute_query,
    fetch_all
)


def notifications():

    st.subheader("🔔 Appointment Notifications")

    user_id = st.number_input(
        "User ID",
        min_value=1,
        step=1
    )

    message = st.text_area(
        "Notification Message"
    )

    if st.button("Send Notification"):

        execute_query(
            """
            INSERT INTO notifications
            (
                user_id,
                message,
                status
            )
            VALUES (?,?,?)
            """,
            (
                user_id,
                message,
                "Unread"
            )
        )

        st.success(
            "Notification Sent"
        )

    st.divider()

    notifications_data = fetch_all(
        """
        SELECT *
        FROM notifications
        ORDER BY notification_id DESC
        """
    )

    if notifications_data:

        df = pd.DataFrame(
            [dict(row) for row in notifications_data]
        )

        st.dataframe(
            df,
            use_container_width=True
        )