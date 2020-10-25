import pytest
from string_lib import char_at_beg


def test_start_with():
    actual = char_at_beg("Newphrase", "N")
    assert actual == True, f"Expected: True, Actual: {actual}"


def test_does_not_start_with():
    actual = char_at_beg("Newphrase", "b")
    assert actual == False, f"Expected: False, Actual: {actual}"


def test_type():
    with pytest.raises(AssertionError):
        char_at_beg("123", "N")
        char_at_beg(["how", "are", "you"], "N")
        char_at_beg(-123, "N")
        char_at_beg(12.34, "N")
