# Cycle budget contract — 2026-08-25

## Scope and result

`Board.find_cycle_period` now rejects a negative `max_generations` value with
`ValueError` before reading or advancing the board. A negative budget previously
skipped the detector loop and returned `None`, which could hide an invalid caller
configuration.

The budget remains inclusive: generation zero is inspected first, and at most
`max_generations` transitions are applied. A period `p` therefore needs a budget
of at least `p` to be observed.

## Evidence

- The regression verifies that `max_generations=-1` raises the documented error.
- The same regression verifies that the board state and rule-call count are
  unchanged when validation fails.
- `python3 -m pytest -q` — 50 passed.
- `python3 -m unittest -v tests.test_board` — 12 tests, OK.
- `python3 -m compileall -q board.py plane.py cli.py creatures rules tests` — passed.
- `git diff --check` — clean.

## Classification

`INCREMENTAL`, EMPIRICAL — direct API validation and regression coverage only.
No cycle-equivalence, rule, board-shape, or CLI format semantics changed.

## Unresolved boundaries

- Non-integer budgets retain Python's existing `range()` type failure behavior.
- Cycle detection still mutates the board while searching and returns only the
  period, not the first repeated generation or phase.
