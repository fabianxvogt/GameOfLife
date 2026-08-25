# Plane self-append ownership — 2026-08-25

## Finding

`Plane.append_plane_bottom` iterated `plane.state` while appending rows to
`self.state`. When the destination was also the source, the list grew during
iteration and the operation did not terminate.

## Change

The method now snapshots the source row containers before adding spacer rows or
appended rows. This makes self-composition finite and keeps the existing row
ownership boundary: appended rows remain independent from the source snapshot.

## Evidence and classification

- `tests/test_plane.py::PlaneInsertTest::test_append_plane_bottom_handles_destination_as_source`
  exercises two repeated self-appends with a spacer row.
- The pre-fix behavior was reproduced with a two-second bounded probe; it timed
  out while iterating the growing list.
- Acceptance checks: `python3 -m pytest -q` and `git diff --check`.
- Classification: **INCREMENTAL / EMPIRICAL**. Evidence is limited to finite
  self-composition and does not claim broader geometry correctness.
