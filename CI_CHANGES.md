# CI Changes Summary

This branch documents recent CI updates made on `feature/linting-fixes`.
It is intended for reviewers to quickly understand what changed and why.

## Summary

- Replaced the custom curl-based Codecov uploader with `codecov/codecov-action@v4` for safer and supported uploads.
- Ensured the unit tests produce a coverage XML file using `pytest-cov`:
  - `pytest --cov=. --cov-report=xml:coverage.xml -q --maxfail=1 --reruns 2`
- Fixed artifact upload paths so coverage and pytest cache are uploaded from the unit test working directory.
- (Transient) added diagnostic steps and a diagnostic collector job during debugging; these have been removed in the final patch.

## Files changed

- `.github/workflows/ci.yml` — main CI pipeline; added Codecov action, updated pytest invocation, fixed artifact paths, removed temporary diagnostics.

## Notes for reviewers

- The Codecov action requires `CODECOV_TOKEN` secret to be configured in repo settings for private repo uploads.
- After this change, Codecov uploads should appear in the Codecov dashboard and README badges should reflect coverage shortly after a successful run.

## Next steps

- Verify a successful run in Actions and confirm upload on Codecov.
- If upload does not appear, inspect `coverage.xml` location in the unit-tests job logs and adjust `files` patterns in the Codecov action.
- Optionally add a PR badge update once Codecov coverage is stable.
