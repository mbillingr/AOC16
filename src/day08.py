from collections import Counter
from functools import reduce

import numpy as np
from matplotlib import pyplot as plt

from utils.puzzle import Puzzle
from utils import parsing as p

RECT = p.Group(p.Str("rect") + p.Drop(" ") + p.Number() + p.Drop("x") + p.Number())
ROT_ROW = p.Group(
    p.Str("rotate row") + p.Drop(" y=") + p.Number() + p.Drop(" by ") + p.Number()
)
ROT_COL = p.Group(
    p.Str("rotate column") + p.Drop(" x=") + p.Number() + p.Drop(" by ") + p.Number()
)
PARSER = p.SeparatedList(
    RECT | ROT_ROW | ROT_COL,
    p.Str("\n"),
)


class Day07(Puzzle):
    def __init__(self, height: int, width: int, name: str):
        super().__init__(name)
        self.display = np.zeros((height, width))

    def parse(self, input: str):
        return PARSER.parse(input)

    def apply_op(self, op):
        match op:
            case ("rect", x, y):
                self.display[:y, :x] = 1
            case ("rotate row", y, n):
                self.display[y, :] = np.roll(self.display[y, :], n)
            case ("rotate column", x, n):
                self.display[:, x] = np.roll(self.display[:, x], n)


class Part1(Day07):
    def __init__(self, height: int, width: int):
        super().__init__(height, width, "Day 07/1")

    def solve(self, parsed):
        for op in parsed:
            self.apply_op(op)
        plt.imshow(self.display)
        return np.sum(self.display)


class Part2(Day07):
    def __init__(self, height: int, width: int):
        super().__init__(height, width, "Day 07/2")

    def solve(self, parsed):
        for op in parsed:
            self.apply_op(op)


EXAMPLE1 = """rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
"""


Part1(3, 7).check(EXAMPLE1, 6)
Part1(6, 50).run("../data/input08.txt")

plt.title("Part 2")
plt.show()
