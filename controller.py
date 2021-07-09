import re
from models import Tournament, Player
from settings import players_table, tournaments_table, Info, display_players, display_tournaments
#from tinydb import TinyDB, Query
#db = TinyDB('db.json')
#PlayerInfo = Query() # doc TinyDB -> Fruit = Query()
#tournaments_table = db.table('tournaments')
#players_table = db.table('players')

class Controller:
	def __init__(self, view):
		# view
		self.view = view

	# def get_players(self):
	# 	while len(self.tournament.players) < 8:
	# 		choice = self.view.display_menu_player()
	# 		if choice == 1:
	# 			player_id = self.add_player_to_db()
	# 		else:
	# 			player_id = self.search_player_to_db(name)
	# 		self.tournament.players.append(player_id)

	# def get_ranking(self): #récupère le classement pour la premiere génération

	# def generation(players, scores, reversely=True):	#Actuelement ne vérifie pas si le match a déjà eu lieu
	# 													#reversely=False pour utilisé le classement
	# 	zipped_data = zip(scores, players)
	# 	sorted_zipped_data = sorted(zipped_data, reverse=reversely)
	# 	sorted_score, sorted_players = zip(*sorted_zipped_data)

	# 	upper_half = sorted_players[:4]
	# 	lower_half = sorted_players[4:]

	# 	return [(upper_half[i], lower_half[i]) for i in range(4)]

	# def add_turn(self, players, scores, first=False)
	# 	turn_name = self.view.prompt_turn_name()
	# 	turn = Turn(name)
	# 	matchs_list = self.generation(players, scores, False)
	# 	self.view.display_matchs(matchs_list)
	# 	self.turn = turn

	# def update_scores(self, match_result)

	# def end_turn(self, turn, scores)
	# 	while len(turn.matchs) < 4:
	# 		match_result = self.view.prompt_match_result()
	# 		turn.matchs.append(match_result)
	# 		self.update_scores(match_result)
	# 	turn.close_turn()
	# 	self.tournament.turns.append(turn)

	def run(self):
		choice = -1
		while choice != '0': #0 = quitter programme
			choice = self.view.display_menu()

			if choice == '1': #Créer un tournoi
				(
					name,
					location,
					date,
					description,
					time_control,
					turns_number
					) = self.view.prompt_tournament_info()
				tournament = Tournament(name, location, date, description, time_control, turns_number)
				tournament.add_to_db(tournaments_table)
				display_tournaments()

			elif choice == '2':#load tournament
				research = self.view.prompt_research()
				tournament = Tournament()
				results = tournament.search_in_db(research, tournaments_table, Info)
				selection = self.view.prompt_research_result(results, 'tournament')
				print(selection)
				print(results[int(selection)])
				tournament_id = tournament.get_id(results[int(selection)], tournaments_table, Info)
				tournament.load_from_database(tournament_id, tournaments_table)
				print(tournament)

			elif choice == '3':#Ajout joueur a la bdd
				(
					name, 
					birth_date, 
					gender, 
					ranking
					)  = self.view.prompt_player_info()
				player = Player(name, birth_date, gender, ranking)
				player.add_to_db(players_table)
				display_players()

			elif choice == '4':#load player
				research = self.view.prompt_research()
				player = Player()
				results = player.search_in_db(research, players_table, Info)
				selection = self.view.prompt_research_result(results, 'player')
				player_id = player.get_id(results[int(selection)], players_table, Info)
				player.load_from_database(player_id, players_table)
				print(player)
			# # Créer tournoi puis directement ajout joueur ?
			# # Option pour ajouter un joueur a la bdd sans l'ajouter au tournoi
			# elif choice == 2:#Selectionner les joueurs du tournois
			# 	self.get_players()
			# 	rankings = self.get_ranking()
			# 	players = self.tournament.players
			# 	scores = [0]*8

			# elif choice == 3:#Démarrer un tour
			# 	self.add_turn(players, rankings, True)

			# elif choice == 4:#Terminer un tour + entrée des résultats du tour
			# 	self.end_turn(turn, scores)

			# elif choice == 5:#Mettre a jour le classement
			# 	self.view.update_rankings()

			# elif choice == 6#Afficher un rapport
			# 	self.view.display_report()

			# elif choice == 7:#Chargement des données
			# 	self.view.load_data()

			# elif choice == 8:#Sauvegarde des données
			# 	self.view.save_data()
		

		


		
		





