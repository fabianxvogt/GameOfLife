# CLI stepping — 2026-08-25

## Change

Added `cli.py`, a small dependency-free runner that loads the existing `X`/`_`
pattern format (or the built-in glider), selects Conway or HighLife, and either
prints a bounded generation sequence or accepts prompt-driven step/reset/quit
commands. The existing board and legacy `main.py` behavior are unchanged.

## Evidence

- `python3 -m pytest -q`: verified after the change.
- `python3 cli.py --steps 0`: prints generation zero deterministically.
- `python3 cli.py --interactive`: remains bounded by explicit user commands or
  EOF; it does not run an unbounded loop.

## Classification

`INCREMENTAL / EMPIRICAL`: focused interface and regression coverage only. No
new rule semantics, performance claim, or visual frontend is introduced.
