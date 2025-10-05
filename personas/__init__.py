"""Runtime loader for persona JSON files stored in the `personas/` folder.

API:
 - list_personas() -> list[str]
 - load_persona(name) -> dict

The loader looks for .json files directly under the `personas` package.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

_ROOT = Path(__file__).parent


def _persona_files() -> List[Path]:
    return sorted([p for p in _ROOT.glob("*.json") if p.is_file()])


def list_personas() -> List[str]:
    """Return available persona basenames (without .json)."""
    return [p.stem for p in _persona_files()]


def load_persona(name: str) -> Dict[str, Any]:
    """Load a persona by name (basename without .json).

    Raises FileNotFoundError if not present.
    """
    path = _ROOT / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf8") as fh:
        return json.load(fh)


__all__ = ["list_personas", "load_persona"]
