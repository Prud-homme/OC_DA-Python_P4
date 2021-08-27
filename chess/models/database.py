from tinydb import TinyDB, Query
import re

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

	def create_item(self, serial_data: dict) -> None:
		"""Insertion of serialized data in the table"""
		self.table.insert(serial_data)

	def update_item(self, serial_data: dict, item_id: int) -> None:
		"""Update a table element with new serialized data"""
		self.table.update(serial_data, doc_ids=[item_id])
		
	def delete_item(self, item_id: int) -> None:
		"""Delete a table element with its id"""
		self.table.remove(doc_ids=[item_id])

	def search_item(self, serial_data: dict) -> list:
		"""Search for complete or partial serialized data in the table"""
		return self.table.search(Query().fragment(serial_data))
	
	def get_id(self, serial_data: dict) -> int:
		"""Get the id of an element in the table thanks to its serialized data"""
		item = self.table.get(Query().fragment(serial_data))
		return item.doc_id

	def exist_id(self, item_id: int) -> bool:
		"""Gives the existence of an id in the table"""
		return self.table.contains(doc_id=item_id)

	def get_item_with_id(self, item_id: int) -> dict:
		"""Get the serialized data of an element of the table thanks to its id"""
		return self.table.all()[item_id-1]

	def search_by_name(self, search_name):
		"""Search by name (if the field exist) in the table"""
		if self.table.search(Query().name.exists()):
			return self.table.search(Query().name.search(search_name, flags=re.IGNORECASE))
		else:
			return []

	def search_by_location(self, search_location):
		"""Search by location (if the field exist) in the table"""
		if self.table.search(Query().location.exists()):
			return self.table.search(Query().location.search(search_location, flags=re.IGNORECASE))
		else:
			return []
