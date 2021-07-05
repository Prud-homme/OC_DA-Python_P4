from datetime import datetime

class Turn:
	def __init__(self, name):
		""""""
		self.name = name
		self.start_date = get_current_time()
		self.matchs = []

	def close_turn(self):
		""""""
		self.end_date = get_current_time()

	def get_current_time(): #Static method
		""""""
		now = datetime.now()
		return now.strftime("Date: %d/%m/%Y, Time: %H:%M")#:%S")

	def __str__(self):
		return f"{self.name} débuté à {self.start_date}."