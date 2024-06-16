
import random

from creatures.combinations.stream.stream_inverter.inline_inverter import InlineInverter
from creatures.single.cyclic.moving.spaceship import Spaceship
from plane import RIGHT
from rules.conways_rule import ConwaysRule
from board import Board
from creatures.single.cyclic.moving.moving import GLIDER

rule = ConwaysRule()

size = 200
board = Board(x_size=size, y_size=size, chance_for_active_cell=0)
glider_canon = InlineInverter()
glider_canon.append_plane(glider_canon.copy(), append_side=RIGHT, n = 2)
board.insert_creature_in_all_corners(glider_canon)

for i in range(0, 1000000):
    is_stable = board.apply_rule(rule)
    print(board)
    print(i)
    print(f'{ "=" * size } \n')
    if is_stable:
        print("State is stable (only blinkers left)")
        break
        