"""Runtime-safe adapter for whisperline_extracted.

This adapter tries to import `whisperline_extracted` from three locations,
in order:
  1. Installed package (normal import)
  2. Path set via WHISPERLINE_LOCAL_PATH
  3. A `third_party/whisperline_extracted` vendored directory inside the repo

If the implementation cannot be found, calls to transcribe_file() raise a
RuntimeError with clear installation instructions.
"""
from __future__ import annotations

import importlib
import logging
import os
import sys
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


def _attempt_import() -> tuple[Optional[object], Optional[BaseException]]:
    """Try to find an importable whisperline_extracted implementation."""
    try:
        mod = importlib.import_module("whisperline_extracted")
        return mod, None
    except Exception as exc:
        # not installed; try environment-provided path
        local = os.environ.get("WHISPERLINE_LOCAL_PATH")
        if local and os.path.isdir(local):
            if local not in sys.path:
                sys.path.insert(0, local)
            try:
                mod = importlib.import_module("whisperline_extracted")
                return mod, None
            except Exception:
                pass

        # try vendored third_party path
        repo_third = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "third_party"))
        vendor_path = os.path.join(repo_third, "whisperline_extracted")
        if os.path.isdir(vendor_path):
            if repo_third not in sys.path:
                sys.path.insert(0, repo_third)
            try:
                mod = importlib.import_module("whisperline_extracted")
                return mod, None
            except Exception:
                pass

        return None, exc


_impl, _import_error = _attempt_import()


def transcribe_file(path: str, **kwargs) -> Optional[Dict[str, Any]]:
    """Transcribe an audio file using whisperline_extracted.

    Raises:
        RuntimeError: if no implementation is available.
    """
    if _impl is None:
        msg = (
            "whisperline_extracted is not installed.\n"
            "Options:\n"
            "  1) Install it locally (editable):\n"
            "       git clone https://github.com/pottersblack/whisperline_extracted.git /tmp/whisperline_extracted\n"
            "       pip install -e /tmp/whisperline_extracted\n"
            "  2) Set WHISPERLINE_LOCAL_PATH environment variable to a local clone path.\n"
            "  3) Vendor the code under third_party/whisperline_extracted in this repo.\n"
        )
        logger.error(msg)
        raise RuntimeError(msg) from _import_error

    for name in ("transcribe_file", "transcribe", "transcribe_audio", "run_transcription"):
        fn = getattr(_impl, name, None)
        if callable(fn):
            return fn(path, **kwargs)

    raise RuntimeError("whisperline_extracted installed but no known entrypoint found")
