# GameOfLife pattern-loader wave — 2026-08-25

## Scope and result

`CreatureLoader.load_creature_from_file` now reads through a context manager and
removes only terminal `\r`/`\n` characters before delegating to the existing
string loader. Newline-terminated creature fixtures therefore load without an
extra empty row, while the `X`/non-`X` cell mapping is unchanged.

No board, plane, rule, or boundary behavior changed. Finite-board semantics
remain the same.

## Regression and evidence

- A temporary `glider.txt` fixture containing `_X_`, `__X`, and `XXX` plus a
  trailing newline loaded as the five-cell `GLIDER` pattern.
- `python3 -m pytest -q tests/test_creature.py` — **4 passed**.
- `python3 -m pytest -q` — **18 passed**.
- `git diff --check` — clean.

## Classification

`INCREMENTAL`, EMPIRICAL evidence limited to newline-terminated file loading and
the existing parser. This does not establish a complete pattern-file format or
make claims about unbounded Life behavior.

## Remaining roadmap scope

Pattern-file saving and any broader format decisions remain open in the roadmap.
