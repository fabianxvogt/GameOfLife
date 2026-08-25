# Empty and side-specific composition — 2026-08-25

## Finding

Empty `Plane()` instances reused the mutable `NULL_STATE` list. Appending to
one empty plane could therefore make later empty planes inherit its rows. In
addition, `append_plane` rotated the destination before copying its source;
when both arguments were the same plane, left, top, and right composition
used the already-rotated destination as the source.

## Change

Empty instances now own fresh state. Bottom composition snapshots source rows,
uses the source width when an empty destination needs spacer rows, and treats
an empty source as a no-op. Side-specific composition copies and rotates the
source before rotating the destination, so self-composition matches the
independent-source geometry.

## Evidence and classification

- `tests/test_plane.py` checks empty-state isolation, empty-destination
  composition on all four sides, source ownership, and side-specific
  self-composition against an independent source.
- The bounded probes cover one asymmetric 2×3 pattern, two spacer rows, and
  one spacer between repeated copies; no unbounded computation is involved.
- Acceptance checks: `python3 -m pytest -q` and `git diff --check`.
- Classification: **INCREMENTAL / EMPIRICAL**. Evidence is bounded to these
  finite composition cases and makes no broader claim about plane geometry.
