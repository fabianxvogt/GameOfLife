import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from creatures.combinations.combined_creature import CombinedCreature
from creatures.creature import Creature, CreatureLoader
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

    def test_load_creature_from_file_accepts_trailing_newline(self):
        with TemporaryDirectory() as temporary_directory:
            fixture_path = Path(temporary_directory) / "glider.txt"
            fixture_path.write_text("_X_\n__X\nXXX\n", encoding="utf-8")

            loaded = CreatureLoader.load_creature_from_file(fixture_path)

        self.assertEqual(loaded.state, GLIDER.state)

    def test_save_and_reload_round_trips_creature_pattern(self):
        with TemporaryDirectory() as temporary_directory:
            pattern_path = Path(temporary_directory) / "glider.txt"

            CreatureLoader.save_creature_to_file(GLIDER, pattern_path)
            saved_text = pattern_path.read_text(encoding="utf-8")
            loaded = CreatureLoader.load_creature_from_file(pattern_path)

        self.assertEqual(saved_text, "_X_\n__X\nXXX\n")
        self.assertEqual(loaded.state, GLIDER.state)


if __name__ == "__main__":
    unittest.main()
