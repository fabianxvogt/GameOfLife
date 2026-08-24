# GameOfLife
My experiments with John Conway's Game of Life

This is an implementation of the Game of Life as a console app, combined with a library for different creatures.

You can import your creatures, place them somewhere on the board and run them with your own rules.

## Quickstart

Run a three-cell blinker for one generation:

```python
from board import Board
from rules.conways_rule import ConwaysRule

board = Board(
    initial_state=[
        [False, True, False],
        [False, True, False],
        [False, True, False],
    ]
)
print(repr(board))
board.apply_rule(ConwaysRule())
print(repr(board))
```

Expected output:

```text
_X_
_X_
_X_
___
XXX
___
```

The project is tested with Python 3.9+ using `python3 -m pytest -q`.

The creature library includes `creatures.single.glider.GLIDER`, the canonical
nine-cell `creatures.single.lwss.LWSS`, and the 36-cell
`creatures.single.gosper_glider_gun.GOSPER_GLIDER_GUN`. On a large enough finite
board, four Conway generations translate the glider by one cell down and one
cell right, while four generations translate the LWSS two cells right. The
Gosper fixture's 36×9 core returns after 30 generations; the regression suite
pins these bounded behaviors.
`Board.find_cycle_period` can optionally compare translation-normalized live-cell
geometry with `normalize_translation=True` when analyzing moving patterns.
The rule interface also includes `rules.highlife_rule.HighLifeRule`, implementing
HighLife's `B36/S23` birth and survival counts.
Creature patterns can be saved and loaded with
`CreatureLoader.save_creature_to_file(...)` and
`CreatureLoader.load_creature_from_file(...)`. The canonical text format uses
`X` for live cells and `_` for dead cells, with one row per line.

## Command-line stepping

The dependency-free runner prints a bounded sequence of generations. With no
pattern argument it starts from the built-in glider:

```shell
python3 cli.py --steps 4
python3 cli.py --pattern path/to/pattern.txt --x 4 --y 2 --rule highlife --steps 3
```

Pattern files are placed from their top-left corner with the non-negative
`--x` and `--y` offsets; the finite board grows just enough to contain the
pattern.

Use `--interactive` for a prompt-driven session. Press Enter (or type `s`) to
step, `r` to reset to the loaded pattern, and `q` to quit:

```shell
python3 cli.py --interactive
```
