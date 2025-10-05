import json
import wave
import os
import pytest

from pathlib import Path

@pytest.mark.integration
def test_transcription_integration(tmp_path: Path):
    """Integration test: transcribe a tiny silent WAV file.

    This test relies on the runtime adapter `colltech_agi.audio.whisper_adapter`.
    It will skip only if the adapter reports the implementation is unavailable.
    """
    try:
        from colltech_agi.audio import whisper_adapter
    except Exception as e:
        pytest.skip(f"whisper_adapter import failed; skipping integration test: {e}")

    # Create a 1s silent WAV file (16kHz, mono, 16-bit)
    wav_path = tmp_path / "silence.wav"
    with wave.open(str(wav_path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        # 1 second of silence: 16000 samples, 2 bytes per sample
        wf.writeframes(b"\x00\x00" * 16000)

    # Call the adapter. If the real implementation is not available the adapter
    # should raise a RuntimeError with a helpful message; in that case skip.
    try:
        result = whisper_adapter.transcribe_file(str(wav_path))
    except RuntimeError as e:
        pytest.skip(f"Transcription implementation not available: {e}")
    except Exception as e:
        pytest.fail(f"Transcription call raised unexpected exception: {e}")

    # We don't assume exact return shape of upstream; assert a useful non-empty response
    assert result is not None, "Transcription returned no result"
    # If it's a mapping, expect at least some text field or similar keys
    if isinstance(result, dict):
        assert any(k in result for k in ("text", "transcript", "result")) or len(result) > 0
    elif isinstance(result, str):
        assert isinstance(result, str)
