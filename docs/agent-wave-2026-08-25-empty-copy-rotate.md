# Empty-plane copy and rotation boundary

The empty `Plane()` sentinel already rotated safely and reported zero width
and height, but that behavior had no direct regression covering copy plus
rotation. A second probe found that `Plane.rotate()` creates tuple rows and
`Plane.copy()` preserved those rows, so a copied rotated plane failed when a
caller used the mutating `add_empty_col()` operation.

`Plane.copy()` now deep-copies the state and normalizes each copied row to a
list. This keeps copies independently mutable without changing the source
plane's rotated tuple rows.

Evidence:

- Empty original/copy rotation remains `state == []` with dimensions `(0, 0)`.
- A copied rotated plane accepts `add_empty_col()` and remains independent.
- A `1×1` plane remains unchanged after four rotations.
- Full suite: `python3 -m unittest discover -s tests -p 'test_*.py' -q`.

Classification: **INCREMENTAL / EMPIRICAL**. The claim is limited to these
finite transform and copy boundaries.
