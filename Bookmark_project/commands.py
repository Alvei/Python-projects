""" Defines a list of actions that should be executed in response to a user's choice.
    By encapsulating the logic of each action as a command Object, and providing a
    consistent way to trigger them via an excute method, these actions can be decoupled
    from the presentation layer.
    Business logic layer.
"""

import sys
from datetime import datetime
import logging
from typing import Dict, List
import requests
from database import DatabaseManager  # Persistence layer


logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.CRITICAL)

db = DatabaseManager("bookmarks.db")  # Create instance of data base


class CreateBookmarksTableCommand:
    """ Create a bookmark table. """

    def execute(self) -> None:
        """ Execute persistent layer command. That also includes definition of table. """
        db.create_table(
            "bookmarks",
            {
                "id": "integer primary key autoincrement",
                "title": "text not null",
                "url": "text not null",
                "notes": "text",
                "date_added": "text not null",
            },
        )


class AddBookmarkCommand:
    """ Add a bookmark to table that accepts an optional timestamp argument. """

    def execute(self, data: Dict, timestamp=None) -> str:
        """ Execute persistent layer command and enrich the data with current time. """
        data["date_added"] = timestamp or datetime.utcnow().isoformat()
        db.add("bookmarks", data)
        return "Bookmark added!"


class ListBookmarksCommand:
    """ List bookmarks in the db. Need to use fetchall() to iterate over cursor. """

    def __init__(self, order_by: str = "date_added") -> None:
        """ Define the ordering method. It does by date by default. """
        self.order_by = order_by

    def execute(self) -> List:
        """ Execute persistent layer command. """
        return db.select("bookmarks", order_by=self.order_by).fetchall()


class ImportGitHubStarsCommand:
    """ Command class that imports the URL of repos that are starred for a given users. """

    def _extract_bookmark_info(self, repo: dict) -> dict:
        """ Extract the bookmark info from the passed repo dictionary. """
        return {
            "title": repo["name"],
            "url": repo["html_url"],
            "notes": repo["description"],
        }

    def execute(self, data: dict):
        """ Requests information from the specified URL and returns bookmark info. """
        bookmarks_imported = 0

        github_username = data["github_username"]
        # This is the URL of the first page using the username
        next_page_of_results = f"https://api.github.com/users/{github_username}/starred"

        while next_page_of_results:
            # Get content of github page using the specified header
            stars_response = requests.get(
                next_page_of_results,
                headers={"Accept": "application/vnd.github.v3.star+json"},
                timeout=3,
            )

            # Do some basic error checking for requests.get()
            try:
                stars_response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print(f"\nA HTTP Error: {errh}\n")
            except requests.exceptions.ConnectionError as errc:
                print(f"\nAn Error Connecting: {errc}")
            except requests.exceptions.Timeout as errt:
                print(f"\nA Timeout Error: {errt}")
            except requests.exceptions.RequestException as err:
                print(f"\nAn unknown Error: {err}")
            else:
                print(f"\nSuccessful request to github: {github_username}\n")

            # Convert the response to json and then loop over each elements
            for repo_info in stars_response.json():
                repo = repo_info["repo"]

                # If we are using the existing timestamp, convert to same date format
                if data["preserve_timestamps"]:
                    timestamp = datetime.strptime(
                        repo_info["starred_at"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                else:
                    timestamp = None

                bookmarks_imported += 1
                AddBookmarkCommand().execute(
                    self._extract_bookmark_info(repo),
                    timestamp=timestamp,
                )

            # The "link" header rel=next contains the link to the next page if available
            next_page_of_results = stars_response.links.get("next", {}).get("url")

        return f"Imported {bookmarks_imported} bookmarks from starred repos!"


class DeleteBookmarkCommand:
    """ Delete boomark. """

    def execute(self, data: int) -> str:
        """ Execute persistent layer command. """
        db.delete("bookmarks", {"id": data})
        return "Bookmark deleted!"


class EditBookmarkCommand:
    """ Allows editing of Bookmarks. """

    def execute(self, data: dict) -> str:
        """ Execute persistent layer command. """
        db.update(
            "bookmarks",
            {"id": data["id"]},
            data["update"],
        )
        return "Bookmark updated!"


class QuitCommand:
    """ Quit program. """

    def execute(self):
        """ Use OS command to exit program(). """
        sys.exit()


def main():
    """ Test harness. """

    data = {
        "title": "First Bookmark",
        "url": "https://first.com",
        "notes": "text",
    }

    CreateBookmarksTableCommand().execute()
    AddBookmarkCommand().execute(data)
    AddBookmarkCommand().execute(data)
    DeleteBookmarkCommand().execute(3)
    my_bookmarks = ListBookmarksCommand().execute()
    print(type(CreateBookmarksTableCommand()))

    for my_bookmark in my_bookmarks:
        print(my_bookmark)


if __name__ == "__main__":
    main()
