from typing import Any

from utils.puzzle import Puzzle
from utils import parsing as p


RUNLEN = p.Group(
    p.Drop("(") + p.Number() + p.Drop("x") + p.Number() + p.Drop(")")
) + p.String(p.Repeat(p.AnyChar()))


class Day00(Puzzle):
    def __init__(self, part: Any):
        super().__init__(f"Day 05/{part}")

    def parse(self, input: str):
        return self.decompress(input)

    def decompress(self, input: str):
        input = "".join(input.split())
        output = ""
        while input:
            if input[0] == "(":
                s, rest = self.parse_compressed(input)
            else:
                s, rest = self.parse_literal(input)
            output += s
            input = rest
        return output

    def parse_literal(self, input: str) -> tuple[str, str]:
        idx = input.find("(")
        if idx == -1:
            return input, ""
        return input[:idx], input[idx:]


class Part1(Day00):
    def __init__(self):
        super().__init__("1")

    def parse_compressed(self, input: str) -> tuple[str, str]:
        (n_ch, times), rest = RUNLEN.parse(input)
        pattern, rest = rest[:n_ch], rest[n_ch:]
        return pattern * times, rest

    def solve(self, parsed):
        return len(parsed)


class Part2(Day00):
    def __init__(self):
        super().__init__("2")

    def parse_compressed(self, input: str) -> tuple[str, str]:
        (n_ch, times), rest = RUNLEN.parse(input)
        pattern, rest = rest[:n_ch], rest[n_ch:]
        pattern = self.decompress(pattern)
        return pattern * times, rest

    def solve(self, parsed):
        return len(parsed)


Part1().check("ADVENT", 6)
Part1().check("A(1x5)BC", 7)
Part1().check("(3x3)XYZ", 9)
Part1().check("A(2x2)BCD(2x2)EFG", 11)
Part1().check("(6x1)(1x3)A", 6)
Part1().check("X(8x2)(3x3)ABCY", 18)
Part1().run("../data/input09.txt", wrong=(152852,))

Part2().check("(3x3)XYZ", 9)
Part2().check("X(8x2)(3x3)ABCY", len("XABCABCABCABCABCABCY"))
Part2().check("(27x12)(20x12)(13x14)(7x10)(1x12)A", 241920)
Part2().check("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN", 445)
Part2().run("../data/input09.txt")
