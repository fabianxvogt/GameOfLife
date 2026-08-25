# Creature copy after rotation — 2026-08-25

`Plane.copy()` already normalized rows copied from rotated planes to mutable
lists, but `Creature.copy()` had its own implementation that returned the
deep-copied tuple rows unchanged. A rotated creature copy therefore raised
`TypeError` when callers mutated a copied cell, even though ordinary creature
copies supported that operation.

`Creature.copy()` now applies the same row-container normalization as
`Plane.copy()`. The copy remains independently owned, and its row mutation
continues to work after `add_empty_row()` and `add_empty_col()`.

Evidence:

- A creature rotated five times can be copied and directly mutated.
- The copied rows are mutable lists after the tuple-producing rotation.
- Subsequent row/column padding does not alter the rotated source.
- Full suite: `python3 -m unittest discover -s tests -p 'test_*.py' -q`.

Classification: **INCREMENTAL / EMPIRICAL**. The evidence is limited to the
finite rotated-copy ownership boundary.
