from datetime import date
import random


neighbours = [0, 1, 0, 0, 1, 0, 1, 0]

class Rule:
    def __init__(self) -> None:
        pass
    def cell_is_alive(cell: bool, neighbours: dict) -> bool:
        pass

class ConwaysRule(Rule):
    def __init__(self) -> None:
        super().__init__()

    def cell_is_alive(self, cell: bool, neighbours: dict) -> bool:
        if len(neighbours) != 8 or not all(isinstance(n, bool) for n in neighbours):
            raise ValueError('Invalid neigbours!')
        no_of_neighbours = neighbours.count(True)

        if cell and no_of_neighbours in [2, 3]: # survival
            return True
        
        if cell and no_of_neighbours < 2: # underpopulation
            return False
        
        if cell and no_of_neighbours > 3: # overpopulation
            return False
        
        if not cell and no_of_neighbours == 3: # reproduction
            return True
        
        return False
class Board():
    def __init__(self, initial_state: list) -> None:
        self.state = initial_state
        self.last_state = None
    def apply_rule(self, rule) -> bool:
        state_is_stable = False
        new_state = self.get_new_state(rule)
        if new_state == self.last_state or new_state == self.state:
            state_is_stable = True
        self.last_state = self.state
        self.state = self.get_new_state(rule)
        return state_is_stable
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
                    self.state[i+1][j-1] if i < len(row) - 1 and j > 0 else False,
                    self.state[i+1][j]   if i < len(row) - 1 else False,
                    self.state[i+1][j+1] if i < len(row) - 1 and j < len(row) - 1 else False,
                ]
                new_row.append(rule.cell_is_alive(cell, neighbours))
            new_state.append(new_row)
        return new_state
    def __str__(self) -> str:
        return '\n'.join([ ''.join(['█' if cell else ' ' for cell in row]) for row in self.state ])

def generate_random_state(size: int, chance_for_active_cell: float) -> list:
    return [ [ random.random() < chance_for_active_cell for _ in range(0,size) ] for _ in range(0,size) ]

rule = ConwaysRule()
size = 200
initial_state = generate_random_state(size, 0.2)
board = Board(initial_state)
#print(board)
iterations = 100000
# plt.imshow(initial_state, cmap='Greys',  interpolation='nearest')
# plt.axis('off')
# plt.show()

for i in range(0, iterations):
    is_stable = board.apply_rule(rule)
    print(board)
    print(i)
    print(f'{ "=" * size } \n')
    if is_stable:
        print("State is stable (only blinkers left)")
        break
        