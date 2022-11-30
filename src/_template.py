from typing import Any

from utils.puzzle import Puzzle, DirectInput
from utils import parsing as p


PARSER = p.SeparatedList(
    p.String(p.NotOneOf("\n") * ...),
    p.Str("\n"),
)


class Day00(Puzzle):
    def __init__(self, part: Any):
        super().__init__(f"Day 05/{part}")

    def parse(self, input: str):
        return PARSER.parse(input)


class Part1(Day00):
    def __init__(self):
        super().__init__("1")

    def solve(self, parsed):
        print(parsed)


class Part2(Day00):
    def __init__(self):
        super().__init__("2")

    def solve(self, parsed):
        print(parsed)


Part1().check("abc", "expected")
Part1().run(DirectInput("abcdefg"))  # or filename instead of DirectInput

Part2().check("abc", "expected")
Part2().run(DirectInput("abcdefg"))  # or filename instead of DirectInput
