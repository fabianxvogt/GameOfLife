# Empty-row rotation and composition boundary — 2026-08-25

`Plane.add_empty_row()` previously appended an empty list to `Plane()`. That
created a zero-width row outside the rectangular state contract, reported
dimensions `(0, 1)`, and caused `Plane.copy()` to reject the resulting state.

The method now treats the empty plane as a no-op, matching `add_empty_col()`
and the empty composition boundary. For non-empty planes it rebuilds existing
rows as lists before appending the new row. This closes the corresponding
mutability gap after repeated rotations and all four composition sides, where
the existing rows may be tuples.

Evidence:

- `Plane().add_empty_row()` preserves `state == []`, dimensions `(0, 0)`, and
  copyability.
- A twice-repeated side composition followed by five rotations accepts
  `add_empty_row()`, direct row mutation, and `add_empty_col()` for every
  append side.
- The resulting states remain rectangular, all destination rows are owned
  mutable lists, and the source remains unchanged.
- Full suite: `python3 -m unittest discover -s tests -p 'test_*.py' -q`.

Classification: **INCREMENTAL / EMPIRICAL**. The evidence covers the empty-row
and bounded rotation/composition boundaries; it makes no broader claim about
all plane operations.
