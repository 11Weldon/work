import hashlib
from uuid import uuid4


def hash_password_sha256(password: str) -> str:
    salt = uuid4().hex
    return (
        hashlib.sha256(salt.encode() + password.encode()).hexdigest()
        + ":"
        + salt
        + ":sha256"
    )