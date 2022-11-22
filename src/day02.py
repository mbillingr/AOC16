from utils import manhattan as mt
from utils.puzzle import Puzzle
from utils import parsing as p


PARSER = p.SeparatedList(
    p.Group((p.Str("U") | p.Str("D") | p.Str("L") | p.Str("R")) * ...),
    p.Str("\n"),
)


class Day02(Puzzle):
    def parse(self, input: str):
        return PARSER.parse(input)

    def solve(self, parsed):
        pos = next(p for p, k in self.keypad.items() if k == "5")
        result = ""
        for row in parsed:
            for d in row:
                match d:
                    case "U":
                        pos_ = pos + mt.NORTH
                    case "D":
                        pos_ = pos + mt.SOUTH
                    case "L":
                        pos_ = pos + mt.WEST
                    case "R":
                        pos_ = pos + mt.EAST
                    case _:
                        raise ValueError(d)
                if pos_ in self.keypad:
                    pos = pos_
            result += self.keypad[pos]
        return result


class Part1(Day02):
    def __init__(self):
        super().__init__("Day 02/1")
        self.keypad = {
            mt.Point(0, 2): "1",
            mt.Point(1, 2): "2",
            mt.Point(2, 2): "3",
            mt.Point(0, 1): "4",
            mt.Point(1, 1): "5",
            mt.Point(2, 1): "6",
            mt.Point(0, 0): "7",
            mt.Point(1, 0): "8",
            mt.Point(2, 0): "9",
        }


class Part2(Day02):
    def __init__(self):
        super().__init__("Day 02/2")
        self.keypad = {
            mt.Point(2, 4): "1",
            mt.Point(1, 3): "2",
            mt.Point(2, 3): "3",
            mt.Point(3, 3): "4",
            mt.Point(0, 2): "5",
            mt.Point(1, 2): "6",
            mt.Point(2, 2): "7",
            mt.Point(3, 2): "8",
            mt.Point(4, 2): "9",
            mt.Point(1, 1): "A",
            mt.Point(2, 1): "B",
            mt.Point(3, 1): "C",
            mt.Point(2, 0): "D",
        }


Part1().check("ULL\nRRDDD\nLURDL\nUUUUD", "1985")
Part1().run("../data/input02.txt")

Part2().check("ULL\nRRDDD\nLURDL\nUUUUD", "5DB3")
Part2().run("../data/input02.txt")
