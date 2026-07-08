from __future__ import annotations

import io

from PIL import Image

from app.ingestion.company_logos.normalize import LOGO_SIZE, normalize_logo_image


def _png_bytes(size: int) -> bytes:
    img = Image.new("RGBA", (size, size), (255, 0, 0, 255))
    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


def test_normalize_logo_image_resizes_to_target() -> None:
    normalized = normalize_logo_image(_png_bytes(256))
    assert normalized is not None
    with Image.open(io.BytesIO(normalized)) as img:
        assert img.size == (LOGO_SIZE, LOGO_SIZE)
        assert img.mode == "RGBA"


def test_normalize_logo_image_rejects_tiny_source() -> None:
    assert normalize_logo_image(_png_bytes(16)) is None
