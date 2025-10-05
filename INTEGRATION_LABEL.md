Please create the following GitHub label in this repository to enable the label-based integration test trigger used by the CI workflow.

- Label name: `run-integration`
- Color: `#0e8a16` (green) — optional
- Description: "Apply to a PR to trigger integration tests in CI."

Usage:

1. Create the label in the repository Settings → Labels with the exact name `run-integration`.
2. Add the label to a Pull Request to trigger the `integration-tests` job in `.github/workflows/ci.yml`.

Notes:
- The integration job is opt-in because integration tests may require additional secrets or external services.
- Repository admins should ensure any required secrets (for example, external service keys) are present before triggering integrations.
