# Plane composition row isolation — 2026-08-25

## Finding

`Plane.append_plane_bottom` reused each source row when composing planes. A
later mutation through either the source plane or the composed plane could
therefore change the other object.

## Change

`Plane.add_row` now stores a shallow copy of the row. Cell values are booleans,
so copying the row container is sufficient to isolate this composition
boundary without changing the geometry or runtime dependencies.

## Evidence and classification

- The regression in `tests/test_plane.py` mutates both sides after composition
  and verifies that their row containers remain independent.
- Negative-y `CombinedCreature` placement and empty-component filtering were
  probed during the audit and showed no additional defect in this scope.
- Acceptance checks: `python3 -m pytest -q` and `git diff --check`.
- Classification: **INCREMENTAL / EMPIRICAL**. Evidence is limited to row
  ownership during finite plane composition.
