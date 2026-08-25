# CombinedCreature coordinate contract — 2026-08-25

## Scope and result

`CombinedCreature` now computes the global component bounds before allocating
its state. Each component is then inserted relative to that shared origin.
This preserves the logical spacing of mappings that contain more than one
negative coordinate.

Previously, sequential extension could shift the existing state without
updating the coordinate system for later components. For example, placing a
two-cell component at `(-1, 0)` and a one-cell component at `(-2, 0)` could
produce `[True, False, True, True]` instead of the contiguous three-cell
geometry required by those coordinates.

## Evidence

- `tests/test_creature.py` checks the multiple-negative-coordinate case.
- `python3 -m pytest -q` is the acceptance check.
- No changes were made to license metadata or runtime dependencies.

## Classification

`INCREMENTAL`, `EMPIRICAL` evidence limited to finite component placement and
coordinate preservation. No broader pattern-behavior claim is implied.
