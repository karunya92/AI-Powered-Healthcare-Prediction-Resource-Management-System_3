"""
Application Settings
"""

import os

# Application Information
APP_NAME = "AI-Powered Healthcare Prediction & Resource Management System"
APP_VERSION = "1.0.0"

# Database
DATABASE_PATH = ":memory:"
PLACEHOLDER_DATABASE_PATH = os.path.join("database", "healthcare.db")

# Security
SECRET_KEY = "healthcare_secret_key_2026"
DEBUG = True

# File Upload Settings
UPLOAD_FOLDER = "uploads"
MAX_FILE_SIZE_MB = 20

# ML Models Path
MODEL_PATH = "ml_models"

# Datasets Path
DATASET_PATH = "datasets"

# Dashboard Settings
DEFAULT_THEME = "light"

# Hospital Settings
TOTAL_BEDS = 200
TOTAL_DOCTORS = 50
TOTAL_NURSES = 120

# Notification Settings
EMAIL_ENABLED = False
SMS_ENABLED = False
WHATSAPP_ENABLED = False
