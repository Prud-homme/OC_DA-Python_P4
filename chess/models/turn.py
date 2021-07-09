from datetime import datetime

class Turn:
	def __init__(self, name):
		""""""
		self.name = name
		self.start_date = self.get_current_time()
		self.matchs = []

	def add_match(self, match):
		""""""
		self.matchs.append(match)

	def close_turn(self):
		""""""
		self.end_date = self.get_current_time()

	def __str__(self):
		return f"{self.name} débuté à {self.start_date}."

	@staticmethod
	def get_current_time(): #Static method
		""""""
		now = datetime.now()
		return now.strftime("Date: %d/%m/%Y, Time: %H:%M")#:%S")