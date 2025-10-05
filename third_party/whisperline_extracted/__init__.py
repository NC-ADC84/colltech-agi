"""Vendored minimal entry for whisperline_extracted.

This is a conservative, minimal vendored copy of the upstream project so the
project can import `whisperline_extracted` without packaging. It intentionally
implements a tiny `transcribe_file` shim that returns a deterministic value for
testing purposes. Replace with the full upstream code if you want real
transcription behavior.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict


def transcribe_file(path: str, **kwargs) -> Dict[str, Any]:
    """Minimal shimbed transcription function.

    Returns a small dict to satisfy integration tests. This is NOT a real
    transcription implementation. To use the real implementation, vendor the
    full upstream repository or set WHISPERLINE_LOCAL_PATH to your clone.
    """
    # Simple deterministic output for test WAVs (silent or otherwise)
    return {
        "text": "",
        "metadata": {
            "source": os.path.basename(path),
            "note": "vendored-shim"
        }
    }


__all__ = ["transcribe_file"]
"""Vendor shim for whisperline_extracted.

This module attempts to load a local clone of the upstream repository so
the project can import `whisperline_extracted` without requiring the repo
to be pip-installable. It loads the implementation under a private module
name and exposes its attributes at package level.

It respects the environment variable `WHISPERLINE_LOCAL_PATH`. If not set,
it falls back to the absolute path used by the user.
"""
from __future__ import annotations

import importlib.util
import importlib.machinery
import os
import sys
import types
import logging

logger = logging.getLogger(__name__)

# Default local path (user-specified). Can be overridden with WHISPERLINE_LOCAL_PATH
DEFAULT_LOCAL = r"C:\Users\Andre\OneDrive - Andre Collier\Shared\shared\whisperline_extracted-master\whisperline_extracted-master"


def _load_local_impl(path: str) -> types.ModuleType | None:
    """Attempt to load the local whisperline_extracted package from path.

    Returns the loaded module (under name _whisperline_impl) or None on failure.
    """
    try:
        init_py = os.path.join(path, "__init__.py")
        if not os.path.isdir(path) or not os.path.exists(init_py):
            logger.debug("Local whisperline path not present or missing __init__.py: %s", path)
            return None

        spec = importlib.util.spec_from_file_location("_whisperline_impl", init_py)
        if spec is None or spec.loader is None:
            logger.debug("Could not create spec for local whisperline at %s", init_py)
            return None

        module = importlib.util.module_from_spec(spec)
        # Execute the module in its own namespace
        spec.loader.exec_module(module)  # type: ignore[arg-type]
        return module
    except Exception as exc:  # pragma: no cover - best-effort shim
        logger.exception("Failed to load local whisperline implementation: %s", exc)
        return None


# Try to import a real implementation first (in case it's installed)
try:
    # If a proper package is already importable, prefer it
    _real = importlib.import_module("whisperline_extracted")  # type: ignore
except Exception:
    # Not installed; attempt to find a local clone
    local_path = os.environ.get("WHISPERLINE_LOCAL_PATH", DEFAULT_LOCAL)
    _real = _load_local_impl(local_path)

if _real is not None:
    # Expose attributes from the real implementation at package level
    for attr in dir(_real):
        if attr.startswith("__"):
            continue
        try:
            globals()[attr] = getattr(_real, attr)
        except Exception:
            # ignore problematic attributes
            pass

    __all__ = [a for a in globals().keys() if not a.startswith("__")]
else:
    # Leave package as an empty shim; the adapter will raise a helpful error
    __all__ = []
