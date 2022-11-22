import pytest

from utils import parsing as p


def test_parse_any_char():
    sut = p.AnyChar()
    assert sut.parse("xyz") == ["x"]


def test_any_char_fails_on_empty_string():
    sut = p.AnyChar()
    with pytest.raises(p.ParseError):
        sut.parse("")


def test_parse_specific_char():
    sut = p.Str("a")
    assert sut.parse("abc") == ["a"]


def test_fail_to_parse_char():
    sut = p.Str("b")
    with pytest.raises(p.ParseError):
        sut.parse("c")


def test_char_fails_on_empty_string():
    sut = p.Str("x")
    with pytest.raises(p.ParseError):
        sut.parse("")


def test_parse_empty_string():
    sut = p.Empty()
    assert sut.parse("") == []


def test_fail_to_parse_empty_string():
    sut = p.Empty()
    with pytest.raises(p.ParseError):
        sut.parse("x")


@pytest.mark.parametrize("digit", "0123456789")
def test_parse_digit(digit):
    assert p.Digit().parse(digit) == [digit]


@pytest.mark.parametrize("digit", "x+$O")
def test_parse_digit_fail(digit):
    with pytest.raises(p.ParseError):
        p.Digit().parse(digit)


@pytest.mark.parametrize("src", "1x+~O")
def test_parse_predicate_char(src):
    assert p.CharPredicate(lambda ch: True).parse(src) == [src[0]]


@pytest.mark.parametrize("src", "1x+~O")
def test_parse_predicate_char_fail(src):
    with pytest.raises(p.ParseError):
        p.CharPredicate(lambda ch: False).parse(src)


def test_parse_sequence():
    assert p.Sequence(p.AnyChar(), p.AnyChar()).parse("abcde") == ["a", "b"]
    assert p.Sequence(p.Str("a"), p.Str("b")).parse("abcde") == ["a", "b"]
    assert p.Sequence(p.Str("a"), p.Empty()).parse("a") == ["a"]
    assert p.Sequence(
        p.Sequence(p.Str("a"), p.Str("b")), p.Sequence(p.Str("c"), p.Str("d"))
    ).parse("abcde") == ["a", "b", "c", "d"]

    with pytest.raises(p.ParseError):
        p.Sequence(p.Str("x"), p.Str("y")).parse("ay")

    with pytest.raises(p.ParseError):
        p.Sequence(p.Str("x"), p.Str("y")).parse("xa")


def test_parse_alternative():
    assert p.Alternative(p.Str("a"), p.Str("b")).parse("abcde") == ["a"]
    assert p.Alternative(p.Str("a"), p.Str("b")).parse("bcde") == ["b"]

    with pytest.raises(p.ParseError):
        p.Alternative(p.Str("a"), p.Str("b")).parse("cde")


@pytest.mark.parametrize(
    "src, expected",
    [
        ("", []),
        ("x", ["x"]),
        ("xxx", ["x", "x", "x"]),
        ("xy", ["x"]),
    ],
)
def test_parse_repetition(src, expected):
    assert p.Repeat(p.Str("x")).parse(src) == expected


@pytest.mark.parametrize(
    "src, expected",
    [
        ("x", ["x"]),
        ("xxx", ["x", "x", "x"]),
        ("xy", ["x"]),
    ],
)
def test_parse_nonempty_repetition(src, expected):
    assert p.OneOrMore(p.Str("x")).parse(src) == expected

    with pytest.raises(p.ParseError):
        p.OneOrMore(p.AnyChar()).parse("")


def test_nested_repetition_on_failing_parser_does_not_loop_infinitely():
    sut = p.Repeat(p.Repeat(p.Str("x")))
    assert sut.parse("abc") == []


def test_parse_dependent():
    sut = p.Depends(p.AnyChar(), lambda chl: p.Str(chl[0]))

    assert sut.parse("xx") == ["x", "x"]
    assert sut.parse("yy") == ["y", "y"]
    with pytest.raises(p.ParseError):
        sut.parse("xy")


def test_parse_transform():
    assert p.Transform(lambda x: int(x[0]), p.Digit()).parse("789") == 7


def test_parse_number():
    assert p.Number().parse("012") == [12]


def test_parse_string():
    assert p.Str("abc").parse("abcdef") == ["abc"]


def test_ignore_parseresult():
    assert p.Drop(p.Str("foo")).parse("foobar") == []


@pytest.mark.parametrize(
    "src, expected",
    [
        ("", []),
        ("42", [42]),
        ("123,456,789", [123, 456, 789]),
    ],
)
def test_separated_list(src, expected):
    sut = p.SeparatedList(p.Number(), p.Str(","))
    assert sut.parse(src) == expected


def test_grouping():
    assert p.Repeat(p.Group(p.Sequence(p.Str("A"), p.Str("B")))).parse("ABABABA") == [
        ("A", "B"),
        ("A", "B"),
        ("A", "B"),
    ]

    sut = p.Group(p.Repeat(p.Digit()))
    assert sut.parse("") == [()]

    sut = p.SeparatedList(p.Group(p.Repeat(p.Digit())), p.Str(";"))
    assert sut.parse("12;345") == [("1", "2"), ("3", "4", "5")]

    sut = p.SeparatedList(
        p.Group(p.Repeat(p.SkipWhitespace() + p.Number())), p.Str("\n")
    )
    assert sut.parse("   1   2\n   3   4") == [(1, 2), (3, 4)]


def test_sugar():
    assert p.AnyChar() + p.Digit() == p.Sequence(p.AnyChar(), p.Digit())
    assert p.Str("+") | p.Str("-") == p.Alternative(p.Str("+"), p.Str("-"))
    assert p.Digit() + "foo" == p.Sequence(p.Digit(), p.Str("foo"))
    assert "x" + p.Digit() == p.Sequence(p.Str("x"), p.Digit())
    assert p.AnyChar() * ... == p.OneOrMore(p.AnyChar())
