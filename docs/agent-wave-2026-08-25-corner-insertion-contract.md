# Corner insertion contract — 2026-08-25

## Finding

`Plane.insert_plane_in_all_corners` attempted to derive dimensions from the
three rotated copies even when the source plane was empty. The first insertion
returned early, but the next `x_len()` call on an empty rotated source raised
`IndexError` instead of treating an empty source as a no-op.

## Change

The method now returns before creating rotated copies when `plane.state` is
empty. Non-empty insertion continues to use independent rotated copies and the
existing insertion path, so source ownership is preserved.

## Evidence and classification

- The empty-source regression verifies a non-empty destination is unchanged.
- A bounded asymmetric 2×3 source on an 8×7 destination verifies all four
  rotated corner coordinate sets explicitly.
- Mutating the composed destination afterward leaves the source unchanged.
- Acceptance checks: `python3 -m pytest -q` and `git diff --check`.

Classification: **INCREMENTAL / EMPIRICAL**. Evidence is limited to the finite
source and destination fixtures above; it makes no unbounded geometry claim.
