import pytest
from string_lib import camelcase


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("how_are_you", "HowAreYou"),
        ("How_are_you", "HowAreYou"),
        ("HOW_are_you", "HowAreYou"),
        ("HOW_ARE_YOU", "HowAreYou"),
        ("AlloComment_ca", "AllocommentCa"),
        ("bon_jour", "BonJour"),
    ],
)
def test_working_values(test_input, expected):
    actual = camelcase(test_input)
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"


def test_type():
    with pytest.raises(AssertionError):
        camelcase("123")
        camelcase(["how", "are", "you"])
        camelcase(-123)
        camelcase(12.34)
