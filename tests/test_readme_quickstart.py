import unittest
from pathlib import Path

from board import Board
from rules.conways_rule import ConwaysRule


class ReadmeQuickstartTest(unittest.TestCase):
    def test_readme_documents_dependency_free_setup(self):
        readme = Path(__file__).parents[1] / "README.md"
        readme_text = readme.read_text(encoding="utf-8")

        self.assertIn("Python's standard library", readme_text)
        self.assertIn("python3 -m pytest -q", readme_text)

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
