import base64
import json

import pytest

from app.services.recommended_cursor import decode_recommended_cursor, encode_recommended_cursor


def test_encode_decode_round_trip() -> None:
    cursor = encode_recommended_cursor(200)
    assert decode_recommended_cursor(cursor) == 200


def test_decode_rejects_negative_offset() -> None:
    payload = base64.urlsafe_b64encode(json.dumps({"o": -1}).encode()).decode()
    with pytest.raises(ValueError):
        decode_recommended_cursor(payload)


def test_decode_rejects_invalid_payload() -> None:
    with pytest.raises(ValueError):
        decode_recommended_cursor("not-a-valid-cursor")
