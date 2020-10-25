import pytest
from string_lib import convert_to_int


@pytest.mark.parametrize(
    "test_input, expected", [("123,456", 123456), ("1,234", 1234), ("01,234", 1234)]
)
def test_working_values(test_input, expected):
    actual = convert_to_int(test_input)
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"


def test_string_with_missing_comma():
    actual = convert_to_int("178100,301")
    assert actual is None, f"Expected: None, Actual: {actual}"


def test_on_string_with_incorrectly_placed_comma():
    actual = convert_to_int("12,72,891")
    assert actual is None, f"Expected: None, Actual: {actual}"


def test_on_string_with_character():
    actual = convert_to_int("1,2c4,891")
    assert actual is None, f"Expected: None, Actual: {actual}"


def test_on_float_valued_string():
    actual = convert_to_int("23,816.92")
    assert actual is None, f"Expected: None, Actual: {actual}"


def test_type():
    with pytest.raises(AssertionError):
        convert_to_int(123)
        convert_to_int(123.23)
        convert_to_int(-123)
        convert_to_int(True)

