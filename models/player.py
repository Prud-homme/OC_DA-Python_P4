class Player:
	def __init__(self, name, birth_date, gender, ranking):
		""""""
		self.name = name
		self.birth_date = birth_date
		self.gender = gender
		self.ranking = ranking

	def serializing(self):
		""""""
		return {
		'name': self.name,
		'birth_date': self.birth_date,
		'gender': self.gender,
		'ranking': self.ranking
		}

	def __str__(self):
		return ("Informations du joueur: "
				f"{self.name}, {self.birth_date}, {self.gender}, {self.ranking}.")

	def add_to_db(self):
		players_table.insert(self.serializing())

	def search_in_db(name):#a revoir en cas de résultat multiple avec un view.display etc.
		player = players_table.get(PlayerInfo.name == name)
		return player.doc_id
	def id_to_ranking(table, id):
		return table.all()[id]['ranking']
	@staticmethod
	


	#import re
	#players_table.search(PlayerInfo.name.search('pow', flags=re.IGNORECASE))
"""
def unserializing(player_data):
	name = player_data['name']
	birth_date = player_data['birth_date']
	gender = player_data['gender']
	ranking = player_data['ranking']
	return Player(name, birth_date, gender, ranking)
"""