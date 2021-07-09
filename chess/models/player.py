import re
class Player:
	def __init__(self, name="", birth_date="", gender="", ranking=""):
		""""""
		self.name = name
		self.birth_date = birth_date
		self.gender = gender
		self.ranking = ranking

	def __str__(self):
		return ("Informations du joueur: "
				f"{self.name}, {self.birth_date}, {self.gender}, {self.ranking}.")

	def serializing(self):
		""""""
		return {
				'name': self.name,
				'birth_date': self.birth_date,
				'gender': self.gender,
				'ranking': self.ranking
				}

	def unserializing(self, player_data):#{'name':...}
		""""""
		self.name = player_data['name']
		self.birth_date = player_data['birth_date']
		self.gender = player_data['gender']
		self.ranking = player_data['ranking']

	def add_to_db(self, players_table):
		""""""
		players_table.insert(self.serializing())

	def load_from_database(self, player_id, players_table):
		player_data = players_table.all()[player_id-1]
		self.unserializing(player_data)


	@staticmethod
	def search_in_db(research, players_table, Info):
		""""""
		return players_table.search(
			Info.name.search(research, flags=re.IGNORECASE) \
			| \
			Info.birth_date.search(research, flags=re.IGNORECASE) \
			| \
			Info.gender.search(research, flags=re.IGNORECASE) \
			| \
			Info.ranking.search(research, flags=re.IGNORECASE)
			)

	@staticmethod
	def get_id(player_data, players_table, Info):
		""""""
		player = players_table.get(Info.fragment(player_data))
		return player.doc_id
