""" Defines a list of actions that should be executed in response to a user's choice.
    By encapsulating the logic of each action as a command Object, and providing a
    consistent way to trigger them via an excute method, these actions can be decoupled
    from the presentation layer.
    Business logic layer.
"""

import sys
from datetime import datetime
import requests
from typing import Dict, List, Optional
from database import DatabaseManager  # Persistence layer
import logging

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

    def execute(self, data: Dict, timestamp: None) -> str:
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

        next_page_of_results = f"https://api.github.com/users/{github_username}/starred"

        while next_page_of_results:

            stars_response = requests.get(
                next_page_of_results,
                headers={"Accept": "application/vnd.github.v3.star+json"},
            )

            # If the response was successful, no Exception will be raised
            try:
                stars_response.raise_for_status()
            except Exception as err:
                print(f"\nError occurred: {err}\n")  # Python 3.6
            else:
                print(f"Successful request to github: {github_username}\n")

            next_page_of_results = stars_response.links.get("next", {}).get("url")

            for repo_info in stars_response.json():
                repo = repo_info["repo"]

                if data["preserve_timestamps"]:
                    timestamp = datetime.strptime(
                        repo_info["starred_at"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                else:
                    timestamp = None

                bookmarks_imported += 1
                AddBookmarkCommand().execute(  # <9>
                    self._extract_bookmark_info(repo), timestamp=timestamp,
                )

        return f"Imported {bookmarks_imported} bookmarks from starred repos!"  # <10>


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
            "bookmarks", {"id": data["id"]}, data["update"],
        )
        return "Bookmark updated!"


class QuitCommand:
    """ Quit program. """

    def execute(self):
        """ Use OS command to exit program(). """
        sys.exit()


def main():
    """ Test harness. """

    table_name = "bookmark"
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
