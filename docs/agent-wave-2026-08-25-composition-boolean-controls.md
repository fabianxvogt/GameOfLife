# Composition boolean controls — 2026-08-25

## Finding

Python booleans are instances of `int`, so `True` and `False` can accidentally
be accepted as repetition or spacing controls unless they are rejected
explicitly. The composition implementation already performs that rejection
before its empty-source and non-positive-repetition exits; the audit found no
new runtime mutation defect.

## Change

Added regression coverage for boolean `n` and `space_between` values on the
public `append_plane` entry point with an empty destination and on
`append_plane_bottom` with a one-cell destination. The tests verify the
destination and source remain unchanged, including all four append sides.

## Evidence and classification

- `tests/test_plane.py` covers `True`/`False` controls and pre-mutation
  `TypeError` behavior for both composition entry points.
- The bounded append probe covered empty and one-cell destinations, one- and
  two-cell sources, all four sides, repeated composition, and negative/zero/
  positive spacing; rectangularity, population, and source ownership held.
- Acceptance checks: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s
  tests -p 'test_*.py' -q` and `git diff --check`.
- Classification: **INCREMENTAL / EMPIRICAL**. Evidence is limited to finite
  control validation and the listed composition cases.

No runtime implementation, dependency, or license files were changed.
