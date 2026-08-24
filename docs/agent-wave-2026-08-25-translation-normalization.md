# Game of Life translation-normalization wave — 2026-08-25

## Scope and result

Added `Plane.normalized_state_key()`, an immutable key that crops dead outer
rows and columns while preserving the active-cell geometry. `Board.find_cycle_period`
now accepts the opt-in `normalize_translation=True` flag. Its default remains
exact finite-board state comparison, including padding.

## Evidence

- A padded diagonal pair normalizes to its two-cell geometry.
- A glider on an 8×8 board returns period 4 under translation-normalized
  comparison, matching its bounded four-generation displacement.
- `python3 -m pytest -q` — 20 tests passed.
- `git diff --check` — clean.

## Classification

`INCREMENTAL`, EMPIRICAL evidence limited to the finite board and Conway rule
fixtures above. The helper does not claim that every moving pattern remains
unbounded or that translation is the only meaningful pattern equivalence.
