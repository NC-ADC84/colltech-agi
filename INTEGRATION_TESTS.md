Integration tests

How to run integration tests locally:

1. Ensure required fixtures and CLI binary are present in the `colltech-agi` folder:
   - `colltech_agi_cli.py` (CLI entrypoint)
   - `test_batch_input.txt` fixture

2. Install dev dependencies (recommended in a venv):

```powershell
python -m pip install -r requirements.txt
```

3. Run integration tests only:

```powershell
python -m pytest -q -m integration
```

4. Run all tests (including integration):

```powershell
python -m pytest -q -m "integration or not integration"
```

Notes:
- Integration tests are deselected by default to keep fast feedback loops (see `pytest.ini`).
- The CI workflow exposes an `integration-tests` job that runs only when manually triggered (workflow_dispatch) or when commit messages contain `[run integration]`.
