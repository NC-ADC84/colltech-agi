"""
Simple settings persistence for CollTech-AGI.

Persists a small JSON file `.colltech_settings.json` in the workspace root.
Only non-sensitive flags should be stored here (e.g., allow_all_directories).
"""
from pathlib import Path
import json
from typing import Any, Dict

DEFAULTS = {
    "allow_all_directories": False
}


def settings_path(workspace: str = None) -> Path:
    base = Path(workspace) if workspace else Path.cwd()
    return (base / '.colltech_settings.json').resolve()


def load_settings(workspace: str = None) -> Dict[str, Any]:
    p = settings_path(workspace)
    if not p.exists():
        return dict(DEFAULTS)
    try:
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)
            out = dict(DEFAULTS)
            out.update({k: data.get(k, DEFAULTS[k]) for k in DEFAULTS.keys()})
            return out
    except Exception:
        return dict(DEFAULTS)


def save_settings(settings: Dict[str, Any], workspace: str = None) -> Path:
    p = settings_path(workspace)
    try:
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2)
        return p
    except Exception:
        raise
