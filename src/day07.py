from collections import Counter
from functools import reduce

from utils.puzzle import Puzzle
from utils import parsing as p

WORD = p.String(p.Letter() * ...)
PARSER = p.SeparatedList(
    p.Group(WORD + p.Repeat(p.Drop("[") + WORD + p.Drop("]") + WORD)),
    p.Str("\n"),
)


class Day07(Puzzle):
    def parse(self, input: str):
        return PARSER.parse(input)


class Part1(Day07):
    def __init__(self):
        super().__init__("Day 07/1")

    def solve(self, parsed):
        return sum(1 for ip in parsed if supports_tls(ip))


def supports_tls(elements):
    normal = elements[0::2]
    hypernet = elements[1::2]

    return any(map(abba_in, normal)) and not any(map(abba_in, hypernet))


def abba_in(string: str) -> bool:
    return any(is_abba(string[i : i + 4]) for i in range(len(string)))


def is_abba(chars: str) -> bool:
    if len(chars) != 4:
        return False

    if chars[0] == chars[1]:
        return False

    return chars == chars[::-1]


class Part2(Day07):
    def __init__(self):
        super().__init__("Day 07/2")

    def solve(self, parsed):
        return sum(1 for ip in parsed if supports_ssl(ip))


def supports_ssl(elements):
    supernet = elements[0::2]
    hypernet = elements[1::2]

    supernet_abas = filter(is_aba, flatten(map(overlapping_triples, supernet)))
    hypernet_babs = filter(is_aba, flatten(map(overlapping_triples, hypernet)))

    hypernet_abas = map(invert, hypernet_babs)

    return bool(set(supernet_abas).intersection(hypernet_abas))


def overlapping_triples(string):
    return (string[i : i + 3] for i in range(len(string) - 2))


def flatten(iteriter):
    for it in iteriter:
        yield from it


def is_aba(triple):
    return len(triple) == 3 and triple[0] == triple[2] and triple[0] != triple[1]


def invert(aba):
    return aba[1] + aba[0] + aba[1]


EXAMPLE1 = """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
"""

EXAMPLE2 = """aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb
"""


Part1().check(EXAMPLE1, 2)
Part1().run("../data/input07.txt")

Part2().check(EXAMPLE2, 3)
Part2().run("../data/input07.txt")
