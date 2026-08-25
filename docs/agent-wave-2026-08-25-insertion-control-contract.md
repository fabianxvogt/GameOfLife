# Plane insertion-control contract — 2026-08-25

## Scope and result

`Plane.insert_plane_at` now validates its coordinate controls before reading
the source into an expanded destination. `start_x` and `start_y` must be
integers but not booleans, and `allow_plane_extension` must be a boolean.
Previously, Python's `bool`/`int` relationship allowed `True` or `False` to be
used as coordinate `1` or `0`, and arbitrary truthy values changed whether
the destination could grow.

## Evidence

- Regression coverage rejects boolean and non-integer coordinates plus
  non-boolean extension flags.
- Each invalid-control case leaves both source and destination state
  unchanged.
- The existing negative-coordinate and extension geometry tests remain in
  `tests/test_plane.py`.

Classification: **INCREMENTAL / EMPIRICAL**. The evidence covers the public
insertion-control boundary and existing finite placement fixtures; it makes
no claim about unbounded board behavior.
