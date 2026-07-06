import uuid
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.config import get_settings
from app.main import app


def _extract_otp_from_email(mock_send_email) -> str:
    import re

    match = re.search(r">(\d{6})<", mock_send_email.call_args.kwargs["html"])
    assert match is not None
    return match.group(1)


@pytest.fixture
def api_headers() -> dict[str, str]:
    settings = get_settings()
    return {"X-API-Key": settings.api_key}


@pytest.fixture
def mock_send_email():
    with patch("app.services.auth_flow.send_email", new_callable=AsyncMock) as mock:
        mock.return_value = True
        yield mock


@pytest.mark.asyncio
async def test_signup_and_login_flow(api_headers, mock_send_email) -> None:
    email = f"auth-{uuid.uuid4()}@example.com"
    password = "secure-password"
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test", headers=api_headers) as client:
        signup_request = await client.post(
            "/auth/signup/request",
            json={"name": "Auth User", "email": email, "password": password},
        )
        assert signup_request.status_code == 200
        challenge_token = signup_request.json()["challenge_token"]
        otp = _extract_otp_from_email(mock_send_email)

        signup_verify = await client.post(
            "/auth/signup/verify",
            json={"email": email, "code": otp, "challenge_token": challenge_token},
        )
        assert signup_verify.status_code == 200
        candidate = signup_verify.json()
        assert candidate["email"] == email

        duplicate = await client.post(
            "/auth/signup/request",
            json={"name": "Another", "email": email, "password": password},
        )
        assert duplicate.status_code == 409

        login_request = await client.post(
            "/auth/login/request",
            json={"email": email, "password": password},
        )
        assert login_request.status_code == 200
        login_challenge = login_request.json()["challenge_token"]
        login_otp = _extract_otp_from_email(mock_send_email)

        login_verify = await client.post(
            "/auth/login/verify",
            json={"email": email, "code": login_otp, "challenge_token": login_challenge},
        )
        assert login_verify.status_code == 200
        assert login_verify.json()["id"] == candidate["id"]


@pytest.mark.asyncio
async def test_login_rejects_google_account(api_headers, mock_send_email) -> None:
    email = f"google-{uuid.uuid4()}@example.com"
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test", headers=api_headers) as client:
        oauth = await client.post(
            "/candidates/oauth",
            json={
                "email": email,
                "name": "Google User",
                "google_sub": f"google-{uuid.uuid4()}",
                "email_verified": True,
            },
        )
        assert oauth.status_code == 200

        login_request = await client.post(
            "/auth/login/request",
            json={"email": email, "password": "any-password"},
        )
        assert login_request.status_code == 403
        assert "Google" in login_request.json()["detail"]


@pytest.mark.asyncio
async def test_login_rejects_wrong_password(api_headers, mock_send_email) -> None:
    email = f"wrong-{uuid.uuid4()}@example.com"
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test", headers=api_headers) as client:
        signup_request = await client.post(
            "/auth/signup/request",
            json={"name": "Wrong Pass", "email": email, "password": "correct-password"},
        )
        assert signup_request.status_code == 200

        code = _extract_otp_from_email(mock_send_email)
        await client.post(
            "/auth/signup/verify",
            json={
                "email": email,
                "code": code,
                "challenge_token": signup_request.json()["challenge_token"],
            },
        )

        login_request = await client.post(
            "/auth/login/request",
            json={"email": email, "password": "wrong-password"},
        )
        assert login_request.status_code == 401


@pytest.mark.asyncio
async def test_legacy_lookup_disabled(api_headers) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers=api_headers) as client:
        response = await client.get("/candidates/lookup", params={"email": "x@example.com"})
    assert response.status_code == 410


@pytest.mark.asyncio
async def test_legacy_create_disabled(api_headers) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers=api_headers) as client:
        response = await client.post(
            "/candidates",
            json={"email": f"legacy-{uuid.uuid4()}@example.com", "name": "Legacy"},
        )
    assert response.status_code == 410
