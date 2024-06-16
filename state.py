import random

NULL_STATE = []

def generate_random_state(x_size: int, y_size, chance_for_active_cell: float) -> list:
    return [ [ random.random() < chance_for_active_cell for _ in range(y_size) ] for _ in range(x_size) ]

def generate_empty_state(x_size: int, y_size: int) -> list:
    return [ [ False for _ in range(y_size) ] for _ in range(x_size) ]

    
def generate_state_from_state_string(state_str: str) -> list:
    rows = state_str.strip().split('\n')
    row_len = 0
    state = []
    for i, row in enumerate(rows):
        if i == 0:
            row_len = len(row)
        elif len(row) != row_len:
            raise ValueError('Creature load error: Rows lengths are not identical!')
        creature_row = []
        for cell in row:
            creature_row.append(cell == 'X')
        state.append(creature_row)
    return state
