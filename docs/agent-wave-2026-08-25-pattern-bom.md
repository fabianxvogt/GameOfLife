# GameOfLife UTF-8 BOM compatibility — 2026-08-25

## Scope and result

`CreatureLoader.load_creature_from_file` now reads pattern files as UTF-8 with
an optional leading byte-order mark ignored. Editors that emit a UTF-8 BOM
therefore produce the same `X`/`_` creature geometry as BOM-free files. The
existing terminal-newline handling and canonical save format are unchanged.

## Regression and evidence

- A temporary UTF-8 file containing a BOM plus the canonical glider rows loads
  as the five-cell `GLIDER` pattern.
- `python3 -m pytest -q tests/test_creature.py tests/test_cli.py` — **18 passed**.
- `python3 -m pytest -q` — **42 passed**.
- `python3 -m compileall -q board.py plane.py cli.py creatures rules tests` — passed.
- `git diff --check` — clean.

## Classification

`INCREMENTAL`, EMPIRICAL evidence limited to optional UTF-8 BOM handling in the
existing text format. This does not introduce a new pattern format or claim
broader editor/file compatibility.
