class Match:
	def __init__(self, player1, score1, player2, score2):
		""""""
		self.match = ([player1, score1], [player2, score2])

	def __str__(self):
		return f"Match: {self.match}"