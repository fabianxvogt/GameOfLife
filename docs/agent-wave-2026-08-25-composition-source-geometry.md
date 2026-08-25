# Composition source geometry — 2026-08-25

`Plane.append_plane` temporarily rotates the destination so the existing
bottom-append implementation can handle all four sides. It previously rotated
the source plane in place as well and never restored it. A caller could
therefore observe a changed source orientation and swapped `x_len()`/`y_len()`
after using it as a composition input.

The method now rotates a copy of the source. The composed destination keeps the
existing side-specific geometry, while the input plane remains unchanged.

Evidence:

- `tests/test_plane.py::PlaneInsertTest::test_append_plane_preserves_source_geometry_when_rotating_for_side`
  composes a 3×2 source on the right and checks both its cells and dimensions
  after composition.
- The full test suite and `git diff --check` are the acceptance checks for this
  narrow API contract.

Classification: **INCREMENTAL / EMPIRICAL**. The evidence covers the rotated
composition boundary and makes no broader claim about all plane operations.
