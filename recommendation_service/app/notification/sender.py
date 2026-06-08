from __future__ import annotations

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import structlog

from app.config import Settings

log = structlog.get_logger(__name__)


async def send_email(*, to: str, subject: str, html: str, settings: Settings) -> bool:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.email_from
    msg["To"] = to
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=30) as server:
            if settings.smtp_use_tls:
                server.starttls()
            if settings.smtp_username:
                server.login(settings.smtp_username, settings.smtp_password)
            server.sendmail(settings.email_from, [to], msg.as_string())
        return True
    except Exception as exc:
        log.error("email_send_failed", to=to, error=str(exc))
        return False
