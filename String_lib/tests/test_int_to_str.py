import pytest
from string_lib import int_to_str


@pytest.mark.parametrize(
    "test_input, expected", [(123, "123"), (-1230, "-1230"), (0, "0"),],
)
def test_working_values(test_input, expected):
    actual = int_to_str(test_input)
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"


def test_type():
    with pytest.raises(AssertionError):
        int_to_str("123")
        int_to_str([1, 2, 3])
        int_to_str(12.34)
