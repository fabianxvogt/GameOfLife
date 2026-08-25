# Unequal plane composition geometry — 2026-08-25

## Finding

`Plane.append_plane_bottom` previously used the destination's first-row width
for separator rows but copied source rows at their original width. With
unequal dimensions, this created ragged intermediate state. Side-specific
composition then rotated that state with `zip`, which truncated the longer
rows and silently dropped live cells.

## Change

The bottom primitive and side-specific assembly now pad rows with dead cells to
the maximum cross-axis extent. This keeps every result rectangular and makes
the existing top/left alignment explicit for unequal dimensions. The previous
equal-dimension ordering and row-container conventions are retained.

## Evidence and classification

- A focused regression covers both source-wider and destination-wider planes on
  all four append sides, checking rectangular output, population preservation,
  and source ownership.
- A direct bottom-composition regression checks the exact padded state and
  separator geometry.
- Acceptance checks: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q` and
  `git diff --check`.
- Classification: **INCREMENTAL / EMPIRICAL**. The correction is limited to
  finite unequal-dimension composition; it makes no broader claim about Life
  behavior.

No license metadata or dependency files were changed.
