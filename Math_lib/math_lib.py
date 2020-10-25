""" math_lib.py """
from math import sqrt, factorial, comb
from typing import List, Tuple, Optional  # Optional necessary when None or int

# import sys
# sys.setrecursionlimit(20000)

# Global constants
MAX_RECURSION = 500
MAX_LOOP = 996
MAX_SIEVE = 7878


def find_divisors(number1: int, number2: int) -> Tuple[int, ...]:
    """Find the common divisors of number1 and number2
    Assumes that number1 and number2 are positive ints
    Returns a tuple containing all common divisors."""
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
    """Find the smallest and largest common divisors of number1 and number2 other than 1.
    Assumes that number1 and number2 are positive ints."""
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


def divisors(number: int, small: int, large: int) -> bool:
    """Returns True if number has a divisor in the range of small to large.
    Returns False otherwise."""

    # Catch wrong entries
    assert number >= 0
    assert small >= 0
    assert large >= 0

    if small > large:
        return False

    if number % small == 0:  # Is number divisible by small?
        return True

    # Default is that it is not divisible and therefore increment and do a recursion
    return divisors(number, small + 1, large)


def is_prime(number: int) -> bool:
    """ For any number greater or equal to 2, return True if number is prime and False if not. """
    assert number >= 2

    # Check if can divide with any number from 2 to (number-1).
    if divisors(number, 2, number - 1):
        return False

    return True


def is_prime_sqrt(number: int) -> bool:
    """ For any number greater or requal to 2, Return True is n is prime, False if not. """

    assert number >= 2

    new_num = int(
        sqrt(number)
    )  # Trick to improve efficiency. Only do half of the numbers

    # Check if can divide with any number from 2 to (number-1).
    if divisors(number, 2, new_num):
        return False

    return True


def list_primes(beg: int, end: int) -> list:
    """ Returns a list of prime numbers between beg and end. """
    assert beg >= 2 and end < MAX_RECURSION

    if beg == end:
        return []

    if is_prime(beg):
        # print('Found a prime ', beg)
        # Put beg in [] to convert into a list to use concatenation and then do recursion.
        return [beg] + list_primes(beg + 1, end)

    # Default is no prime number was found increment the beg number.
    return list_primes(beg + 1, end)


def list_primes_sqrt(beg: int, end: int) -> List[int]:
    """ Returns a list of prime numbers between beg and end. """

    assert beg >= 2 and end < 3 * MAX_RECURSION

    if beg == end:
        return []

    if is_prime_sqrt(beg):
        # print('Found a prime ', beg)
        # Put beg in [] to convert into a list to use concatenation and then do recursion.
        return [beg] + list_primes_sqrt(beg + 1, end)

    # Default is no prime number was found increment the beg number.
    return list_primes_sqrt(beg + 1, end)


def list_primes_loop(beg: int, end: int) -> list:
    """ Returns a list of prime numbers between beg and end. """

    assert beg >= 2 and end < MAX_LOOP

    my_list: List[int] = []

    if beg == end:
        return []

    for num in range(beg, end):
        if is_prime(num):
            # print( 'Found a prime ', num)
            my_list = my_list + [num]
    return my_list


def sift(number: int, num_list: list) -> List[int]:
    """ Returns the list of numbers that are not multiple of n. """

    def my_func(var):
        return var % number != 0

    # Use list() because filter() return an iterator
    return list(filter(my_func, num_list))


def prime_sieve(num_list: list) -> List[int]:
    """Returns list of prime number using sieve algo which eliminates multiples
    of any prime found to speed up implementation.
    Assumes 1st number is a prime so works if start at 2."""

    assert (len(num_list) - 1) < MAX_SIEVE

    if num_list == []:
        return []

    assert is_prime(num_list[0])  # Make sure 1st number is a prime by default

    # Removing the prime number from numList
    # Then use a sift function to remove the multiple of prime in remaining list
    # This new shorter list is use recursively by primeSieve
    prime = num_list[0]
    return [prime] + prime_sieve(sift(prime, num_list[1:]))


def my_combination(item_n: int, group_r: int) -> float:
    """ Function that implements the basic combination.
        item_n:  total number of items
        group_r: size of group taken each time. """

    assert isinstance(item_n, int) and isinstance(group_r, int)
    assert (item_n - group_r) > 0  # myCombination() input test

    return factorial(item_n) / (factorial(group_r) * factorial(item_n - group_r))


def my_binomial_prob(prob: float, k: int, num_trial: int) -> float:
    """ Function that calculates a single Binomial Proabability.
        k:   number of successes
        n-k: number of failures """

    assert (num_trial - k) > 0  # my_combination() input test
    assert isinstance(num_trial, int) and isinstance(k, int)
    assert isinstance(prob, float)

    failure_q = 1 - prob  # probability of failure

    ans = my_combination(num_trial, k) * prob ** k * failure_q ** (num_trial - k)
    return ans


def main():
    """ Main code """
    min_div, max_div = find_extreme_divisors(100, 200)
    print(f"Min Divisor = {min_div}\t\t=> Answer = 2")
    print(f"Max Divisor = {max_div}\t=> Answer = 100")
    print(f"7 is prime?: {is_prime(7)} and 9 is prime?: {is_prime(9)}")
    print(f"\n# Prime [2, 500]: {len(list_primes(2, 499))} => Answer 94")
    print(f"# Prime [2, 500]: {len(list_primes_sqrt(2, 499))} => Answer 94")
    print(f"# Prime [2, 500]: {len(prime_sieve(range(2, 499)))} => Answer 94")

    prob = 0.1
    k = 1  # number of success
    num = 5  # number of trials

    # Build a list of probabilities if you try n times
    print(my_combination(7, 5), comb(7, 5))
    ans = [my_binomial_prob(prob, k, index) for index in range(2, num + 1)]
    print(f"\n{ans}")


if __name__ == "__main__":
    main()
