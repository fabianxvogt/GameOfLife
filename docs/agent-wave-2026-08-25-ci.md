# CI evidence — 2026-08-25

## Change

Added `.github/workflows/tests.yml`, which runs on `push` and `pull_request`.
The workflow uses Ubuntu, Python 3.11, installs only `pytest`, and runs the
existing dependency-light command `python -m pytest -q`. It requests read-only
repository contents permission.

## Verification

- Local command: `python3 -m pytest -q`
- Result: 25 passed
- Runtime source files were unchanged.
- Classification: INCREMENTAL — reproducibility and regression protection only;
  no claim about model behavior beyond the existing tests.
