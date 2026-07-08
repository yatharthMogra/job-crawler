from __future__ import annotations

import io
from typing import Optional

from PIL import Image

LOGO_SIZE = 128
MIN_DIMENSION = 17
MIN_BYTES = 200


def normalize_logo_image(content: bytes) -> Optional[bytes]:
    if len(content) < MIN_BYTES:
        return None
    try:
        with Image.open(io.BytesIO(content)) as img:
            if img.width <= MIN_DIMENSION or img.height <= MIN_DIMENSION:
                return None
            img = img.convert("RGBA")
            fitted = _fit_contain(img, LOGO_SIZE)
            out = io.BytesIO()
            fitted.save(out, format="PNG", optimize=True)
            normalized = out.getvalue()
            return normalized if len(normalized) >= MIN_BYTES else None
    except Exception:
        return None


def _fit_contain(img: Image.Image, size: int) -> Image.Image:
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    img.thumbnail((size, size), Image.Resampling.LANCZOS)
    offset = ((size - img.width) // 2, (size - img.height) // 2)
    canvas.paste(img, offset, img if img.mode == "RGBA" else None)
    return canvas
