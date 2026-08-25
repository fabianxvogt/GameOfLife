import unittest

from plane import Plane


class PlaneInsertTest(unittest.TestCase):
    def test_empty_initial_state_preserves_size_constructor_behavior(self):
        plane = Plane(initial_state=[], x_size=2, y_size=3)

        self.assertEqual(plane.state, [[False, False, False], [False, False, False]])

    def test_initial_state_rejects_text_instead_of_treating_it_as_rows(self):
        with self.assertRaisesRegex(TypeError, "list of boolean rows"):
            Plane(initial_state="X_")

    def test_initial_state_requires_rectangular_boolean_rows(self):
        with self.assertRaisesRegex(ValueError, "equal lengths"):
            Plane(initial_state=[[True], [False, True]])
        with self.assertRaisesRegex(TypeError, "cells must be bool"):
            Plane(initial_state=[[1]])

    def test_rotate_uses_python39_compatible_zip_behavior(self):
        plane = Plane(initial_state=[[True, False, False], [False, True, False]])

        plane.rotate()

        self.assertEqual(
            plane.state,
            [(False, True), (True, False), (False, False)],
        )

    def test_normalized_state_key_removes_dead_padding(self):
        plane = Plane(
            initial_state=[
                [False, False, False, False],
                [False, True, False, False],
                [False, False, True, False],
                [False, False, False, False],
            ]
        )

        self.assertEqual(plane.normalized_state_key(), ((True, False), (False, True)))

    def test_copy_does_not_share_nested_state(self):
        original = Plane(initial_state=[[True, False], [False, True]])

        copied = original.copy()
        copied.state[0][0] = False

        self.assertTrue(original.state[0][0])
        self.assertIsNot(original.state, copied.state)
        self.assertIsNot(original.state[0], copied.state[0])

    def test_insert_plane_rejects_negative_coordinates_without_extension(self):
        destination = Plane(x_size=2, y_size=2)
        source = Plane(initial_state=[[True]])

        with self.assertRaises(ValueError):
            destination.insert_plane_at(source, -1, 0)

    def test_insert_plane_extends_for_negative_coordinates(self):
        destination = Plane(initial_state=[[False, False], [False, False]])
        source = Plane(initial_state=[[True, False], [False, True]])

        destination.insert_plane_at(source, -1, -1, allow_plane_extension=True)

        self.assertEqual(
            destination.state,
            [
                [True, False, False],
                [False, True, False],
                [False, False, False],
            ],
        )

    def test_insert_plane_extends_empty_destination(self):
        destination = Plane()
        source = Plane(initial_state=[[True, False], [False, True]])

        destination.insert_plane_at(source, 1, 2, allow_plane_extension=True)

        self.assertEqual(
            destination.state,
            [
                [False, False, False],
                [False, False, False],
                [False, True, False],
                [False, False, True],
            ],
        )

    def test_insert_plane_grows_multiple_rows_and_columns(self):
        destination = Plane(initial_state=[[False]])
        source = Plane(initial_state=[[True, True, False], [False, True, False]])

        destination.insert_plane_at(source, 2, 3, allow_plane_extension=True)

        self.assertEqual(len(destination.state), 5)
        self.assertTrue(all(len(row) == 5 for row in destination.state))
        self.assertEqual(destination.state[3][2:5], [True, True, False])
        self.assertEqual(destination.state[4][2:5], [False, True, False])

    def test_insert_plane_rejects_out_of_range_coordinates_without_extension(self):
        destination = Plane(initial_state=[[False, False], [False, False]])
        source = Plane(initial_state=[[True]])

        with self.assertRaises(ValueError):
            destination.insert_plane_at(source, 2, 1)
        with self.assertRaises(ValueError):
            destination.insert_plane_at(source, 1, 2)


if __name__ == "__main__":
    unittest.main()
