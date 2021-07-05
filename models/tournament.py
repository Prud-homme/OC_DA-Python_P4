class Tournament:

	def __init__(self, name, location, date, description, time_control, turns_number=4):
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
		return ("Caractéristiques du tournoi: "
				f"{self.name}, {self.location}, {self.date}, "
				f"{self.time_control}, {self.turns_number} tours.\n"
				f"Description: {self.description}.\n"
				f"Joueurs: {self.players}")

	def create(self):
		name = self.name()
		location = self.location
		date = self.date
		description = self.description
		time_control = self.time_control
		turns_number = self.turns_number
		return Tournament(name, location, date, description, time_control, turns_number)
	
