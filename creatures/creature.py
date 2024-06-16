from plane import Plane
from state import generate_state_from_state_string
import copy

class Creature(Plane):
    def __init__(self, state) -> None:
        if isinstance(state, list):
            super().__init__(state)
        elif isinstance(state, str):
            super().__init__(generate_state_from_state_string(state))

    def copy(self):
        return Creature(copy.copy(self.state))
    

class CreatureLoader:
    def load_creature_from_str(creature_str: str) -> Creature:
        rows = creature_str.split('\n')
        row_len = 0
        creature_state = []
        for i, row in enumerate(rows):
            if i == 0:
                row_len = len(row)
            elif len(row) != row_len:
                raise ValueError('Creature load error: Rows lengths are not identical!')
            creature_row = []
            for cell in row:
                creature_row.append(cell == 'X')
            creature_state.append(creature_row)
        return Creature(creature_state)

    def load_creature_from_file(filename: str) -> Creature:
        creature_str = open(filename).read()
        return CreatureLoader.load_creature_from_str(creature_str)