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

The creature library also includes `creatures.single.glider.GLIDER`. On a
large enough finite board, four Conway generations translate it by one cell
down and one cell right; the regression suite pins that bounded behavior.
`Board.find_cycle_period` can optionally compare translation-normalized live-cell
geometry with `normalize_translation=True` when analyzing moving patterns.
The rule interface also includes `rules.highlife_rule.HighLifeRule`, implementing
HighLife's `B36/S23` birth and survival counts.
