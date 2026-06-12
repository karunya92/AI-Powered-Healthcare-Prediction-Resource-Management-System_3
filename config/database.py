"""
Database Configuration
"""

import sqlite3
from config.settings import DATABASE_PATH

_MEMORY_URI = "file:healthcare_shared_runtime?mode=memory&cache=shared"
_MEMORY_KEEPER = None
_MIGRATIONS_READY = False


def _memory_connection():
    global _MEMORY_KEEPER
    if _MEMORY_KEEPER is None:
        _MEMORY_KEEPER = sqlite3.connect(
            _MEMORY_URI,
            uri=True,
            check_same_thread=False
        )
        _MEMORY_KEEPER.row_factory = sqlite3.Row

    conn = sqlite3.connect(
        _MEMORY_URI,
        uri=True,
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row
    return conn


def get_connection():
    """
    Create database connection
    """
    if DATABASE_PATH == ":memory:":
        return _memory_connection()

    conn = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """
    Create all required tables
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Patients
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        doctor_id INTEGER,
        age INTEGER,
        gender TEXT,
        blood_group TEXT,
        phone TEXT,
        address TEXT,
        insurance_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Doctors
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors(
        doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_name TEXT,
        specialization TEXT,
        experience INTEGER,
        phone TEXT,
        email TEXT
    )
    """)

    # Appointments
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments(
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        appointment_date TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    # Medical Records
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medical_records(
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        diagnosis TEXT,
        treatment TEXT,
        prescription TEXT,
        report_date TEXT
    )
    """)

    # Beds
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS beds(
        bed_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ward_name TEXT,
        bed_number TEXT,
        status TEXT
    )
    """)

    # Staff
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff(
        staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        role TEXT,
        shift TEXT
    )
    """)

    # Resources
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resources(
        resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
        resource_name TEXT,
        quantity INTEGER,
        available INTEGER
    )
    """)

    # Disease Predictions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions(
        prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        disease TEXT,
        prediction_result TEXT,
        probability REAL,
        prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS allergies(
        allergy_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        allergy_name TEXT,
        severity TEXT
    );

    CREATE TABLE IF NOT EXISTS insurance(
        insurance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        provider_name TEXT,
        policy_number TEXT,
        expiry_date TEXT
    );

    CREATE TABLE IF NOT EXISTS reports(
        report_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        report_type TEXT,
        report_file TEXT,
        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS emergency_contacts(
        contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        contact_name TEXT,
        relationship TEXT,
        phone TEXT,
        phone_number TEXT
    );

    CREATE TABLE IF NOT EXISTS notifications(
        notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        status TEXT DEFAULT 'Unread',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS ward_allocations(
        allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        bed_id INTEGER,
        allocation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS doctor_schedules(
        schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER,
        schedule_date TEXT,
        shift TEXT
    );

    CREATE TABLE IF NOT EXISTS diagnostics(
        diagnostic_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        test_name TEXT,
        result TEXT,
        remarks TEXT,
        test_date TEXT
    );

    CREATE TABLE IF NOT EXISTS prescriptions(
        prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        medicine_name TEXT,
        dosage TEXT,
        duration TEXT,
        instructions TEXT,
        notes TEXT
    );

    CREATE TABLE IF NOT EXISTS vaccinations(
        vaccination_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        vaccine_name TEXT,
        vaccination_date TEXT,
        next_due_date TEXT
    );

    CREATE TABLE IF NOT EXISTS emergency_alerts(
        alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        alert_type TEXT,
        severity TEXT,
        message TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS ambulances(
        ambulance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ambulance_number TEXT,
        driver_name TEXT,
        phone TEXT,
        status TEXT
    );

    CREATE TABLE IF NOT EXISTS email_notifications(
        email_id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipient TEXT,
        recipient_email TEXT,
        subject TEXT,
        message TEXT,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS sms_notifications(
        sms_id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT,
        mobile_number TEXT,
        message TEXT,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS whatsapp_notifications(
        whatsapp_id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT,
        mobile_number TEXT,
        message TEXT,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS medication_reminders(
        reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        medicine_name TEXT,
        dosage TEXT,
        reminder_time TEXT
    );

    CREATE TABLE IF NOT EXISTS equipment(
        equipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        equipment_name TEXT,
        quantity INTEGER,
        status TEXT
    );

    CREATE TABLE IF NOT EXISTS oxygen_units(
        oxygen_id INTEGER PRIMARY KEY AUTOINCREMENT,
        unit_name TEXT,
        quantity INTEGER,
        status TEXT
    );

    CREATE TABLE IF NOT EXISTS ventilators(
        ventilator_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ventilator_name TEXT,
        status TEXT,
        location TEXT
    );

    CREATE TABLE IF NOT EXISTS nurse_allocations(
        allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nurse_name TEXT,
        ward_name TEXT,
        patient_count INTEGER
    );

    CREATE TABLE IF NOT EXISTS staff_shifts(
        shift_id INTEGER PRIMARY KEY AUTOINCREMENT,
        staff_name TEXT,
        role TEXT,
        shift_date TEXT,
        shift_type TEXT
    );
    """)

    conn.commit()
    run_migrations(conn)
    conn.close()


def _ensure_column(conn, table_name, column_name, column_type):
    table_exists = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,)
    ).fetchone()
    if not table_exists:
        return

    columns = [row["name"] for row in conn.execute(f"PRAGMA table_info({table_name})").fetchall()]
    if column_name not in columns:
        try:
            conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
            conn.commit()
        except sqlite3.OperationalError as exc:
            if "duplicate column name" not in str(exc).lower():
                raise


def table_columns(table_name):
    """
    Return existing column names for a table.
    """
    conn = get_connection()
    try:
        return [
            row["name"]
            for row in conn.execute(f"PRAGMA table_info({table_name})").fetchall()
        ]
    finally:
        conn.close()


def run_migrations(conn=None):
    """
    Add columns required by newer UI pages when an older database already exists.
    """
    owns_connection = conn is None
    if conn is None:
        conn = get_connection()

    _ensure_column(conn, "patients", "doctor_id", "INTEGER")
    _ensure_column(conn, "patients", "user_id", "INTEGER")
    _ensure_column(conn, "patients", "username", "TEXT")
    _ensure_column(conn, "doctors", "user_id", "INTEGER")
    _ensure_column(conn, "doctors", "username", "TEXT")
    _ensure_column(conn, "medical_records", "doctor_id", "INTEGER")
    _ensure_column(conn, "medication_reminders", "patient_id", "INTEGER")
    _ensure_column(conn, "emergency_contacts", "patient_id", "INTEGER")
    _ensure_column(conn, "emergency_contacts", "phone_number", "TEXT")
    _ensure_column(conn, "emergency_alerts", "patient_id", "INTEGER")

    if owns_connection:
        conn.close()


def ensure_database_ready():
    global _MIGRATIONS_READY
    if not _MIGRATIONS_READY:
        initialize_database()
        _MIGRATIONS_READY = True


def execute_query(query, params=()):
    ensure_database_ready()
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError as exc:
        if _is_missing_column_error(exc):
            run_migrations(conn)
            cursor.execute(query, params)
        else:
            raise

    conn.commit()
    conn.close()


def fetch_all(query, params=()):
    ensure_database_ready()
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError as exc:
        if _is_missing_column_error(exc):
            run_migrations(conn)
            cursor.execute(query, params)
        else:
            raise

    rows = cursor.fetchall()

    conn.close()

    return rows


def fetch_one(query, params=()):
    ensure_database_ready()
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError as exc:
        if _is_missing_column_error(exc):
            run_migrations(conn)
            cursor.execute(query, params)
        else:
            raise

    row = cursor.fetchone()

    conn.close()

    return row


def _is_missing_column_error(exc):
    message = str(exc).lower()
    return (
        "no such column" in message
        or "no column named" in message
        or "has no column named" in message
    )
