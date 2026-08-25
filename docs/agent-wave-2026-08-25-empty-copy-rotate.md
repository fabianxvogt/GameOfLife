# Empty-plane copy, rotation, and composition mutability

The empty `Plane()` sentinel already rotated safely and reported zero width
and height, but that behavior had no direct regression covering copy plus
rotation. A second probe found that `Plane.rotate()` creates tuple rows and
`Plane.copy()` preserved those rows, so a copied rotated plane failed when a
caller used the mutating `add_empty_col()` operation.

`Plane.copy()` now deep-copies the state and normalizes each copied row to a
list. This keeps copies independently mutable without changing the source
plane's rotated tuple rows.

A follow-up probe found the same tuple-row representation at the direct
mutation boundary: `add_empty_col()` raised `AttributeError` after repeated
rotations or top/left/right composition. It now rebuilds each row as a list
before adding the column, preserving the source-ownership boundary while
keeping the existing rotation representation unchanged.

Evidence:

- Empty original/copy rotation remains `state == []` with dimensions `(0, 0)`.
- A copied rotated plane accepts `add_empty_col()` and remains independent.
- Repeatedly rotated copies accept column mutation without changing the source.
- Composed planes accept repeated rotation and column mutation on all four
  append sides without changing the source plane.
- A `1×1` plane remains unchanged after four rotations.
- Full suite: `python3 -m unittest discover -s tests -p 'test_*.py' -q`.

Classification: **INCREMENTAL / EMPIRICAL**. The claim is limited to these
finite transform and copy boundaries.
