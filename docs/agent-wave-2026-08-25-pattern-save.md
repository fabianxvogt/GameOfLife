# GameOfLife pattern-save wave — 2026-08-25

## Scope and result

Added `CreatureLoader.save_creature_to_file`, which writes the existing
underscore/`X` row format used by `load_creature_from_file`. The writer emits a
single trailing newline; the loader already removes terminal newlines, so saved
patterns can be loaded without changing their cell geometry.

No board, plane, rule, or simulation behavior changed. Board placements and
metadata remain outside this bounded feature.

## Regression and evidence

- Saved the five-cell `GLIDER` to a temporary file and verified the exact text
  `_X_`, `__X`, `XXX`, followed by one newline.
- Loaded that file and verified the state equals the original glider.
- `python3 -m pytest -q tests/test_creature.py` — **5 passed**.
- `python3 -m pytest -q` — **25 passed**.
- `python3 -m compileall -q creatures tests` — passed.
- `git diff --check` — clean.

## Classification

`INCREMENTAL`, EMPIRICAL evidence limited to canonical text serialization and
one in-memory/file round-trip. This does not establish a broader pattern-file
standard or unbounded Life behavior.
