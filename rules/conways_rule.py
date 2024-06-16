

from rules.rule import Rule


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
