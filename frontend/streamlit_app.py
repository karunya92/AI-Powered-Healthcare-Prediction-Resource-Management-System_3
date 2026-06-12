import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.auth_config import AVAILABLE_ROLES, hash_password, validate_password, verify_password
from config.database import execute_query, fetch_all, fetch_one, initialize_database
from config.settings import APP_NAME
from modules.analytics.admin_dashboard import admin_dashboard
from modules.analytics.doctor_dashboard import doctor_dashboard
from modules.analytics.patient_dashboard import patient_dashboard
from modules.appointment_management.approval import approval
from modules.appointment_management.booking import booking
from modules.appointment_management.notifications import notifications
from modules.bed_management.bed_forecasting import bed_forecasting
from modules.bed_management.bed_tracker import bed_tracker
from modules.bed_management.ward_allocation import ward_allocation
from modules.chatbot.chatbot import chatbot
from modules.chatbot.medication_reminder import medication_reminder
from modules.chatbot.symptom_checker import symptom_checker
from modules.disease_prediction.predictor import predictor
from modules.doctor_management.doctor_profile import doctor_profile
from modules.doctor_management.recommendations import recommendations
from modules.doctor_management.schedules import schedules
from modules.ehr.diagnostics import diagnostics
from modules.ehr.medical_records import medical_records
from modules.ehr.prescriptions import prescriptions
from modules.ehr.vaccinations import vaccinations
from modules.emergency_system.alerts import alerts
from modules.emergency_system.ambulance import ambulance
from modules.emergency_system.emergency_contacts import emergency_contacts
from modules.notifications.email_service import email_service
from modules.notifications.sms_service import sms_service
from modules.notifications.whatsapp_service import whatsapp_service
from modules.patient_management.allergies import allergies
from modules.patient_management.insurance import insurance
from modules.patient_management.patient_history import patient_history
from modules.patient_management.patient_registration import patient_registration
from modules.outcome_prediction.icu_prediction import icu_prediction
from modules.outcome_prediction.mortality_model import mortality_model
from modules.outcome_prediction.recovery_model import recovery_model
from modules.outcome_prediction.stay_duration import stay_duration
from modules.report_analysis.blood_test_analysis import blood_test_analysis
from modules.report_analysis.ecg_analysis import ecg_analysis
from modules.report_analysis.mri_analysis import mri_analysis
from modules.report_analysis.ocr_engine import ocr_engine
from modules.report_analysis.xray_analysis import xray_analysis
from modules.reporting.disease_statistics import disease_statistics
from modules.reporting.occupancy_reports import occupancy_reports
from modules.reporting.recovery_reports import recovery_reports
from modules.reporting.resource_reports import resource_reports
from modules.resource_management.equipment import equipment
from modules.resource_management.forecasting import forecasting as resource_forecasting
from modules.resource_management.oxygen_units import oxygen_units
from modules.resource_management.ventilator import ventilator
from modules.staff_management.nurse_allocation import nurse_allocation
from modules.staff_management.shift_scheduler import shift_scheduler
from modules.staff_management.workload_prediction import workload_prediction
from modules.treatment_engine.medication_advisor import medication_advisor
from modules.treatment_engine.specialist_recommender import specialist_recommender
from modules.treatment_engine.treatment_recommender import treatment_recommender
from utils.access_control import (
    accessible_medical_records,
    accessible_patient_ids,
    accessible_patients,
    current_doctor,
    current_patient,
    placeholders,
)


