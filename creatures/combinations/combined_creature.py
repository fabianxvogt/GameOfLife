from creatures.creature import Creature
from plane import NULL_STATE


class CombinedCreature(Creature):
    def __init__(self, combined_creatures: dict[tuple[int, int], Creature]) -> None:
        placements = [
            (start_x, start_y, creature)
            for (start_x, start_y), creature in combined_creatures.items()
            if creature.state
        ]
        if not placements:
            super().__init__(NULL_STATE)
            return

        min_x = min(0, *(start_x for start_x, _, _ in placements))
        min_y = min(0, *(start_y for _, start_y, _ in placements))
        max_x = max(
            start_x + creature.x_len()
            for start_x, _, creature in placements
        )
        max_y = max(
            start_y + creature.y_len()
            for _, start_y, creature in placements
        )

        super().__init__([
            [False] * (max_x - min_x)
            for _ in range(max_y - min_y)
        ])
        for start_x, start_y, creature in placements:
            super().insert_plane_at(
                creature,
                start_x - min_x,
                start_y - min_y,
                allow_plane_extension=False,
            )
