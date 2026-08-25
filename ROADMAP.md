# GameOfLife Roadmap

Console implementation of Conway's Game of Life with a pluggable library: creatures
(`creatures/`), swappable rules (`rules/rule.py`, `conways_rule.py`), board/plane/state
modules, and a pytest suite (`tests/`). Import creatures, place them, run them under your
own rules.

## Now

1. [x] Write a concrete runnable blinker quickstart with expected console output.
2. [x] Verify the test suite green after this week's bounds/stability fixes
   (`python3 -m pytest -q`) and note the Python version in the README. (Done
   2026-08-25; 64 tests pass on the documented Python 3.9+ runtime.)
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
- 2026-08-25: made `CreatureLoader` reject non-`X`/non-`_` symbols instead of
  silently converting them to dead cells, with canonical-alphabet and invalid-
  symbol regressions. [EMPIRICAL]
- 2026-08-25: added a rectangular boolean-state contract for `Plane` and
  `Creature` constructors, preventing text states from being silently treated
  as board rows. [EMPIRICAL]
- 2026-08-25: made `Board.find_cycle_period` reject negative generation budgets
  before mutating the board, with a direct-API regression aligned with the CLI's
  non-negative bounded controls. [EMPIRICAL]
- 2026-08-25: made `Board.find_cycle_period` reject non-integer generation
  budgets, including booleans, with a no-mutation regression aligned with the
  CLI's integer-only `--steps` control. [EMPIRICAL]
- 2026-08-25: made `Plane.copy()` deep-copy nested cell rows, preventing a
  mutation through a copied plane from changing the original state. [EMPIRICAL]
- 2026-08-25: made `CombinedCreature` normalize all component coordinates against
  one global bounding box, preserving spacing when multiple components extend
  into negative coordinates. [EMPIRICAL]
- 2026-08-25: made plane composition copy appended row containers, preventing
  source/composed-state aliasing through `append_plane_bottom`. [EMPIRICAL]
- 2026-08-25: made side-specific plane composition rotate a source copy instead
  of mutating the input plane's orientation or dimensions. [EMPIRICAL]
- 2026-08-25: made bottom plane composition snapshot source rows before
  iteration, preventing non-terminating self-composition. [EMPIRICAL]
- 2026-08-25: isolated empty-plane state and fixed side-specific self-
  composition to preserve finite source geometry and termination. [EMPIRICAL]
- 2026-08-25: validated integer append controls before plane composition can
  rotate or otherwise mutate the destination. [EMPIRICAL]
- 2026-08-25: padded unequal-width plane composition to a rectangular extent,
  preventing side-specific rotation from truncating source cells. [EMPIRICAL]
- 2026-08-25: rejected invalid `append_side` values before composition can
  rotate or mutate the destination, with bounded evidence for non-positive
  repetition and spacing controls. [EMPIRICAL]
- 2026-08-25: rejected boolean/non-integer `Plane.insert_plane_at` coordinates
  and non-boolean extension flags before placement can mutate either plane.
  [EMPIRICAL]
- 2026-08-25: pinned the exact-fit `Plane.insert_plane_at` bottom-right
  boundary for a one-cell source in a minimal `2×2` destination. [EMPIRICAL]
- 2026-08-25: pinned an exact top-right fit for a multi-cell source and its
  post-insertion ownership boundary, so destination edits do not mutate the
  source. [EMPIRICAL]
- 2026-08-25: made `Plane.insert_plane_in_all_corners` treat an empty source as
  a no-op, with bounded asymmetric-corner coordinate and source-ownership
  regressions. [EMPIRICAL]
- 2026-08-25: made all-corner insertion preflight rotated source geometry, so a
  source that only partially fits fails without leaving the first corner
  inserted. [EMPIRICAL]
- 2026-08-25: made empty `Plane()` dimensions total by returning zero width
  alongside zero height, with a minimal-destination composition regression.
  [EMPIRICAL]
- 2026-08-25: pinned rejection of boolean `n` and `space_between` composition
  controls before empty-destination and one-cell bottom composition can
  mutate state. [EMPIRICAL]
- 2026-08-25: made copies of rotated/composed planes remain independently
  mutable, and pinned empty-plane dimensions plus the minimal `1×1` full-turn
  transform boundary. [EMPIRICAL]
- 2026-08-25: made `Plane.add_empty_col()` rebuild tuple-backed rows before
  mutation, closing the repeated-rotation and all-side composition mutability
  boundary without changing source ownership. [EMPIRICAL]
- 2026-08-25: made `Plane.add_empty_row()` preserve the empty-plane sentinel
  and normalize tuple-backed rows before mutation, closing the corresponding
  repeated-rotation and side-composition rectangularity boundary. [EMPIRICAL]
