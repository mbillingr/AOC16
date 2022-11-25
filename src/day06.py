from collections import Counter

from utils.puzzle import Puzzle
from utils import parsing as p


PARSER = p.SeparatedList(
    p.String(p.OneOf("abcdefghijklmnopqrstuvwxyz") * ...),
    p.Str("\n"),
)


class Day06(Puzzle):
    def parse(self, input: str):
        return PARSER.parse(input)

    def solve(self, parsed):
        result = ""
        for i in range(len(parsed[0])):
            counter = Counter(msg[i] for msg in parsed)
            result += self.select(counter)
        return result


class Part1(Day06):
    def __init__(self):
        super().__init__("Day 06/1")

    def select(self, counter):
        return counter.most_common()[0][0]


class Part2(Day06):
    def __init__(self):
        super().__init__("Day 06/2")

    def select(self, counter):
        return counter.most_common()[-1][0]


EXAMPLE1 = """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
"""


Part1().check(EXAMPLE1, "easter")
Part1().run("../data/input06.txt")

Part2().check(EXAMPLE1, "advent")
Part2().run("../data/input06.txt")
