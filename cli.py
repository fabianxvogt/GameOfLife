"""Small dependency-free command-line runner for bounded board stepping."""

from __future__ import annotations

import argparse
import copy
from pathlib import Path
from typing import Callable, Optional, Sequence

from board import Board
from creatures.creature import CreatureLoader
from creatures.single.glider import GLIDER
from rules.conways_rule import ConwaysRule
from rules.highlife_rule import HighLifeRule
from rules.rule import Rule


def non_negative_int(value: str) -> int:
    """Parse a non-negative integer for bounded command-line options."""
    try:
        parsed = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be an integer") from error
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be non-negative")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Step a finite Game of Life board and print each generation."
    )
    parser.add_argument(
        "--pattern",
        type=Path,
        help="X/_ pattern file to load; defaults to the built-in glider",
    )
    parser.add_argument(
        "--rule",
        choices=("conway", "highlife"),
        default="conway",
        help="rule used for each generation (default: conway)",
    )
    parser.add_argument(
        "--steps",
        default=1,
        type=non_negative_int,
        help="number of generations to print after generation zero",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="wait for Enter/step, reset, or quit commands instead of a fixed run",
    )
    return parser


def build_rule(name: str) -> Rule:
    """Return the selected built-in rule."""
    return {"conway": ConwaysRule, "highlife": HighLifeRule}[name]()


def load_board(pattern_path: Optional[Path] = None) -> Board:
    """Load a pattern into an isolated finite board."""
    creature = (
        CreatureLoader.load_creature_from_file(pattern_path)
        if pattern_path is not None
        else GLIDER
    )
    return Board(initial_state=copy.deepcopy(creature.state))


def render_frame(board: Board, generation: int) -> str:
    return f"Generation {generation}\n{board!r}"


def run_steps(board: Board, rule: Rule, steps: int) -> list[str]:
    """Advance ``board`` and return rendered frames from generation zero onward."""
    frames = [render_frame(board, 0)]
    for generation in range(1, steps + 1):
        board.apply_rule(rule)
        frames.append(render_frame(board, generation))
    return frames


def run_interactive(
    board: Board,
    rule: Rule,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> Board:
    """Run a prompt-driven session and return the current board on exit."""
    initial_state = copy.deepcopy(board.state)
    generation = 0
    output_fn(render_frame(board, generation))

    while True:
        try:
            command = input_fn("Command [Enter=step, r=reset, q=quit]: ")
        except EOFError:
            break
        command = command.strip().lower()

        if command in {"q", "quit", "exit"}:
            break
        if command in {"", "s", "step"}:
            board.apply_rule(rule)
            generation += 1
            output_fn(render_frame(board, generation))
            continue
        if command in {"r", "reset"}:
            board = Board(initial_state=copy.deepcopy(initial_state))
            generation = 0
            output_fn(render_frame(board, generation))
            continue
        output_fn("Unknown command. Use Enter, s/step, r/reset, or q/quit.")

    return board


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    board = load_board(args.pattern)
    rule = build_rule(args.rule)

    if args.interactive:
        run_interactive(board, rule)
    else:
        print("\n\n".join(run_steps(board, rule, args.steps)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
