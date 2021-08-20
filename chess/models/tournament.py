import re


class Tournament:

	def __init__(self, name=None, location=None, date=None, description=None, time_control=None, turns_number=4, players_number=8):
		self.name = name
		self.location = location
		self.date = date
		self.description = description
		self.time_control = time_control
		self.turns_number = turns_number
		self.players_number = players_number
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
			f"Joueurs: {self.players}\n"
			f"Tours: {self.turns}"
			)
		return info

	def add_turn(self, turn):
		""""""
		self.turns.append(turn)

	def add_player(self, player_id):
		""""""
		self.players.append(player_id)

	def well_defined(self):
		return self.name!="" and self.location!="" and self.date!="" and self.time_control!=None

	def serializing(self):
		""""""
		return {
				'name': self.name,
				'location': self.location,
				'date': self.date,
				'description': self.description,
				'time_control': self.time_control,
				'turns_number': self.turns_number,
				'players_number': self.players_number,
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
		self.players_number = tournament_data['players_number']
		self.players = tournament_data['players']
		self.turns = tournament_data['turns']

	def insert(self):
		""""""
		if self.well_defined():
			create_item(tournaments_table, self.serializing())
		else:
			print("Unable to add the player to the database, please define his information.")

	def read(self, tournament_id):
		""""""
		tournament_data = read_item_with_id(tournaments_table, tournament_id)
		self.unserializing(tournament_data)

	def update(self, tournament_id):
		""""""
		update_item(tournaments_table, self.serializing(), tournament_id)

	def delete(self, tournament_id):
		delete_item(tournaments_table, tournament_id)

	@staticmethod
	def table_id(tournament_data):
		""""""
		return get_id(tournaments_table, tournament_data)

	# def add_to_db(self, tournaments_table):
	# 	""""""
	# 	tournaments_table.insert(self.serializing())

	# def update_db(self, tournaments_table, tournament_id):
	# 	""""""
	# 	tournaments_table.update(self.serializing(), doc_ids=[tournament_id])

	# def load_from_database(self, tournament_id, tournaments_table):
	# 	tournament_data = tournaments_table.all()[tournament_id-1]
	# 	self.unserializing(tournament_data)

	def load_scores(self):
		scores = [0]*len(self.players)
		for turn in self.turns:
			for match in turn.matchs:
				([player1, score1], [player2, score2]) = match.match
				index1 = self.players.index(player1)
				index2 = self.players.index(player2)
				scores[index1] += float(score1)
				scores[index2] += float(score2)
		return scores

	def load_ranking(self):
		ranking = []
		for tournament_id in self.players:
			tournament_data = tournaments_table.all()[tournament_id]
			ranking.append(int(tournament_data['ranking']))
		return ranking

	@staticmethod
	def search_in_db(research, tournaments_table):
		""""""
		return tournaments_table.search(
			Query().name.search(research, flags=re.IGNORECASE) \
			| \
			Query().location.search(research, flags=re.IGNORECASE) \
			| \
			Query().date.search(research, flags=re.IGNORECASE) \
			| \
			Query().time_control.search(research, flags=re.IGNORECASE) \
			| \
			Query().description.search(research, flags=re.IGNORECASE) 
			)

	# @staticmethod
	# def get_id(tournament_data, tournaments_table):
	# 	""""""
	# 	tournament = tournaments_table.get(Query().fragment(tournament_data))
	# 	return tournament.doc_id