# AI-owned project documentation

This folder is for concise, reviewable notes maintained by coding agents: verified setup instructions, architecture notes, validation commands, and bounded cleanup plans.

The project README and any document marked `human-owned` remain authoritative. Agents must not overwrite those documents or make unsupported claims.

Never store credentials, private data, generated output, logs, datasets, or build artifacts here. Preserve unrelated local work and keep each change focused.

## Roadmap handoffs

- [Publishability decision](../ROADMAP.md#next): README and dependency/setup clarity are covered; license selection remains a human decision.
- [Cellular-automata family connection](../ROADMAP.md#later): the shared write-up linking this project with `toy-projects/CellularAutomata` and the Rule 30 work remains planned.

## Verified instruments

- `Board.find_cycle_period` detects the first repeated board state within a bounded
  non-negative integer generation budget; non-integers and negative budgets are
  rejected before the board is mutated. The period-3 regression test lives in
  `tests/test_board.py`.
- `Board.find_cycle_period(..., normalize_translation=True)` compares live-cell
  geometry after removing dead outer padding, so bounded translating-pattern checks
  can be explicit without changing the default exact-state behavior.
- [Cycle budget contract](agent-wave-2026-08-25-cycle-budget-contract.md) records
  the negative-budget validation and its no-mutation regression.
- `rules.highlife_rule.HighLifeRule` implements HighLife's B36/S23 transition table
  through the existing `Rule.cell_is_alive` interface.
- `CreatureLoader.save_creature_to_file(...)` writes canonical `_`/`X` pattern
  files that round-trip through `CreatureLoader.load_creature_from_file(...)`.
- `CreatureLoader.load_creature_from_file(...)` rejects empty or zero-width
  patterns instead of passing an empty board to the CLI.
- `CreatureLoader.load_creature_from_str(...)` accepts only the canonical `X`
  and `_` symbols, rejecting other characters rather than treating them as
  dead cells.
- [Pattern alphabet validation](agent-wave-2026-08-25-pattern-alphabet.md)
  records the scoped regression and evidence for this loader boundary.
- `CreatureLoader.load_creature_from_file(...)` accepts an optional UTF-8 BOM
  before the first pattern row, preserving geometry for editor-produced files.
- `Plane` and list-backed `Creature` constructors require rectangular 2-D boolean
  state; text, ragged rows, empty rows, and non-boolean cells are rejected.
- `Plane.copy()` returns an independent nested cell-state payload, so mutating a
  copied row cannot mutate the source plane.
- [Plane copy contract](agent-wave-2026-08-25-plane-copy-contract.md) records
  the aliasing regression and its focused test.
- `Plane.append_plane_bottom` copies source row containers, so composing a
  plane does not share mutable rows with its source.
- [Composition row isolation](agent-wave-2026-08-25-composition-row-isolation.md)
  records the bidirectional mutation regression and bounded evidence.
- `Plane.append_plane` rotates a source copy for side-specific composition, so
  using a plane as an input does not change its orientation or dimensions.
- [Composition source geometry](agent-wave-2026-08-25-composition-source-geometry.md)
  records the source-dimension regression and bounded evidence.
- `Plane.append_plane_bottom` snapshots source rows before composition, so a
  plane can be safely appended to itself without iterating a growing list.
- [Plane self-append ownership](agent-wave-2026-08-25-self-append-ownership.md)
  records the bounded termination regression and evidence.
- Empty `Plane()` instances own independent state, and side-specific self-
  composition snapshots the source before rotating the destination.
- [Empty and side-specific composition](agent-wave-2026-08-25-empty-side-composition.md)
  records the bounded geometry and ownership regressions.
- [Composition control contract](agent-wave-2026-08-25-composition-control-contract.md)
  records pre-mutation validation for non-integer append controls.
- [Append-side and non-positive controls](agent-wave-2026-08-25-append-side-controls.md)
  records the public side-domain validation and bounded no-gap behavior.
- `Plane.insert_plane_at` rejects boolean/non-integer coordinates and
  non-boolean extension flags before placement can alter either plane.
- [Insertion-control contract](agent-wave-2026-08-25-insertion-control-contract.md)
  records the invalid-control regression and no-mutation evidence.
- Unequal-width plane composition pads dead cells to a common rectangular
  extent during side-specific assembly, preserving all source cells.
- [Unequal composition geometry](agent-wave-2026-08-25-unequal-composition-geometry.md)
  records the ragged-row truncation regression and bounded evidence.
- `CombinedCreature` computes one global bounding box before inserting components,
  so multiple negative coordinates preserve their logical spacing instead of
  being shifted relative to earlier insertions.
- [CombinedCreature coordinate contract](agent-wave-2026-08-25-combined-creature-coordinates.md)
  records the negative-coordinate regression and its focused test.
- [Constructor state contract](agent-wave-2026-08-25-constructor-state-contract.md)
  records the compatibility coverage and the prevented string-as-board corruption.
- `cli.py --x` and `--y` place a loaded pattern at a non-negative offset on a
  finite board sized just large enough to contain it.
- `cli.py` provides bounded batch stepping and a prompt-driven step/reset/quit
  session without adding runtime dependencies.
- `cli.main(...)` accepts optional input/output callbacks, so interactive CLI
  behavior can be tested or embedded without redirecting process streams.
- The console app and library use only the Python standard library; `pytest` is
  test-only and is invoked with `python3 -m pytest -q`.
- GitHub Actions runs the test suite on Python 3.9 and 3.11, exercising the
  lowest documented runtime as well as the existing CI runtime.
- `creatures.single.lwss.LWSS` provides the canonical nine-cell lightweight
  spaceship pattern used by the bounded translation regression.
- `creatures.single.gosper_glider_gun.GOSPER_GLIDER_GUN` provides the canonical
  36×9, 36-cell Gosper fixture used by the bounded 30-generation core-return
  regression.
- `Plane.rotate()` remains compatible with the documented Python 3.9+ runtime;
  its regression avoids version-specific `zip` keyword arguments.

Classification: INCREMENTAL — empirical instrument and regression test; no claim about
pattern behavior beyond the bounded test.
