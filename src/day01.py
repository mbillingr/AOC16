from dataclasses import dataclass
from typing import Literal, Self

from utils.puzzle import Puzzle
from utils import parsing as p


class ManhattanTurtle:
    def __init__(
        self,
        x: int,
        y: int,
        direction: Literal["NORTH", "SOUTH", "EAST", "WEST"] = "NORTH",
        ignore_direction_for_equality=True,
    ):
        self.x = x
        self.y = y
        self.direction = direction
        self.ignore_direction_for_equality = ignore_direction_for_equality

    def with_x(self, new_x: int) -> Self:
        return ManhattanTurtle(
            new_x, self.y, self.direction, self.ignore_direction_for_equality
        )

    def with_y(self, new_y: int) -> Self:
        return ManhattanTurtle(
            self.x, new_y, self.direction, self.ignore_direction_for_equality
        )

    def with_direction(
        self, new_dir: Literal["NORTH", "SOUTH", "EAST", "WEST"]
    ) -> Self:
        return ManhattanTurtle(
            self.x, self.y, new_dir, self.ignore_direction_for_equality
        )

    def __eq__(self, other):
        if not isinstance(other, ManhattanTurtle):
            return NotImplemented
        if self.ignore_direction_for_equality:
            return self.x == other.x and self.y == other.y
        else:
            return (
                self.x == other.x
                and self.y == other.y
                and self.direction == other.direction
            )

    def __hash__(self):
        if self.ignore_direction_for_equality:
            return hash((self.x, self.y))
        else:
            return hash((self.x, self.y, self.direction))

    def turn_right(self) -> Self:
        match self.direction:
            case "NORTH":
                return self.with_direction("EAST")
            case "EAST":
                return self.with_direction("SOUTH")
            case "SOUTH":
                return self.with_direction("WEST")
            case "WEST":
                return self.with_direction("NORTH")

    def turn_left(self) -> Self:
        match self.direction:
            case "NORTH":
                return self.with_direction("WEST")
            case "EAST":
                return self.with_direction("NORTH")
            case "SOUTH":
                return self.with_direction("EAST")
            case "WEST":
                return self.with_direction("SOUTH")

    def forward(self, dist: int) -> Self:
        match self.direction:
            case "NORTH":
                return self.with_y(self.y + dist)
            case "EAST":
                return self.with_x(self.x + dist)
            case "SOUTH":
                return self.with_y(self.y - dist)
            case "WEST":
                return self.with_x(self.x - dist)


PARSER = p.SeparatedList((p.Str("R") | p.Str("L")) + p.Number(), p.Str(", "))


class Part1(Puzzle):
    def __init__(self):
        super().__init__("Day 01/1")

    def parse(self, input: str):
        return PARSER.parse(input)

    def solve(self, parsed):
        pos = ManhattanTurtle(0, 0)
        for turn, dist in parsed:
            match turn:
                case "R":
                    pos = pos.turn_right()
                case "L":
                    pos = pos.turn_left()
            pos = pos.forward(dist)
        return abs(pos.x) + abs(pos.y)


class Part2(Puzzle):
    def __init__(self):
        super().__init__("Day 01/2")

    def parse(self, input: str):
        return PARSER.parse(input)

    def solve(self, parsed):
        visited = set()
        pos = ManhattanTurtle(0, 0)
        for turn, dist in parsed:
            match turn:
                case "R":
                    pos = pos.turn_right()
                case "L":
                    pos = pos.turn_left()
            for _ in range(dist):
                pos = pos.forward(1)
                if pos in visited:
                    return abs(pos.x) + abs(pos.y)
                visited.add(pos)


part1 = Part1()
part1.check("R2, L3", 5)
part1.check("R2, R2, R2", 2)
part1.check("R5, L5, R5, R3", 12)
part1.run("../data/input01.txt")

part2 = Part2()
part2.check("R8, R4, R4, R8", 4)
part2.run("../data/input01.txt")
