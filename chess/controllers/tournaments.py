from chess.models import Tournament, Player, Turn, Match, Table
from chess.views import main_menu as mm_v, tournaments as t_v, players as p_v
from chess.settings import TIME_CONTROL
t_table = Table('tournaments', 'test.json')
p_table = Table('players', 'test.json')


def tournament_exists(tournament, tournaments_table):
	"""Check for similar tournaments. Returns a boolean about the existence and the list of similar tournaments"""
	partial_data = tournament.partial_serializing()
	result = tournaments_table.search_item(partial_data)

	return len(result)>0, result

def tournament_load_from_result(tournament, tournament_id, result, tournaments_table):
	"""Load a tournament from a tournament list."""
	choice = t_v.display_search_result_t(result)

	if len(result)>0:
		tournament = Tournament()
		tournament_id = tournaments_table.get_id(result[choice])
		serial_data = tournaments_table.get_item_with_id(tournament_id)
		tournament.unserializing(serial_data)

	return tournament, tournament_id


def tournament_selection(tournament, tournament_id, result, tournaments_table):
	choice = t_v.tournament_choice(result)

	if choice==0:
		tournament, tournament_id = tournament_load_from_result(tournament, tournament_id, result, tournaments_table)

	return tournament, tournament_id


def add_players(tournament, tournaments_table, players_table):
	choice = -1
	while choice!=0 and len(tournament.players)!=tournament.players_number:
		choice = t_v.display_menu_add_player()

		if choice==1:
			tournament.add_player(t_v.prompt_player_id())

		elif choice==2:
			result = players_table.search_by_name(t_v.prompt_player_name())
			player_choice = t_v.display_search_result(result)
			if player_choice!=-1:
				tournament.add_player(players_table.get_id(result[int(player_choice)]))

		elif choice==3:
			firstname, lastname, birthdate, gender, ranking = p_v.prompt_new_player()
			player = Player(firstname, lastname, birthdate, gender, ranking)
			players_table.create_item(player.serializing())
			tournament.add_player(players_table.get_id(player.serializing()))

	return tournament

def tournament_save(tournament, tournament_id):
	if tournament_id!=-1:
		t_table.update_item(tournament.serializing(), tournament_id)

	elif tournament!=None:
		serial_data = tournament.serializing()
		t_table.create_item(serial_data)
		tournament_id = tournaments_table.get_id(serial_data)

	return tournament, tournament_id

def new_tournament():
	tournament_id = -1
	name, location, date, description, time_control, turns_number, players_number = t_v.prompt_new_tournament(TIME_CONTROL)
	tournament = Tournament(name, location, date, description, time_control, turns_number, players_number)
	
	exists, result = tournament_exists(tournament, t_table)
	if exists:
		tournament, tournament_id = tournament_selection(tournament, tournament_id, result, t_table)

	tournament = add_players(tournament, t_table, p_table)
	tournament, tournament_id = tournament_save(tournament, tournament_id)

	return tournament, tournament_id

def resume_tournament(tournament, tournament_id):
	choice = -1
	while choice!=0:
		all_players_defined = len(tournament.players)==tournament.players_number
		exist_turns = len(tournament.turns)>0
		choice = t_v.display_menu_resume(tournament.name, all_players_defined, exist_turns)

		if choice==1:
			print('[IN PROGRESS] View informations')
			t_v.display_tournament_info(tournament.name, tournament.location, tournament.date, tournament.description, tournament.time_control)

		elif choice==2:
			print('[IN PROGRESS] View players')
			for player_id in tournament.players:
				serial_data = p_table.get_item_with_id(player_id)
				player = Player()
				player.unserializing(serial_data)
				t_v.display_tournament_player(player_id, player.name, player.birthdate)

		elif choice==3 and not all_players_defined:
			print('[IN PROGRESS] Add players')
			tournament = add_players(tournament, t_table, p_table)
			tournament, tournament_id = tournament_save(tournament, tournament_id)

		elif choice==3 and exist_turns:
			print('[IN PROGRESS] View turns')

		elif choice==4 and all_players_defined:
			print('[IN PROGRESS] View matchs')

		elif choice in [3, 5] and all_players_defined:
			print('[IN PROGRESS] Start turn')
			'''
			turn = Turn(t_v.prompt_turn())
			breakpoint()
			subsubchoice = -1
			while subsubchoice!='0':
				subsubchoice = t_v.display_menu_new_turn(turn.name)

				if subsubchoice=='0':
					print('Saved')
					#return tournament

				elif subsubchoice=='1':
					print('[IN PROGRESS] View matchs')

				elif subsubchoice=='2':
					print('[IN PROGRESS] End turn')
					turn.close_turn()
					tournament.add_turn(turn)
					breakpoint()
					subsubchoice = '0'

				elif subsubchoice=='3':
					print('[IN PROGRESS] Rank')

				elif subsubchoice=='4':
					print('[IN PROGRESS] Score')

				else:
					mm_v.display_try_again()
			'''
		#else:
		#	mm_v.display_try_again()

		#if ongoing:
		#	tempid = t_table.get_id({'name': tournament.name, 'location': tournament.location})
		#	print('Update ID: ',tempid)
			#t_table.update_item(tournament.serializing(),tempid)
	return tournament, tournament_id



def load_tournament(tournament, tournament_id):
	result = []
	choice = t_v.display_menu_load_tournament()
	if choice==1:
		result = t_table.search_by_name(t_v.prompt_tournament_name())
	elif choice==2:
		result = t_table.search_by_location(t_v.prompt_tournament_location())
	tournament, tournament_id = tournament_load_from_result(tournament, tournament_id, result, t_table)
	return tournament, tournament_id

#def update_tournament():

def run(tournament, tournament_id):
	choice = -1
	while choice!='0':
		ongoing = tournament!=None
		choice = t_v.display_menu(ongoing)

		if choice not in ['0', '1', '2', '3']:
			mm_v.display_try_again()

		elif choice=='1' and not ongoing:
			print('[IN PROGRESS] New tournament')
			#name, location, date, description, time_control, turns_number, players_number = t_v.prompt_new_tournament(TIME_CONTROL)
			#tournament = Tournament(name, location, date, description, time_control, turns_number, players_number)
			#while len(tournament.players)<int(players_number):
			#	tournament.add_player(t_v.prompt_player())
			#breakpoint()
			#t_table.create_item(tournament.serializing())
			tournament, tournament_id = new_tournament()
			#breakpoint()
		elif choice=='1' and ongoing:
			
			
			#breakpoint()
			
			print('[IN PROGRESS] Resume a tournament')
			tournament = resume_tournament(tournament, tournament_id)
			

		elif choice=='2':
			print('[IN PROGRESS] Load a tournament')
			tournament, tournament_id = load_tournament(tournament, tournament_id)
			resume_tournament(tournament, tournament_id)

		elif choice=='3':
			print('[IN PROGRESS] Update a tournament')

	return tournament, tournament_id

	