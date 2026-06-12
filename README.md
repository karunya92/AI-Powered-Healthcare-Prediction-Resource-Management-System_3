# AI-Powered Healthcare Prediction & Resource Management System

A Streamlit healthcare operations app for hospital workflow management, disease-risk prediction, EHR records, appointments, resources, notifications, report analysis, treatment guidance, outcome prediction, reporting, and analytics.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The app starts at `http://localhost:8501`.

You can also run:

```bash
python run_app.py
```

## Main App Areas

- Authentication and role-based access for Admin, Doctor, Nurse, and Patient users
- Patient registration, history, allergies, and insurance
- Doctor profiles, schedules, and specialist recommendations
- Appointment booking, approval, and notifications
- EHR records, prescriptions, vaccinations, diagnostics, and report analysis
- Disease, ICU, mortality, recovery, and stay-duration prediction
- Bed, ward, ventilator, oxygen, equipment, resource, and staff management
- Emergency alerts, ambulances, emergency contacts, and notification tools
- Chatbot, symptom checker, medication reminders, treatment recommendations, and reports

## Notes

The files under `ml_models/` are placeholders. Replace the rule-based prediction modules with trained models when your `.pkl` files are available.

By default the app uses an in-memory SQLite database for clean Streamlit sessions. `database/schema.sql` mirrors the runtime schema for deployments that initialize SQLite directly.

This project is educational starter code and is not a medical device. Clinical decisions must be reviewed by licensed healthcare professionals.
