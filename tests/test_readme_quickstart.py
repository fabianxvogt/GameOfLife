import unittest

from board import Board
from rules.conways_rule import ConwaysRule


class ReadmeQuickstartTest(unittest.TestCase):
    def test_blinker_example_matches_documented_output(self):
        board = Board(
            initial_state=[
                [False, True, False],
                [False, True, False],
                [False, True, False],
            ]
        )

        before = repr(board)
        board.apply_rule(ConwaysRule())

        self.assertEqual(before, "_X_\n_X_\n_X_")
        self.assertEqual(repr(board), "___\nXXX\n___")
