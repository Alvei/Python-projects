""" math_lib.py """
from typing import Tuple, Optional  # Optional necessary when None or int


def find_divisors(number1: int, number2: int) -> Tuple[int, ...]:
    """ Find the common divisors of number1 and number2
        Assumes that number1 and number2 are positive ints
        Returns a tuple containing all common divisors. """
    assert number1 >= 1 and number2 >= 1
    assert isinstance(number1, int) and isinstance(number2, int)

    # Initialize the empty tuple of unknown legnth
    divisors: Tuple[int, ...] = ()

    for num in range(1, min(number1, number2) + 1):
        # print("num = ", num)
        if number1 % num == 0 and number2 % num == 0:
            # print("found divisor = ", num)
            divisors = divisors + (num,)
    return divisors


def find_extreme_divisors(
    number1: int, number2: int
) -> Tuple[Optional[int], Optional[int]]:
    """ Find the smallest and largest common divisors of number1 and number2 other than 1.
        Assumes that number1 and number2 are positive ints. """
    assert number1 >= 2 and number2 >= 2
    assert isinstance(number1, int) and isinstance(number2, int)

    min_val, max_val = None, None
    print(f"[{number1} & {number2}]")

    for index in range(2, min(number1, number2) + 1):

        # Check if it devides both numbers
        if number1 % index == 0 and number2 % index == 0:
            print(f"index = {index} [{min_val}, {max_val}]")
            if min_val is None or index < min_val:
                min_val = index
            if max_val is None or index > max_val:
                max_val = index

    return (min_val, max_val)


def main():
    """ Main code """
    min_div, max_div = find_extreme_divisors(100, 200)
    print(f"Min Divisor = {min_div}\t\t=> Answer = 2")
    print(f"Max Divisor = {max_div}\t=> Answer = 100")


if __name__ == "__main__":
    main()
