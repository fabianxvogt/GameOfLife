# Gosper glider gun wave — 2026-08-25

## Change

Added `creatures.single.gosper_glider_gun.GOSPER_GLIDER_GUN`, a dependency-free
36×9 fixture with 36 live cells decoded into the project's `_`/`X` creature
format. The source pattern is the standard Gosper glider gun listed by
[LifeWiki](https://conwaylife.com/wiki/Gosper%27s_glider_gun).

## Evidence

- The creature test checks nine rows, width 36 for every row, and population 36.
- A 140×100 padded finite board returns the exact 36×9 gun core after 30
  Conway generations.
- The same bounded run has population 41 after generation 30, recording the
  emitted live-cell residue without treating it as an unbounded-growth proof.
- `python3 -m pytest -q` — expected 34 tests passed after this change.
- `python3 -m compileall -q board.py plane.py cli.py creatures rules tests` —
  passed.
- `git diff --check` — clean.

## Classification

`INCREMENTAL / EMPIRICAL`: evidence is limited to the fixed fixture, Conway's
rule, and one finite board size. It does not establish behavior on an infinite
board, preservation near finite-board edges, or compatibility with other rules.

## Next falsifiable check

Add a bounded second-cycle population check only if a future test needs to
exercise repeated emissions; keep board dimensions explicit so boundary effects
remain visible.
