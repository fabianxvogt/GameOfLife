# Empty-plane dimension boundary — 2026-08-25

## Finding

`Plane()` is the documented empty-plane sentinel used by composition code. Its
`y_len()` correctly returned `0`, but `x_len()` indexed a missing first row and
raised `IndexError`. That made a valid empty destination unsafe to inspect
before or between composition operations.

## Change

`Plane.x_len()` now returns `0` when the plane has no rows and retains the
existing first-row width for non-empty rectangular planes. No corner-placement
behavior changed: a non-empty source still fails atomically when an empty
destination cannot contain all four copies without extension.

## Evidence and classification

- The regression checks `(x_len(), y_len()) == (0, 0)` for an empty destination,
  then verifies that a one-cell bottom composition reports `(1, 1)`.
- Bounded corner probes covered empty, `1×1`, single-row, and single-column
  destinations; valid placements matched the existing corner geometry, while
  non-fitting placements remained `ValueError` with no mutation.
- Acceptance checks: `python3 -m unittest discover -s tests -p 'test_*.py' -q`
  and `git diff --check`.
- Classification: **INCREMENTAL / EMPIRICAL**. Evidence is limited to empty
  and minimal finite planes; it makes no broader geometry claim.
