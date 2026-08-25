# Plane copy contract

## Finding

`Plane.copy()` previously reused the source plane's nested row lists. A caller
could mutate one cell through the returned plane and silently change the source
plane as well, violating the expected copy boundary.

## Change

`Plane.copy()` now deep-copies the state payload using Python's standard library.
The regression in `tests/test_plane.py` mutates a copied cell and verifies that
the source cell and row containers remain independent.

## Evidence and classification

- Focused regression: `python3 -m pytest -q tests/test_plane.py -k copy`
- Full suite: `python3 -m pytest -q`
- `git diff --check`
- Classification: **INCREMENTAL / EMPIRICAL**. This verifies state-container
  isolation only; it makes no claim about simulation behavior.
