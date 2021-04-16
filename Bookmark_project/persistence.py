# persistence.py
# Introduce an abstraction layer to help swap the database if necessary

from abc import ABC, abstractmethod

from database import DatabaseManager


class PersistenceLayer(ABC):
    @abstractmethod
    def create(self, data):
        """ Required """
        raise NotImplementedError("Persistence layer must implement a create mehtod.")

    @abstractmethod
    def list(self, order_by=None):
        """ Required """
        raise NotImplementedError("Persistence layer must implement a create mehtod.")

    @abstractmethod
    def edit(self, bookmark_id, boomark_data):
        """ Required """
        raise NotImplementedError("Persistence layer must implement a create mehtod.")

    @abstractmethod
    def delete(self, bookmark_id: int):
        """ Required """
        raise NotImplementedError("Persistence layer must implement a create mehtod.")


class BookmarkDatabase(PersistenceLayer):
    def __init__(self) -> None:
        """ Constructor. """
        self.table_name: str = "bookmarks"
        self.db = DatabaseManager("bookmarks.db")

    def create(self, bookmark_data):
        """ Required """
        self.db.add(self.table_name, bookmark_data)

    def list(self, order_by=None):
        """ Required """
        return self.db.select(self.table_name, order_by=order_by).fetchall()

    def edit(self, bookmark_id: int, boomark_data):
        """ Required """
        self.db.update(self.table_name, {"id": bookmark_id}, boomark_data)

    def delete(self, bookmark_id: int):
        """ Required """
        self.db.delete(self.table_name, {"id": bookmark_id})
