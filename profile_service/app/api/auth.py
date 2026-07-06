from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import require_api_key
from app.config import Settings, get_settings
from app.database import get_db
from app.models.candidate import Candidate
from app.schemas.auth import ChallengeResponse, LoginRequest, SignupRequest, VerifyOtpRequest
from app.schemas.candidate import CandidateResponse
from app.services.auth_flow import (
    request_login_otp,
    request_signup_otp,
    verify_login_otp,
    verify_signup_otp,
)

router = APIRouter(prefix="/auth", tags=["auth"], dependencies=[Depends(require_api_key)])


@router.post("/signup/request", response_model=ChallengeResponse)
async def signup_request_otp(
    payload: SignupRequest,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> ChallengeResponse:
    result = await request_signup_otp(
        db,
        name=payload.name,
        email=str(payload.email),
        password=payload.password,
        settings=settings,
    )
    return ChallengeResponse.model_validate(result)


@router.post("/signup/verify", response_model=CandidateResponse)
async def signup_verify_otp(
    payload: VerifyOtpRequest,
    db: AsyncSession = Depends(get_db),
) -> Candidate:
    return await verify_signup_otp(
        db,
        email=str(payload.email),
        code=payload.code,
        challenge_token=payload.challenge_token,
    )


@router.post("/login/request", response_model=ChallengeResponse)
async def login_request_otp(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> ChallengeResponse:
    result = await request_login_otp(
        db,
        email=str(payload.email),
        password=payload.password,
        settings=settings,
    )
    return ChallengeResponse.model_validate(result)


@router.post("/login/verify", response_model=CandidateResponse)
async def login_verify_otp(
    payload: VerifyOtpRequest,
    db: AsyncSession = Depends(get_db),
) -> Candidate:
    return await verify_login_otp(
        db,
        email=str(payload.email),
        code=payload.code,
        challenge_token=payload.challenge_token,
    )
