from __future__ import annotations

import hashlib
import secrets
from datetime import UTC, datetime, timedelta

import bcrypt

OTP_EXPIRY_MINUTES = 10
MAX_VERIFY_ATTEMPTS = 5
MAX_REQUESTS_PER_WINDOW = 3
REQUEST_WINDOW_MINUTES = 15
MIN_PASSWORD_LENGTH = 8


def normalize_email(email: str) -> str:
    return email.strip().lower()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str | None) -> bool:
    if not password_hash:
        return False
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False


def generate_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_otp(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


def verify_otp(code: str, code_hash: str) -> bool:
    return secrets.compare_digest(hash_otp(code), code_hash)


def generate_challenge_token() -> str:
    return secrets.token_urlsafe(32)


def otp_expires_at(*, now: datetime | None = None) -> datetime:
    current = now or datetime.now(UTC)
    return current + timedelta(minutes=OTP_EXPIRY_MINUTES)


def request_window_start(*, now: datetime | None = None) -> datetime:
    current = now or datetime.now(UTC)
    return current - timedelta(minutes=REQUEST_WINDOW_MINUTES)


def validate_password(password: str) -> str | None:
    if len(password) < MIN_PASSWORD_LENGTH:
        return f"Password must be at least {MIN_PASSWORD_LENGTH} characters."
    return None
