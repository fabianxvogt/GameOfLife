# Lightweight spaceship — 2026-08-25

## Change

Added `creatures.single.lwss.LWSS`, a dependency-free nine-cell lightweight
spaceship using the canonical four-row pattern `o2bo$4bo$o3bo$b4o`. The
pattern is recorded in the Conway Life reference as a period-4 spaceship that
translates two cells horizontally per cycle:
<https://conwaylife.com/wiki/Lightweight_spaceship>.

## Evidence

- `tests/test_creature.py` checks the fixture population is nine live cells.
- `tests/test_board.py` inserts the pattern into a padded finite board, applies
  Conway's rule four times, and checks the exact translated live-cell set.
- `python3 -m pytest -q` — 32 tests passed.
- `python3 -m compileall -q board.py plane.py cli.py creatures rules tests` — passed.
- `git diff --check` — clean.

## Classification

`INCREMENTAL / EMPIRICAL`: the fixture and regression verify one bounded
orientation and four-generation run. They do not establish unbounded motion,
behavior near finite-board edges, or behavior under rules other than Conway's.
