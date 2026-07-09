from __future__ import annotations

import base64
import json


def encode_recommended_cursor(scan_offset: int) -> str:
    payload = json.dumps({"o": scan_offset}, separators=(",", ":"))
    return base64.urlsafe_b64encode(payload.encode()).decode()


def decode_recommended_cursor(cursor: str) -> int:
    raw = base64.urlsafe_b64decode(cursor.encode())
    payload = json.loads(raw.decode())
    offset = payload.get("o")
    if not isinstance(offset, int) or offset < 0:
        raise ValueError("Invalid cursor offset")
    return offset
