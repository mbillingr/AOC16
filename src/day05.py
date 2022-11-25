from hashlib import md5

from utils.puzzle import Puzzle, DirectInput
from utils import parsing as p


class Day02(Puzzle):
    def parse(self, input: str):
        return input.encode()


def infinite_range():
    i = 0
    while True:
        yield i
        i += 1


class Part1(Day02):
    def __init__(self):
        super().__init__("Day 05/1")

    def solve(self, parsed):
        passwd = ""
        for index in infinite_range():
            hexhash = md5(parsed + str(index).encode()).hexdigest()
            if hexhash.startswith("00000"):
                passwd += hexhash[5]
                print(passwd, index, hexhash)
            if len(passwd) >= 8:
                return passwd


class Part2(Day02):
    def __init__(self):
        super().__init__("Day 05/2")

    def solve(self, parsed):
        passwd = {}
        for index in infinite_range():
            hexhash = md5(parsed + str(index).encode()).hexdigest()
            if hexhash.startswith("00000"):
                try:
                    index = int(hexhash[5])
                except ValueError:
                    continue
                if index >= 8:
                    continue
                if index in passwd:
                    continue
                passwd[index] = hexhash[6]
                print("".join(passwd.get(i, "_") for i in range(8)), hexhash)
            if len(passwd) >= 8:
                return "".join(passwd[i] for i in range(8))


#Part1().check("abc", "18f47a30")
#Part1().run(DirectInput("wtnhxymk"))

Part2().check("abc", "05ace8e3")
Part2().run(DirectInput("wtnhxymk"))
