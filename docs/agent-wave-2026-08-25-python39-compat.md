# Python 3.9 rotation compatibility — 2026-08-25

## Result

Replaced the Python 3.10-only `zip(strict=False)` call in `Plane.rotate()` with
the equivalent Python 3.9-compatible default behavior. Added a regression that
checks the rotated matrix shape and values.

## Evidence

- `python3 -m unittest discover -s tests -q` passes with the rotation regression.
- The runtime implementation uses no `zip` keyword arguments after the change.
- `git diff --check` passes.

## Classification

`INCREMENTAL / EMPIRICAL`: compatibility repair only; no simulation semantics
or licensing decision changed.
