import itertools

from utils.puzzle import Puzzle
from utils import parsing as p


PARSER1 = p.Repeat(
    p.Group(p.Repeat(p.SkipWhitespace() + p.Number())) + p.Drop(p.Optional(p.Str("\n")))
)

PARSER2 = p.Repeat(
    p.Repeat(p.SkipWhitespace() + p.Number()) + p.Drop(p.Optional(p.Str("\n")))
)


class Part1(Puzzle):
    def __init__(self):
        super().__init__("Day 03/1")

    def parse(self, input: str):
        return PARSER1.parse(input)

    def solve(self, parsed):
        return sum(1 for triple in parsed if is_possible(triple))


class Part2(Puzzle):
    def __init__(self):
        super().__init__("Day 03/2")

    def parse(self, input: str):
        return PARSER2.parse(input)

    def solve(self, parsed):
        arranged = parsed[0::3] + parsed[1::3] + parsed[2::3]
        arranged = iter(arranged)
        triples = iter(lambda: tuple(itertools.islice(arranged, 3)), ())
        return sum(1 for triple in triples if is_possible(triple))


def is_possible(triple):
    triple = sorted(triple)
    return triple[0] + triple[1] > triple[2]


Part1().check("5 10 25", 0)
Part1().check("5 10 25\n11 11 11", 1)
Part1().run("../data/input03.txt")

Part2().run("../data/input03.txt")
