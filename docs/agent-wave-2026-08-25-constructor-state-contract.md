# Game of Life constructor state contract — 2026-08-25

## Scope and result

`Plane(initial_state=...)` now requires a rectangular 2-D list of boolean
cells. Empty `[]` remains the empty-plane sentinel used by composition code.
`Creature` still accepts its existing pattern-string and list forms, but now
rejects unsupported constructor types explicitly.

This closes a concrete silent-corruption path: before the contract,
`Plane(initial_state="X_")` treated the string as two one-cell rows, reported
the wrong dimensions, and rendered `_` as live because both characters were
truthy. Invalid state input now fails at construction.

## Compatibility and evidence

- Existing boolean list states, built-in creature strings, and empty-plane
  composition remain supported.
- Ragged rows, empty rows, non-boolean cells, text passed to `Plane`, and
  unsupported `Creature` state types have focused regressions.
- `python3 -m pytest -q` is the acceptance check.

## Classification

`INCREMENTAL`, EMPIRICAL evidence limited to constructor boundary behavior and
the finite state representation. No broader simulation or pattern-format
redesign is implied.
