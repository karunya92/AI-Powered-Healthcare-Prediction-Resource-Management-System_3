import hashlib


def hash_password(password):
    """
    Hash password using SHA256
    """

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def verify_password(
    password,
    hashed_password
):
    """
    Verify password
    """

    return (
        hash_password(password)
        == hashed_password
    )


def encrypt_text(text):
    """
    Simple text encryption
    """

    return hashlib.md5(
        text.encode()
    ).hexdigest()