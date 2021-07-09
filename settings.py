from tinydb import TinyDB, Query
db = TinyDB('db.json')
players_table = db.table('players')
tournaments_table = db.table('tournaments')
Info = Query()

#####################

def display_player(player_data):
	info = (
		f'Nom: {player_data["name"]}\n'
		f'Date: {player_data["birth_date"]}\n'
		f'Genre: {player_data["gender"]}\n'
		f'Rang: {player_data["ranking"]}\n'
		)
	print(info)

def display_players():
	for i in range(len(players_table)):
		print(f"--- Player {i} ---")
		display_player(players_table.all()[i])

def display_tournament(tournament_data):
	info = (
		f"Nom: {tournament_data['name']}\n"
		f"Lieu: {tournament_data['location']}\n"
		f"Date: {tournament_data['date']}\n"
		f"Controle: {tournament_data['time_control']}\n"
		f"Nombre de tours: {tournament_data['turns_number']}\n"
		f"Description: {tournament_data['description']}\n"
		f"Joueurs: {tournament_data['players']}\n"
		f"Tours: {tournament_data['turns']}"
		)
	print(info)

def display_tournaments():
	for i in range(len(tournaments_table)):
		print(f"--- Tournament {i} ---")
		display_tournament(tournaments_table.all()[i])
