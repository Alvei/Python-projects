import pytest
from string_lib import int_list_to_int


@pytest.mark.parametrize(
    "test_input, expected",
    [([12, 15, 17], 121517), ([2, 15, 17], 21517), ([15, 17], 1517),],
)
def test_working_values(test_input, expected):
    actual = int_list_to_int(test_input)
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"


def test_type():
    with pytest.raises(AssertionError):
        int_list_to_int("123")
        int_list_to_int(-123)
        int_list_to_int(12.34)
