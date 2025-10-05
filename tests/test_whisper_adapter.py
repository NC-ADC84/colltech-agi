import os
import importlib
import pytest

from colltech_agi.audio import whisper_adapter


def test_transcribe_raises_when_missing(monkeypatch):
    """If the whisper implementation is not available, transcribe_file should raise RuntimeError."""
    # Ensure WHISPERLINE_LOCAL_PATH points to a non-existent directory
    monkeypatch.setenv("WHISPERLINE_LOCAL_PATH", "C:\\nonexistent_path_for_tests")

    # Reload the adapter to pick up the env change
    importlib.reload(whisper_adapter)

    with pytest.raises(RuntimeError):
        whisper_adapter.transcribe_file("dummy.wav")


def test_adapter_message_contains_install_hint(monkeypatch):
    monkeypatch.setenv("WHISPERLINE_LOCAL_PATH", "C:\\nonexistent_path_for_tests")
    importlib.reload(whisper_adapter)

    with pytest.raises(RuntimeError) as exc:
        whisper_adapter.transcribe_file("dummy.wav")

    text = str(exc.value)
    assert (
        "whisperline_extracted is not installed" in text
        or "no known entrypoint" in text
    )
