# CHANGES

## v3.0.1 – File Operations Integrated (release)

- Natural-language file commands: UI recognizes "search", "find", "list files" and converts them to backend commands (/list, /read, /search).
- Runtime UI toggle: "Allow full-drive access" checkbox added to Personality control panel. This toggles the backend flag `allow_all_directories` at runtime (in-memory).
- Environment opt-in: `COLLTECH_ALLOW_ALL_DRIVES` environment variable allows all drives at backend init when set to '1'/'true'.
- Self‑Heal manager: conservative diagnostics and repair utility (`colltech_agi_self_heal.py`) with a UI button.
- Save Diagnostics: Save JSON diagnostics to workspace with `colltech_diagnostics_<timestamp>.json`.
- Persisted settings: `.colltech_settings.json` introduced to persist minimal, non-sensitive flags (e.g. allow_all_directories).

Notes:
- The runtime toggle writes to `.colltech_settings.json` in the workspace root. This file is intentionally minimal and does not store secrets.
- Self‑Heal is intentionally conservative and will not modify user data.
