# GameOfLife Roadmap

Console implementation of Conway's Game of Life with a pluggable library: creatures
(`creatures/`), swappable rules (`rules/rule.py`, `conways_rule.py`), board/plane/state
modules, and a pytest suite (`tests/`). Import creatures, place them, run them under your
own rules.

## Now

1. [x] Write a concrete runnable blinker quickstart with expected console output.
2. [x] Verify the test suite green after this week's bounds/stability fixes
   (`pytest tests/ -v`) and note the Python version in the README. (Done
   2026-08-25; 39 tests pass on the documented Python 3.9+ runtime.)
3. [x] Add 2–3 more classic creatures (glider, lightweight spaceship, and Gosper
   glider gun) with bounded tests. (Done 2026-08-25.)

## Next

- [x] Simple interactive mode: prompt-driven step/reset/quit controls from the
  console. (Done 2026-08-25.)
- [x] Pattern file format: load/save creature placements instead of code-only definitions.
  (Canonical creature save/load round-trip and bounded `cli.py --x`/`--y` board
  placement are covered. Done 2026-08-25.)
- CI: run the test suite on Python 3.9 and 3.11 on pushes and pull requests.
  (Done 2026-08-25.)
- Decide publishability under the portfolio checklist (license, README polish).
  README dependency/setup clarity is covered; license selection remains a human
  decision.

## Later

- Performance: board rendering and stepping are fine at toy sizes; only optimize if a
  pattern class needs it. SPECULATIVE that numpy would help — measure first.
- Connection point to `toy-projects/CellularAutomata` and the Rule 30 work: a shared
  "cellular automata family" write-up linking the three projects.
- Optional visual frontend if the console ever becomes the bottleneck for fun.

## Done

- 2026-08-22: deep-copy fix for creature state; Plane insertion extension-bounds fix;
  rectangular board bounds + stability tests fixed.
- Core implemented: board, plane, state modules; creature library started; Conway's rule
  plus a generic rule interface.
- Test suite covering board, creature, and plane behavior.
- 2026-08-22: added `Board.find_cycle_period` with a period-3 regression test for
  oscillators beyond the legacy period-2 stability signal.
- 2026-08-22: fixed `CombinedCreature` coordinate-mapping iteration and added a regression test.
- 2026-08-24: added and verified a runnable blinker quickstart in the README. [EMPIRICAL]
- 2026-08-25: added a reusable glider creature and a four-generation translation
  regression on a padded finite board. [EMPIRICAL]
- 2026-08-25: made `CreatureLoader` accept newline-terminated pattern files and
  added a temporary glider-file regression. [EMPIRICAL]
- 2026-08-25: added an opt-in translation-normalized cycle key and a bounded
  four-generation glider cycle regression. [EMPIRICAL]
- 2026-08-25: added `HighLifeRule` with focused B36/S23 and Conway-difference
  regressions. [EMPIRICAL]
- 2026-08-25: added canonical creature-pattern saving with a file round-trip
  regression using the existing `_`/`X` loader format. [EMPIRICAL]
- 2026-08-25: added a minimal GitHub Actions workflow running the dependency-light
  pytest suite on pushes and pull requests. [EMPIRICAL]
- 2026-08-25: added the dependency-free `cli.py` runner for bounded batch stepping
  and prompt-driven step/reset/quit sessions. [EMPIRICAL]
- 2026-08-25: added the canonical nine-cell lightweight spaceship (LWSS) and a
  four-generation, two-cell translation regression on a padded finite board.
  [EMPIRICAL]
- 2026-08-25: added the canonical 36×9 Gosper glider gun fixture and a
  30-generation finite-board core-return regression. [EMPIRICAL]
- 2026-08-25: added bounded non-negative `cli.py --x`/`--y` placement for
  loaded patterns, with a finite board sized to contain the placement. [EMPIRICAL]
- 2026-08-25: expanded GitHub Actions to exercise the documented Python 3.9+
  support on Python 3.9 and 3.11. [EMPIRICAL]
- 2026-08-25: replaced the Python 3.10-only `zip(strict=False)` rotation call
  with the Python 3.9-compatible default and added a rotation regression. [EMPIRICAL]
- 2026-08-25: exposed optional `cli.main(...)` input/output callbacks so the
  interactive entry point has a dependency-free test seam. [EMPIRICAL]
- 2026-08-25: rejected empty or zero-width pattern files before they can create
  a silently empty CLI board, with a loader regression. [EMPIRICAL]
- 2026-08-25: made pattern-file loading ignore an optional UTF-8 BOM, with a
  geometry-preserving loader regression. [EMPIRICAL]
