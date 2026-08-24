# GameOfLife pattern-placement wave — 2026-08-25

Added non-negative `--x` and `--y` offsets to the dependency-free CLI. The
loaded creature is inserted at that top-left offset on a finite board sized
just large enough to contain the placement. The existing zero-offset behavior
remains unchanged.

Validation:

- `tests/test_cli.py` checks a two-row pattern placed at `(1, 2)`.
- The full pytest suite passes.

This is bounded empirical behavior: negative offsets are rejected, and the
board does not grow during stepping. It does not claim any unbounded pattern
behavior or broader file-format semantics.

Classification: INCREMENTAL — a small placement convenience backed by one
focused regression test.
