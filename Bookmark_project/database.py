""" Persistence layer module. """

import sqlite3
from datetime import datetime
from typing import Dict, Sequence
import logging

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.CRITICAL)


class DatabaseManager:
    """ Class that encapsulates all the persistence layer functionalities. """

    def __init__(self, database_path: str) -> None:
        """ Create and store a sqlite3 connection with path: database_path.
            File is created automatically it does not already exist on computer.
        """
        self.connection = sqlite3.connect(database_path)

    def __del__(self) -> None:
        """ Close the connection with sqlite3 db. """
        self.connection.close()

    def _execute(self, statement: str, values: Sequence = None) -> sqlite3.Cursor:
        """ Execute a sqlite3 statement using Cursor objects, transaction context,
            and basic security.
            PARAMETERS:
                statement: Accepts a statement as a string argument
                values: Optional placeholder Sequence to help with SQL injection
            RETURNS: Query results or empty list via a Cursor object.
        """

        # Creates a transaction context that allows roll-back if an error occurs
        with self.connection:
            cursor = self.connection.cursor()
            logging.debug(f"execute=> {statement}, {values or []}")
            cursor.execute(
                statement, values or []
            )  # default 2nd argument is empty list
            return cursor

    def create_table(self, table_name: str, columns: Dict[str, str]) -> None:
        """ Create an sqlite3 table.
            PARAMETERS:
                table_name: name of the table
                columns: dictionary of {column name: data type and constraints}
        """

        # Constructs the column definitions, with their data types and constraints by unpacking dict
        columns_with_types = [
            f"{column_name} {data_type}" for column_name, data_type in columns.items()
        ]

        statement = f"""CREATE TABLE IF NOT EXISTS {table_name}
            ({', '.join(columns_with_types)});"""
        self._execute(statement)

    def drop_table(self, table_name: str) -> None:
        """ Remove a table. """
        self._execute(f"DROP TABLE {table_name};")

    def add(self, table_name: str, data: Dict) -> None:
        """ Add a table line. """
        placeholders = ", ".join("?" * len(data))  # Keeps track of number of values
        column_names = ", ".join(data.keys())
        column_values = tuple(
            data.values()
        )  # excute needs a list or tuple => do conversion

        statement = f"""INSERT INTO {table_name}
            ({column_names})
            VALUES ({placeholders});
            """
        self._execute(
            statement, column_values,
        )

    def delete(self, table_name: str, criteria: Dict) -> None:
        """ Delete a row in a table.
            PARAMETERS:
                table_name: name of table
                criteria: a non-optional argument (otherwise all is deleted!)
        """
        placeholders = [f"{column} = ?" for column in criteria.keys()]
        delete_criteria = " AND ".join(placeholders)
        self._execute(
            f"""
            DELETE FROM {table_name}
            WHERE {delete_criteria};
            """,
            tuple(criteria.values()),
        )

    def select(self, table_name: str, criteria: Dict = None, order_by: str = None):
        """ Query the database.
            PARAMETERS:
                table_name: name of table
                criteria: Optional dictionary of criteria, it fetches all record by default
                order_by:
        """
        criteria = criteria or {}

        query = f"SELECT * FROM {table_name}"

        if criteria:
            placeholders = [f"{column} = ?" for column in criteria.keys()]
            select_criteria = " AND ".join(placeholders)
            query += f" WHERE {select_criteria}"

        if order_by:
            query += f" ORDER BY {order_by}"

        return self._execute(query, tuple(criteria.values()),)

    def update(self, table_name: str, criteria: dict, data: dict) -> None:
        """ Update a bookmark.
            PARAMETERS:
                table_name: name of table
                criteria:
                data:
        """
        update_placeholders = [f"{column} = ?" for column in criteria.keys()]
        update_criteria = " AND ".join(update_placeholders)

        data_placeholders = ", ".join(f"{key} = ?" for key in data.keys())

        values = tuple(data.values()) + tuple(criteria.values())

        self._execute(
            f"""
            UPDATE {table_name}
            SET {data_placeholders}
            WHERE {update_criteria};
            """,
            values,
        )


def main():
    """ Test harness. """
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
    data["date_added"] = datetime.utcnow().isoformat()

    test_db.create_table(table_name, col_definition)
    test_db.add(table_name, data)
    test_db.add(table_name, data)
    test_db.delete(table_name, {"id": 2})


if __name__ == "__main__":
    main()
