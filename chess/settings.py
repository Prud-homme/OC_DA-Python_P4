from tinydb import TinyDB, Query
db = TinyDB('db.json')
players_table = db.table('players')
tournaments_table = db.table('tournaments')
Info = Query()