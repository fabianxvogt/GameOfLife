
from creatures.creature import Creature


class InlineInverter(Creature):
    def __init__(self) -> None:
        super().__init__("""
_______________________X_X__________
_____________________X___X__________
_____________X_______X______________
____________XXXX____X____X________XX
___________XX_X_X____X____________XX
XX________XXX_X__X___X___X__________
XX_________XX_X_X______X_X__________
____________XXXX____________________
_____________X______________________
""")