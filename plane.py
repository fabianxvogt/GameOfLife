from __future__ import annotations

import copy
from typing import Any

from rules.rule import Rule
from state import NULL_STATE, generate_empty_state, generate_random_state

BOTTOM = 0
LEFT = 1
TOP = 2
RIGHT = 3


class Plane:
    def __init__(
        self, initial_state: Any = None, x_size=0, y_size=0, chance_for_active_cell=0
    ) -> None:
        self.state: Any = None
        if initial_state is not None and not (
            isinstance(initial_state, list) and not initial_state
        ):
            self._validate_initial_state(initial_state)
            self.state = initial_state
        elif x_size > 0 and y_size > 0:
            if chance_for_active_cell > 0:
                self.state = generate_random_state(
                    x_size, y_size, chance_for_active_cell
                )
            else:
                self.state = generate_empty_state(x_size, y_size)
        else:
            self.state = NULL_STATE
        self.last_state = NULL_STATE

    @staticmethod
    def _validate_initial_state(initial_state: Any) -> None:
        if not isinstance(initial_state, list):
            raise TypeError("initial_state must be a list of boolean rows")
        if not initial_state:
            return
        if not all(isinstance(row, (list, tuple)) for row in initial_state):
            raise TypeError("initial_state must be a list of boolean rows")

        row_width = len(initial_state[0])
        if row_width == 0:
            raise ValueError("initial_state rows cannot be empty")
        if any(len(row) != row_width for row in initial_state):
            raise ValueError("initial_state rows must have equal lengths")
        if any(
            not isinstance(cell, bool)
            for row in initial_state
            for cell in row
        ):
            raise TypeError("initial_state cells must be bool")

    def x_len(self):
        return len(self.state[0])

    def y_len(self):
        return len(self.state)

    def normalized_state_key(self) -> tuple[tuple[bool, ...], ...]:
        """Return the live-cell geometry without absolute board translation.

        Dead rows and columns around the active cells are removed, making the
        result useful for comparing the same pattern at different positions.
        An entirely inactive plane is represented by an empty tuple.
        """
        active_cells = [
            (y, x)
            for y, row in enumerate(self.state)
            for x, cell in enumerate(row)
            if cell
        ]
        if not active_cells:
            return ()

        min_y = min(y for y, _ in active_cells)
        max_y = max(y for y, _ in active_cells)
        min_x = min(x for _, x in active_cells)
        max_x = max(x for _, x in active_cells)

        return tuple(
            tuple(
                bool(self.state[y][x]) if x < len(self.state[y]) else False
                for x in range(min_x, max_x + 1)
            )
            for y in range(min_y, max_y + 1)
        )

    def add_empty_row(self):
        self.state.append([False] * self.x_len())

    def add_row(self, row):
        self.state.append(list(row))

    def add_empty_col(self):
        [self.state[i].append(False) for i in range(self.y_len())]

    def rotate_by(self, steps):
        for _ in range(steps):
            self.rotate()
        return self

    def rotate(self):
        self.state = list(zip(*self.state[::-1]))
        return self

    def copy(self):
        return Plane(copy.deepcopy(self.state))

    def __str__(self) -> str:
        return "\n".join(
            ["".join(["█" if cell else " " for cell in row]) for row in self.state]
        )

    def __repr__(self) -> str:
        return "\n".join(
            ["".join(["X" if cell else "_" for cell in row]) for row in self.state]
        )

    def append_plane_bottom(self, plane: Plane, n=1, space_between=2):
        for _ in range(n):
            for _ in range(space_between):
                self.add_empty_row()
            for row in plane.state:
                self.add_row(row)

    def append_plane(self, plane: Plane, append_side=BOTTOM, n=1, space_between=2):
        self.rotate_by(append_side)
        rotated_plane = plane.copy().rotate_by(append_side)
        self.append_plane_bottom(rotated_plane, n, space_between)
        self.rotate_by(0 if append_side == BOTTOM else 4 - append_side)

    def insert_plane_at(
        self, plane: Plane, start_x, start_y, allow_plane_extension=False
    ):
        source_height = len(plane.state)
        source_width = max((len(row) for row in plane.state), default=0)
        if source_height == 0 or source_width == 0:
            return

        current_height = len(self.state)
        current_width = max((len(row) for row in self.state), default=0)
        end_x = start_x + source_width
        end_y = start_y + source_height

        if not allow_plane_extension and (
            start_x < 0
            or start_y < 0
            or end_x > current_width
            or end_y > current_height
        ):
            raise ValueError("Out of bounds!")

        top_padding = max(0, -start_y) if allow_plane_extension else 0
        left_padding = max(0, -start_x) if allow_plane_extension else 0
        target_width = max(current_width + left_padding, end_x + left_padding)
        target_height = max(current_height + top_padding, end_y + top_padding)

        expanded_state = [[False] * target_width for _ in range(target_height)]
        for y, row in enumerate(self.state):
            for x, cell in enumerate(row):
                expanded_state[y + top_padding][x + left_padding] = cell

        for y, row in enumerate(plane.state):
            for x, cell in enumerate(row):
                expanded_state[y + start_y + top_padding][
                    x + start_x + left_padding
                ] = cell

        self.state = expanded_state

    def insert_plane_in_all_corners(self, plane: Plane):
        plane_b = plane.copy().rotate_by(1)
        plane_c = plane.copy().rotate_by(2)
        plane_d = plane.copy().rotate_by(3)

        self.insert_plane_at(plane, 0, 0)
        self.insert_plane_at(plane_b, self.x_len() - plane_b.x_len(), 0)
        self.insert_plane_at(
            plane_c, self.x_len() - plane_c.x_len(), self.y_len() - plane_c.y_len()
        )
        self.insert_plane_at(plane_d, 0, self.y_len() - plane_d.y_len())

    def add_empty_border(self):
        empty_row = tuple([False] * self.x_len())
        border_state = [empty_row] + self.state + [empty_row]
        for i, row in enumerate(border_state):
            border_state[i] = tuple([False] + list(row) + [False])
        self.state = border_state
        return self

    def collapse_to_active_cells(self):
        for _ in range(4):
            self.remove_empty_top_rows()
            self.rotate()

    def remove_empty_top_rows(self):
        collapsed_state = []

        start_found = False
        for row in self.state:
            if not start_found and any(row):
                start_found = True
            if start_found:
                collapsed_state.append(row)
        self.state = collapsed_state

    def get_variation(self, rule, variation_steps=0) -> Plane:
        if variation_steps == 0:
            return self
        variation = self.copy()
        for _ in range(variation_steps):
            variation.next_variation(rule)
        return variation

    def next_variation(self, rule):
        self.add_empty_border()
        self.apply_rule(rule)
        self.collapse_to_active_cells()

    def apply_rule(self, rule) -> bool:
        self.last_state = self.state
        self.state = self.get_new_state(rule)
        return False

    def get_new_state(self, rule: Rule):
        new_state = []
        for i, row in enumerate(self.state):
            new_row = []
            for j, cell in enumerate(row):
                neighbours = [
                    self.state[i - 1][j - 1] if i > 0 and j > 0 else False,
                    self.state[i - 1][j] if i > 0 else False,
                    self.state[i - 1][j + 1] if i > 0 and j < len(row) - 1 else False,
                    self.state[i][j - 1] if j > 0 else False,
                    self.state[i][j + 1] if j < len(row) - 1 else False,
                    self.state[i + 1][j - 1]
                    if i < len(self.state) - 1 and j > 0
                    else False,
                    self.state[i + 1][j] if i < len(self.state) - 1 else False,
                    self.state[i + 1][j + 1]
                    if i < len(self.state) - 1 and j < len(row) - 1
                    else False,
                ]
                new_row.append(rule.cell_is_alive(cell, neighbours))
            new_state.append(new_row)
        return new_state
