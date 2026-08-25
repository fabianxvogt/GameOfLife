# Append-side and non-positive composition controls — 2026-08-25

## Finding

`Plane.append_plane` accepted values outside the four public side constants.
For example, `append_side=4` or `append_side=-1` entered the fallback rotation
path and changed the destination geometry instead of rejecting the invalid
control. Boolean and non-integer values could fail only after the method had
started its rotation path, while float and boolean lookalikes could also be
accepted as side constants.

## Change

`append_side` is now validated before the empty-source and non-positive-
repetition exits. It must be an integer (excluding booleans) and one of
`BOTTOM`, `LEFT`, `TOP`, or `RIGHT`. The fallback arbitrary-rotation path was
removed.

The existing integer behavior for non-positive controls remains unchanged:
`n <= 0` is a no-op, while `space_between <= 0` produces no separator. The
bounded tests compare negative spacing with zero spacing on all four sides;
they do not claim that negative spacing is a preferred public input.

## Evidence and classification

- Invalid side values `4`, `-1`, `1.0`, `1.5`, `False`, `True`, `"right"`, and
  `None` are
  checked for pre-mutation rejection and source preservation.
- `n` values `0` and `-1` are checked as no-ops for all sides and both
  composition entry points.
- Negative spacing is compared with zero spacing for two repeated insertions
  on all four sides, with source ownership checked afterward.
- Acceptance checks: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q` and
  `git diff --check`.
- Classification: **INCREMENTAL / EMPIRICAL**. Evidence is bounded to the
  listed control values and finite composition cases.

No license metadata or dependency files were changed.
