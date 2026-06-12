import re


def validate_email(email):

    pattern = (
        r"^[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}$"
    )

    return bool(
        re.match(
            pattern,
            email
        )
    )


def validate_phone(phone):

    pattern = r"^[0-9]{10}$"

    return bool(
        re.match(
            pattern,
            phone
        )
    )


def validate_age(age):

    try:
        age = int(age)

        return (
            age >= 0
            and age <= 120
        )

    except Exception:
        return False


def validate_required(value):

    return (
        value is not None
        and str(value).strip() != ""
    )