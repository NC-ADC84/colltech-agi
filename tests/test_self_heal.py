import os
import json
import tempfile
from pathlib import Path

from colltech_agi_self_heal import SelfHealManager


def test_save_report_happy_path(tmp_path):
    """SelfHeal.save_report should write a JSON file into the provided workspace."""
    mgr = SelfHealManager(workspace_path=str(tmp_path))
    report = {'checks': {'ok': True}, 'repairs': []}
    out = mgr.save_report(report, filename='test_diag.json')
    p = Path(out)
    assert p.exists()
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['checks']['ok'] is True


def test_save_report_unwritable(tmp_path, monkeypatch):
    """If the workspace directory is not writable, saving should raise an exception."""
    # Create a directory and make it read-only
    dirpath = tmp_path / 'readonly'
    dirpath.mkdir()

    # On Windows, removing write permission is complex; simulate by monkeypatching open to raise
    mgr = SelfHealManager(workspace_path=str(dirpath))

    def fake_open(*args, **kwargs):
        raise PermissionError("No permission to write")

    monkeypatch.setattr('builtins.open', fake_open)

    try:
        try:
            mgr.save_report({'checks': {}}, filename='should_fail.json')
            assert False, "Expected exception due to unwritable workspace"
        except PermissionError:
            # Expected
            pass
    finally:
        # Restore by monkeypatch fixture automatically
        pass
