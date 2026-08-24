"""The canonical Gosper glider gun pattern."""

from creatures.creature import Creature


# Decoded from the standard 36x9 B3/S23 RLE pattern.
GOSPER_GLIDER_GUN = Creature(
    "________________________X___________\n"
    "______________________X_X___________\n"
    "____________XX______XX____________XX\n"
    "___________X___X____XX____________XX\n"
    "XX________X_____X___XX______________\n"
    "XX________X___X_XX____X_X___________\n"
    "__________X_____X_______X___________\n"
    "___________X___X____________________\n"
    "____________XX______________________"
)
