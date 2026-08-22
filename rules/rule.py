class Rule:
    def __init__(self) -> None:
        pass
    def cell_is_alive(self, cell: bool, neighbours: list[bool]) -> bool:
        raise NotImplementedError
