import unittest

from board import Board
from rules.conways_rule import ConwaysRule


class BoardTest(unittest.TestCase):
    def test_apply_rule_advances_a_blinker(self):
        board = Board(
            initial_state=[
                [False, True, False],
                [False, True, False],
                [False, True, False],
            ]
        )

        self.assertFalse(board.apply_rule(ConwaysRule()))
        self.assertEqual(
            board.state,
            [
                [False, False, False],
                [True, True, True],
                [False, False, False],
            ],
        )

    def test_apply_rule_reports_a_still_life_as_stable(self):
        block = [
            [True, True],
            [True, True],
        ]
        board = Board(initial_state=block)

        self.assertTrue(board.apply_rule(ConwaysRule()))
        self.assertEqual(board.state, block)

    def test_apply_rule_reports_a_blinker_stable_after_two_steps(self):
        vertical = [
            [False, True, False],
            [False, True, False],
            [False, True, False],
        ]
        horizontal = [
            [False, False, False],
            [True, True, True],
            [False, False, False],
        ]
        board = Board(initial_state=vertical)
        rule = ConwaysRule()

        self.assertFalse(board.apply_rule(rule))
        self.assertEqual(board.state, horizontal)
        self.assertTrue(board.apply_rule(rule))
        self.assertEqual(board.state, vertical)

    def test_apply_rule_handles_rectangular_boards(self):
        board = Board(
            initial_state=[
                [False, False, False],
                [False, False, False],
            ]
        )

        self.assertTrue(board.apply_rule(ConwaysRule()))
        self.assertEqual(
            board.state,
            [
                [False, False, False],
                [False, False, False],
            ],
        )

    def test_apply_rule_computes_the_next_state_once(self):
        board = Board(initial_state=[[False]])
        calls = []

        def next_state(_rule):
            calls.append(True)
            return [[True]]

        board.get_new_state = next_state

        self.assertFalse(board.apply_rule(object()))
        self.assertEqual(calls, [True])
        self.assertEqual(board.state, [[True]])


if __name__ == "__main__":
    unittest.main()
