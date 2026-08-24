import unittest

from board import Board
from rules.conways_rule import ConwaysRule
from rules.highlife_rule import HighLifeRule


def neighbours_with(count):
    return [index < count for index in range(8)]


class HighLifeRuleTest(unittest.TestCase):
    def setUp(self):
        self.rule = HighLifeRule()

    def test_survival_is_two_or_three_neighbours(self):
        self.assertTrue(self.rule.cell_is_alive(True, neighbours_with(2)))
        self.assertTrue(self.rule.cell_is_alive(True, neighbours_with(3)))
        self.assertFalse(self.rule.cell_is_alive(True, neighbours_with(1)))
        self.assertFalse(self.rule.cell_is_alive(True, neighbours_with(4)))

    def test_birth_is_three_or_six_neighbours(self):
        self.assertTrue(self.rule.cell_is_alive(False, neighbours_with(3)))
        self.assertTrue(self.rule.cell_is_alive(False, neighbours_with(6)))
        self.assertFalse(self.rule.cell_is_alive(False, neighbours_with(2)))
        self.assertFalse(self.rule.cell_is_alive(False, neighbours_with(5)))

    def test_rejects_invalid_neighbour_lists(self):
        with self.assertRaises(ValueError):
            self.rule.cell_is_alive(False, [True] * 7)
        with self.assertRaises(ValueError):
            self.rule.cell_is_alive(False, [True] * 7 + [1])

    def test_six_neighbour_birth_differs_from_conway(self):
        state = [
            [True, True, False],
            [True, False, True],
            [False, True, True],
        ]
        highlife_board = Board(initial_state=state)
        conway_board = Board(initial_state=state)

        highlife_board.apply_rule(self.rule)
        conway_board.apply_rule(ConwaysRule())

        self.assertTrue(highlife_board.state[1][1])
        self.assertFalse(conway_board.state[1][1])


if __name__ == "__main__":
    unittest.main()
