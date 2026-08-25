# Corner insertion atomicity — 2026-08-25

## Finding

`Plane.insert_plane_in_all_corners` could insert the source at the top-left
corner and then raise `ValueError` when a rotated copy was too wide or tall.
That left the destination partially changed even though the all-corners
operation failed.

## Change

The method now checks the destination bounds against all four source rotations
before performing the first insertion. The existing `ValueError` behavior is
preserved, but failed operations leave both destination and source unchanged.

## Evidence and classification

- A 3×2 destination and 3×2 source fit the first orientation but not its 2×3
  rotation; the regression verifies the error and no partial mutation.
- Acceptance checks: `python3 -m unittest discover -s tests -p 'test_*.py' -q`
  and `git diff --check`.
- Classification: **INCREMENTAL / EMPIRICAL**. Evidence is limited to this
  finite partial-fit case; it makes no broader geometry claim.
