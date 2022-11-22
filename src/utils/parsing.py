import abc
import operator
from dataclasses import dataclass
from typing import Any, Callable


class Parser(abc.ABC):
    """An abstract parser"""

    @abc.abstractmethod
    def apply(self, src: str) -> (Any, str):
        pass

    def parse(self, src: str) -> Any:
        result, _ = self.apply(src)
        return result

    def __add__(self, other):
        match other:
            case Parser():
                return Sequence(self, other)
            case str():
                return Sequence(self, Str(other))
            case _:
                return NotImplemented

    def __radd__(self, other):
        match other:
            case str():
                return Sequence(Str(other), self)
            case _:
                return NotImplemented

    def __mul__(self, other):
        if other is ...:
            return OneOrMore(self)
        return NotImplemented

    def __or__(self, other):
        if isinstance(other, Parser):
            return Alternative(self, other)
        return NotImplemented


@dataclass
class ParseError(Exception):
    """Could not parse the input string"""

    parser: Parser
    state: str


class Empty(Parser):
    """Parse the empty string"""

    def apply(self, src: str) -> (Any, str):
        if src:
            raise ParseError(self, src)
        return [], src

    def __eq__(self, other):
        return isinstance(other, Empty)


class Null(Parser):
    """Parse any string but don't change the parsing state.
    (Useful as initializer for iteratively building parsers)"""

    def apply(self, src: str) -> (Any, str):
        return [], src

    def __eq__(self, other):
        return isinstance(other, Null)


class CharPredicate(Parser):
    """Parse any string whose first character matches a predicate"""

    def __init__(self, predicate: Callable[[str], bool]):
        self.pred = predicate

    def apply(self, src: str) -> (Any, str):
        if not src or not self.pred(src[0]):
            raise ParseError(self, src)
        return [src[0]], src[1:]

    def __eq__(self, other):
        return isinstance(other, CharPredicate) and self.pred == other.pred


class AnyChar(CharPredicate):
    """Parse strings starting with any character"""

    def __init__(self):
        super().__init__(_always_true)


def _always_true(_):
    return True


class Digit(CharPredicate):
    """Parse strings with a leading digit"""

    def __init__(self):
        super().__init__(str.isdigit)


class Whitespace(CharPredicate):
    """Parse strings with a leading whitespace character"""

    def __init__(self):
        super().__init__(_is_whitespace)


def _is_whitespace(s):
    return s.isspace() and "\n" not in s


@dataclass
class Str(Parser):
    """Parse strings with specific prefix"""

    string: str

    def apply(self, src: str) -> (Any, str):
        if src.startswith(self.string):
            n = len(self.string)
            return [src[:n]], src[n:]
        raise ParseError(self, src)


@dataclass
class Sequence(Parser):
    """Combine two parsers to match in sequence"""

    first: Parser
    second: Parser

    def apply(self, src: str) -> (Any, str):
        r1, s1 = self.first.apply(src)
        r2, s2 = self.second.apply(s1)
        return r1 + r2, s2


@dataclass
class Alternative(Parser):
    """If the first parser fails, try the second"""

    first: Parser
    second: Parser

    def apply(self, src: str) -> (Any, str):
        try:
            return self.first.apply(src)
        except ParseError:
            pass

        try:
            return self.second.apply(src)
        except ParseError:
            pass

        raise ParseError(self, src)


@dataclass
class Repeat(Parser):
    """Repeatedly apply a parser until it fails"""

    item: Parser

    def apply(self, src: str) -> (Any, str):
        result = []
        while True:
            try:
                x, newsrc = self.item.apply(src)
            except ParseError:
                break
            if src == newsrc:
                break
            src = newsrc
            result.extend(x)
        return result, src


@dataclass
class Transform(Parser):
    """Apply a function to a parser's result"""

    func: Callable[[Any], Any]
    parser: Parser

    def apply(self, src):
        r, s = self.parser.apply(src)
        return self.func(r), s


class Drop(Transform):
    """Drop a parser's result"""

    def __init__(self, parser: Parser):
        super().__init__(_empty, parser)


class Group(Transform):
    def __init__(self, parser: Parser):
        super().__init__(_group, parser)


def _group(lst: list[Any]):
    return [tuple(lst)]


class OneOrMore(Sequence):
    """Repeatedly apply a parser until it fails - must succeed at least once"""

    def __init__(self, item: Parser):
        super().__init__(item, Repeat(item))


class Depends(Parser):
    """Match two parsers in sequence, but the second parser is constructed depending on the first's result"""

    def __init__(self, first: Parser, make_second: Callable[[Any], Parser]):
        assert isinstance(first, Parser)
        self.first = first
        self.make_second = make_second

    def apply(self, src: str) -> (Any, str):
        r1, s1 = self.first.apply(src)
        second = self.make_second(r1)
        r2, s2 = second.apply(s1)
        return r1 + r2, s2


def compose(*funcs):
    def composition(arg):
        for f in funcs:
            arg = f(arg)
        return arg

    return composition


class Number(Transform):
    digits_to_int = compose("".join, int, lambda x: [x])

    def __init__(self):
        super().__init__(Number.digits_to_int, OneOrMore(Digit()))


@dataclass
class SeparatedList(Alternative):
    def __init__(self, item: Parser, separator: Parser):
        super().__init__(
            Sequence(
                item,
                Repeat(Sequence(Drop(separator), item)),
            ),
            Null(),
        )


def _empty(_):
    return []


class SkipWhitespace(Drop):
    def __init__(self):
        super().__init__(Repeat(Whitespace()))


class Optional(Alternative):
    def __init__(self, parser: Parser):
        super().__init__(parser, Null())