FEATURE_PAGES = {
    "Dashboard": None,
    "My Patient Records": None,
    "My Doctor & Records": None,
    "Patient Registration": patient_registration,
    "Patient History": patient_history,
    "Allergies": allergies,
    "Insurance": insurance,
    "Doctor Profiles": doctor_profile,
    "Doctor Recommendations": recommendations,
    "Doctor Schedules": schedules,
    "Book Appointment": booking,
    "Appointment Approval": approval,
    "Appointment Notifications": notifications,
    "Medical Records": medical_records,
    "Prescriptions": prescriptions,
    "Vaccinations": vaccinations,
    "Diagnostics": diagnostics,
    "Disease Prediction": predictor,
    "ICU Prediction": icu_prediction,
    "Mortality Prediction": mortality_model,
    "Recovery Prediction": recovery_model,
    "Stay Duration Prediction": stay_duration,
    "Blood Test Analysis": blood_test_analysis,
    "ECG Analysis": ecg_analysis,
    "MRI Analysis": mri_analysis,
    "OCR Report Reader": ocr_engine,
    "X-Ray Analysis": xray_analysis,
    "Treatment Recommender": treatment_recommender,
    "Medication Advisor": medication_advisor,
    "Specialist Recommender": specialist_recommender,
    "Bed Tracker": bed_tracker,
    "Bed Forecasting": bed_forecasting,
    "Ward Allocation": ward_allocation,
    "Ventilators": ventilator,
    "Oxygen Units": oxygen_units,
    "Equipment": equipment,
    "Resource Forecasting": resource_forecasting,
    "Shift Scheduler": shift_scheduler,
    "Nurse Allocation": nurse_allocation,
    "Staff Workload Prediction": workload_prediction,
    "Emergency Alerts": alerts,
    "Ambulance": ambulance,
    "Emergency Contacts": emergency_contacts,
    "Disease Statistics": disease_statistics,
    "Occupancy Reports": occupancy_reports,
    "Recovery Reports": recovery_reports,
    "Resource Reports": resource_reports,
    "Chatbot": chatbot,
    "Symptom Checker": symptom_checker,
    "Medication Reminder": medication_reminder,
    "Email Service": email_service,
    "SMS Service": sms_service,
    "WhatsApp Service": whatsapp_service,
}

ROLE_PAGES = {
    "Admin": [
        "Dashboard",
        "Patient Registration",
        "Patient History",
        "Doctor Profiles",
        "Doctor Schedules",
        "Book Appointment",
        "Appointment Approval",
        "Appointment Notifications",
        "Medical Records",
        "Diagnostics",
        "Disease Prediction",
        "ICU Prediction",
        "Mortality Prediction",
        "Recovery Prediction",
        "Stay Duration Prediction",
        "Blood Test Analysis",
        "ECG Analysis",
        "MRI Analysis",
        "OCR Report Reader",
        "X-Ray Analysis",
        "Treatment Recommender",
        "Medication Advisor",
        "Specialist Recommender",
        "Bed Tracker",
        "Bed Forecasting",
        "Ward Allocation",
        "Ventilators",
        "Oxygen Units",
        "Equipment",
        "Resource Forecasting",
        "Shift Scheduler",
        "Nurse Allocation",
        "Staff Workload Prediction",
        "Emergency Alerts",
        "Ambulance",
        "Emergency Contacts",
        "Disease Statistics",
        "Occupancy Reports",
        "Recovery Reports",
        "Resource Reports",
        "Email Service",
        "SMS Service",
        "WhatsApp Service",
    ],
    "Doctor": [
        "Dashboard",
        "My Patient Records",
        "Doctor Profiles",
        "Patient History",
        "Medical Records",
        "Prescriptions",
        "Vaccinations",
        "Diagnostics",
        "Disease Prediction",
        "ICU Prediction",
        "Mortality Prediction",
        "Recovery Prediction",
        "Stay Duration Prediction",
        "Blood Test Analysis",
        "ECG Analysis",
        "MRI Analysis",
        "OCR Report Reader",
        "X-Ray Analysis",
        "Treatment Recommender",
        "Medication Advisor",
        "Specialist Recommender",
        "Doctor Recommendations",
        "Doctor Schedules",
        "Appointment Approval",
        "Chatbot",
    ],
    "Nurse": [
        "Dashboard",
        "Patient Registration",
        "Patient History",
        "Allergies",
        "Bed Tracker",
        "Bed Forecasting",
        "Ward Allocation",
        "Medication Reminder",
        "Nurse Allocation",
        "Staff Workload Prediction",
        "Emergency Alerts",
        "Oxygen Units",
        "Equipment",
        "Resource Forecasting",
    ],
    "Patient": [
        "Dashboard",
        "My Doctor & Records",
        "Patient Registration",
        "Book Appointment",
        "Patient History",
        "Allergies",
        "Insurance",
        "Doctor Recommendations",
        "Treatment Recommender",
        "Medication Advisor",
        "Specialist Recommender",
        "Symptom Checker",
        "Medication Reminder",
        "Chatbot",
        "Emergency Contacts",
    ],
}


