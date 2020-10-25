import pytest
from math import comb
from math_lib import my_combination, my_binomial_prob


def test_valid_combination():
    actual = my_combination(7, 5)
    expected = comb(7, 5)
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"
