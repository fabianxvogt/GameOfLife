from rules.rule import Rule


class HighLifeRule(Rule):
    """The HighLife cellular automaton rule: B36/S23."""

    def __init__(self) -> None:
        super().__init__()

    def cell_is_alive(self, cell: bool, neighbours: list[bool]) -> bool:
        if len(neighbours) != 8 or not all(isinstance(n, bool) for n in neighbours):
            raise ValueError("Invalid neigbours!")

        no_of_neighbours = neighbours.count(True)
        return no_of_neighbours in (2, 3) if cell else no_of_neighbours in (3, 6)
