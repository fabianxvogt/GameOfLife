from creatures.creature import Creature


class CyclicCreature(Creature):
    def __init__(self, state) -> None:
        super().__init__(state)