import re
class Player:
	def __init__(self, firstname=None, lastname=None, birthdate=None, gender=None, ranking=None):
		""""""
		self.firstname = firstname
		self.lastname = lastname
		self.birthdate = birthdate
		self.gender = gender
		self.ranking = ranking
		if None in (firstname, lastname):
			self.name = None
		else:
			self.name = ' '.join((lastname, firstname))

	def __str__(self):
		return ("Informations du joueur: "
				f"{self.name}, {self.birthdate}, {self.gender}, {self.ranking}.")

	def well_defined(self):
		return None not in (self.birthdate, self.gender, self.ranking)


	def serializing(self):
		""""""
		return {
				'firstname': self.firstname,
				'lastname': self.lastname,
				'name': self.name,
				'birthdate': self.birthdate,
				'gender': self.gender,
				'ranking': self.ranking
				}

	def unserializing(self, player_data):
		""""""
		self.firstname = player_data['firstname']
		self.lastname = player_data['lastname']
		self.name = player_data['name']
		self.birthdate = player_data['birthdate']
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
			Query().birthdate.search(research, flags=re.IGNORECASE) \
			| \
			Query().gender.search(research, flags=re.IGNORECASE) \
			| \
			Query().ranking.search(research, flags=re.IGNORECASE)
			)
