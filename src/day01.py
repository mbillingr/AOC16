from utils import manhattan as mt
from utils.puzzle import Puzzle
from utils import parsing as p


PARSER = p.SeparatedList((p.Str("R") | p.Str("L")) + p.Number(), p.Str(", "))


class Part1(Puzzle):
    def __init__(self):
        super().__init__("Day 01/1")

    def parse(self, input: str):
        return PARSER.parse(input)

    def solve(self, parsed):
        pos = mt.Point(0, 0)
        dir = mt.NORTH
        for turn, dist in parsed:
            match turn:
                case "R":
                    dir = dir.turn_right()
                case "L":
                    dir = dir.turn_left()
            pos = pos + dir * dist
        return abs(pos - mt.Point(0, 0))


class Part2(Puzzle):
    def __init__(self):
        super().__init__("Day 01/2")

    def parse(self, input: str):
        return PARSER.parse(input)

    def solve(self, parsed):
        visited = set()
        pos = mt.Point(0, 0)
        dir = mt.NORTH
        for turn, dist in parsed:
            match turn:
                case "R":
                    dir = dir.turn_right()
                case "L":
                    dir = dir.turn_left()
            for _ in range(dist):
                pos = pos + dir
                if pos in visited:
                    return abs(pos - mt.Point(0, 0))
                visited.add(pos)


part1 = Part1()
part1.check("R2, L3", 5)
part1.check("R2, R2, R2", 2)
part1.check("R5, L5, R5, R3", 12)
part1.run("../data/input01.txt")

part2 = Part2()
part2.check("R8, R4, R4, R8", 4)
part2.run("../data/input01.txt")
