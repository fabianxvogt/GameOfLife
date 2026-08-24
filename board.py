from typing import Any

from plane import Plane
from rules.rule import Rule


class Board(Plane):
    def __init__(
        self, initial_state: Any = None, x_size=0, y_size=0, chance_for_active_cell=0
    ) -> None:
        super().__init__(initial_state, x_size, y_size, chance_for_active_cell)

    def insert_creature_at(self, creature, start_x, start_y):
        super().insert_plane_at(creature, start_x, start_y, False)

    def insert_creature_in_all_corners(self, creature):
        super().insert_plane_in_all_corners(creature)

    def apply_rule(self, rule) -> bool:
        new_state = self.get_new_state(rule)
        state_is_stable = new_state == self.last_state or new_state == self.state
        self.last_state = self.state
        self.state = new_state
        return state_is_stable

    def find_cycle_period(self, rule: Rule, max_generations: int = 100):
        """Return the first repeated-state period, or None within the limit."""
        seen = {}
        for generation in range(max_generations + 1):
            state_key = tuple(tuple(row) for row in self.state)
            if state_key in seen:
                return generation - seen[state_key]
            seen[state_key] = generation
            if generation < max_generations:
                self.apply_rule(rule)
        return None

    def get_new_state(self, rule: Rule):
        new_state = []
        last_row = len(self.state) - 1
        for i, row in enumerate(self.state):
            new_row = []
            last_column = len(row) - 1
            for j, cell in enumerate(row):
                neighbours = [
                    self.state[i - 1][j - 1] if i > 0 and j > 0 else False,
                    self.state[i - 1][j] if i > 0 else False,
                    self.state[i - 1][j + 1] if i > 0 and j < last_column else False,
                    self.state[i][j - 1] if j > 0 else False,
                    self.state[i][j + 1] if j < last_column else False,
                    self.state[i + 1][j - 1] if i < last_row and j > 0 else False,
                    self.state[i + 1][j] if i < last_row else False,
                    self.state[i + 1][j + 1]
                    if i < last_row and j < last_column
                    else False,
                ]
                new_row.append(rule.cell_is_alive(cell, neighbours))
            new_state.append(new_row)
        return new_state
