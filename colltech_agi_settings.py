"""Persistent settings helper for CollTech-AGI

Stores minimal, non-sensitive preferences in a JSON file inside the project workspace.
Currently persists:
 - allow_all_directories: bool

The settings filename is `.colltech_settings.json` located in the provided workspace_path (defaults to cwd).
"""
from typing import Dict, Any
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

DEFAULT_FILENAME = ".colltech_settings.json"


def _get_path(workspace_path: str = None) -> Path:
    base = Path(workspace_path) if workspace_path else Path.cwd()
    return (base / DEFAULT_FILENAME).resolve()


def load_settings(workspace_path: str = None) -> Dict[str, Any]:
    """Load settings from workspace; return empty dict if missing or on error."""
    p = _get_path(workspace_path)
    try:
        if not p.exists():
            return {}
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.exception("Failed to load settings from %s: %s", p, e)
        return {}


def save_settings(settings: Dict[str, Any], workspace_path: str = None) -> str:
    """Save settings dict to workspace and return the file path."""
    p = _get_path(workspace_path)
    try:
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        return str(p)
    except Exception as e:
        logger.exception("Failed to save settings to %s: %s", p, e)
        raise
