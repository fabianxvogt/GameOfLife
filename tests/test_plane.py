import unittest

from plane import BOTTOM, LEFT, Plane, RIGHT, TOP


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

    def test_empty_planes_do_not_share_mutable_state(self):
        first = Plane()
        first.append_plane_bottom(Plane(initial_state=[[True]]), space_between=0)

        second = Plane()

        self.assertEqual(first.state, [[True]])
        self.assertEqual(second.state, [])
        self.assertIsNot(first.state, second.state)

    def test_append_plane_bottom_copies_source_rows(self):
        destination = Plane(initial_state=[[False, False]])
        source = Plane(initial_state=[[True, False], [False, True]])

        destination.append_plane_bottom(source, space_between=0)
        source.state[0][0] = False
        destination.state[2][1] = False

        self.assertEqual(
            destination.state,
            [[False, False], [True, False], [False, False]],
        )
        self.assertEqual(source.state, [[False, False], [False, True]])
        self.assertIsNot(destination.state[1], source.state[0])
        self.assertIsNot(destination.state[2], source.state[1])

    def test_append_plane_bottom_handles_destination_as_source(self):
        plane = Plane(initial_state=[[True, False], [False, True]])

        plane.append_plane_bottom(plane, n=2, space_between=1)

        self.assertEqual(
            plane.state,
            [
                [True, False],
                [False, True],
                [False, False],
                [True, False],
                [False, True],
                [False, False],
                [True, False],
                [False, True],
            ],
        )

    def test_append_plane_handles_empty_destination_on_each_side(self):
        source_state = [[True, False, False], [False, True, True]]

        expected_by_side = {
            BOTTOM: [
                [False, False, False],
                [False, False, False],
                [True, False, False],
                [False, True, True],
            ],
            LEFT: [
                (False, False, True, False, False),
                (False, False, False, True, True),
            ],
            TOP: [
                (True, False, False),
                (False, True, True),
                (False, False, False),
                (False, False, False),
            ],
            RIGHT: [
                (True, False, False, False, False),
                (False, True, True, False, False),
            ],
        }

        for append_side, expected in expected_by_side.items():
            with self.subTest(append_side=append_side):
                destination = Plane()
                source = Plane(initial_state=[row[:] for row in source_state])

                destination.append_plane(
                    source, append_side=append_side, space_between=2
                )

                self.assertEqual(destination.state, expected)
                self.assertEqual(source.state, source_state)
                source.state[0][0] = False
                self.assertEqual(destination.state, expected)

    def test_append_plane_empty_source_is_a_no_op_on_each_side(self):
        destination_state = [[True, False, True], [False, True, False]]

        for append_side in (BOTTOM, LEFT, TOP, RIGHT):
            with self.subTest(append_side=append_side):
                destination = Plane(
                    initial_state=[row[:] for row in destination_state]
                )

                destination.append_plane(Plane(), append_side=append_side)

                self.assertEqual(destination.state, destination_state)

    def test_append_plane_self_composition_matches_independent_source_on_each_side(
        self,
    ):
        source_state = [[True, False, False], [False, True, True]]

        for append_side in (BOTTOM, LEFT, TOP, RIGHT):
            with self.subTest(append_side=append_side):
                expected = Plane(initial_state=[row[:] for row in source_state])
                expected.append_plane(
                    Plane(initial_state=[row[:] for row in source_state]),
                    append_side=append_side,
                    space_between=1,
                )

                actual = Plane(initial_state=[row[:] for row in source_state])
                actual.append_plane(
                    actual, append_side=append_side, space_between=1
                )

                self.assertEqual(actual.state, expected.state)

    def test_append_plane_preserves_source_geometry_when_rotating_for_side(self):
        destination = Plane(initial_state=[[False, False], [False, False]])
        source = Plane(initial_state=[[True, False, False], [False, True, False]])

        destination.append_plane(source, append_side=RIGHT, space_between=0)

        self.assertEqual(
            source.state,
            [[True, False, False], [False, True, False]],
        )
        self.assertEqual((source.x_len(), source.y_len()), (3, 2))
        self.assertEqual(
            destination.state,
            [
                (True, False, False, False, False),
                (False, True, False, False, False),
            ],
        )

    def test_append_plane_rejects_non_integer_controls_before_rotation(self):
        source = Plane(initial_state=[[True, False], [False, True]])
        original_state = [[True, False], [False, True]]

        for append_side in (BOTTOM, LEFT, TOP, RIGHT):
            for invalid_kwargs in ({"n": 1.5}, {"space_between": 1.5}):
                with self.subTest(append_side=append_side, invalid_kwargs=invalid_kwargs):
                    destination = Plane(initial_state=[row[:] for row in original_state])

                    parameter = next(iter(invalid_kwargs))
                    with self.assertRaisesRegex(
                        TypeError, f"{parameter} must be an integer"
                    ):
                        destination.append_plane(
                            source,
                            append_side=append_side,
                            **invalid_kwargs,
                        )

                    self.assertEqual(destination.state, original_state)

    def test_append_plane_bottom_rejects_non_integer_controls_before_appending(self):
        destination = Plane(initial_state=[[False, False]])
        source = Plane(initial_state=[[True, False]])

        for invalid_kwargs in ({"n": 1.5}, {"space_between": 1.5}):
            with self.subTest(invalid_kwargs=invalid_kwargs):
                with self.assertRaises(TypeError):
                    destination.append_plane_bottom(source, **invalid_kwargs)

                self.assertEqual(destination.state, [[False, False]])

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
