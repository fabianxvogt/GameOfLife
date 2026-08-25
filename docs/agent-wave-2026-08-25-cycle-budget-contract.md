# Cycle budget contract — 2026-08-25

## Scope and result

`Board.find_cycle_period` now rejects invalid `max_generations` values before
reading or advancing the board. Negative budgets raise `ValueError`; previously,
they skipped the detector loop and returned `None`, which could hide an invalid
caller configuration. Non-integer budgets, including booleans, raise `TypeError`;
this prevents direct API callers from receiving an incidental `range()` error or
silently treating `True` as one generation.

The budget remains inclusive: generation zero is inspected first, and at most
`max_generations` transitions are applied. A period `p` therefore needs a budget
of at least `p` to be observed.

## Evidence

- The regression verifies that `max_generations=-1` raises the documented error.
- The same regression verifies that the board state and rule-call count are
  unchanged when validation fails.
- A dependency-free regression verifies that float and boolean budgets raise
  `TypeError` without changing the board or calling the rule.
- `python3 -m pytest -q` — 51 passed.
- `python3 -m unittest -v tests.test_board` — 13 tests, OK.
- `python3 -m compileall -q board.py plane.py cli.py creatures rules tests` — passed.
- `git diff --check` — clean.

## Classification

`INCREMENTAL`, EMPIRICAL — direct API validation and regression coverage only.
No cycle-equivalence, rule, board-shape, or CLI format semantics changed.

## Unresolved boundaries

- Cycle detection still mutates the board while searching and returns only the
  period, not the first repeated generation or phase.
