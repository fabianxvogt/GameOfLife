# Exact top-right insertion ownership

## Scope

Audit the exact-fit `Plane.insert_plane_at` boundary with a multi-cell source
whose right edge lands exactly on the destination boundary at the top row.

## Evidence

`tests/test_plane.py::PlaneInsertTest::test_insert_plane_accepts_exact_top_right_fit_without_source_aliasing`
pins a 3×2 source at `(start_x=3, start_y=0)` in a 4×5 destination. The
source's right edge is exactly `x=5`, no extension is requested, and a later
mutation of the destination does not alter the source.

## Classification

`INCREMENTAL / EMPIRICAL`: this is a finite ownership and boundary regression;
it makes no broader claim about insertion behavior.
