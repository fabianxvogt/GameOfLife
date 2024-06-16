from creatures.creature import Creature
from plane import Plane, NULL_STATE
from state import generate_empty_state


class CombinedCreature(Creature):
    def __init__(self, combined_creatures: dict[(int, int): Creature]) -> None:
        super().__init__(NULL_STATE)
        for (start_x, start_y), creature in combined_creatures:
            super().insert_plane_at(creature, start_x, start_y, allow_plane_extension=True)