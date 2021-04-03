""" Business logic layer.
    Defines a list of actions that should be executed in response to a user's choice.
    By encapsulating the logic of each action as a command Object, and providing a
    consistent way to trigger them via an excute method, these actions can be decoupled
    from the presentation layer.
"""

import sys
from datetime import datetime
from typing import Dict, List
from database import DatabaseManager  # Persistence layer

db = DatabaseManager('bookmarks.db')  # Create instance of data base


class CreateBookmarksTableCommand:
    """ Create a bookmark table. """
    def execute(self) -> None:
        """ Execute persistent layer command. That also includes definition of table. """
        db.create_table('bookmarks', {
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
            'url': 'text not null',
            'notes': 'text',
            'date_added': 'text not null',
        })


class AddBookmarkCommand:
    """ Add a bookmark to table. """
    def execute(self, data: Dict) -> str:
        """ Execute persistent layer command and enrich the data with current time. """
        data['date_added'] = datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Bookmark added!'


class ListBookmarksCommand:
    """ List bookmarks in the db. Need to use fetchall() to iterate over cursor. """
    def __init__(self, order_by: str = 'date_added') -> None:
        """ Define the ordering method. It does by date by default. """
        self.order_by = order_by

    def execute(self) -> List:
        """ Execute persistent layer command. """
        return db.select('bookmarks', order_by=self.order_by).fetchall()


class DeleteBookmarkCommand:
    """ Delete boomark. """
    def execute(self, data: int) -> str:
        """ Execute persistent layer command. """
        db.delete('bookmarks', {'id': data})
        return 'Bookmark deleted!'


class QuitCommand:
    """ Quit program. """
    def execute(self):
        """ Use OS command to exit program(). """
        sys.exit()


def main():
    """ Test harness. """

    table_name = 'bookmark'
    data = {'title': 'First Bookmark',
            'url': 'https://first.com',
            'notes': 'text',}

    CreateBookmarksTableCommand().execute()
    AddBookmarkCommand().execute(data)
    AddBookmarkCommand().execute(data)
    DeleteBookmarkCommand().execute(3)
    my_bookmarks = ListBookmarksCommand().execute()
    print(type(CreateBookmarksTableCommand()))

    for my_bookmark in my_bookmarks:
        print(my_bookmark)


if __name__ == '__main__':
    main()
