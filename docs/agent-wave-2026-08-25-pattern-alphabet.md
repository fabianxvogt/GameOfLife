# GameOfLife pattern alphabet validation — 2026-08-25

## Scope and result

`CreatureLoader.load_creature_from_str` now accepts only the documented
canonical pattern symbols: `X` for a live cell and `_` for a dead cell. Before
this change, every other character was silently interpreted as a dead cell,
which could hide pattern typos or damaged input. The loader now reports the
invalid symbol and its row and column.

The lower-level `Creature` string constructor is unchanged. This keeps the
change limited to file-loader input handling and preserves existing built-in
creature construction. Canonical loader patterns remain compatible, including
the BOM, terminal-newline, and save/reload cases.

## Regression and evidence

- A canonical `_X`/`X_` pattern still loads with the expected geometry.
- A pattern containing `O` is rejected with its one-based row and column.
- The full suite is the acceptance check: `python3 -m pytest -q`.

## Classification

`INCREMENTAL`, EMPIRICAL evidence limited to strict alphabet validation in the
documented `_`/`X` loader format. This does not add RLE, comments, whitespace,
or any other pattern format.
