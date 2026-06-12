"""
Authentication Configuration
"""

import hashlib
import secrets

# Session Configuration
SESSION_TIMEOUT_MINUTES = 60

# Password Rules
MIN_PASSWORD_LENGTH = 8

# Roles
ADMIN = "Admin"
DOCTOR = "Doctor"
NURSE = "Nurse"
PATIENT = "Patient"

AVAILABLE_ROLES = [
    ADMIN,
    DOCTOR,
    NURSE,
    PATIENT
]


def hash_password(password):
    """
    Hash password using SHA256
    """
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def verify_password(password, hashed_password):
    """
    Verify password
    """
    return (
        hashlib.sha256(
            password.encode()
        ).hexdigest()
        == hashed_password
    )


def generate_token():
    """
    Generate session token
    """
    return secrets.token_hex(32)


def validate_password(password):
    """
    Password validation
    """

    if len(password) < MIN_PASSWORD_LENGTH:
        return False

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    return has_upper and has_lower and has_digit