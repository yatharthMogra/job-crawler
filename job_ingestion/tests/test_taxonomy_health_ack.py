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
    raw = json.loads(ack_file.read_text(encoding="utf-8"))
    assert "domains" in raw and "Business" in raw["domains"]

    ack_module.set_domain_acknowledged("Business", acknowledged=False)
    assert ack_module.list_acknowledged_domains() == {}


def test_role_acknowledgements_are_separate(ack_file: Path) -> None:
    ack_module.set_group_acknowledged("domain", "Business", acknowledged=True)
    ack_module.set_group_acknowledged("role", "BACKEND_ENGINEER", acknowledged=True)
    assert "Business" in ack_module.list_acknowledged_domains()
    assert "BACKEND_ENGINEER" in ack_module.list_acknowledged_roles()
    assert ack_module.list_acknowledgements("role") == ack_module.list_acknowledged_roles()


def test_legacy_flat_ack_file_migrates_on_read(ack_file: Path) -> None:
    ack_file.write_text(json.dumps({"Business": "2026-01-01T00:00:00+00:00"}), encoding="utf-8")
    assert ack_module.list_acknowledged_domains()["Business"].startswith("2026")
    assert ack_module.list_acknowledged_roles() == {}
