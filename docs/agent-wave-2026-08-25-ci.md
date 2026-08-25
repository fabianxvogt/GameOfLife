# CI evidence — 2026-08-25

## Change

Added `.github/workflows/tests.yml`, which runs on `push` and `pull_request`.
The initial workflow used Ubuntu and Python 3.11, installed only `pytest`, and
ran the existing dependency-light command `python -m pytest -q`. It requested
read-only repository contents permission. The current workflow keeps those
properties and tests Python 3.9 and 3.11 through its version matrix.

## Verification

- Local command: `python3 -m pytest -q`
- Result: 25 passed
- Runtime source files were unchanged.
- Classification: INCREMENTAL — reproducibility and regression protection only;
  no claim about model behavior beyond the existing tests.
