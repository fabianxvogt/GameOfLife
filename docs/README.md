# AI-owned project documentation

This folder is for concise, reviewable notes maintained by coding agents: verified setup instructions, architecture notes, validation commands, and bounded cleanup plans.

The project README and any document marked `human-owned` remain authoritative. Agents must not overwrite those documents or make unsupported claims.

Never store credentials, private data, generated output, logs, datasets, or build artifacts here. Preserve unrelated local work and keep each change focused.

## Verified instruments

- `Board.find_cycle_period` detects the first repeated board state within a bounded
  generation budget; the period-3 regression test lives in `tests/test_board.py`.
- `Board.find_cycle_period(..., normalize_translation=True)` compares live-cell
  geometry after removing dead outer padding, so bounded translating-pattern checks
  can be explicit without changing the default exact-state behavior.

Classification: INCREMENTAL — empirical instrument and regression test; no claim about
pattern behavior beyond the bounded test.
