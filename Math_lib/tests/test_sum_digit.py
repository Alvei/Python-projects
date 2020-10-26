import pytest
from math_lib import sum_digit


@pytest.mark.parametrize(
    "test_input, expected", [(52, 7), (-111, -3), (234, 9),],
)
def test_valid_sum_digits(test_input, expected):
    actual = sum_digit(test_input)
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"


def test_types():
    with pytest.raises(AssertionError):
        sum_digit("124")
        sum_digit(1.2)
        sum_digit([123, 456])

