from __future__ import annotations

import os
from unittest.mock import patch

from app.embeddings.service import _apply_hf_token


def test_apply_hf_token_sets_env_when_configured() -> None:
    with patch.dict(os.environ, {}, clear=True):
        with patch("app.config.get_settings") as mock_settings:
            mock_settings.return_value.hf_token = "hf_test_token"
            _apply_hf_token()
            assert os.environ["HF_TOKEN"] == "hf_test_token"
            assert os.environ["HUGGING_FACE_HUB_TOKEN"] == "hf_test_token"


def test_apply_hf_token_does_not_override_existing_env() -> None:
    with patch.dict(os.environ, {"HF_TOKEN": "hf_existing"}, clear=True):
        with patch("app.config.get_settings") as mock_settings:
            mock_settings.return_value.hf_token = "hf_from_settings"
            _apply_hf_token()
            assert os.environ["HF_TOKEN"] == "hf_existing"
