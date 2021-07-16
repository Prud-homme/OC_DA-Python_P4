import re
class Tournament:

	def __init__(self, name="", location="", date="", description="", time_control="", turns_number=4):
		""""""
		self.name = name
		self.location = location
		self.date = date
		self.description = description
		self.time_control = time_control
		self.turns_number = turns_number
		self.players = []
		self.turns = []

	def __str__(self):
		info = (
			"Caractéristiques du tournoi:\n"
			f"Nom: {self.name}\n"
			f"Lieu: {self.location}\n"
			f"Date: {self.date}\n"
			f"Controle: {self.time_control}\n"
			f"Tours: {self.turns_number}\n"
			f"Description: {self.description}\n"
			f"Joueurs: {self.players}"
			)
		return info

	def add_turn(self, turn):
		""""""
		self.turns.append(turn)

	def add_player(self, player_id):
		""""""
		self.players.append(player_id)

	def serializing(self):
		""""""
		return {
				'name': self.name,
				'location': self.location,
				'date': self.date,
				'description': self.description,
				'time_control': self.time_control,
				'turns_number': self.turns_number,
				'players': self.players,
				'turns': self.turns,
				}

	def unserializing(self, tournament_data):
		""""""
		self.name = tournament_data['name']
		self.location = tournament_data['location']
		self.date = tournament_data['date']
		self.description = tournament_data['description']
		self.time_control = tournament_data['time_control']
		self.turns_number = tournament_data['turns_number']
		self.players = tournament_data['players']
		self.turns = tournament_data['turns']

	def add_to_db(self, tournaments_table):
		""""""
		tournaments_table.insert(self.serializing())

	def update_db(self, tournaments_table, tournament_id):
		""""""
		tournaments_table.update(self.serializing(), doc_ids=[tournament_id])

	def load_from_database(self, tournament_id, tournaments_table):
		tournament_data = tournaments_table.all()[tournament_id-1]
		self.unserializing(tournament_data)


	@staticmethod
	def search_in_db(research, tournaments_table, Info):
		""""""
		return tournaments_table.search(
			Info.name.search(research, flags=re.IGNORECASE) \
			| \
			Info.location.search(research, flags=re.IGNORECASE) \
			| \
			Info.date.search(research, flags=re.IGNORECASE) \
			| \
			Info.time_control.search(research, flags=re.IGNORECASE) \
			| \
			Info.description.search(research, flags=re.IGNORECASE) 
			)

	@staticmethod
	def get_id(tournament_data, tournaments_table, Info):
		""""""
		tournament = tournaments_table.get(Info.fragment(tournament_data))
		return tournament.doc_id

	#def create(self):
	#	name = self.name
	#	location = self.location
	#	date = self.date
	#	description = self.description
	#	time_control = self.time_control
	#	turns_number = self.turns_number
	#	return Tournament(name, location, date, description, time_control, turns_number)
	
