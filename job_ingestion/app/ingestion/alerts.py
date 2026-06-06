import json
from datetime import datetime, timezone
from pathlib import Path

from app.models.company import Company


def write_failure_alert(
    alerts_path: Path,
    company: Company,
    consecutive_failures: int,
    last_error: str,
) -> None:
    alerts_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "company_id": str(company.id),
        "company_name": company.name,
        "board_token": company.board_token,
        "consecutive_failures": consecutive_failures,
        "last_error": last_error,
    }
    with alerts_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True))
        handle.write("\n")
