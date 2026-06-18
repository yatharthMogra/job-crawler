from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.services import taxonomy_health_ack as ack_module


@pytest.fixture
def ack_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    path = tmp_path / "taxonomy_health_ack.json"
    monkeypatch.setattr(ack_module, "_ACK_PATH", path)
    return path


def test_set_and_list_acknowledged_domains(ack_file: Path) -> None:
    assert ack_module.list_acknowledged_domains() == {}
    ack_module.set_domain_acknowledged("Business", acknowledged=True)
    data = ack_module.list_acknowledged_domains()
    assert "Business" in data
    assert ack_file.exists()

    ack_module.set_domain_acknowledged("Business", acknowledged=False)
    assert ack_module.list_acknowledged_domains() == {}