def rows(query, params=()):
    return [dict(row) for row in fetch_all(query, params)]


def ensure_user_link_columns():
    required_columns = {
        "patients": {
            "doctor_id": "INTEGER",
            "user_id": "INTEGER",
            "username": "TEXT",
        },
        "doctors": {
            "user_id": "INTEGER",
            "username": "TEXT",
        },
        "medical_records": "doctor_id",
    }
    for table_name, columns in required_columns.items():
        existing_columns = {
            row["name"]
            for row in fetch_all(f"PRAGMA table_info({table_name})")
        }
        if not existing_columns:
            continue
        if isinstance(columns, str):
            columns = {columns: "INTEGER"}
        for column_name, column_type in columns.items():
            if column_name not in existing_columns:
                execute_query(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")


def count_table(table_name):
    row = fetch_one(f"SELECT COUNT(*) AS total FROM {table_name}")
    return int(row["total"]) if row else 0


def insert_row(table_name, values):
    existing_columns = {row["name"] for row in fetch_all(f"PRAGMA table_info({table_name})")}
    columns = [column for column in values if column in existing_columns]
    if not columns:
        return
    placeholders = ", ".join("?" for _ in columns)
    column_list = ", ".join(columns)
    params = tuple(values[column] for column in columns)
    execute_query(f"INSERT INTO {table_name} ({column_list}) VALUES ({placeholders})", params)


def prepare_app_data():
    initialize_database()
    ensure_user_link_columns()


def ensure_role_profile(user):
    ensure_user_link_columns()
    user_id = user["user_id"]
    username = user["username"]
    role = user["role"]

    if role == "Patient":
        patient = fetch_one(
            "SELECT patient_id FROM patients WHERE user_id = ? OR username = ?",
            (user_id, username),
        )
        if not patient:
            execute_query(
                """
                UPDATE patients
                SET user_id = ?, username = ?
                WHERE patient_id = (
                    SELECT patient_id
                    FROM patients
                    WHERE LOWER(full_name) = LOWER(?)
                      AND (user_id IS NULL OR user_id = 0)
                      AND (username IS NULL OR TRIM(username) = '')
                    ORDER BY patient_id DESC
                    LIMIT 1
                )
                """,
                (user_id, username, username),
            )

    if role == "Doctor":
        doctor = fetch_one(
            "SELECT doctor_id FROM doctors WHERE user_id = ? OR username = ?",
            (user_id, username),
        )
        if not doctor:
            execute_query(
                """
                UPDATE doctors
                SET user_id = ?, username = ?
                WHERE doctor_id = (
                    SELECT doctor_id
                    FROM doctors
                    WHERE LOWER(doctor_name) = LOWER(?)
                      AND (user_id IS NULL OR user_id = 0)
                      AND (username IS NULL OR TRIM(username) = '')
                    ORDER BY doctor_id DESC
                    LIMIT 1
                )
                """,
                (user_id, username, username),
            )


def configure_page():
    st.set_page_config(page_title=APP_NAME, page_icon="H", layout="wide")
    st.markdown(
        """
        <style>
        .stApp { background: #f5f7fb; }
        .block-container { padding-top: 1.25rem; max-width: 1280px; }
        [data-testid="stMetricValue"] { font-size: 2rem; }
        [data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #dce4ee; }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: #172033;
        }
        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #dce4ee;
            border-radius: 8px;
            padding: 14px;
            box-shadow: 0 8px 22px rgba(23, 32, 51, 0.04);
        }
        .app-title { font-size: 1.8rem; font-weight: 700; margin-bottom: .25rem; }
        .subtle { color: #607086; margin-bottom: 1rem; }
        .user-card {
            background: #edf8fa;
            border: 1px solid #ccecef;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 12px;
        }
        .user-card strong { color: #05606a; }
        .section-card {
            background: #ffffff;
            border: 1px solid #dce4ee;
            border-radius: 8px;
            padding: 14px 16px;
            margin: 10px 0 16px;
        }
        h1, h2, h3 { letter-spacing: 0; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialize_state():
    st.session_state.setdefault("logged_in", False)
    st.session_state.setdefault("user_id", None)
    st.session_state.setdefault("username", "")
    st.session_state.setdefault("role", "")


def register_page():
    st.markdown('<div class="app-title">Create Account</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Register a new user for the healthcare system.</div>', unsafe_allow_html=True)

    with st.form("register_form", clear_on_submit=False):
        username = st.text_input("Username")
        role = st.selectbox("Role", AVAILABLE_ROLES)
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Register")

    if not submitted:
        return

    username = username.strip()
    if not username:
        st.error("Username is required.")
        return
    if password != confirm_password:
        st.error("Passwords do not match.")
        return
    if not validate_password(password):
        st.error("Password must be at least 8 characters and include uppercase, lowercase, and a number.")
        return
    if fetch_one("SELECT * FROM users WHERE username = ?", (username,)):
        st.error("Username already exists.")
        return

    execute_query(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, hash_password(password), role),
    )
    user = fetch_one("SELECT * FROM users WHERE username = ?", (username,))
    if user:
        ensure_role_profile(user)
    st.success("Registration successful. Go to the Login page to continue.")


def login_page():
    st.markdown('<div class="app-title">Login</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Sign in to access dashboard and hospital modules.</div>', unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if not submitted:
        return

    user = fetch_one("SELECT * FROM users WHERE username = ?", (username.strip(),))
    if not user or not verify_password(password, user["password"]):
        st.error("Invalid username or password.")
        return

    st.session_state.logged_in = True
    st.session_state.user_id = user["user_id"]
    st.session_state.username = user["username"]
    st.session_state.role = user["role"]
    ensure_role_profile(user)
    st.success("Login successful.")
    st.rerun()


def logout_button():
    st.sidebar.markdown(
        f"""
        <div class="user-card">
            <strong>{st.session_state.username}</strong><br>
            <span>{st.session_state.role}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()


def operational_overview():
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Patients", count_table("patients"))
    col2.metric("Doctors", count_table("doctors"))
    col3.metric("Appointments", count_table("appointments"))
    col4.metric("Resources", count_table("resources"))

    resources = pd.DataFrame(rows("SELECT resource_name, quantity, available FROM resources ORDER BY resource_name"))
    predictions = pd.DataFrame(rows("SELECT disease, AVG(probability) AS probability FROM predictions GROUP BY disease"))
    beds = pd.DataFrame(rows("SELECT status, COUNT(*) AS total FROM beds GROUP BY status"))

    left, right = st.columns([1.35, 1])
    with left:
        st.subheader("Resource Availability")
        if resources.empty:
            st.info("No resource data available.")
        else:
            chart_df = resources.melt(
                id_vars=["resource_name"],
                value_vars=["quantity", "available"],
                var_name="Metric",
                value_name="Count",
            )
            fig = px.bar(chart_df, x="resource_name", y="Count", color="Metric", barmode="group")
            st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Bed Occupancy")
        if beds.empty:
            st.info("No bed data available.")
        else:
            fig = px.pie(beds, names="status", values="total", hole=0.45)
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Average Disease Risk")
    if predictions.empty:
        st.info("No prediction data available.")
    else:
        predictions["Risk %"] = (predictions["probability"] * 100).round(0)
        fig = px.bar(predictions, x="disease", y="Risk %", color="Risk %", range_y=[0, 100])
        st.plotly_chart(fig, use_container_width=True)


def admin_home():
    st.markdown('<div class="app-title">Admin Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">System-wide overview for hospital operations and resource control.</div>', unsafe_allow_html=True)
    operational_overview()
    with st.expander("Financial overview"):
        admin_dashboard()


def doctor_home():
    st.markdown('<div class="app-title">Doctor Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Clinical worklist for appointments, diagnosis, prescriptions, and patient records.</div>', unsafe_allow_html=True)
    doctor = current_doctor()
    if not doctor:
        st.info("No doctor profile is linked to this login yet.")
        return
    doctor_id = doctor["doctor_id"]
    c1, c2, c3 = st.columns(3)
    pending = fetch_one(
        "SELECT COUNT(*) AS total FROM appointments WHERE doctor_id = ? AND status = 'Pending'",
        (doctor_id,),
    )
    records = fetch_one(
        "SELECT COUNT(*) AS total FROM medical_records WHERE doctor_id = ?",
        (doctor_id,),
    )
    diagnostics = fetch_one(
        """
        SELECT COUNT(DISTINCT dg.diagnostic_id) AS total
        FROM diagnostics dg
        LEFT JOIN patients p ON dg.patient_id = p.patient_id
        LEFT JOIN appointments a ON p.patient_id = a.patient_id
        WHERE p.doctor_id = ? OR a.doctor_id = ?
        """,
        (doctor_id, doctor_id),
    )
    c1.metric("Pending Appointments", int(pending["total"]) if pending else 0)
    c2.metric("Medical Records", int(records["total"]) if records else 0)
    c3.metric("Diagnostics", int(diagnostics["total"]) if diagnostics else 0)

    appointments = pd.DataFrame(rows(
        """
        SELECT a.*, p.full_name AS patient_name
        FROM appointments a
        LEFT JOIN patients p ON a.patient_id = p.patient_id
        WHERE a.doctor_id = ?
        ORDER BY a.appointment_id DESC
        LIMIT 8
        """,
        (doctor_id,),
    ))
    if appointments.empty:
        st.info("No appointments found yet.")
    else:
        st.subheader("Recent Appointments")
        st.dataframe(appointments, use_container_width=True)

    with st.expander("Doctor statistics"):
        doctor_dashboard()


def nurse_home():
    st.markdown('<div class="app-title">Nurse Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Bed allocation, patient support, medication reminders, and ward workload.</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Beds", count_table("beds"))
    c2.metric("Nurse Allocations", count_table("nurse_allocations"))
    c3.metric("Medication Reminders", count_table("medication_reminders"))
    c4.metric("Emergency Alerts", count_table("emergency_alerts"))

    beds = pd.DataFrame(rows("SELECT status, COUNT(*) AS total FROM beds GROUP BY status"))
    if not beds.empty:
        fig = px.pie(beds, names="status", values="total", title="Bed Status", hole=0.45)
        st.plotly_chart(fig, use_container_width=True)


def patient_home():
    st.markdown('<div class="app-title">Patient Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Personal appointment, health history, reminders, and symptom support.</div>', unsafe_allow_html=True)
    patient_ids = accessible_patient_ids()
    if not patient_ids:
        st.info("No patient profile is linked to this login yet.")
        return
    id_placeholders = placeholders(patient_ids)
    params = tuple(patient_ids)
    c1, c2, c3 = st.columns(3)
    appointments = fetch_one(
        f"SELECT COUNT(*) AS total FROM appointments WHERE patient_id IN ({id_placeholders})",
        params,
    )
    records = fetch_one(
        f"SELECT COUNT(*) AS total FROM medical_records WHERE patient_id IN ({id_placeholders})",
        params,
    )
    reminders = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM medication_reminders mr
        LEFT JOIN patients p ON mr.patient_name = p.full_name
        WHERE p.patient_id IN ({})
        """.format(id_placeholders),
        params,
    )
    c1.metric("Appointments", int(appointments["total"]) if appointments else 0)
    c2.metric("Health Records", int(records["total"]) if records else 0)
    c3.metric("Reminders", int(reminders["total"]) if reminders else 0)

    left, right = st.columns(2)
    with left:
        st.subheader("Quick Help")
        st.write("- Book an appointment")
        st.write("- Check symptoms")
        st.write("- Review reminders")
        st.write("- Save emergency contacts")
    with right:
        patient_dashboard()


def doctor_patient_records_page():
    ensure_user_link_columns()

    st.markdown('<div class="app-title">My Patient Records</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Doctor view: assigned patients and their clinical records.</div>', unsafe_allow_html=True)

    doctor = current_doctor()
    if not doctor:
        st.info("No doctor profile is linked to this login yet.")
        return
    doctor_id = doctor["doctor_id"]
    st.success(f"Showing records for {doctor['doctor_name']} - {doctor['specialization'] or 'Not specified'}")

    patients = pd.DataFrame([dict(row) for row in accessible_patients()])
    records = pd.DataFrame([dict(row) for row in accessible_medical_records()])

    c1, c2 = st.columns(2)
    c1.metric("Assigned Patients", 0 if patients.empty else len(patients))
    c2.metric("Medical Records", 0 if records.empty else len(records))

    st.write("### Assigned Patients")
    if patients.empty:
        st.info("No patients assigned to this doctor.")
    else:
        st.dataframe(patients, use_container_width=True)

    st.write("### Patient Medical Records")
    if records.empty:
        st.info("No records written by this doctor yet.")
    else:
        st.dataframe(records, use_container_width=True)


def patient_doctor_records_page():
    ensure_user_link_columns()

    st.markdown('<div class="app-title">My Doctor & Records</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Patient view: assigned doctor and personal medical records.</div>', unsafe_allow_html=True)

    patient = current_patient()
    if not patient:
        st.info("No patient profile is linked to this login yet.")
        return

    patient_id = patient["patient_id"]

    c1, c2, c3 = st.columns(3)
    c1.metric("Patient ID", patient["patient_id"])
    c2.metric("Age", patient["age"] or 0)
    c3.metric("Blood Group", patient["blood_group"] or "NA")

    st.write("### Assigned Doctor")
    if patient["doctor_name"]:
        st.success(f"{patient['doctor_name']} - {patient['specialization']}")
        st.write(f"Phone: {patient['doctor_phone'] or 'NA'}")
        st.write(f"Email: {patient['doctor_email'] or 'NA'}")
    else:
        st.warning("No doctor assigned yet.")

    medical_records = pd.DataFrame(rows(
        """
        SELECT record_id, report_date, diagnosis, treatment, prescription
        FROM medical_records
        WHERE patient_id = ?
        ORDER BY record_id DESC
        """,
        (patient_id,)
    ))

    st.write("### My Medical Records")
    if medical_records.empty:
        st.info("No medical records found for this patient.")
    else:
        st.dataframe(medical_records, use_container_width=True)


def dashboard_page():
    role = st.session_state.get("role", "Patient")
    if role == "Admin":
        admin_home()
    elif role == "Doctor":
        doctor_home()
    elif role == "Nurse":
        nurse_home()
    else:
        patient_home()


def run_feature_page(page_name):
    if page_name == "Dashboard":
        dashboard_page()
        return
    if page_name == "My Patient Records":
        doctor_patient_records_page()
        return
    if page_name == "My Doctor & Records":
        patient_doctor_records_page()
        return

    page_func = FEATURE_PAGES[page_name]
    try:
        page_func()
    except Exception as exc:
        st.error(f"Could not open {page_name}: {exc}")
        st.info("The page loaded safely, but this module needs a small data or schema adjustment.")


def main():
    configure_page()
    initialize_state()
    prepare_app_data()

    st.sidebar.title("AI Healthcare System")

    if not st.session_state.logged_in:
        auth_page = st.sidebar.radio("Account", ["Login", "Register"], index=0)
        st.title(APP_NAME)
        if auth_page == "Login":
            login_page()
        else:
            register_page()
        return

    logout_button()
    allowed_pages = ROLE_PAGES.get(st.session_state.role, ROLE_PAGES["Patient"])
    page_name = st.sidebar.selectbox("Modules", allowed_pages)
    st.title(APP_NAME)
    run_feature_page(page_name)


if __name__ == "__main__":
    main()
