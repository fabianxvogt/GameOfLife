from creatures.single.cyclic.moving.moving_creature import MovingCreature


SPACESHIP = """
___X____
__XXXX__
_XX_X_X_
XXX_X__X
_XX_X_X_
__XXXX__
___X____
"""

class Spaceship(MovingCreature):
    def __init__(self) -> None:
        super().__init__(SPACESHIP)