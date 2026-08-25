import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from creatures.combinations.combined_creature import CombinedCreature
from creatures.creature import Creature, CreatureLoader
from creatures.single.glider import GLIDER
from creatures.single.gosper_glider_gun import GOSPER_GLIDER_GUN
from creatures.single.lwss import LWSS


class CreatureTest(unittest.TestCase):
    def test_constructor_still_accepts_pattern_strings(self):
        creature = Creature("_X\nX_")

        self.assertEqual(creature.state, [[False, True], [True, False]])

    def test_constructor_rejects_unsupported_state_types(self):
        with self.assertRaisesRegex(TypeError, "pattern string or a list"):
            Creature(42)

    def test_copy_isolates_nested_state(self):
        original = Creature([[True, False], [False, True]])

        copied = original.copy()
        copied.state[0][0] = False
        copied.state[1].append(True)

        self.assertEqual(original.state, [[True, False], [False, True]])
        self.assertEqual(copied.state, [[False, False], [False, True, True]])

    def test_copy_after_rotation_normalizes_tuple_rows_and_preserves_source(self):
        original = Creature(
            [[True, False, True], [False, True, False]]
        )
        original.rotate_by(5)
        original_snapshot = [tuple(row) for row in original.state]

        copied = original.copy()
        copied.state[0][0] = not copied.state[0][0]
        copied.add_empty_row()
        copied.add_empty_col()

        self.assertTrue(all(isinstance(row, list) for row in copied.state))
        self.assertEqual(
            [tuple(row) for row in original.state], original_snapshot
        )

    def test_combined_creature_accepts_coordinate_mapping(self):
        combined = CombinedCreature({(1, 2): Creature([[True]])})

        self.assertTrue(combined.state[2][1])

    def test_combined_creature_preserves_multiple_negative_coordinates(self):
        combined = CombinedCreature(
            {
                (-1, 0): Creature([[True, True]]),
                (-2, 0): Creature([[True]]),
            }
        )

        self.assertEqual(combined.state, [[True, True, True]])

    def test_glider_pattern_has_five_live_cells(self):
        self.assertEqual(sum(map(sum, GLIDER.state)), 5)

    def test_lwss_pattern_has_nine_live_cells(self):
        self.assertEqual(sum(map(sum, LWSS.state)), 9)

    def test_gosper_glider_gun_has_canonical_bounds_and_population(self):
        self.assertEqual(len(GOSPER_GLIDER_GUN.state), 9)
        self.assertEqual({len(row) for row in GOSPER_GLIDER_GUN.state}, {36})
        self.assertEqual(sum(map(sum, GOSPER_GLIDER_GUN.state)), 36)

    def test_load_creature_from_file_accepts_trailing_newline(self):
        with TemporaryDirectory() as temporary_directory:
            fixture_path = Path(temporary_directory) / "glider.txt"
            fixture_path.write_text("_X_\n__X\nXXX\n", encoding="utf-8")

            loaded = CreatureLoader.load_creature_from_file(fixture_path)

        self.assertEqual(loaded.state, GLIDER.state)

    def test_load_creature_from_file_ignores_utf8_bom(self):
        with TemporaryDirectory() as temporary_directory:
            fixture_path = Path(temporary_directory) / "glider-with-bom.txt"
            fixture_path.write_text(
                "\ufeff_X_\n__X\nXXX\n", encoding="utf-8"
            )

            loaded = CreatureLoader.load_creature_from_file(fixture_path)

        self.assertEqual(loaded.state, GLIDER.state)

    def test_load_creature_from_str_accepts_canonical_x_and_underscore_symbols(self):
        loaded = CreatureLoader.load_creature_from_str("_X\nX_")

        self.assertEqual(loaded.state, [[False, True], [True, False]])

    def test_load_creature_from_str_rejects_non_canonical_symbols(self):
        with self.assertRaisesRegex(
            ValueError,
            "Invalid pattern symbol 'O' at row 1, column 2",
        ):
            CreatureLoader.load_creature_from_str("XO_\n___")

    def test_load_creature_from_file_rejects_empty_pattern(self):
        with TemporaryDirectory() as temporary_directory:
            fixture_path = Path(temporary_directory) / "empty.txt"
            fixture_path.write_text("\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Pattern rows cannot be empty"):
                CreatureLoader.load_creature_from_file(fixture_path)

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
