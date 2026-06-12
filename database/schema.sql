-- ==========================================
-- AI Healthcare System Database Schema
-- ==========================================

-- USERS
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PATIENTS
CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    doctor_id INTEGER,
    user_id INTEGER,
    username TEXT,
    age INTEGER,
    gender TEXT,
    blood_group TEXT,
    phone TEXT,
    address TEXT,
    insurance_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DOCTORS
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_name TEXT NOT NULL,
    user_id INTEGER,
    username TEXT,
    specialization TEXT,
    experience INTEGER,
    phone TEXT,
    email TEXT
);

-- APPOINTMENTS
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_date TEXT,
    status TEXT DEFAULT 'Pending',
    FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id)
);

-- MEDICAL RECORDS
CREATE TABLE IF NOT EXISTS medical_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    diagnosis TEXT,
    treatment TEXT,
    prescription TEXT,
    report_date TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
);

-- ALLERGIES
CREATE TABLE IF NOT EXISTS allergies (
    allergy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    allergy_name TEXT,
    severity TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
);

-- INSURANCE
CREATE TABLE IF NOT EXISTS insurance (
    insurance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    provider_name TEXT,
    policy_number TEXT,
    expiry_date TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
);

-- BEDS
CREATE TABLE IF NOT EXISTS beds (
    bed_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ward_name TEXT,
    bed_number TEXT,
    status TEXT
);

-- STAFF
CREATE TABLE IF NOT EXISTS staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    role TEXT,
    shift TEXT
);

-- RESOURCES
CREATE TABLE IF NOT EXISTS resources (
    resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_name TEXT,
    quantity INTEGER,
    available INTEGER
);

-- PREDICTIONS
CREATE TABLE IF NOT EXISTS predictions (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    disease TEXT,
    prediction_result TEXT,
    probability REAL,
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- REPORTS
CREATE TABLE IF NOT EXISTS reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    report_type TEXT,
    report_file TEXT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- EMERGENCY CONTACTS
CREATE TABLE IF NOT EXISTS emergency_contacts (
    contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    contact_name TEXT,
    relationship TEXT,
    phone TEXT,
    phone_number TEXT
);

-- NOTIFICATIONS
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT,
    status TEXT DEFAULT 'Unread',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- WARD ALLOCATIONS
CREATE TABLE IF NOT EXISTS ward_allocations (
    allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    bed_id INTEGER,
    allocation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DOCTOR SCHEDULES
CREATE TABLE IF NOT EXISTS doctor_schedules (
    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER,
    schedule_date TEXT,
    shift TEXT
);

-- DIAGNOSTICS
CREATE TABLE IF NOT EXISTS diagnostics (
    diagnostic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    test_name TEXT,
    result TEXT,
    remarks TEXT,
    test_date TEXT
);

-- PRESCRIPTIONS
CREATE TABLE IF NOT EXISTS prescriptions (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    medicine_name TEXT,
    dosage TEXT,
    duration TEXT,
    instructions TEXT,
    notes TEXT
);

-- VACCINATIONS
CREATE TABLE IF NOT EXISTS vaccinations (
    vaccination_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    vaccine_name TEXT,
    vaccination_date TEXT,
    next_due_date TEXT
);

-- EMERGENCY ALERTS
CREATE TABLE IF NOT EXISTS emergency_alerts (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    alert_type TEXT,
    severity TEXT,
    message TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AMBULANCES
CREATE TABLE IF NOT EXISTS ambulances (
    ambulance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ambulance_number TEXT,
    driver_name TEXT,
    phone TEXT,
    status TEXT
);

-- EMAIL NOTIFICATIONS
CREATE TABLE IF NOT EXISTS email_notifications (
    email_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient TEXT,
    recipient_email TEXT,
    subject TEXT,
    message TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SMS NOTIFICATIONS
CREATE TABLE IF NOT EXISTS sms_notifications (
    sms_id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT,
    mobile_number TEXT,
    message TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- WHATSAPP NOTIFICATIONS
CREATE TABLE IF NOT EXISTS whatsapp_notifications (
    whatsapp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT,
    mobile_number TEXT,
    message TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MEDICATION REMINDERS
CREATE TABLE IF NOT EXISTS medication_reminders (
    reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    patient_name TEXT,
    medicine_name TEXT,
    dosage TEXT,
    reminder_time TEXT
);

-- EQUIPMENT
CREATE TABLE IF NOT EXISTS equipment (
    equipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_name TEXT,
    quantity INTEGER,
    status TEXT
);

-- OXYGEN UNITS
CREATE TABLE IF NOT EXISTS oxygen_units (
    oxygen_id INTEGER PRIMARY KEY AUTOINCREMENT,
    unit_name TEXT,
    quantity INTEGER,
    status TEXT
);

-- VENTILATORS
CREATE TABLE IF NOT EXISTS ventilators (
    ventilator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ventilator_name TEXT,
    status TEXT,
    location TEXT
);

-- NURSE ALLOCATIONS
CREATE TABLE IF NOT EXISTS nurse_allocations (
    allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nurse_name TEXT,
    ward_name TEXT,
    patient_count INTEGER
);

-- STAFF SHIFTS
CREATE TABLE IF NOT EXISTS staff_shifts (
    shift_id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_name TEXT,
    role TEXT,
    shift_date TEXT,
    shift_type TEXT
);
