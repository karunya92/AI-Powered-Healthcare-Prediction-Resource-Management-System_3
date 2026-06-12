import streamlit as st

from config.database import execute_query, fetch_one
from config.auth_config import (
    hash_password,
    validate_password,
    AVAILABLE_ROLES
)


def register():

    st.subheader("📝 User Registration")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    role = st.selectbox(
        "Role",
        AVAILABLE_ROLES
    )

    if st.button("Register"):

        if not username:
            st.warning("Username required")
            return

        if password != confirm_password:
            st.error("Passwords do not match")
            return

        if not validate_password(password):
            st.error(
                """
                Password must contain:
                - 8 characters
                - 1 uppercase letter
                - 1 lowercase letter
                - 1 number
                """
            )
            return

        existing_user = fetch_one(
            """
            SELECT * FROM users
            WHERE username = ?
            """,
            (username,)
        )

        if existing_user:
            st.error("Username already exists")
            return

        hashed_password = hash_password(password)

        execute_query(
            """
            INSERT INTO users
            (username,password,role)
            VALUES (?,?,?)
            """,
            (
                username,
                hashed_password,
                role
            )
        )

        st.success("Registration Successful")