import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from board import Board
from cli import build_rule, load_board, main, run_interactive, run_steps
from creatures.single.glider import GLIDER
from rules.conways_rule import ConwaysRule
from rules.highlife_rule import HighLifeRule


class CliTest(unittest.TestCase):
    def test_run_steps_renders_generation_zero_and_advances(self):
        board = Board(
            initial_state=[
                [False, True, False],
                [False, True, False],
                [False, True, False],
            ]
        )

        frames = run_steps(board, ConwaysRule(), 1)

        self.assertEqual(len(frames), 2)
        self.assertEqual(frames[0], "Generation 0\n_X_\n_X_\n_X_")
        self.assertEqual(frames[1], "Generation 1\n___\nXXX\n___")

    def test_load_board_reads_pattern_file_without_sharing_state(self):
        with TemporaryDirectory() as temporary_directory:
            pattern_path = Path(temporary_directory) / "pattern.txt"
            pattern_path.write_text("_X_\n__X\nXXX\n", encoding="utf-8")

            board = load_board(pattern_path)

        self.assertEqual(board.state, GLIDER.state)
        board.state[0][1] = False
        self.assertTrue(GLIDER.state[0][1])

    def test_load_board_places_pattern_at_requested_offset(self):
        with TemporaryDirectory() as temporary_directory:
            pattern_path = Path(temporary_directory) / "pattern.txt"
            pattern_path.write_text("XX\n_X\n", encoding="utf-8")

            board = load_board(pattern_path, start_x=1, start_y=2)

        self.assertEqual(
            board.state,
            [
                [False, False, False],
                [False, False, False],
                [False, True, True],
                [False, False, True],
            ],
        )

    def test_load_board_rejects_negative_placement_offsets(self):
        with self.assertRaises(ValueError):
            load_board(start_x=-1)

    def test_main_places_saved_pattern_with_cli_offsets(self):
        with TemporaryDirectory() as temporary_directory:
            pattern_path = Path(temporary_directory) / "pattern.txt"
            pattern_path.write_text("XX\nXX\n", encoding="utf-8")

            from contextlib import redirect_stdout
            from io import StringIO

            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "--pattern",
                        str(pattern_path),
                        "--x",
                        "1",
                        "--y",
                        "2",
                        "--steps",
                        "0",
                    ]
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            output.getvalue(), "Generation 0\n___\n___\n_XX\n_XX\n"
        )

    def test_rule_selection_includes_highlife(self):
        self.assertIsInstance(build_rule("highlife"), HighLifeRule)

    def test_interactive_session_supports_step_reset_and_quit(self):
        board = load_board()
        commands = iter(["", "reset", "quit"])
        output = []

        result = run_interactive(
            board,
            ConwaysRule(),
            input_fn=lambda prompt: next(commands),
            output_fn=output.append,
        )

        self.assertEqual(output[0].splitlines()[0], "Generation 0")
        self.assertEqual(output[1].splitlines()[0], "Generation 1")
        self.assertEqual(output[2].splitlines()[0], "Generation 0")
        self.assertEqual(result.state, GLIDER.state)

    def test_main_can_print_a_saved_pattern_without_stepping(self):
        with TemporaryDirectory() as temporary_directory:
            pattern_path = Path(temporary_directory) / "pattern.txt"
            pattern_path.write_text("XX\nXX\n", encoding="utf-8")

            from contextlib import redirect_stdout
            from io import StringIO

            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(["--pattern", str(pattern_path), "--steps", "0"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue(), "Generation 0\nXX\nXX\n")


if __name__ == "__main__":
    unittest.main()
