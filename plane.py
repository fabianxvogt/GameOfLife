from typing import Self

from rules.rule import Rule
from state import NULL_STATE, generate_empty_state, generate_random_state

BOTTOM = 0
LEFT = 1
TOP = 2
RIGHT = 3

class Plane:
    def __init__(self, initial_state: list[list] = None, x_size = 0, y_size = 0, chance_for_active_cell = 0) -> None:
        if initial_state:
            self.state = initial_state
        elif x_size > 0 and y_size > 0:
            if chance_for_active_cell > 0:
                self.state = generate_random_state(x_size, y_size, chance_for_active_cell)
            else:    
                self.state = generate_empty_state(x_size, y_size)
        else:
            self.state = NULL_STATE
        self.last_state = NULL_STATE

    def x_len(self):
        return len(self.state[0])
    
    def y_len(self):
        return len(self.state)
    
    def add_empty_row(self):
        self.state.append([False] * self.x_len())

    def add_row(self, row):
        self.state.append(row)

    def add_empty_col(self):
        [self.state[i].append(False) for i in range(self.y_len())]

    def rotate_by(self, steps):
        for i in range(steps):
            self.rotate()
        return self
    
    def rotate(self):
        self.state = list(list(zip(*self.state[::-1])))
        return self
    
    def copy(self):
        return Plane(self.state)
    
    def __str__(self) -> str:
        return '\n'.join([ ''.join(['█' if cell else ' ' for cell in row]) for row in self.state ])
    
    def __repr__(self) -> str:
        return '\n'.join([''.join(['X' if cell else '_' for cell in row]) for row in self.state])

    def append_plane_bottom(self, plane: Self, n = 1, space_between = 2):
        for i in range(n):
            for s in range(space_between):
                self.add_empty_row()
            for row in plane.state:
                self.add_row(row)

    def append_plane(self, plane: Self, append_side = BOTTOM, n = 1, space_between = 2):
        self.rotate_by(append_side)
        plane.rotate_by(append_side)
        self.append_plane_bottom(plane, n, space_between)
        self.rotate_by(0 if append_side == BOTTOM else 4 - append_side)

    def insert_plane_at(self, plane: Self, start_x, start_y, allow_plane_extension = False):
        current_y = start_y
        for row in plane.state:
            if current_y >= self.y_len(): 
                if allow_plane_extension:
                    self.add_empty_row()
                else:
                    raise ValueError("Out of bounds!")
            
            current_x = start_x
            for cell in row:
                if current_x >= self.x_len(): 
                    if allow_plane_extension:
                        self.add_empty_col()
                    else:
                        raise ValueError("Out of bounds!")
                self.state[current_y][current_x] = cell
                current_x += 1

            current_y += 1

    def insert_plane_in_all_corners(self, plane: Self):
        plane_b = plane.copy().rotate_by(1)
        plane_c = plane.copy().rotate_by(2)
        plane_d = plane.copy().rotate_by(3)

        self.insert_plane_at(plane, 0, 0)
        self.insert_plane_at(plane_b, self.x_len() - plane_b.x_len(), 0)
        self.insert_plane_at(plane_c, self.x_len() - plane_c.x_len(), self.y_len() - plane_c.y_len())
        self.insert_plane_at(plane_d, 0, self.y_len() - plane_d.y_len())

    def add_empty_border(self):
        empty_row = tuple([False] * self.x_len())
        border_state = [empty_row] +  self.state + [empty_row]
        for i, row in enumerate(border_state):
            border_state[i] = tuple([False] + list(row) + [False])
        self.state = border_state
        return self
            
    def collapse_to_active_cells(self):
        for i in range(4):
            self.remove_empty_top_rows()
            self.rotate()

    def remove_empty_top_rows(self):
        collapsed_state = []
        
        start_found = False
        for y, row in enumerate(self.state):
            if not start_found and any(cell == True for cell in row):
                start_found = True
            if start_found:
                collapsed_state.append(row)
        self.state = collapsed_state

    def get_variation(self, rule, variation_steps = 0) -> Self:
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

    def apply_rule(self, rule):
        self.last_state = self.state
        self.state = self.get_new_state(rule)
    
    def get_new_state(self, rule: Rule):
        new_state = []
        for i, row in enumerate(self.state):
            new_row = []
            for j, cell in enumerate(row):
                neighbours = [
                    self.state[i-1][j-1] if i > 0 and j > 0 else False,
                    self.state[i-1][j]   if i > 0 else False,
                    self.state[i-1][j+1] if i > 0 and j < len(row) - 1 else False,
                    self.state[i][j-1]   if j > 0 else False,
                    self.state[i][j+1]   if j < len(row) - 1 else False,
                    self.state[i+1][j-1] if i < len(self.state) - 1 and j > 0 else False,
                    self.state[i+1][j]   if i < len(self.state) - 1 else False,
                    self.state[i+1][j+1] if i < len(self.state) - 1 and j < len(row) - 1 else False,
                ]
                new_row.append(rule.cell_is_alive(cell, neighbours))
            new_state.append(new_row)
        return new_state
    


    
