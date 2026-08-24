# GameOfLife glider wave — 2026-08-25

## Change

Added the reusable `GLIDER` creature and a bounded regression asserting that
four Conway generations translate its five live cells by one row and one
column on an 8×8 board.

## Evidence

- `python3 -m pytest -q` — 17 tests passed.
- `git diff --check` — clean.

## Classification

`INCREMENTAL`, EMPIRICAL evidence limited to the fixed finite board and Conway
rule. The test does not establish unbounded spaceship behavior or translation
normalization for the cycle detector.

## Next falsifiable check

Add a lightweight-spaceship fixture only after documenting the finite-boundary
semantics it is intended to exercise.
