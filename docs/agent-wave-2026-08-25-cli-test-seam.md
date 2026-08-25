# CLI test seam — 2026-08-25

## Scope and result

`cli.main(...)` now accepts optional input and output callbacks and forwards
them to the existing interactive runner. Normal command-line use still uses
the built-in `input` and `print` functions; tests and embedders can exercise
the same entry point without redirecting process-wide streams.

## Evidence

- `tests/test_cli.py` runs an interactive `main(...)` session with injected
  callbacks and verifies the generation-zero frame.
- `python3 -m pytest -q` — 40 tests passed.
- `python3 -m compileall -q board.py plane.py cli.py creatures rules tests` —
  passed.
- `git diff --check` — clean.

## Classification

`INCREMENTAL`, EMPIRICAL — a narrow dependency-free testability improvement;
no CLI commands, simulation rules, or board semantics changed.
