import re

def is_valid_gmail(email: str) -> bool:
    if not email or " " in email:
        return False
    return email.endswith("@gmail.com")


def is_valid_email(email: str) -> bool:
    """Accept any reasonable email format (e.g. for admin login)."""
    if not email:
        return False
    s = str(email).strip()
    if " " in s or "@" not in s:
        return False
    return "." in s.split("@")[-1]


def validate_password(password: str):
    if not password:
        return False, "Password is required"

    if " " in password:
        return False, "Password must not contain spaces"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r"[\d]", password):
        return False, "Password must contain at least one digit"

    if not re.search(r"[$@#]", password):
        return False, "Password must contain at least one special character ($ @ #)"

    if re.search(r"[^A-Za-z0-9$@#]", password):
        return False, "Only $ @ # special characters are allowed"

    return True, ""
