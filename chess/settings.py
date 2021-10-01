from database import Table

DATABASE = "test.json"
TOURNAMENTS_TABLE = Table("Tournaments", DATABASE)
PLAYERS_TABLE = Table("Players", DATABASE)
TIME_CONTROL = ["bullet", "blitz", "coup rapide"]
SCORE_VALUES = ["0", "0.5", "1/2", "0,5", "1"]
