import unittest

from board import Board
from rules.conways_rule import ConwaysRule
from rules.rule import Rule


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

    def test_find_cycle_period_detects_period_three(self):
        states = [[[False]], [[True]], [[True, True]]]
        board = Board(initial_state=states[0])
        calls = 0

        def next_state(rule):
            nonlocal calls
            calls += 1
            return states[calls % len(states)]

        board.get_new_state = next_state

        self.assertEqual(board.find_cycle_period(Rule(), max_generations=4), 3)

    def test_find_cycle_period_detects_padded_pulsar(self):
        pulsar = [
            [cell == "X" for cell in row]
            for row in (
                "...............",
                "...XXX...XXX...",
                "...............",
                ".X....X.X....X.",
                ".X....X.X....X.",
                ".X....X.X....X.",
                "...XXX...XXX...",
                "...............",
                "...XXX...XXX...",
                ".X....X.X....X.",
                ".X....X.X....X.",
                ".X....X.X....X.",
                "...............",
                "...XXX...XXX...",
                "...............",
            )
        ]
        board = Board(initial_state=pulsar)

        self.assertEqual(board.find_cycle_period(ConwaysRule(), max_generations=3), 3)

    def test_apply_rule_computes_the_next_state_once(self):
        board = Board(initial_state=[[False]])
        calls = []

        def next_state(rule):
            calls.append(True)
            return [[True]]

        board.get_new_state = next_state

        self.assertFalse(board.apply_rule(Rule()))
        self.assertEqual(calls, [True])
        self.assertEqual(board.state, [[True]])


if __name__ == "__main__":
    unittest.main()
