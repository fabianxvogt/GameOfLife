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

    def test_empty_plane_copy_rotate_preserves_zero_dimensions(self):
        original = Plane()
        copied = original.copy()

        original.rotate()
        copied.rotate_by(4)

        for plane in (original, copied):
            with self.subTest(plane=plane):
                self.assertEqual(plane.state, [])
                self.assertEqual((plane.x_len(), plane.y_len()), (0, 0))

        self.assertIsNot(original.state, copied.state)

    def test_copy_after_rotation_keeps_rows_mutable(self):
        original = Plane(initial_state=[[True, False], [False, True]])
        original.rotate()

        copied = original.copy()
        copied.add_empty_col()

        self.assertEqual(
            copied.state,
            [[False, True, False], [True, False, False]],
        )
        self.assertEqual(original.state, [(False, True), (True, False)])

    def test_repeated_rotations_keep_column_mutation_source_owned(self):
        source_state = [[True, False, False], [False, True, True]]
        original = Plane(initial_state=[row[:] for row in source_state])
        rotated = original.copy().rotate_by(8)

        rotated.add_empty_col()

        self.assertEqual(
            rotated.state,
            [row + [False] for row in source_state],
        )
        self.assertEqual(original.state, source_state)

    def test_composition_and_repeated_rotation_keep_rows_mutable_and_source_owned(
        self,
    ):
        source = Plane(
            initial_state=[[True, False, True], [False, True, False]]
        )
        source.rotate_by(8)
        source_snapshot = [list(row) for row in source.state]

        for append_side in (BOTTOM, LEFT, TOP, RIGHT):
            with self.subTest(append_side=append_side):
                destination = Plane(
                    initial_state=[[False, False], [False, False]]
                )

                destination.append_plane(
                    source,
                    append_side=append_side,
                    n=2,
                    space_between=1,
                )
                destination.rotate_by(4)
                destination.add_empty_col()
                destination.state[0][0] = not destination.state[0][0]

                self.assertTrue(
                    all(isinstance(row, list) for row in destination.state)
                )
                self.assertEqual(
                    [list(row) for row in source.state], source_snapshot
                )

    def test_rotate_by_full_turn_preserves_minimal_plane(self):
        plane = Plane(initial_state=[[True]])

        self.assertIs(plane.rotate_by(4), plane)
        self.assertEqual(plane.state, [(True,)])
        self.assertEqual((plane.x_len(), plane.y_len()), (1, 1))

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

    def test_empty_plane_reports_zero_dimensions_before_composition(self):
        destination = Plane()

        self.assertEqual((destination.x_len(), destination.y_len()), (0, 0))

        destination.append_plane(
            Plane(initial_state=[[True]]), append_side=BOTTOM, space_between=0
        )

        self.assertEqual((destination.x_len(), destination.y_len()), (1, 1))

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

    def test_append_plane_bottom_pads_unequal_widths_without_losing_cells(self):
        destination = Plane(initial_state=[[True, False]])
        source = Plane(initial_state=[[False, True, False], [True, True, False]])

        destination.append_plane_bottom(source, space_between=1)

        self.assertEqual(
            destination.state,
            [
                [True, False, False],
                [False, False, False],
                [False, True, False],
                [True, True, False],
            ],
        )
        self.assertEqual(sum(map(sum, destination.state)), 4)
        self.assertTrue(all(len(row) == 3 for row in destination.state))

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

    def test_append_plane_preserves_unequal_geometry_on_each_side(self):
        cases = [
            (
                [[True, False], [False, False]],
                [[False, True, False], [True, True, False]],
            ),
            (
                [[True, False, True], [False, False, True]],
                [[False, True]],
            ),
        ]

        expected_first_case = {
            BOTTOM: [
                [True, False, False],
                [False, False, False],
                [False, False, False],
                [False, True, False],
                [True, True, False],
            ],
            LEFT: [
                (True, False, False, False, True, False),
                (False, False, False, True, True, False),
            ],
            TOP: [
                (False, True, False),
                (True, True, False),
                (False, False, False),
                (True, False, False),
                (False, False, False),
            ],
            RIGHT: [
                (False, True, False, False, True, False),
                (True, True, False, False, False, False),
            ],
        }

        for case_number, (destination_state, source_state) in enumerate(cases):
            destination_height = len(destination_state)
            destination_width = len(destination_state[0])
            source_height = len(source_state)
            source_width = len(source_state[0])
            expected_population = sum(map(sum, destination_state)) + sum(
                map(sum, source_state)
            )

            for append_side in (BOTTOM, LEFT, TOP, RIGHT):
                with self.subTest(
                    append_side=append_side,
                    destination_width=destination_width,
                    source_width=source_width,
                ):
                    destination = Plane(
                        initial_state=[row[:] for row in destination_state]
                    )
                    source = Plane(initial_state=[row[:] for row in source_state])

                    destination.append_plane(
                        source,
                        append_side=append_side,
                        space_between=1,
                    )

                    if append_side in (BOTTOM, TOP):
                        expected_height = (
                            destination_height + source_height + 1
                        )
                        expected_width = max(destination_width, source_width)
                    else:
                        expected_height = max(destination_height, source_height)
                        expected_width = (
                            destination_width + source_width + 1
                        )

                    self.assertEqual(len(destination.state), expected_height)
                    self.assertEqual(
                        {len(row) for row in destination.state},
                        {expected_width},
                    )
                    self.assertEqual(
                        sum(map(sum, destination.state)), expected_population
                    )
                    self.assertEqual(source.state, source_state)
                    if case_number == 0:
                        self.assertEqual(
                            destination.state, expected_first_case[append_side]
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

    def test_append_plane_rejects_boolean_controls_before_empty_destination_noop(
        self,
    ):
        source_state = [[True]]

        for append_side in (BOTTOM, LEFT, TOP, RIGHT):
            for invalid_kwargs in ({"n": True}, {"space_between": False}):
                with self.subTest(
                    append_side=append_side, invalid_kwargs=invalid_kwargs
                ):
                    destination = Plane()
                    source = Plane(initial_state=[row[:] for row in source_state])

                    with self.assertRaisesRegex(
                        TypeError,
                        next(iter(invalid_kwargs)) + " must be an integer",
                    ):
                        destination.append_plane(
                            source,
                            append_side=append_side,
                            **invalid_kwargs,
                        )

                    self.assertEqual(destination.state, [])
                    self.assertEqual(source.state, source_state)

    def test_append_plane_bottom_rejects_boolean_controls_before_one_cell_mutation(
        self,
    ):
        source = Plane(initial_state=[[True]])

        for invalid_kwargs in ({"n": True}, {"space_between": False}):
            with self.subTest(invalid_kwargs=invalid_kwargs):
                destination = Plane(initial_state=[[False]])

                with self.assertRaisesRegex(
                    TypeError,
                    next(iter(invalid_kwargs)) + " must be an integer",
                ):
                    destination.append_plane_bottom(source, **invalid_kwargs)

                self.assertEqual(destination.state, [[False]])
                self.assertEqual(source.state, [[True]])

    def test_append_plane_rejects_invalid_sides_before_mutation(self):
        source_state = [[True, False, False], [False, True, True]]
        destination_state = [[False, False], [True, False]]
        invalid_sides = (
            (4, ValueError),
            (-1, ValueError),
            (1.0, TypeError),
            (1.5, TypeError),
            (False, TypeError),
            (True, TypeError),
            ("right", TypeError),
            (None, TypeError),
        )

        for append_side, exception_type in invalid_sides:
            with self.subTest(append_side=append_side):
                destination = Plane(
                    initial_state=[row[:] for row in destination_state]
                )
                source = Plane(initial_state=[row[:] for row in source_state])

                with self.assertRaisesRegex(
                    exception_type,
                    "append_side must be one of BOTTOM, LEFT, TOP, RIGHT",
                ):
                    destination.append_plane(
                        source,
                        append_side=append_side,
                        n=2,
                        space_between=1,
                    )

                self.assertEqual(destination.state, destination_state)
                self.assertEqual(source.state, source_state)

    def test_append_plane_non_positive_repetition_is_a_no_op_on_each_side(self):
        source_state = [[True, False], [False, True]]
        destination_state = [[False, True], [True, False]]

        for append_side in (BOTTOM, LEFT, TOP, RIGHT):
            for n in (0, -1):
                with self.subTest(append_side=append_side, n=n):
                    destination = Plane(
                        initial_state=[row[:] for row in destination_state]
                    )
                    source = Plane(initial_state=[row[:] for row in source_state])

                    destination.append_plane(
                        source,
                        append_side=append_side,
                        n=n,
                        space_between=2,
                    )

                    self.assertEqual(destination.state, destination_state)
                    self.assertEqual(source.state, source_state)

    def test_negative_spacing_is_bounded_no_gap_behavior(self):
        source_state = [[True, False], [False, True]]
        destination_state = [[False, True], [True, False]]

        for append_side in (BOTTOM, LEFT, TOP, RIGHT):
            with self.subTest(append_side=append_side):
                expected = Plane(
                    initial_state=[row[:] for row in destination_state]
                )
                expected.append_plane(
                    Plane(initial_state=[row[:] for row in source_state]),
                    append_side=append_side,
                    n=2,
                    space_between=0,
                )

                actual = Plane(
                    initial_state=[row[:] for row in destination_state]
                )
                source = Plane(initial_state=[row[:] for row in source_state])
                actual.append_plane(
                    source,
                    append_side=append_side,
                    n=2,
                    space_between=-1,
                )

                self.assertEqual(actual.state, expected.state)
                self.assertEqual(source.state, source_state)

    def test_append_plane_bottom_non_positive_repetition_is_a_no_op(self):
        destination = Plane(initial_state=[[False, True], [True, False]])
        source = Plane(initial_state=[[True, False], [False, True]])
        original_state = [row[:] for row in destination.state]

        for n in (0, -1):
            with self.subTest(n=n):
                destination.append_plane_bottom(
                    source, n=n, space_between=2
                )
                self.assertEqual(destination.state, original_state)
                self.assertEqual(source.state, [[True, False], [False, True]])

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

    def test_insert_plane_accepts_exact_bottom_right_fit_without_extension(self):
        destination = Plane(initial_state=[[False, False], [False, False]])
        source = Plane(initial_state=[[True]])

        destination.insert_plane_at(source, 1, 1)

        self.assertEqual(
            destination.state,
            [[False, False], [False, True]],
        )

    def test_insert_plane_accepts_exact_top_right_fit_without_source_aliasing(self):
        destination = Plane(initial_state=[[False] * 5 for _ in range(4)])
        source_state = [[True, False], [False, True], [True, True]]
        source = Plane(initial_state=[row[:] for row in source_state])

        destination.insert_plane_at(source, 3, 0)

        self.assertEqual(
            destination.state,
            [
                [False, False, False, True, False],
                [False, False, False, False, True],
                [False, False, False, True, True],
                [False, False, False, False, False],
            ],
        )
        self.assertEqual(source.state, source_state)

        destination.state[0][3] = False

        self.assertEqual(source.state, source_state)

    def test_insert_plane_rejects_invalid_coordinate_controls_before_mutation(self):
        source_state = [[True, False], [False, True]]
        destination_state = [[False, False], [False, False]]
        invalid_controls = (
            (True, 0, False, "start_x must be an integer"),
            (0, False, False, "start_y must be an integer"),
            (1.5, 0, False, "start_x must be an integer"),
            (0, 1.5, False, "start_y must be an integer"),
            (0, 0, 0, "allow_plane_extension must be a boolean"),
            (0, 0, "yes", "allow_plane_extension must be a boolean"),
        )

        for start_x, start_y, allow_extension, message in invalid_controls:
            with self.subTest(
                start_x=start_x,
                start_y=start_y,
                allow_extension=allow_extension,
            ):
                destination = Plane(
                    initial_state=[row[:] for row in destination_state]
                )
                source = Plane(initial_state=[row[:] for row in source_state])

                with self.assertRaisesRegex(TypeError, message):
                    destination.insert_plane_at(
                        source,
                        start_x,
                        start_y,
                        allow_plane_extension=allow_extension,
                    )

                self.assertEqual(destination.state, destination_state)
                self.assertEqual(source.state, source_state)

    def test_insert_plane_in_all_corners_empty_source_is_a_no_op(self):
        destination_state = [[False, True, False], [True, False, True]]
        destination = Plane(initial_state=[row[:] for row in destination_state])

        destination.insert_plane_in_all_corners(Plane())

        self.assertEqual(destination.state, destination_state)

    def test_insert_plane_in_all_corners_preserves_asymmetric_coordinates_and_source(self):
        source_state = [[True, False, False], [False, True, True]]
        source = Plane(initial_state=[row[:] for row in source_state])
        destination = Plane(initial_state=[[False] * 7 for _ in range(8)])

        destination.insert_plane_in_all_corners(source)

        self.assertEqual(
            {
                (y, x)
                for y, row in enumerate(destination.state)
                for x, cell in enumerate(row)
                if cell
            },
            {
                (0, 0), (1, 1), (1, 2),
                (0, 6), (1, 5), (2, 5),
                (6, 4), (6, 5), (7, 6),
                (5, 1), (6, 1), (7, 0),
            },
        )
        self.assertEqual(source.state, source_state)

        destination.state[0][0] = False
        self.assertEqual(source.state, source_state)

    def test_insert_plane_in_all_corners_rejects_partial_fit_without_mutation(self):
        destination_state = [[False, False] for _ in range(3)]
        source_state = [[True, False], [False, True], [True, True]]
        destination = Plane(initial_state=[row[:] for row in destination_state])
        source = Plane(initial_state=[row[:] for row in source_state])

        with self.assertRaisesRegex(ValueError, "Out of bounds!"):
            destination.insert_plane_in_all_corners(source)

        self.assertEqual(destination.state, destination_state)
        self.assertEqual(source.state, source_state)


if __name__ == "__main__":
    unittest.main()
