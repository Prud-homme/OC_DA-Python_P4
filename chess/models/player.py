import re
class Player:
	def __init__(self, name="", birth_date="", gender="", ranking=None):
		""""""
		self.name = name
		self.birth_date = birth_date
		self.gender = gender
		self.ranking = ranking

	def __str__(self):
		return ("Informations du joueur: "
				f"{self.name}, {self.birth_date}, {self.gender}, {self.ranking}.")

	def well_defined(self):
		return self.name!="" and self.birth_date!="" and self.gender!="" and self.ranking!=None

	def serializing(self):
		""""""
		return {
				'name': self.name,
				'birth_date': self.birth_date,
				'gender': self.gender,
				'ranking': self.ranking
				}

	def unserializing(self, player_data):
		""""""
		self.name = player_data['name']
		self.birth_date = player_data['birth_date']
		self.gender = player_data['gender']
		self.ranking = player_data['ranking']

	def insert(self):
		""""""
		if self.well_defined():
			create_item(players_table, self.serializing())
		else:
			raise m_exc.PlayerBadDefined(
				"Unable to add the player to the database, please define his information.")

	def read(self, player_id):
		""""""
		player_data = read_item_with_id(players_table, player_id)
		self.unserializing(player_data)

	def update(self, player_id):
		""""""
		update_item(players_table, self.serializing(), player_id)

	def delete(self, player_id):
		delete_item(players_table, player_id)

	@staticmethod
	def table_id(player_data):
		""""""
		return get_id(players_table, player_data)

	@staticmethod
	def research(research):
		""""""
		return players_table.search(
			Query().name.search(research, flags=re.IGNORECASE) \
			| \
			Query().birth_date.search(research, flags=re.IGNORECASE) \
			| \
			Query().gender.search(research, flags=re.IGNORECASE) \
			| \
			Query().ranking.search(research, flags=re.IGNORECASE)
			)
