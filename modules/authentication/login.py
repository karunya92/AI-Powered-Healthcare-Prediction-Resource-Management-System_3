import streamlit as st

from config.database import fetch_one
from config.auth_config import verify_password


def login():

    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if not username or not password:
            st.warning("Please enter username and password")
            return False

        user = fetch_one(
            """
            SELECT * FROM users
            WHERE username = ?
            """,
            (username,)
        )

        if user is None:
            st.error("User not found")
            return False

        if verify_password(password, user["password"]):

            st.session_state.logged_in = True
            st.session_state.username = user["username"]
            st.session_state.role = user["role"]

            st.success("Login Successful")
            return True

        st.error("Invalid Password")
        return False

    return False