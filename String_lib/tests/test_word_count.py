import pytest
from string_lib import (
    count_words,
    count_words_basic,
    count_words_defaultdict_class,
    count_words_counter,
)


def test_simple_sentence():
    expected = {"oh": 1, "what": 2, "a": 2, "day": 2, "lovely": 1}
    actual = count_words_basic("oh what a day what a lovely day")
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"

    actual = count_words_defaultdict_class("oh what a day what a lovely day")
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"

    actual = count_words_counter("oh what a day what a lovely day")
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"

    actual = count_words("oh what a day what a lovely day")
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"


def test_apostrophe():
    expected = {"don't": 1, "stop": 1, "believing": 1}
    actual = count_words_basic("don't stop believing")
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"

    actual = count_words_defaultdict_class("don't stop believing")
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"

    actual = count_words_counter("don't stop believing")
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"

    actual = count_words("don't stop believing")
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"


def test_capitalization():
    expected = {"oh": 1, "what": 2, "a": 2, "day": 2, "lovely": 1}
    actual = count_words_basic("Oh what a day what a lovely day")
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"

    actual = count_words_defaultdict_class("Oh what a day what a lovely day")
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"

    actual = count_words_counter("Oh what a day what a lovely day")
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"

    actual = count_words("Oh what a day what a lovely day")
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"


def test_symbols():
    expected = {"te": 1, "gusta": 1, "python": 1}
    actual = count_words("¿Te gusta Python?")
    assert actual == expected, f"Expected: {expected}, Actual: {actual}"

    #   actual = count_words_basic("¿Te gusta Python?")
    #   assert actual == expected, f"Expected: {expected}, Actual: {actual}"

    # actual = count_words_defaultdict_class("¿Te gusta Python?")
    # assert actual == expected, f"Expected: {expected}, Actual: {actual}"

    # actual = count_words_counter("¿Te gusta Python?")
    # assert actual == expected, f"Expected: {expected}, Actual: {actual}"

