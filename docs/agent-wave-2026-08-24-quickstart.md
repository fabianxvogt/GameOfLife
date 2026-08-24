# GameOfLife quickstart wave — 2026-08-24

## Change

Added a runnable three-cell blinker example to the README, including its
expected `repr()` output. A regression test executes the same board transition
so documentation and behavior cannot silently drift.

## Evidence

- `python3 -m pytest -q` — 15 tests passed.
- `python3 -m unittest -v tests.test_readme_quickstart` — passed.
- `git diff --check` — clean.

## Classification

`INCREMENTAL`, EMPIRICAL evidence limited to the documented finite board and
one Conway transition. No claim is made about general Life behavior.

## Next falsifiable check

Add a glider example only after deciding whether moving patterns should be
compared by exact board state or translation-normalized state.
