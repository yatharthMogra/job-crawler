from __future__ import annotations

import uuid
from datetime import UTC, datetime

import structlog
from fastapi import HTTPException, status
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.models.auth_challenge import AuthChallenge
from app.models.candidate import Candidate
from app.services.auth_crypto import (
    MAX_REQUESTS_PER_WINDOW,
    MAX_VERIFY_ATTEMPTS,
    OTP_EXPIRY_MINUTES,
    generate_challenge_token,
    generate_otp,
    hash_otp,
    hash_password,
    normalize_email,
    otp_expires_at,
    request_window_start,
    validate_password,
    verify_otp,
    verify_password,
)
from app.services.email import render_otp_email, send_email

log = structlog.get_logger(__name__)

GOOGLE_SIGNIN_MESSAGE = "This account uses Google sign-in. Please continue with Google."
INVALID_CREDENTIALS_MESSAGE = "Incorrect email or password."
ACCOUNT_EXISTS_MESSAGE = "An account with this email already exists."


async def _count_recent_requests(db: AsyncSession, email: str, purpose: str) -> int:
    result = await db.execute(
        select(func.count())
        .select_from(AuthChallenge)
        .where(
            AuthChallenge.email == email,
            AuthChallenge.purpose == purpose,
            AuthChallenge.created_at >= request_window_start(),
        )
    )
    return int(result.scalar_one())


async def _invalidate_open_challenges(db: AsyncSession, email: str, purpose: str) -> None:
    await db.execute(
        update(AuthChallenge)
        .where(
            AuthChallenge.email == email,
            AuthChallenge.purpose == purpose,
            AuthChallenge.consumed_at.is_(None),
        )
        .values(consumed_at=datetime.now(UTC))
    )


async def _get_candidate_by_email(db: AsyncSession, email: str) -> Candidate | None:
    result = await db.execute(select(Candidate).where(Candidate.email == email))
    return result.scalar_one_or_none()


async def _create_challenge(
    db: AsyncSession,
    *,
    email: str,
    purpose: str,
    pending_name: str | None = None,
    pending_password_hash: str | None = None,
) -> tuple[AuthChallenge, str]:
    if await _count_recent_requests(db, email, purpose) >= MAX_REQUESTS_PER_WINDOW:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many verification requests. Please try again later.",
        )

    await _invalidate_open_challenges(db, email, purpose)

    code = generate_otp()
    challenge = AuthChallenge(
        email=email,
        purpose=purpose,
        challenge_token=generate_challenge_token(),
        code_hash=hash_otp(code),
        pending_name=pending_name,
        pending_password_hash=pending_password_hash,
        expires_at=otp_expires_at(),
    )
    db.add(challenge)
    await db.flush()
    return challenge, code


async def request_signup_otp(
    db: AsyncSession,
    *,
    name: str,
    email: str,
    password: str,
    settings: Settings,
) -> dict[str, int | str]:
    normalized_email = normalize_email(email)
    trimmed_name = name.strip()

    if not trimmed_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required.")

    password_error = validate_password(password)
    if password_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=password_error)

    existing = await _get_candidate_by_email(db, normalized_email)
    if existing is not None:
        if existing.signup_method == "google":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=GOOGLE_SIGNIN_MESSAGE)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ACCOUNT_EXISTS_MESSAGE)

    challenge, code = await _create_challenge(
        db,
        email=normalized_email,
        purpose="signup",
        pending_name=trimmed_name,
        pending_password_hash=hash_password(password),
    )
    await db.commit()

    subject, html = render_otp_email(code=code, purpose="signup")
    sent = await send_email(to=normalized_email, subject=subject, html=html, settings=settings)
    if not sent and settings.smtp_username:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to send verification email. Please try again later.",
        )
    if not sent:
        log.info("dev_otp_signup", email=normalized_email, code=code)

    return {
        "challenge_token": challenge.challenge_token,
        "expires_in": OTP_EXPIRY_MINUTES * 60,
    }


async def request_login_otp(
    db: AsyncSession,
    *,
    email: str,
    password: str,
    settings: Settings,
) -> dict[str, int | str]:
    normalized_email = normalize_email(email)
    candidate = await _get_candidate_by_email(db, normalized_email)

    if candidate is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_CREDENTIALS_MESSAGE)

    if candidate.signup_method == "google":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=GOOGLE_SIGNIN_MESSAGE)

    if not verify_password(password, candidate.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_CREDENTIALS_MESSAGE)

    challenge, code = await _create_challenge(
        db,
        email=normalized_email,
        purpose="login",
    )
    await db.commit()

    subject, html = render_otp_email(code=code, purpose="login")
    sent = await send_email(to=normalized_email, subject=subject, html=html, settings=settings)
    if not sent and settings.smtp_username:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to send verification email. Please try again later.",
        )
    if not sent:
        log.info("dev_otp_login", email=normalized_email, code=code)

    return {
        "challenge_token": challenge.challenge_token,
        "expires_in": OTP_EXPIRY_MINUTES * 60,
    }


async def _get_open_challenge(
    db: AsyncSession,
    *,
    email: str,
    purpose: str,
    challenge_token: str,
) -> AuthChallenge:
    result = await db.execute(
        select(AuthChallenge).where(
            AuthChallenge.email == email,
            AuthChallenge.purpose == purpose,
            AuthChallenge.challenge_token == challenge_token,
            AuthChallenge.consumed_at.is_(None),
        )
    )
    challenge = result.scalar_one_or_none()
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid or expired verification code.",
        )

    if challenge.expires_at < datetime.now(UTC):
        challenge.consumed_at = datetime.now(UTC)
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Verification code has expired. Please request a new one.",
        )

    if challenge.attempts >= MAX_VERIFY_ATTEMPTS:
        challenge.consumed_at = datetime.now(UTC)
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Too many failed attempts. Please request a new code.",
        )

    return challenge


async def verify_signup_otp(
    db: AsyncSession,
    *,
    email: str,
    code: str,
    challenge_token: str,
) -> Candidate:
    normalized_email = normalize_email(email)
    challenge = await _get_open_challenge(
        db,
        email=normalized_email,
        purpose="signup",
        challenge_token=challenge_token,
    )

    if not verify_otp(code.strip(), challenge.code_hash):
        challenge.attempts += 1
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid or expired verification code.",
        )

    if not challenge.pending_name or not challenge.pending_password_hash:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid or expired verification code.",
        )

    existing = await _get_candidate_by_email(db, normalized_email)
    if existing is not None:
        challenge.consumed_at = datetime.now(UTC)
        await db.commit()
        if existing.signup_method == "google":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=GOOGLE_SIGNIN_MESSAGE)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ACCOUNT_EXISTS_MESSAGE)

    candidate = Candidate(
        email=normalized_email,
        name=challenge.pending_name,
        password_hash=challenge.pending_password_hash,
        signup_method="email",
        email_verified=True,
    )
    db.add(candidate)
    challenge.consumed_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(candidate)
    return candidate


async def verify_login_otp(
    db: AsyncSession,
    *,
    email: str,
    code: str,
    challenge_token: str,
) -> Candidate:
    normalized_email = normalize_email(email)
    challenge = await _get_open_challenge(
        db,
        email=normalized_email,
        purpose="login",
        challenge_token=challenge_token,
    )

    if not verify_otp(code.strip(), challenge.code_hash):
        challenge.attempts += 1
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid or expired verification code.",
        )

    candidate = await _get_candidate_by_email(db, normalized_email)
    if candidate is None:
        challenge.consumed_at = datetime.now(UTC)
        await db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_CREDENTIALS_MESSAGE)

    challenge.consumed_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(candidate)
    return candidate
