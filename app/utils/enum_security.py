from cryptography.fernet import Fernet, InvalidToken
from app.constants.secure_fields import SecureFields
from app.core.config import get_settings
from typing import Any
import logging


# Load settings ONCE
settings = get_settings()


# Collect sensitive field names
SECURE_KEYS = {field.value for field in SecureFields}


# 🔐 Load encryption key from ENV (MANDATORY)
SECRET_KEY = settings.ENUM_ENCRYPTION_KEY


# 🚨 Hard fail if key missing (THIS IS GOOD)
if not SECRET_KEY:
    raise RuntimeError(
        "ENUM_ENCRYPTION_KEY is missing. "
        "Encryption/Decryption cannot work without a stable key."
    )


# Fernet expects BYTES
fernet = Fernet(SECRET_KEY.encode())


# -------------------- CORE FUNCTIONS --------------------

def encrypt_value(value: Any):
    """
    Encrypt a single value.
    """
    if value is None:
        return None

    return fernet.encrypt(str(value).encode()).decode()


def decrypt_value(value: Any):
    """
    Decrypt a single value.
    If value is not encrypted, return as-is.
    """
    if value is None:
        return None

    try:
        return fernet.decrypt(value.encode()).decode()
    except InvalidToken:
        # Value was not encrypted with this key
        return value


def encrypt_secure_fields(data: Any):
    """
    Recursively encrypt sensitive fields.
    """
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if key in SECURE_KEYS:
                result[key] = encrypt_value(value)
            else:
                result[key] = encrypt_secure_fields(value)
        return result

    if isinstance(data, list):
        return [encrypt_secure_fields(item) for item in data]

    return data


def decrypt_secure_fields(data: Any):
    """
    Recursively decrypt sensitive fields.
    """
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if key in SECURE_KEYS:
                result[key] = decrypt_value(value)
            else:
                result[key] = decrypt_secure_fields(value)
        return result

    if isinstance(data, list):
        return [decrypt_secure_fields(item) for item in data]

    return data
