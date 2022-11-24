from collections import Counter

from utils.puzzle import Puzzle
from utils import parsing as p


PARSER = p.SeparatedList(
    p.Group(
        p.Group(
            (p.String(p.OneOf("abcdefghijklmnopqrstuvwxyz") * ...) + p.Drop("-")) * ...
        )
        + p.Number()
        + p.Drop("[")
        + p.String(p.OneOf("abcdefghijklmnopqrstuvwxyz") * ...)
        + p.Drop("]")
    ),
    p.Str("\n"),
)


class Day02(Puzzle):
    def parse(self, input: str):
        return PARSER.parse(input)


def is_real(name, checksum):
    return (
        "".join(
            map(
                lambda x: x[1],
                sorted(map(lambda x: (-x[1], x[0]), Counter("".join(name)).items()))[
                    :5
                ],
            )
        )
        == checksum
    )


class Part1(Day02):
    def __init__(self):
        super().__init__("Day 04/1")

    def solve(self, parsed):
        return sum(
            sector_id for name, sector_id, checksum in parsed if is_real(name, checksum)
        )


class Part2(Day02):
    def __init__(self):
        super().__init__("Day 04/2")

    def solve(self, parsed):
        result = None
        for name, sector_id, checksum in parsed:
            if not is_real(name, checksum):
                continue
            mapping = {
                ch: chr(ord("a") + (ord(ch) - ord("a") + sector_id) % 26)
                for ch in "abcdefghijklmnopqrstuvwxyz"
            }
            real_name = "".join(mapping.get(ch, ch) for ch in " ".join(name))
            print(sector_id, real_name)
            if "north" in real_name and "pole" in real_name and "object" in real_name:
                assert result is None
                result = sector_id
        return result


Part1().check(
    """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]""",
    1514,
)
Part1().run("../data/input04.txt")

Part2().run("../data/input04.txt")
