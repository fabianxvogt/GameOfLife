# HighLife rule — 2026-08-25

## Change

Added `rules.highlife_rule.HighLifeRule` without changing the `Rule` interface.
It applies HighLife's `B36/S23` rule: a live cell survives with 2 or 3 neighbors;
a dead cell is born with 3 or 6 neighbors.

## Evidence

- Direct transition tests cover survival, birth, invalid neighbor lists, and the
  distinguishing six-neighbor birth.
- A board-level regression confirms the six-neighbor birth occurs under HighLife
  but not Conway for the same 3×3 state.
- Classification: **INCREMENTAL**, empirical and bounded; no claim is made about
  long-run pattern behavior or universality.

## Verification

Run `python3 -m pytest -q tests/test_highlife_rule.py tests/test_board.py` and the
full `python3 -m pytest -q` suite after this change.
