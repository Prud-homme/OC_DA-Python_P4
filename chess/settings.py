import os

from database import Table

chessdir = os.path.dirname(os.path.realpath(__file__))
maindir = os.path.dirname(chessdir)
DATABASE_PATH = os.path.join(maindir, "database.json")
TOURNAMENTS_TABLE = Table("Tournaments", DATABASE_PATH)
PLAYERS_TABLE = Table("Players", DATABASE_PATH)
TIME_CONTROL = ["bullet", "blitz", "coup rapide"]
ICONS = ["🥇", "🥈", "🥉"]
