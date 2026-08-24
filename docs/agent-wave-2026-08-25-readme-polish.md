# README and dependency metadata polish — 2026-08-25

## Scope and result

Removed the unused NumPy pin from `requirements.txt` and documented that the
console app and library use only Python's standard library. The README now gives
one explicit test command, while `pytest` remains a test-only tool.

## Evidence

- `rg` over the project source finds no NumPy import or other third-party runtime
  dependency.
- `tests/test_readme_quickstart.py` checks the documented setup statement and
  continues to verify the runnable blinker example.
- `python3 -m pytest -q tests/test_readme_quickstart.py` — 2 passed.
- `python3 -m pytest -q` — 38 passed.
- A `python3 -S` import probe over the runtime modules passed without site
  packages.
- `git diff --check` — clean.
- The license decision remains open and is not inferred by this change.

## Classification

`INCREMENTAL / EMPIRICAL`: metadata and onboarding clarity only; no simulation
semantics, licensing terms, or publication decision were changed.
