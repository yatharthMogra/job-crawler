from __future__ import annotations

import structlog
import resend

from app.config import Settings

log = structlog.get_logger(__name__)


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
