import abc
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Tuple


class Puzzle(abc.ABC):
    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def solve(self, parsed_input: Any) -> Any:
        """compute puzzle solution"""

    @abc.abstractmethod
    def parse(self, input: str) -> Any:
        """convert result from string to something the solver understands"""

    def check(self, input: str, expected: Any):
        start = datetime.now()
        result = self.solve(self.parse(input))
        if result == expected:
            print(f"{datetime.now() - start} -- OK  {result}")
        else:
            raise AssertionError(f"expected {expected}, got {result}")

    def run(self, filename: Optional[str] = None, wrong: Tuple[Any, ...] = ()):
        start = datetime.now()
        match filename:
            case None:
                input_str = ""
            case DirectInput(inp):
                input_str = inp
            case _:
                with open(filename, "rt") as f:
                    input_str = f.read()
        result = self.solve(self.parse(input_str))

        if result in wrong:
            raise AssertionError(f"wrong result: {result}")

        print(f"{datetime.now() - start} -- {self.name}: {result}")


@dataclass
class DirectInput:
    input: str
