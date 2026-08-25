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
        return Creature(copy.deepcopy(self.state))
    

class CreatureLoader:
    @staticmethod
    def load_creature_from_str(creature_str: str) -> Creature:
        rows = creature_str.split('\n')
        row_len = len(rows[0])
        if row_len == 0:
            raise ValueError('Creature load error: Pattern rows cannot be empty!')

        creature_state = []
        for row in rows:
            if len(row) != row_len:
                raise ValueError('Creature load error: Rows lengths are not identical!')
            creature_row = []
            for cell in row:
                creature_row.append(cell == 'X')
            creature_state.append(creature_row)
        return Creature(creature_state)

    @staticmethod
    def load_creature_from_file(filename: str) -> Creature:
        with open(filename) as creature_file:
            creature_str = creature_file.read().rstrip("\r\n")
        return CreatureLoader.load_creature_from_str(creature_str)

    @staticmethod
    def save_creature_to_file(creature: Creature, filename: str) -> None:
        """Save a creature in the text format accepted by the loader.

        ``X`` represents a live cell and ``_`` represents a dead cell. A final
        newline is written for conventional text-file behavior; the loader
        already treats terminal newlines as insignificant.
        """
        with open(filename, "w", encoding="utf-8", newline="\n") as creature_file:
            creature_file.write(repr(creature))
            creature_file.write("\n")
