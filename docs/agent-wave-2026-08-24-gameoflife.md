# Game of Life cycle instrument — 2026-08-24

## Scope and result

The existing `Board.find_cycle_period` implementation already provides the requested
hashed-state cycle detector: it stores immutable row tuples in a dictionary and returns
the first repeated state's period within `max_generations`. No production detector change
was needed.

The focused board tests now include a canonical period-3 pulsar surrounded by a one-cell
dead border, which is necessary on this finite board because the unpadded pulsar produces
births just outside its 13×13 bounding box. The existing `CombinedCreature` regression
continues to exercise the required `{(x, y): Creature}` mapping contract.

## Changed and relevant paths

- `tests/test_board.py` — added the padded pulsar period-3 regression.
- `tests/test_creature.py` — existing direct dict-contract regression preserved.
- `board.py` and `creatures/combinations/combined_creature.py` — existing detector and
  contract fixes inspected and preserved; they were already present before this lane's
  test addition.
- `docs/agent-wave-2026-08-24-gameoflife.md` — this lane report.

Unrelated pre-existing edits in the worktree were not changed.

## Verification

- `python3 -m pytest -q tests/test_board.py tests/test_creature.py` → **9 passed**.
- `python3 -m unittest -v tests.test_board tests.test_creature` → **9 tests, OK**.
- `python3 -m pytest -q` → **14 passed**.
- `git diff --check` → **clean**.

The `pytest` executable is not on PATH; the module invocation above is the working
equivalent.

## Classification

**INCREMENTAL** — bounded empirical regression coverage for an existing instrument. The
test demonstrates exact-state period-3 detection on a known oscillator and confirms the
coordinate-mapping creature contract. It makes no claim about unbounded Life behavior.

## Unresolved boundary semantics

- Detection compares exact fixed-board states. A glider or spaceship that translates is
  not recognized as cyclic unless it reaches an exact repeated board state.
- Moving patterns can hit the finite boundary and later become a still life or empty
  board; the method reports the eventual exact repeat, not a causal fate label.
- `max_generations` is an inclusive transition budget: a period `p` needs at least `p`
  transitions to be observed. The method mutates the board while searching and returns
  only the period, not the first repeat generation or phase.

## Next experiment

Run the detector on a padded R-pentomino and record its first exact repeat and transient
length. Then decide, with a separate regression case for a glider, whether the API needs
translation-normalized keys before adding explicit `still_life`, `dies`, `oscillator`, or
`grows` fate labels.
