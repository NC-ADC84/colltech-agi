"""Simple personas loader for colltech_agi.

This module looks for JSON persona files in the same folder and
exposes a tiny API used by the GUI and tests:

- list_personas() -> list of persona names (filenames without .json)
- load_persona(name) -> dict loaded from the JSON file

The importer `scripts/import_personalities.py` writes normalized JSON
into this folder so they become available at runtime.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

_HERE = Path(__file__).resolve().parent


def _persona_files() -> List[Path]:
    return sorted(p for p in _HERE.glob("*.json") if p.is_file())


def list_personas() -> List[str]:
    """Return a list of persona names available (filename sans .json)."""
    return [p.stem for p in _persona_files()]


def load_persona(name: str) -> Optional[Dict]:
    """Load a persona by name (basename without extension).

    Returns the parsed JSON dict or None if not found.
    """
    path = _HERE / f"{name}.json"
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


__all__ = ["list_personas", "load_persona"]
