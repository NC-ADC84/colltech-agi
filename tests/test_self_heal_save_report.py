import json
import os
import tempfile
from pathlib import Path
import pytest

from colltech_agi_self_heal import SelfHealManager


def test_save_report_happy_path(tmp_path):
    mgr = SelfHealManager(workspace_path=str(tmp_path))
    report = mgr.run_heal()
    out = mgr.save_report(report)
    assert os.path.exists(out)
    # Validate JSON
    with open(out, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert isinstance(data, dict)
    assert 'checks' in data


def test_save_report_unwritable(monkeypatch, tmp_path):
    mgr = SelfHealManager(workspace_path=str(tmp_path))
    report = mgr.run_heal()

    # Monkeypatch open to raise PermissionError when called during save_report
    import builtins

    real_open = builtins.open

    def fake_open(*args, **kwargs):
        raise PermissionError("No permission to write")

    monkeypatch.setattr('builtins.open', fake_open)

    with pytest.raises(PermissionError):
        mgr.save_report(report)

    # Restore open just in case (monkeypatch should handle this automatically)
    monkeypatch.setattr('builtins.open', real_open)
