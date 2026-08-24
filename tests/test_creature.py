import unittest

from creatures.combinations.combined_creature import CombinedCreature
from creatures.creature import Creature
from creatures.single.glider import GLIDER


class CreatureTest(unittest.TestCase):
    def test_copy_isolates_nested_state(self):
        original = Creature([[True, False], [False, True]])

        copied = original.copy()
        copied.state[0][0] = False
        copied.state[1].append(True)

        self.assertEqual(original.state, [[True, False], [False, True]])
        self.assertEqual(copied.state, [[False, False], [False, True, True]])

    def test_combined_creature_accepts_coordinate_mapping(self):
        combined = CombinedCreature({(1, 2): Creature([[True]])})

        self.assertTrue(combined.state[2][1])

    def test_glider_pattern_has_five_live_cells(self):
        self.assertEqual(sum(map(sum, GLIDER.state)), 5)


if __name__ == "__main__":
    unittest.main()
