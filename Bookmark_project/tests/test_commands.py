import pytest
import sys
import pprint

# Necessary to make sure that it looks for command one directory above and current
sys.path.insert(0, "../")
sys.path.insert(0, "./")
# pprint.pprint(sys.path)

from commands import ImportGitHubStarsCommand


def test_extract():
    gitstars = ImportGitHubStarsCommand()
    expected = {
        "title": "repo_name",
        "url": "html_url",
        "notes": "repo_description",
    }
    json_input = {
        "name": "repo_name",
        "html_url": "html_url",
        "description": "repo_description",
    }  # these are the keys used by Github
    actual = gitstars._extract_bookmark_info(json_input)
    assert actual == expected, f"Expected: {expected}, Actual: {actual}" ""

