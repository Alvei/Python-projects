import pytest
import sqlite3
from datetime import datetime
from database import DatabaseManager

# Could move conftest.py file
"""@pytest.fixture(scope=module)
def cnt(database_path):

    connection = sqlite3.connect(database_path)
    yield connection
    connection.close()


@pytest.fixture
def cursor(cnt):
    cursor = cnt.cursor()
    yield cursor
    cnt.rollback()


def test_table_exists(cursor):
    cursor.execute
"""


def test_add():
    """ Test creating and adding a table. """
    database_filename = "dummy_db.db"
    test_db = DatabaseManager(database_filename)

    table_name = "bookmark"
    col_definition = {
        "id": "integer primary key autoincrement",
        "title": "text not null",
        "url": "text not null",
        "notes": "text",
        "date_added": "text not null",
    }
    data = {
        "title": "First Bookmark",
        "url": "https://first.com",
        "notes": "text",
    }

    test_db.create_table(table_name, col_definition)
    test_db.add(table_name, data)
    ans = test_db.select(database_filename)
