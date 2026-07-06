from __future__ import annotations

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import structlog

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
    if not settings.smtp_username or not settings.smtp_password:
        log.warning("email_send_skipped", to=to, reason="smtp_not_configured")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.email_from
    msg["To"] = to
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=30) as server:
            if settings.smtp_use_tls:
                server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.sendmail(settings.email_from, [to], msg.as_string())
        return True
    except Exception as exc:
        log.error("email_send_failed", to=to, error=str(exc))
        return False
