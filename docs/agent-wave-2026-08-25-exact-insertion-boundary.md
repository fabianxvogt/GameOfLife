# Exact insertion boundary — 2026-08-25

The insertion contract distinguishes a source that ends exactly at the
destination's right and bottom edges from one that starts outside the finite
board. The former is valid when plane extension is disabled; the latter is
rejected.

The regression in
`tests/test_plane.py::PlaneInsertTest::test_insert_plane_accepts_exact_bottom_right_fit_without_extension`
places a one-cell source at `(1, 1)` in a `2×2` destination. The resulting
live cell is at the final valid coordinate and the destination dimensions are
unchanged. The neighboring `(2, 1)` and `(1, 2)` cases remain covered by the
existing out-of-range rejection test.

Classification: **INCREMENTAL / EMPIRICAL**. This closes the finite exact-fit
coordinate boundary only; it makes no claim about larger or extended boards.
