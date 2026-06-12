import streamlit as st


class Roles:

    ADMIN = "Admin"
    DOCTOR = "Doctor"
    NURSE = "Nurse"
    PATIENT = "Patient"


def is_admin():

    return (
        st.session_state.get("role")
        == Roles.ADMIN
    )


def is_doctor():

    return (
        st.session_state.get("role")
        == Roles.DOCTOR
    )


def is_nurse():

    return (
        st.session_state.get("role")
        == Roles.NURSE
    )


def is_patient():

    return (
        st.session_state.get("role")
        == Roles.PATIENT
    )


def has_access(allowed_roles):

    role = st.session_state.get("role")

    return role in allowed_roles


def show_current_role():

    if "role" in st.session_state:
        st.sidebar.success(
            f"Role: {st.session_state.role}"
        )