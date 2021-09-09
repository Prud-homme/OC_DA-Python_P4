import re
from typing import Optional

from tinydb import Query, TinyDB


class Table:
    """
    A class to represent a table of a json database.
    The operations on this table are done with the python package TinyDB.
    """

    def __init__(self, table_name: str, database: str) -> None:
        """Constructs all the necessary attributes for the table object."""
        self.table_name = table_name
        self.database = database
        self.table = TinyDB(database).table(table_name)

    def create_item(self, serial_data: dict) -> bool:
        """Insertion of serialized data in the table"""
        try:
            self.table.insert(serial_data)
            print('Successful insert.')
            return True
        except:
            print('An error was encountered, insertion canceled')
            return False

    def update_item(self, serial_data: dict, item_id: int) -> bool:
        """Update a table element with new serialized data"""
        if self.exist_id(item_id):
            self.table.update(serial_data, doc_ids=[item_id])
            return True
        else:
            return False

    def delete_item(self, item_id: int) -> bool:
        """Delete a table element with its id"""
        if self.exist_id(item_id):
            self.table.remove(doc_ids=[item_id])
            return True
        else:
            return False

    def search_items(self, serial_data: dict) -> Optional[list]:
        """Search for complete or partial serialized data in the table"""
        items = self.table.search(Query().fragment(serial_data))
        if len(items) > 0:
            return items
        else:
            return None

    def get_id(self, serial_data: dict) -> Optional[int]:
        """Get the id of an element in the table thanks to its serialized data"""
        item = self.table.get(Query().fragment(serial_data))
        if item != None:
            return item.doc_id
        else:
            return None

    def exist_id(self, item_id: int) -> bool:
        """Gives the existence of an id in the table"""
        return self.table.contains(doc_id=item_id)

    def exist_serial_data(self, serial_data: dict) -> bool:
        """Gives the existence of a item in the table thanks to its serialized data"""
        return len(self.search_item(serial_data)) > 0

    def get_item_with_id(self, item_id: int) -> Optional[dict]:
        """Get the serialized data of an element of the table thanks to its id"""
        if self.exist_id(item_id):
            return self.table.all()[item_id - 1]
        else:
            return None

    def search_by_first_and_last_name(
        self, firstname_searched: str, lastname_searched: str
    ) -> Optional[list]:
        """Search by name (if the field exist) in the table"""
        result1 = []
        result2 = []

        if self.table.search(Query().firstname.exists()):
            result1 = self.table.search(
                Query().firstname.search(firstname_searched, flags=re.IGNORECASE)
            )

        if self.table.search(Query().lastname.exists()):
            result2 = self.table.search(
                Query().lastname.search(lastname_searched, flags=re.IGNORECASE)
            )

        if len(result1) > 0 and len(result2) == 0:
            return result1

        elif len(result2) > 0 and len(result1) == 0:
            return result2

        elif len(result1) > 0 and len(result2) > 0:
            return [elt1 for elt1 in result1 for elt2 in result2 if elt1 == elt2]

        else:
            return None

    def search_by_name(self, name_searched: str) -> Optional[list]:
        """Search by location (if the field exist) in the table"""
        result = []
        if self.table.search(Query().name.exists()):
            return self.table.search(
                Query().name.search(name_searched, flags=re.IGNORECASE)
            )
        else:
            return None

    def search_by_location(self, location_searched) -> Optional[list]:
        """Search by location (if the field exist) in the table"""
        if self.table.search(Query().location.exists()):
            return self.table.search(
                Query().location.search(location_searched, flags=re.IGNORECASE)
            )
        else:
            return None
