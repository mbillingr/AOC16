from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        match other:
            case Vect(dx, dy):
                return Point(self.x + dx, self.y + dy)
            case _:
                return NotImplemented

    def __sub__(self, other):
        match other:
            case Point(x, y):
                return Vect(self.x - x, self.y - y)
            case Vect(dx, dy):
                return Point(self.x - dx, self.y - dy)
            case _:
                return NotImplemented


@dataclass(frozen=True)
class Vect:
    x: int
    y: int

    def turn_left(self):
        return Vect(-self.y, self.x)

    def turn_right(self):
        return Vect(self.y, -self.x)

    def __abs__(self):
        return abs(self.x) + abs(self.y)

    def __add__(self, other):
        match other:
            case Vect(dx, dy):
                return Vect(self.x + dx, self.y + dy)
            case _:
                return NotImplemented

    def __sub__(self, other):
        match other:
            case Vect(dx, dy):
                return Vect(self.x - dx, self.y - dy)
            case _:
                return NotImplemented

    def __mul__(self, other):
        match other:
            case int(n):
                return Vect(self.x * n, self.y * n)
            case _:
                return NotImplemented


EAST = Vect(1, 0)
WEST = Vect(-1, 0)
NORTH = Vect(0, 1)
SOUTH = Vect(0, -1)
