SHELL := /bin/bash
export TZ=UTC LC_ALL=C LANG=C PYTHONHASHSEED=1337 OFFLINE=1

.PHONY: unit property coverage redteam sbom modelcheck proof security licenses drift attest report all

unit: ; pytest -q
property: ; pytest -q -k property --max-examples=100
coverage: ; pytest --cov=src --cov-report=xml
redteam: ; pytest -q tests/test_fuzz_example.py
sbom: ; cyclonedx-bom -o out/sbom.json
modelcheck: ; tlacli check specs/spec.tla || exit 14
proof: ; smt-run specs/proof_obligations.json || exit 15
security: ; bandit -q -r src || exit 21
licenses: ; pip-audit -r requirements.txt || true
drift: ; python -m src.compliance.drift_monitor
attest: ; python scripts/emit_attestation.py > out/attestation.json
report: ; python scripts/emit_build_report.py > out/build_report.json
consciousness: ; python comprehensive_consciousness_demo.py
all: unit property redteam coverage modelcheck proof security sbom report attest

# CollTech-AGI specific targets
run: consciousness
test-consciousness: ; python -m pytest tests/test_catch_system.py -v
