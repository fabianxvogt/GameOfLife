from creatures.creature import Creature


class MovingCreature(Creature):
    def __init__(self, state) -> None:
        super().__init__(state)