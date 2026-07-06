from __future__ import annotations

import structlog
import resend

from app.config import Settings

log = structlog.get_logger(__name__)


def render_otp_email(*, code: str, purpose: str) -> tuple[str, str]:
    action = "sign up" if purpose == "signup" else "sign in"
    subject = f"Your Job Scout verification code"
    html = f"""
    <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto;">
      <h2 style="margin-bottom: 8px;">Verify your email</h2>
      <p style="color: #555;">Use this code to {action} to Job Scout. It expires in 10 minutes.</p>
      <p style="font-size: 32px; font-weight: bold; letter-spacing: 6px; margin: 24px 0;">{code}</p>
      <p style="color: #888; font-size: 13px;">If you didn't request this, you can ignore this email.</p>
    </div>
    """
    return subject, html


async def send_email(*, to: str, subject: str, html: str, settings: Settings) -> bool:
    if not settings.resend_api_key:
        log.warning("email_send_skipped", to=to, reason="resend_not_configured")
        return False

    try:
        resend.api_key = settings.resend_api_key
        resend.Emails.send(
            {
                "from": settings.email_from,
                "to": to,
                "subject": subject,
                "html": html,
            }
        )
        return True
    except Exception as exc:
        log.error("email_send_failed", to=to, error=str(exc))
        return False
