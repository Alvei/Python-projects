""" Series of small text processing functions."""
from collections import Counter, defaultdict
import re
from typing import Union, List, Dict


def camelcase(my_string: str) -> str:
    """Takes string like this how_are_you and returns string like HowAreYou."""
    assert isinstance(my_string, str)
    return "".join([word.capitalize() for word in my_string.split("_")])


def convert_to_int(integer_string_with_commas: str) -> Union[int, None]:
    """Converts numerical strings to become int. It handles various cases with punctuation.
    Returns None when something unusual happens."""

    assert isinstance(integer_string_with_commas, str)

    comma_separated_parts: list = integer_string_with_commas.split(",")

    # Check for special cases
    for num, part in enumerate(comma_separated_parts):
        if len(part) > 3:
            return None

        # Skip over the 1st part since it could have 1 or 2
        if num != 0 and len(part) != 3:
            return None

        if not part.isdigit():
            return None

    integer_string_without_commas: str = "".join(comma_separated_parts)

    # It will not work if you have a decimal still in the string
    try:
        return int(integer_string_without_commas)
    except ValueError:
        return None


def char_at_beg(my_string: str, char: str) -> bool:
    """Check to see if a character is at beginning of string."""
    assert isinstance(my_string, str)
    if my_string.startswith(char):
        return True
    return False


def int_list_to_int(lst: List[int]) -> int:
    """ Converting integer list to create an integer. """
    assert isinstance(lst, list)
    res = int("".join(map(str, lst)))
    return res


def int_to_str(number: int) -> str:
    """Returns a decimal string representation of number."""
    assert isinstance(number, int)

    digits = "0123456789"
    result = ""

    if number == 0:  # base case
        return "0"

    if number < 0:
        number = abs(number)
        while number > 0:
            result = digits[number % 10] + result
            number = number // 10  # Remove the last digit
        result = "-" + result
    else:
        while number > 0:
            result = digits[number % 10] + result
            number = number // 10  # Remove the last digit

    return result


def count_words(phrase: str) -> Dict[str, int]:
    """ Uses Counter and Regex to do the work. Counter objects are a dictionary-like
        object specifically meant for counting the number of times
        things are seen and storing the things as keys and the times
        seen as values. You can think of it as essentially a set that counts
        the number of times it sees each thing, a multi-set of sorts."""

    # .findall() returns a list. Searchs for words, apostrophs or dashes.
    # \b is a forced word break
    search_result = re.findall(r"\b[\w'-]+\b", phrase.lower())
    return Counter(search_result)


def count_words_counter(phrase: str) -> Dict[str, int]:
    """ Uses Counter to do the work. Counter objects are a dictionary-like
        object specifically meant for counting the number of times
        things are seen and storing the things as keys and the times
        seen as values. You can think of it as essentially a set that counts
        the number of times it sees each thing, a multi-set of sorts.
        Does not pass the punctuation test. """
    return Counter(phrase.lower().split())


def count_words_defaultdict_class(phrase: str) -> Dict[str, int]:
    """ Enumerate and count words in a phrase.
        Uses the defaultdict class to do the work.
        Does not pass the punctuation test. """
    count = defaultdict(int)
    for word in phrase.lower().split():
        count[word] += 1
    return count


def count_words_basic(phrase: str) -> Dict[str, int]:
    """ Enumerate and count words in a phrase.
        While the setdefault trick is cool not efficient b/c two loops.
        Does not pass the ¿ test. """

    words = []
    # Strip the punctuation characters for the list created by .split() method.
    for word in phrase.lower().split():
        words.append(word.strip(',;.!?"()'))

    my_dict = {}
    # check to see if my_dict[key] exist. If not, set to zero, if yes, do nothing.
    for word in words:
        my_dict.setdefault(word, 0)
        my_dict[word] += 1

    return my_dict


def main():
    """ Main."""
    my_string = "1,4c6"
    ans = convert_to_int(my_string)
    print(f"{type(my_string)}: {my_string} => {type(ans)}: {ans}")
    print(f"{char_at_beg('NewPhrase', 'N')}")
    print(f"Simple case using a string as an input: {camelcase('HoW_are_you')}")
    my_lst = [12, 15, 17]
    print(int_list_to_int(my_lst))
    print(f"{int_to_str(-123)}")
    phrases = [
        "oh what a day what a lovely day",
        "don't stop believing",
        "Oh what a day what a lovely day",
        "Oh what a day, what a lovely day!",
        "¿Te gusta Python?",
    ]

    print("BASIC")
    [print(count_words_basic(phrase)) for phrase in phrases]

    print("DEFAULTDICT CLASS")
    [print(count_words_defaultdict_class(phrase)) for phrase in phrases]

    print("COUNTER OBJECT")
    [print(count_words_counter(phrase)) for phrase in phrases]

    print("RE OBJECT")
    [print(count_words(phrase)) for phrase in phrases]


if __name__ == "__main__":
    main()
